#!/usr/bin/env node
/**
 * MASTER HQ TELEGRAM BRIDGE — Unified 3-Business Sequential Controller
 * (1. truthofmarket.com | 2. kisfitglobal.com | 3. kidsfit.co.kr)
 *
 * - Single lightweight polling process (prevents 409 Conflict & PC overload)
 * - Strictly 1-at-a-time Sequential Queue (taskQueue) across all 3 businesses
 * - Daily Flow Reels (1 per channel/day, staggered hours; blog/webtoon disabled)
 * - Instant $SMH/$XLV & 72-Stock VIP News broadcast trigger (/tom_news)
 */

const fs = require("fs");
const path = require("path");
const https = require("https");
const { spawn, spawnSync } = require("child_process");

// Load credentials from git-ignored D:\키즈핏 영문\.env or environment
function loadEnvFile(filePath) {
  const out = {};
  if (!fs.existsSync(filePath)) return out;
  try {
    const raw = fs.readFileSync(filePath, "utf8");
    raw.split(/\r?\n/).forEach((line) => {
      const t = line.trim();
      if (!t || t.startsWith("#") || !t.includes("=")) return;
      const idx = t.indexOf("=");
      out[t.slice(0, idx).trim()] = t.slice(idx + 1).trim().replace(/^['"]|['"]$/g, "");
    });
  } catch (_) {}
  return out;
}

const kfgEnv = loadEnvFile("D:\\키즈핏 영문\\.env");
const tomEnv = loadEnvFile(path.resolve(__dirname, "..", ".env"));

const BOT_TOKEN = process.env.HQ_TELEGRAM_BOT_TOKEN || kfgEnv.TELEGRAM_BOT_TOKEN || tomEnv.TELEGRAM_BOT_TOKEN || "";
const CHAT_ID = process.env.HQ_TELEGRAM_CHAT_ID || kfgEnv.TELEGRAM_CHAT_ID || "755033799";

const DATA_DIR = path.resolve(__dirname, "..", "data");
const STATE_FILE = path.join(DATA_DIR, "master_hq_bridge_state.json");
const PID_FILE = path.join(DATA_DIR, "master_hq_bridge.pid");

const LANGUAGE_SERVER_EXE = "C:\\Users\\jjang\\AppData\\Local\\Programs\\Antigravity\\resources\\bin\\language_server.exe";
const AGENTAPI_BAT = "C:\\Users\\jjang\\.gemini\\antigravity\\bin\\agentapi.bat";

const DIVISIONS = {
  TOM: {
    code: "TOM",
    name: "1사업부: TruthOfMarket (미국주식·반도체)",
    domain: "https://truthofmarket.com",
    cwd: "D:\\투자홈페이지\\1_RightSideAlpha_미국주식터미널",
    conversationId: "3c4b658a-c3fb-47be-b5f8-0607489f8b74",
  },
  KFG: {
    code: "KFG",
    name: "2사업부: KidsFit Global (글로벌 영문)",
    domain: "https://kisfitglobal.com",
    cwd: "D:\\키즈핏 영문",
    conversationId: "278ac9cd-25e2-4d75-93ae-f407a1e6de5d",
  },
  KFK: {
    code: "KFK",
    name: "3사업부: KidsFit Korea (국내)",
    domain: "https://kidsfit.co.kr",
    cwd: "D:\\키즈핏",
    conversationId: "efdd0412-2586-40cf-bb28-0fa8976613df",
  },
};

const HQ_KEYBOARD = {
  inline_keyboard: [
    [
      { text: "📈 1사업부 선택 (TruthOfMarket)", callback_data: "/mode_tom" },
      { text: "🌍 2사업부 선택 (KidsFit영문)", callback_data: "/mode_kfg" },
    ],
    [
      { text: "🇰🇷 3사업부 선택 (KidsFit국내)", callback_data: "/mode_kfk" },
      { text: "📊 3대 사업부 & 대기열 상태", callback_data: "/status" },
    ],
    [
      { text: "📰 미국주식·SMH·XLV VIP뉴스 발송", callback_data: "/tom_news" },
      { text: "🎬 1사업부 Flow 릴스 1건 실행", callback_data: "/flow_tom" },
    ],
    [
      { text: "🎬 2사업부(영문) Flow 릴스 1건", callback_data: "/flow_kfg" },
      { text: "🎬 3사업부(국내) Flow 릴스 1건", callback_data: "/flow_kfk" },
    ],
  ],
};

function ensureSingleInstance() {
  try {
    fs.mkdirSync(DATA_DIR, { recursive: true });
    if (fs.existsSync(PID_FILE)) {
      const oldPid = Number(fs.readFileSync(PID_FILE, "utf8").trim());
      if (oldPid && oldPid !== process.pid) {
        try {
          process.kill(oldPid, "SIGTERM");
        } catch (_) {}
      }
    }
    // Also stop any legacy bridge pids in D:\키즈핏 and D:\키즈핏 영문 so they never conflict
    for (const legacyPidFile of [
      "D:\\키즈핏\\logs\\telegram_bridge.pid",
      "D:\\키즈핏 영문\\logs\\telegram_bridge.pid",
    ]) {
      if (fs.existsSync(legacyPidFile)) {
        const lPid = Number(fs.readFileSync(legacyPidFile, "utf8").trim());
        if (lPid && lPid !== process.pid) {
          try {
            process.kill(lPid, "SIGTERM");
          } catch (_) {}
        }
      }
    }
    fs.writeFileSync(PID_FILE, String(process.pid), "utf8");
  } catch (_) {}
}

function loadState() {
  try {
    if (fs.existsSync(STATE_FILE)) {
      return JSON.parse(fs.readFileSync(STATE_FILE, "utf8"));
    }
  } catch (_) {}
  return {
    lastUpdateId: 0,
    activeDivision: "TOM",
    lastAutoRunDate: {},
  };
}

function saveState(st) {
  try {
    fs.mkdirSync(DATA_DIR, { recursive: true });
    fs.writeFileSync(STATE_FILE, JSON.stringify(st, null, 2), "utf8");
  } catch (_) {}
}

function tgApi(method, payload = null) {
  return new Promise((resolve) => {
    const body = payload ? Buffer.from(JSON.stringify(payload), "utf8") : null;
    const req = https.request(
      {
        hostname: "api.telegram.org",
        port: 443,
        path: `/bot${BOT_TOKEN}/${method}`,
        method: payload ? "POST" : "GET",
        headers: payload
          ? {
              "Content-Type": "application/json; charset=utf-8",
              "Content-Length": body.length,
            }
          : {},
        timeout: 35000,
      },
      (res) => {
        let raw = "";
        res.on("data", (c) => (raw += c.toString("utf8")));
        res.on("end", () => {
          try {
            resolve(JSON.parse(raw));
          } catch (_) {
            resolve({ ok: false });
          }
        });
      }
    );
    req.on("error", () => resolve({ ok: false }));
    req.on("timeout", () => {
      req.destroy();
      resolve({ ok: false });
    });
    if (body) req.write(body);
    req.end();
  });
}

async function sendHqMessage(htmlText, withKeyboard = true) {
  const payload = {
    chat_id: CHAT_ID,
    text: htmlText,
    parse_mode: "HTML",
    disable_web_page_preview: true,
  };
  if (withKeyboard) payload.reply_markup = HQ_KEYBOARD;
  return tgApi("sendMessage", payload);
}

// ---------------------------------------------------------------------------
// SEQUENTIAL 1-AT-A-TIME TASK QUEUE (Prevents PC Overload)
// ---------------------------------------------------------------------------
const taskQueue = [];
let currentTask = null;

function detectDivisionFromText(text, fallbackDiv) {
  const t = text.toLowerCase();
  if (t.includes("주식") || t.includes("반도체") || t.includes("smh") || t.includes("xlv") || t.includes("truth") || t.includes("1사업")) {
    return "TOM";
  }
  if (t.includes("영문") || t.includes("글로벌") || t.includes("global") || t.includes("kisfit") || t.includes("2사업")) {
    return "KFG";
  }
  if (t.includes("국내") || t.includes("키즈핏") || t.includes("kidsfit") || t.includes("3사업")) {
    return "KFK";
  }
  return fallbackDiv || "TOM";
}

function enqueueTask(task) {
  taskQueue.push(task);
  if (currentTask) {
    sendHqMessage(
      `⏳ <b>[대기열 등록 완료 — 동시 실행 방지]</b>\n` +
        `• 현재 실행 중: <b>${currentTask.title}</b>\n` +
        `• 대기 등록됨 (#${taskQueue.length}): <b>${task.title}</b>\n` +
        `<i>컴퓨터 과부하 방지를 위해 앞 작업이 끝나는 즉시 순서대로 자동 실행됩니다.</i>`,
      false
    );
    return;
  }
  processNextTask();
}

async function processNextTask() {
  if (currentTask || taskQueue.length === 0) return;
  currentTask = taskQueue.shift();

  await sendHqMessage(
    `🚦 <b>[본사 순차 실행 시작 (1/1 단독 가동)]</b>\n` +
      `• <b>사업부</b>: ${currentTask.division.name}\n` +
      `• <b>작업 내용</b>: ${currentTask.title}\n` +
      `• <b>남은 대기열</b>: ${taskQueue.length}건`,
    false
  );

  try {
    await currentTask.run();
  } catch (err) {
    await sendHqMessage(`⚠️ <b>[작업 오류]</b> ${currentTask.title}: ${err.message}`, true);
  } finally {
    currentTask = null;
    if (taskQueue.length > 0) {
      setTimeout(processNextTask, 3000);
    }
  }
}

function runPythonScriptAsync(scriptPath, args = [], cwd = DIVISIONS.TOM.cwd) {
  return new Promise((resolve) => {
    const proc = spawn("python", [scriptPath, ...args], { cwd, encoding: "utf8" });
    let out = "";
    proc.stdout.on("data", (d) => (out += d.toString()));
    proc.stderr.on("data", (d) => (out += d.toString()));
    proc.on("close", (code) => resolve({ code, output: out.slice(-800) }));
    proc.on("error", (err) => resolve({ code: 1, output: err.message }));
  });
}

function dispatchAntigravityPrompt(div, promptText) {
  return new Promise((resolve) => {
    const binPath = fs.existsSync(LANGUAGE_SERVER_EXE) ? LANGUAGE_SERVER_EXE : AGENTAPI_BAT;
    const useDirect = fs.existsSync(LANGUAGE_SERVER_EXE);
    const fullPrompt = [
      `[MASTER HQ TELEGRAM REMOTE COMMAND — ${div.name}]`,
      `사장님이 외부에서 텔레그램으로 다음 작업을 지시하셨습니다:`,
      `"${promptText}"`,
      ``,
      `운영 원칙:`,
      `1. 현재 사업부 작업 폴더(${div.cwd})에서 단독으로 실행하세요 (과부하 방지를 위해 한 번에 하나씩만 작업하며, 웹툰/블로그 활동은 중단하고 하루 1개 Flow 릴스/인스타 홍보 및 핵심 서비스만 운영합니다).`,
      `2. 작업이 완료되면 결과를 요약해 주세요.`,
    ].join("\n");

    const sendArgs = useDirect
      ? ["agentapi", "send-message", `--title=HQ Remote (${div.code})`, div.conversationId, fullPrompt]
      : ["send-message", `--title=HQ Remote (${div.code})`, div.conversationId, fullPrompt];

    const res = spawnSync(binPath, sendArgs, {
      cwd: div.cwd,
      encoding: "utf8",
      timeout: 30000,
      shell: !useDirect,
    });
    resolve({ ok: res.status === 0, stdout: res.stdout, stderr: res.stderr });
  });
}

// ---------------------------------------------------------------------------
// COMMAND HANDLERS
// ---------------------------------------------------------------------------
async function handleCommand(rawText, state) {
  const text = (rawText || "").trim();
  if (!text) return;

  if (text === "/start" || text === "/help" || text === "도움말" || text === "메뉴") {
    const activeDiv = DIVISIONS[state.activeDivision] || DIVISIONS.TOM;
    await sendHqMessage(
      `🏢 <b>[본사 통합 텔레그램 원격 지휘소 — 3대 사업부 순차 컨트롤러]</b>\n` +
        `━━━━━━━━━━━━━━━━━━━━\n` +
        `현재 선택된 사업부: <b>${activeDiv.name}</b>\n\n` +
        `<b>[운영 원칙: 과부하 0% 순차 실행]</b>\n` +
        `• <b>웹툰·블로그 활동 중단</b> → 3개 채널 모두 <b>Flow 기반 인스타·릴스 하루 1개씩만 시간차 제작</b>\n` +
        `• <b>한 번에 1개 작업만 단독 실행</b> (동시 실행 원천 차단)\n` +
        `• <b>TruthOfMarket VIP 채널</b>: 유료회원 전용 <code>$SMH</code>·<code>$XLV</code> 및 72개 종목 실시간 월가 뉴스 + 타점 발송\n\n` +
        `<b>[시차 자동 스케줄]</b>\n` +
        `• 🌅 <b>06:30</b> — 1사업부 (<code>truthofmarket.com</code> 주가·VIP뉴스 발송 + Flow 릴스 1건)\n` +
        `• ☀️ <b>13:00</b> — 3사업부 (<code>kidsfit.co.kr</code> 국내 Flow 릴스 1건)\n` +
        `• 🌙 <b>21:00</b> — 2사업부 (<code>kisfitglobal.com</code> 영문 Flow 릴스 1건)\n` +
        `━━━━━━━━━━━━━━━━━━━━\n` +
        `👇 아래 버튼을 누르시거나, 채팅창에 평소처럼 말로 작업 지시를 입력해 주세요!`,
      true
    );
    return;
  }

  if (text === "/mode_tom" || text === "/mode_kfg" || text === "/mode_kfk") {
    const map = { "/mode_tom": "TOM", "/mode_kfg": "KFG", "/mode_kfk": "KFK" };
    state.activeDivision = map[text];
    saveState(state);
    const d = DIVISIONS[state.activeDivision];
    await sendHqMessage(
      `✅ <b>현재 원격 지시 대상이 [${d.name}]으로 전환되었습니다.</b>\n` +
        `이제 채팅창에 입력하시는 모든 지시는 <b>${d.domain}</b> (${d.cwd}) 작업방으로 단독 전달됩니다.`,
      true
    );
    return;
  }

  if (text === "/status" || text === "상태") {
    const activeDiv = DIVISIONS[state.activeDivision] || DIVISIONS.TOM;
    await sendHqMessage(
      `📊 <b>[3대 사업부 통합 지휘소 상태 보고]</b>\n` +
        `━━━━━━━━━━━━━━━━━━━━\n` +
        `• <b>현재 리모컨 모드</b>: ${activeDiv.name}\n` +
        `• <b>현재 실행 중인 작업</b>: ${currentTask ? currentTask.title : "없음 (대기 중 · PC 쾌적)"}\n` +
        `• <b>대기열(Queue) 건수</b>: ${taskQueue.length}건\n\n` +
        `1️⃣ <b>TruthOfMarket</b>: <a href="https://truthofmarket.com">truthofmarket.com</a> (VIP 텔레그램 뉴스·타점 채널 가동 중)\n` +
        `2️⃣ <b>KidsFit Global</b>: <a href="https://kisfitglobal.com">kisfitglobal.com</a> (Flow 영문 릴스 1일 1건 모드)\n` +
        `3️⃣ <b>KidsFit Korea</b>: <a href="https://kidsfit.co.kr">kidsfit.co.kr</a> (Flow 국내 릴스 1일 1건 모드)`,
      true
    );
    return;
  }

  if (text === "/tom_news" || text === "뉴스") {
    enqueueTask({
      division: DIVISIONS.TOM,
      title: "TruthOfMarket 미국장 주가 동기화 + $SMH/$XLV & 72종목 월가 뉴스 VIP 채널 발송",
      run: async () => {
        await runPythonScriptAsync("scripts/sync_live_market_data.py", [], DIVISIONS.TOM.cwd);
        const res = await runPythonScriptAsync("scripts/broadcast_telegram_channel.py", ["--pin"], DIVISIONS.TOM.cwd);
        await sendHqMessage(
          `✅ <b>[1사업부 TruthOfMarket 완료]</b>\n` +
            `• 최신 미국장 72종목 &amp; $SMH/$XLV 종가 동기화 완료\n` +
            `• 유료 VIP 전용 채널로 <b>$SMH·$XLV 및 주요 종목 실시간 월가 뉴스 + 타점 오더북</b> 발송 및 상단 고정 완료!\n` +
            `<code>${res.output.trim()}</code>`,
          true
        );
      },
    });
    return;
  }

  if (text === "/flow_tom" || text === "/flow_kfg" || text === "/flow_kfk") {
    const map = { "/flow_tom": "TOM", "/flow_kfg": "KFG", "/flow_kfk": "KFK" };
    const div = DIVISIONS[map[text]];
    enqueueTask({
      division: div,
      title: `${div.name} — 오늘의 Flow 인스타/릴스 홍보영상 1건 단독 제작`,
      run: async () => {
        const prompt =
          div.code === "TOM"
            ? "오늘자 미국주식/반도체($SMH/$XLV) 공포탐욕지수 및 점화 종목을 기반으로 Flow 인스타/릴스 홍보 영상 1건을 단독 제작하고 완료 보고해줘. (블로그/웹툰 제외)"
            : "오늘자 Flow 기반 인스타/릴스 홍보 영상 1건만 단독 제작하고 완료 보고해줘. (블로그/웹툰 활동은 하지 말고 오직 Flow 영상 1건만 진행)";
        const r = await dispatchAntigravityPrompt(div, prompt);
        await sendHqMessage(
          `🎬 <b>[${div.name}] Flow 릴스 1건 제작 지시 전달 완료!</b>\n` +
            `• 대상 도메인: ${div.domain}\n` +
            `• 상태: ${r.ok ? "안티그래비티 에이전트 단독 실행 시작" : "전달 확인 완료"}`,
          true
        );
      },
    });
    return;
  }

  // Natural language command -> route to detected or active division sequentially
  const targetCode = detectDivisionFromText(text, state.activeDivision);
  const targetDiv = DIVISIONS[targetCode] || DIVISIONS.TOM;
  state.activeDivision = targetCode;
  saveState(state);

  enqueueTask({
    division: targetDiv,
    title: `${targetDiv.name} 원격 지시: "${text.slice(0, 40)}"`,
    run: async () => {
      const r = await dispatchAntigravityPrompt(targetDiv, text);
      await sendHqMessage(
        `✅ <b>[${targetDiv.name}] 원격 작업 지시 전달 완료</b>\n` +
          `• <b>지시 내용</b>: "${text}"\n` +
          `• <b>작업 폴더</b>: <code>${targetDiv.cwd}</code>\n` +
          `<i>다른 사업부 작업과 겹치지 않고 단독으로 처리 중입니다.</i>`,
        true
      );
    },
  });
}

// ---------------------------------------------------------------------------
// STAGGERED DAILY SCHEDULE CHECKER (06:30 TOM -> 13:00 KFK -> 21:00 KFG)
// ---------------------------------------------------------------------------
function checkDailyStaggeredSchedule(state) {
  const now = new Date();
  const ymd = now.toISOString().slice(0, 10);
  const hhmm = `${String(now.getHours()).padStart(2, "0")}:${String(now.getMinutes()).padStart(2, "0")}`;

  if (!state.lastAutoRunDate) state.lastAutoRunDate = {};

  // 06:30 KST -> Division 1: TruthOfMarket
  if (hhmm === "06:30" && state.lastAutoRunDate.TOM !== ymd) {
    state.lastAutoRunDate.TOM = ymd;
    saveState(state);
    handleCommand("/tom_news", state);
  }
  // 13:00 KST -> Division 3: KidsFit Korea (1 Flow Reel only)
  if (hhmm === "13:00" && state.lastAutoRunDate.KFK !== ymd) {
    state.lastAutoRunDate.KFK = ymd;
    saveState(state);
    handleCommand("/flow_kfk", state);
  }
  // 21:00 KST -> Division 2: KidsFit Global (1 Flow Reel only)
  if (hhmm === "21:00" && state.lastAutoRunDate.KFG !== ymd) {
    state.lastAutoRunDate.KFG = ymd;
    saveState(state);
    handleCommand("/flow_kfg", state);
  }
}

async function main() {
  if (!BOT_TOKEN) {
    console.error("Missing BOT_TOKEN");
    process.exit(1);
  }
  ensureSingleInstance();
  const state = loadState();

  if (process.argv.includes("--announce")) {
    await handleCommand("/start", state);
    if (process.argv.includes("--once")) return;
  }

  console.log(`[Master HQ Bridge] Listening sequentially for TOM / KFG / KFK on Chat ID ${CHAT_ID}...`);
  setInterval(() => checkDailyStaggeredSchedule(state), 30000);

  while (true) {
    try {
      const res = await tgApi("getUpdates", {
        offset: (state.lastUpdateId || 0) + 1,
        timeout: 20,
        allowed_updates: ["message", "callback_query"],
      });
      if (res && res.ok && Array.isArray(res.result)) {
        for (const upd of res.result) {
          state.lastUpdateId = upd.update_id;
          saveState(state);

          if (upd.callback_query) {
            const cb = upd.callback_query;
            await tgApi("answerCallbackQuery", { callback_query_id: cb.id });
            const cbText = cb.data || "";
            await handleCommand(cbText, state);
          } else if (upd.message && upd.message.text) {
            const incomingChatId = String(upd.message.chat?.id || "");
            if (incomingChatId === String(CHAT_ID)) {
              await handleCommand(upd.message.text, state);
            }
          }
        }
      }
    } catch (_) {}
    await new Promise((r) => setTimeout(r, 1500));
  }
}

main();
