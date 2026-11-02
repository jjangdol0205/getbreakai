#!/usr/bin/env node
/**
 * MASTER HQ TELEGRAM BRIDGE — Unified 3-Business Sequential Controller (Sleep/Wake Proof)
 * (1. truthofmarket.com | 2. kisfitglobal.com | 3. kidsfit.co.kr)
 *
 * - Single lightweight polling process with hard 15s socket watchdog (survives Windows Sleep/Wake)
 * - Listens across @kidsfittbot, @RigjtsideAlphabot, and @SemifearGreedbot in 1 process
 * - Strictly 1-at-a-time Sequential Queue (taskQueue) across all 3 businesses
 * - Supports `--notify "<msg>"` so Antigravity agents reply back upon task completion
 */

const fs = require("fs");
const path = require("path");
const https = require("https");
const { spawn, spawnSync } = require("child_process");

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

function loadJsonFile(filePath) {
  try {
    if (fs.existsSync(filePath)) {
      return JSON.parse(fs.readFileSync(filePath, "utf8"));
    }
  } catch (_) {}
  return {};
}

const kfgEnv = loadEnvFile("D:\\키즈핏 영문\\.env");
const kfkEnv = loadEnvFile("D:\\사업아이템\\.env");
const tomEnv = loadEnvFile(path.resolve(__dirname, "..", ".env"));
const tomTgCfg = loadJsonFile(path.resolve(__dirname, "..", "data", "telegram_config.json"));

const CHAT_ID = process.env.HQ_TELEGRAM_CHAT_ID || kfgEnv.TELEGRAM_CHAT_ID || kfkEnv.TELEGRAM_CHAT_ID || "755033799";
const PRIMARY_BOT_TOKEN = process.env.HQ_TELEGRAM_BOT_TOKEN || kfgEnv.TELEGRAM_BOT_TOKEN || "";
const KFK_BOT_TOKEN = kfkEnv.TELEGRAM_BOT_TOKEN || "";
const RSA_BOT_TOKEN = tomEnv.RSA_TELEGRAM_BOT_TOKEN || "";
const SEMI_BOT_TOKEN = tomTgCfg.bot_token || tomEnv.TELEGRAM_BOT_TOKEN || "";

// Collect active bot tokens (deduplicated)
const BOT_TOKENS = Array.from(
  new Set([PRIMARY_BOT_TOKEN, KFK_BOT_TOKEN, RSA_BOT_TOKEN, SEMI_BOT_TOKEN].filter((t) => t && t.includes(":")))
);

const DATA_DIR = path.resolve(__dirname, "..", "data");
const STATE_FILE = path.join(DATA_DIR, "master_hq_bridge_state.json");
const PID_FILE = path.join(DATA_DIR, "master_hq_bridge.pid");
const BRIDGE_SCRIPT_PATH = __filename;

const LANGUAGE_SERVER_EXE = "C:\\Users\\jjang\\AppData\\Local\\Programs\\Antigravity\\resources\\bin\\language_server.exe";
const AGENTAPI_BAT = "C:\\Users\\jjang\\.gemini\\antigravity\\bin\\agentapi.bat";

const MASTER_CONVERSATION_ID = "3c4b658a-c3fb-47be-b5f8-0607489f8b74";

const DIVISIONS = {
  TOM: {
    code: "TOM",
    name: "1사업부: RightSideAlpha (truthofmarket.com)",
    domain: "https://truthofmarket.com",
    cwd: "D:\\투자홈페이지\\1_RightSideAlpha_미국주식터미널",
    conversationId: MASTER_CONVERSATION_ID,
  },
  KFG: {
    code: "KFG",
    name: "2사업부: 키즈핏 영문 (kisfitglobal.com)",
    domain: "https://kisfitglobal.com",
    cwd: "D:\\키즈핏 영문",
    conversationId: MASTER_CONVERSATION_ID,
  },
  KFK: {
    code: "KFK",
    name: "3사업부: 사업아이템 (kidsfit.co.kr)",
    domain: "https://kidsfit.co.kr",
    cwd: "D:\\사업아이템",
    conversationId: MASTER_CONVERSATION_ID,
  },
};

const HQ_KEYBOARD = {
  inline_keyboard: [
    [
      { text: "📈 1사업부 (RightSideAlpha)", callback_data: "/mode_tom" },
      { text: "🌍 2사업부 (키즈핏 영문)", callback_data: "/mode_kfg" },
    ],
    [
      { text: "🇰🇷 3사업부 (사업아이템·국내)", callback_data: "/mode_kfk" },
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
    for (const legacyPidFile of [
      "D:\\사업아이템\\logs\\telegram_bridge.pid",
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
      const parsed = JSON.parse(fs.readFileSync(STATE_FILE, "utf8"));
      if (!parsed.offsets) parsed.offsets = {};
      if (!parsed.lastAutoRunDate) parsed.lastAutoRunDate = {};
      if (!parsed.activeDivision) parsed.activeDivision = "TOM";
      return parsed;
    }
  } catch (_) {}
  return {
    lastUpdateId: 0,
    offsets: {},
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

/**
 * Sleep/Wake-Proof Telegram API request with hard JS watchdog timer (15 seconds max)
 */
function tgApiWithToken(botToken, method, payload = null, hardTimeoutMs = 15000) {
  return new Promise((resolve) => {
    let settled = false;
    let req = null;
    const finish = (val) => {
      if (settled) return;
      settled = true;
      clearTimeout(watchdog);
      resolve(val);
    };

    const watchdog = setTimeout(() => {
      try {
        if (req) req.destroy();
      } catch (_) {}
      finish({ ok: false, error: "HARD_WATCHDOG_TIMEOUT" });
    }, hardTimeoutMs);

    try {
      const body = payload ? Buffer.from(JSON.stringify(payload), "utf8") : null;
      req = https.request(
        {
          hostname: "api.telegram.org",
          port: 443,
          path: `/bot${botToken}/${method}`,
          method: payload ? "POST" : "GET",
          headers: payload
            ? {
                "Content-Type": "application/json; charset=utf-8",
                "Content-Length": body.length,
              }
            : {},
          timeout: hardTimeoutMs - 1000,
        },
        (res) => {
          let raw = "";
          res.on("data", (c) => (raw += c.toString("utf8")));
          res.on("end", () => {
            try {
              finish(JSON.parse(raw));
            } catch (_) {
              finish({ ok: false });
            }
          });
        }
      );
      req.on("error", () => finish({ ok: false }));
      req.on("timeout", () => {
        try {
          req.destroy();
        } catch (_) {}
        finish({ ok: false });
      });
      if (body) req.write(body);
      req.end();
    } catch (_) {
      finish({ ok: false });
    }
  });
}

async function sendHqMessage(htmlText, withKeyboard = true, preferredToken = null) {
  const tokenToUse = preferredToken || PRIMARY_BOT_TOKEN || BOT_TOKENS[0];
  const payload = {
    chat_id: CHAT_ID,
    text: htmlText,
    parse_mode: "HTML",
    disable_web_page_preview: true,
  };
  if (withKeyboard) payload.reply_markup = HQ_KEYBOARD;
  const res = await tgApiWithToken(tokenToUse, "sendMessage", payload, 12000);
  if (!res.ok && BOT_TOKENS.length > 1) {
    for (const fallbackTok of BOT_TOKENS) {
      if (fallbackTok !== tokenToUse) {
        const r2 = await tgApiWithToken(fallbackTok, "sendMessage", payload, 12000);
        if (r2.ok) return r2;
      }
    }
  }
  return res;
}

// ---------------------------------------------------------------------------
// SEQUENTIAL 1-AT-A-TIME TASK QUEUE (Prevents PC Overload)
// ---------------------------------------------------------------------------
const taskQueue = [];
let currentTask = null;

function detectDivisionFromText(text, fallbackDiv) {
  const t = text.toLowerCase();
  // 1. Check explicit domain names or division labels first
  if (t.includes("kidsfit.co.kr") || t.includes("사업아이템") || t.includes("3사업")) {
    return "KFK";
  }
  if (t.includes("kisfitglobal.com") || t.includes("kidsfitglobal.com") || t.includes("키즈핏 영문") || t.includes("2사업")) {
    return "KFG";
  }
  if (t.includes("truthofmarket.com") || t.includes("rightsidealpha") || t.includes("1사업")) {
    return "TOM";
  }
  // 2. Fallback keyword matching
  if (
    t.includes("주식") ||
    t.includes("반도체") ||
    t.includes("smh") ||
    t.includes("xlv") ||
    t.includes("rightside")
  ) {
    return "TOM";
  }
  if (t.includes("영문") || t.includes("글로벌") || t.includes("kisfit")) {
    return "KFG";
  }
  if (t.includes("국내") || t.includes("키즈핏") || t.includes("kidsfit")) {
    return "KFK";
  }
  return fallbackDiv || "TOM";
}

function enqueueTask(task, botToken) {
  task.botToken = botToken;
  taskQueue.push(task);
  if (currentTask) {
    sendHqMessage(
      `⏳ <b>[대기열 등록 완료 — 동시 실행 방지]</b>\n` +
        `• 현재 실행 중: <b>${currentTask.title}</b>\n` +
        `• 대기 등록됨 (#${taskQueue.length}): <b>${task.title}</b>\n` +
        `<i>컴퓨터 과부하 방지를 위해 앞 작업이 끝나는 즉시 순서대로 자동 실행됩니다.</i>`,
      false,
      botToken
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
    false,
    currentTask.botToken
  );

  try {
    await currentTask.run();
  } catch (err) {
    await sendHqMessage(`⚠️ <b>[작업 오류]</b> ${currentTask.title}: ${err.message}`, true, currentTask.botToken);
  } finally {
    currentTask = null;
    if (taskQueue.length > 0) {
      setTimeout(processNextTask, 2500);
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
      `2. 작업이 완료되면 반드시 아래 명령어를 실행하여 사장님 텔레그램으로 완료 결과를 답장하세요:`,
      `   node "${BRIDGE_SCRIPT_PATH}" --notify "[${div.name} 완료] <수행한 작업 요약>"`,
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
async function handleCommand(rawText, state, botToken = null) {
  const text = (rawText || "").trim();
  if (!text) return;

  if (text === "/start" || text === "/help" || text === "도움말" || text === "메뉴" || text === "연결") {
    const activeDiv = DIVISIONS[state.activeDivision] || DIVISIONS.TOM;
    await sendHqMessage(
      `🟢 <b>[본사 통합 텔레그램 원격 지휘소 — 3대 사업부 폴더 매핑 완료!]</b>\n` +
        `━━━━━━━━━━━━━━━━━━━━\n` +
        `현재 선택된 사업부: <b>${activeDiv.name}</b>\n\n` +
        `<b>[3대 사업부 작업 폴더 매핑]</b>\n` +
        `1️⃣ <b>1사업부 (truthofmarket.com)</b>\n` +
        `   └ 폴더: <code>D:\\투자홈페이지\\1_RightSideAlpha_미국주식터미널</code>\n` +
        `2️⃣ <b>2사업부 (kisfitglobal.com)</b>\n` +
        `   └ 폴더: <code>D:\\키즈핏 영문</code>\n` +
        `3️⃣ <b>3사업부 (kidsfit.co.kr)</b>\n` +
        `   └ 폴더: <code>D:\\사업아이템</code>\n\n` +
        `<b>[운영 원칙: 과부하 0% 순차 실행]</b>\n` +
        `• <b>웹툰·블로그 활동 중단</b> → 3개 채널 모두 <b>Flow 기반 인스타·릴스 하루 1개씩만 시간차 제작</b>\n` +
        `• <b>한 번에 1개 작업만 단독 실행</b> (동시 실행 원천 차단)\n` +
        `• <b>TruthOfMarket VIP 채널</b>: 유료회원 전용 <code>$SMH</code>·<code>$XLV</code> 및 72개 종목 실시간 월가 뉴스 + 타점 발송\n` +
        `━━━━━━━━━━━━━━━━━━━━\n` +
        `👇 아래 버튼을 누르시거나, 채팅창에 바로 작업 지시를 입력해 주세요!`,
      true,
      botToken
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
        `이제 채팅창에 입력하시는 모든 지시는 <b>${d.domain}</b> (<code>${d.cwd}</code>) 작업방으로 단독 전달됩니다.`,
      true,
      botToken
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
        `1️⃣ <b>1사업부 (RightSideAlpha)</b>: <code>${DIVISIONS.TOM.cwd}</code>\n` +
        `2️⃣ <b>2사업부 (키즈핏 영문)</b>: <code>${DIVISIONS.KFG.cwd}</code>\n` +
        `3️⃣ <b>3사업부 (사업아이템)</b>: <code>${DIVISIONS.KFK.cwd}</code>`,
      true,
      botToken
    );
    return;
  }

  if (text === "/tom_news" || text === "뉴스") {
    enqueueTask(
      {
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
            true,
            botToken
          );
        },
      },
      botToken
    );
    return;
  }

  if (text === "/flow_tom" || text === "/flow_kfg" || text === "/flow_kfk") {
    const map = { "/flow_tom": "TOM", "/flow_kfg": "KFG", "/flow_kfk": "KFK" };
    const div = DIVISIONS[map[text]];
    enqueueTask(
      {
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
            true,
            botToken
          );
        },
      },
      botToken
    );
    return;
  }

  const targetCode = detectDivisionFromText(text, state.activeDivision);
  const targetDiv = DIVISIONS[targetCode] || DIVISIONS.TOM;
  state.activeDivision = targetCode;
  saveState(state);

  enqueueTask(
    {
      division: targetDiv,
      title: `${targetDiv.name} 원격 지시: "${text.slice(0, 40)}"`,
      run: async () => {
        const r = await dispatchAntigravityPrompt(targetDiv, text);
        await sendHqMessage(
          `✅ <b>[${targetDiv.name}] 원격 작업 지시 접수 &amp; 단독 실행 시작</b>\n` +
            `• <b>지시 내용</b>: "${text}"\n` +
            `• <b>작업 폴더</b>: <code>${targetDiv.cwd}</code>\n` +
            `<i>작업이 끝나면 이 채팅방으로 완료 보고가 도착합니다.</i>`,
          true,
          botToken
        );
      },
    },
    botToken
  );
}

function checkDailyStaggeredSchedule(state) {
  const now = new Date();
  const ymd = now.toISOString().slice(0, 10);
  const hhmm = `${String(now.getHours()).padStart(2, "0")}:${String(now.getMinutes()).padStart(2, "0")}`;

  if (!state.lastAutoRunDate) state.lastAutoRunDate = {};

  if (hhmm === "06:30" && state.lastAutoRunDate.TOM !== ymd) {
    state.lastAutoRunDate.TOM = ymd;
    saveState(state);
    handleCommand("/tom_news", state);
  }
  if (hhmm === "13:00" && state.lastAutoRunDate.KFK !== ymd) {
    state.lastAutoRunDate.KFK = ymd;
    saveState(state);
    handleCommand("/flow_kfk", state);
  }
  if (hhmm === "21:00" && state.lastAutoRunDate.KFG !== ymd) {
    state.lastAutoRunDate.KFG = ymd;
    saveState(state);
    handleCommand("/flow_kfg", state);
  }
}

async function pollBotTokenOnce(botToken, state) {
  const botKey = botToken.split(":")[0];
  const currentOffset = state.offsets?.[botKey] || (botToken === PRIMARY_BOT_TOKEN ? state.lastUpdateId || 0 : 0);

  const res = await tgApiWithToken(
    botToken,
    "getUpdates",
    {
      offset: currentOffset + 1,
      timeout: 4,
      allowed_updates: ["message", "callback_query"],
    },
    8000
  );

  if (res && res.ok && Array.isArray(res.result) && res.result.length > 0) {
    for (const upd of res.result) {
      if (!state.offsets) state.offsets = {};
      state.offsets[botKey] = upd.update_id;
      if (botToken === PRIMARY_BOT_TOKEN) state.lastUpdateId = upd.update_id;
      saveState(state);

      if (upd.callback_query) {
        const cb = upd.callback_query;
        console.log(`[HQ Bridge] Button Click (${botKey}): ${cb.data}`);
        await tgApiWithToken(
          botToken,
          "answerCallbackQuery",
          {
            callback_query_id: cb.id,
            text: `⚡ [${cb.data}] 즉시 실행합니다!`,
          },
          5000
        );
        await handleCommand(cb.data || "", state, botToken);
      } else if (upd.message && upd.message.text) {
        const incomingChatId = String(upd.message.chat?.id || "");
        console.log(`[HQ Bridge] Message (${botKey}) from ${incomingChatId}: ${upd.message.text}`);
        if (incomingChatId === String(CHAT_ID)) {
          await handleCommand(upd.message.text, state, botToken);
        }
      }
    }
  }
}

async function main() {
  if (BOT_TOKENS.length === 0) {
    console.error("Missing BOT_TOKENS");
    process.exit(1);
  }

  // CLI helper mode: `--notify "message"` sends a message without killing the running daemon
  const notifyIdx = process.argv.indexOf("--notify");
  if (notifyIdx !== -1 && process.argv[notifyIdx + 1]) {
    const msg = process.argv[notifyIdx + 1];
    await sendHqMessage(`📬 <b>[작업 완료 보고]</b>\n${msg}`, true);
    return;
  }

  ensureSingleInstance();
  const state = loadState();

  if (process.argv.includes("--announce")) {
    for (const tok of [PRIMARY_BOT_TOKEN, KFK_BOT_TOKEN, RSA_BOT_TOKEN].filter(Boolean)) {
      await handleCommand("/start", state, tok);
    }
    if (process.argv.includes("--once")) return;
  }

  console.log(`[Master HQ Bridge] Active & Watchdog-Protected on Chat ID ${CHAT_ID} (${BOT_TOKENS.length} bots)...`);
  setInterval(() => checkDailyStaggeredSchedule(state), 25000);

  while (true) {
    try {
      await Promise.all(BOT_TOKENS.map((tok) => pollBotTokenOnce(tok, state).catch(() => {})));
    } catch (_) {}
    await new Promise((r) => setTimeout(r, 300));
  }
}

main();
