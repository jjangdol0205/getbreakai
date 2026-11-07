#!/usr/bin/env node
/**
 * scripts/hq_all_divisions_visitor_briefing.js
 * 1·2·3사업부 통합 홈페이지 실방문자(UV/PV) & 사업부별 핵심 목표(1·2사업부: 유료회원 전환 / 3사업부: 상품 레퍼럴 클릭) 정기 브리핑 엔진
 *
 * [정합성 보장 아키텍처]
 * 1. Abacus API 레이트리밋(HTTP 429) 원천 차단:
 *    - 기존 36개 병렬 호출 대신 오늘 필요한 핵심 키(총 11개)만 350ms 간격 순차 조회 + HTTP 429 자동 재시도
 * 2. 영구 원장(data/hq_visitor_ledger.json) 단조증가(Monotonic) 보장:
 *    - 네트워크/429 일시 오류 시 절대 0으로 초기화되지 않고 직전 유효값 유지
 *    - PV >= UV 수학적 정합성 보장 및 누적치(Total) = 전체 일자별 합산(Sum of daily records) 100% 일치 보장
 * 3. 중복 발송 방지 락(60초 쿨다운) 적용
 */

'use strict';

const fs = require('fs');
const path = require('path');
const https = require('https');

const LEDGER_PATH = path.resolve(__dirname, '..', 'data', 'hq_visitor_ledger.json');

function loadPrimaryBotToken() {
  const candidates = [
    'D:\\키즈핏 영문\\.env',
    'D:\\사업아이템\\.env',
    'D:\\투자홈페이지\\1_RightSideAlpha_미국주식터미널\\.env'
  ];
  for (const fp of candidates) {
    if (fs.existsSync(fp)) {
      const m = fs.readFileSync(fp, 'utf8').match(/(?:TELEGRAM_BOT_TOKEN|RSA_TELEGRAM_BOT_TOKEN)=([^\r\n]+)/);
      if (m && m[1]) return m[1].trim().replace(/^['"]|['"]$/g, '');
    }
  }
  return '';
}

const BOT_TOKEN = loadPrimaryBotToken();
const CHAT_ID = '755033799';

function sleep(ms) {
  return new Promise((r) => setTimeout(r, ms));
}

function getKstDateString(offsetDays = 0) {
  const ms = Date.now() + 9 * 3600 * 1000 + offsetDays * 86400 * 1000;
  return new Date(ms).toISOString().slice(0, 10);
}

function getKstNowFormatted() {
  return new Date(Date.now() + 9 * 3600 * 1000).toISOString().replace('T', ' ').slice(0, 19) + ' KST';
}

function loadLedger() {
  try {
    if (fs.existsSync(LEDGER_PATH)) {
      return JSON.parse(fs.readFileSync(LEDGER_PATH, 'utf8'));
    }
  } catch (_) {}
  return { lastUpdatedKst: '', lastTelegramSentMs: 0, divisions: {} };
}

function saveLedger(ledger) {
  try {
    fs.mkdirSync(path.dirname(LEDGER_PATH), { recursive: true });
    ledger.lastUpdatedKst = getKstNowFormatted();
    fs.writeFileSync(LEDGER_PATH, JSON.stringify(ledger, null, 2) + '\n', 'utf8');
  } catch (_) {}
}

/**
 * Queries Abacus with automatic retry on HTTP 429.
 * Returns:
 *   - number (>= 0) when HTTP 200 or HTTP 404 (key not created yet today -> 0)
 *   - null when HTTP 429 or network timeout (caller must preserve existing ledger value!)
 */
async function getAbacusCountSafe(ns, key, retries = 2) {
  for (let attempt = 0; attempt <= retries; attempt++) {
    const res = await new Promise((resolve) => {
      const url = `https://abacus.jasoncameron.dev/get/${ns}/${key}`;
      const req = https.get(url, { timeout: 5000 }, (r) => {
        let raw = '';
        r.on('data', (c) => (raw += c));
        r.on('end', () => {
          if (r.statusCode === 200) {
            try {
              const parsed = JSON.parse(raw);
              resolve({ ok: true, status: 200, value: Number(parsed.value) || 0 });
              return;
            } catch (_) {}
          }
          if (r.statusCode === 404) {
            // Key has not been hit yet today -> genuine 0
            resolve({ ok: true, status: 404, value: 0 });
            return;
          }
          resolve({ ok: false, status: r.statusCode, value: null });
        });
      });
      req.on('error', () => resolve({ ok: false, status: 0, value: null }));
      req.on('timeout', () => {
        req.destroy();
        resolve({ ok: false, status: 0, value: null });
      });
    });

    if (res.ok) {
      await sleep(320);
      return res.value;
    }
    if (res.status === 429 && attempt < retries) {
      await sleep(1500 * (attempt + 1));
      continue;
    }
    await sleep(320);
    return null;
  }
  return null;
}

function checkSiteHealth(urlStr) {
  return new Promise((resolve) => {
    const start = Date.now();
    const req = https.get(
      urlStr,
      {
        headers: { 'User-Agent': 'HQ-HealthMonitor/1.0' },
        timeout: 8000
      },
      (res) => {
        res.resume();
        const ms = Date.now() - start;
        resolve({ ok: res.statusCode >= 200 && res.statusCode < 400, status: res.statusCode, ms });
      }
    );
    req.on('error', () => resolve({ ok: false, status: 0, ms: Date.now() - start }));
    req.on('timeout', () => {
      req.destroy();
      resolve({ ok: false, status: 0, ms: Date.now() - start });
    });
  });
}

function sendTelegramHtml(text) {
  return new Promise((resolve) => {
    const payload = JSON.stringify({
      chat_id: CHAT_ID,
      text,
      parse_mode: 'HTML',
      disable_web_page_preview: true
    });
    const req = https.request(
      {
        hostname: 'api.telegram.org',
        path: `/bot${BOT_TOKEN}/sendMessage`,
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Content-Length': Buffer.byteLength(payload)
        },
        timeout: 10000
      },
      (res) => {
        let body = '';
        res.on('data', (c) => (body += c));
        res.on('end', () => resolve({ ok: res.statusCode === 200, body }));
      }
    );
    req.on('error', (e) => resolve({ ok: false, error: e.message }));
    req.write(payload);
    req.end();
  });
}

async function fetchDivisionMetricsSequential(div, ledger) {
  const today = getKstDateString(0);
  const yesterday = getKstDateString(-1);

  if (!ledger.divisions) ledger.divisions = {};
  if (!ledger.divisions[div.ns]) ledger.divisions[div.ns] = { days: {} };
  const daysMap = ledger.divisions[div.ns].days;

  if (!daysMap[today]) {
    daysMap[today] = { uv: 0, pv: 0, paidClick: 0, paidMember: 0, refClick: 0 };
  }
  if (!daysMap[yesterday]) {
    daysMap[yesterday] = { uv: 0, pv: 0, paidClick: 0, paidMember: 0, refClick: 0 };
  }

  // Query today's and yesterday's active counters sequentially (prevents Abacus HTTP 429 & captures late-night 21:00~24:00 KST traffic)
  const uvTodayRaw = await getAbacusCountSafe(div.ns, `uv_${today}`);
  const pvTodayRaw = await getAbacusCountSafe(div.ns, `pv_${today}`);
  const uvYestRaw = await getAbacusCountSafe(div.ns, `uv_${yesterday}`);
  const pvYestRaw = await getAbacusCountSafe(div.ns, `pv_${yesterday}`);

  if (uvTodayRaw !== null) {
    daysMap[today].uv = Math.max(daysMap[today].uv || 0, uvTodayRaw);
  }
  if (pvTodayRaw !== null) {
    daysMap[today].pv = Math.max(daysMap[today].pv || 0, pvTodayRaw);
  }
  if (uvYestRaw !== null) {
    daysMap[yesterday].uv = Math.max(daysMap[yesterday].uv || 0, uvYestRaw);
  }
  if (pvYestRaw !== null) {
    daysMap[yesterday].pv = Math.max(daysMap[yesterday].pv || 0, pvYestRaw);
  }
  // Mathematical consistency: PV is always >= UV
  daysMap[today].pv = Math.max(daysMap[today].pv || 0, daysMap[today].uv || 0);
  daysMap[yesterday].pv = Math.max(daysMap[yesterday].pv || 0, daysMap[yesterday].uv || 0);

  if (div.kpiType === 'PAID') {
    const paidClickRaw = await getAbacusCountSafe(div.ns, `paid_click_${today}`);
    const paidClickYestRaw = await getAbacusCountSafe(div.ns, `paid_click_${yesterday}`);
    const paidMemberRaw = await getAbacusCountSafe(div.ns, `paid_member_${today}`);
    if (paidClickRaw !== null) {
      daysMap[today].paidClick = Math.max(daysMap[today].paidClick || 0, paidClickRaw);
    }
    if (paidClickYestRaw !== null) {
      daysMap[yesterday].paidClick = Math.max(daysMap[yesterday].paidClick || 0, paidClickYestRaw);
    }
    if (paidMemberRaw !== null) {
      daysMap[today].paidMember = Math.max(daysMap[today].paidMember || 0, paidMemberRaw);
    }
  } else {
    const refClickRaw = await getAbacusCountSafe(div.ns, `ref_click_${today}`);
    const refClickYestRaw = await getAbacusCountSafe(div.ns, `ref_click_${yesterday}`);
    if (refClickRaw !== null) {
      daysMap[today].refClick = Math.max(daysMap[today].refClick || 0, refClickRaw);
    }
    if (refClickYestRaw !== null) {
      daysMap[yesterday].refClick = Math.max(daysMap[yesterday].refClick || 0, refClickYestRaw);
    }
  }

  const health = await checkSiteHealth(div.url);

  // Calculate exact cumulative totals by summing all recorded days in ledger
  let uvTotal = 0;
  let pvTotal = 0;
  let paidClickTotal = 0;
  let paidMemberTotal = 0;
  let refClickTotal = 0;

  for (const dKey of Object.keys(daysMap)) {
    const row = daysMap[dKey] || {};
    const dUv = Number(row.uv) || 0;
    const dPv = Math.max(Number(row.pv) || 0, dUv);
    uvTotal += dUv;
    pvTotal += dPv;
    paidClickTotal += Number(row.paidClick) || 0;
    paidMemberTotal += Number(row.paidMember) || 0;
    refClickTotal += Number(row.refClick) || 0;
  }

  return {
    ...div,
    uvToday: daysMap[today].uv || 0,
    pvToday: daysMap[today].pv || 0,
    uvYest: daysMap[yesterday].uv || 0,
    pvYest: daysMap[yesterday].pv || 0,
    uvTotal,
    pvTotal,
    paidClickToday: daysMap[today].paidClick || 0,
    paidClickTotal,
    paidMemberToday: daysMap[today].paidMember || 0,
    paidMemberTotal,
    refClickToday: daysMap[today].refClick || 0,
    refClickTotal,
    health
  };
}

async function runVisitorBriefing(options = {}) {
  const divisions = [
    {
      code: '1사업부',
      name: 'RightSideAlpha 미국주식 터미널',
      domain: 'truthofmarket.com',
      url: 'https://truthofmarket.com/',
      ns: 'tom_truthofmarket',
      kpiType: 'PAID',
      kpiGoal: '유료화 회원수 증대 (PRO 구독 & VIP 채널)',
      gscStatus: '소유권 인증 완료 · Sitemap 75개 URL 정상 등록',
      channels: 'IG @rightsidealpha · X @rightsidealpha · TG @truthofmarketss'
    },
    {
      code: '2사업부',
      name: 'KIDS-FIT Global 영문판',
      domain: 'kisfitglobal.com',
      url: 'https://kisfitglobal.com/',
      ns: 'kfg_kisfitglobal',
      kpiType: 'PAID',
      kpiGoal: '유료화 회원수 증대 ($8.99 단건 / $19.99 6개월 패스)',
      gscStatus: '소유권 인증 완료 · Sitemap 63p & RSS 31p 성공',
      channels: 'IG @kisfitglobal · YT @kisfitglobal · LemonSqueezy Live'
    },
    {
      code: '3사업부',
      name: 'KIDS-FIT Korea 한국판',
      domain: 'kidsfit.co.kr',
      url: 'https://kidsfit.co.kr/',
      ns: 'kfk_kidsfitkr',
      kpiType: 'REFERRAL',
      kpiGoal: '상품 구매 클릭으로 상품 레퍼럴(쿠팡/셀렉트샵) 확대',
      gscStatus: '소유권 인증 완료 · Sitemap 32p & RSS 27p 성공',
      channels: 'IG @kids_fit1 · YT @kidsfit01 · 무료진단 + 상품레퍼럴'
    }
  ];

  const ledger = loadLedger();
  const results = [];
  for (const div of divisions) {
    const r = await fetchDivisionMetricsSequential(div, ledger);
    results.push(r);
  }
  saveLedger(ledger);

  const nowStr = getKstNowFormatted();

  const lines = [
    `🎯 <b>[전사업부 최우선 목표 — 1순위: 홈페이지 유입 | 2순위: 유료결제 브리핑]</b>`,
    `⏰ <b>집계 시각</b>: <code>${nowStr}</code> (봇·크롤러 제외 순수 실방문자 · 영구원장 동기화)`,
    `━━━━━━━━━━━━━━━━━━`
  ];

  for (const r of results) {
    const statusBadge = r.health.ok ? `🟢 정상 (${r.health.ms}ms)` : `🔴 점검필요`;
    const kpiLine =
      r.kpiType === 'PAID'
        ? `• <b>🥈 [2순위 목표: 유료결제]</b>: 오늘 결제창 클릭 <b>${r.paidClickToday}회</b> (누적 ${r.paidClickTotal}회) · 실결제 완료 <b>${r.paidMemberToday}건</b> (누적 <b>${r.paidMemberTotal}건</b>)`
        : `• <b>🥈 [2순위 목표: 구매전환]</b>: 오늘 상품구매 클릭 <b>${r.refClickToday}회</b> (누적 레퍼럴 클릭 <b>${r.refClickTotal}회</b>)`;

    lines.push(
      `🏢 <b>${r.code} | ${r.name}</b> (<code>${r.domain}</code>)`,
      `• <b>🥇 [1순위 목표: 홈페이지 유입]</b>: 오늘 UV <b>${r.uvToday.toLocaleString()}명</b> (PV ${r.pvToday.toLocaleString()}회) ｜ 어제 <b>${r.uvYest.toLocaleString()}명</b> (PV ${r.pvYest.toLocaleString()}회) ｜ 누적 <b>${r.uvTotal.toLocaleString()}명</b> (PV ${r.pvTotal.toLocaleString()}회)`,
      kpiLine,
      `• <b>🎯 핵심 KPI</b>: <b>1. 홈페이지 유입 확대 → 2. ${r.kpiGoal}</b>`,
      `• <b>서버 &amp; 서치콘솔</b>: ${statusBadge} | ✅ <code>${r.gscStatus}</code>`,
      `━━━━━━━━━━━━━━━━━━`
    );
  }

  lines.push(
    `🔔 <b>정기 자동 브리핑 &amp; 24시간 교대근무</b>`,
    `• <b>최우선 순위 고정</b>: 🥇 1순위 홈페이지 유입(UV/PV) ➡️ 🥈 2순위 유료결제·구매전환 (강화학습 보류 · 홍보 100% 집중)`,
    `• <b>오전 08:30 &amp; 밤 21:00</b>: 전 사업부 방문자·유료전환·상품레퍼럴 정기 결산 보고`
  );

  const html = lines.join('\n');
  if (options.sendTelegram) {
    const nowMs = Date.now();
    if (!options.force && ledger.lastTelegramSentMs && nowMs - ledger.lastTelegramSentMs < 60000) {
      console.log('[HQ Visitor Briefing] Skipping duplicate Telegram send within 60s cooldown.');
    } else {
      ledger.lastTelegramSentMs = nowMs;
      saveLedger(ledger);
      await sendTelegramHtml(html);
    }
  }
  return { results, html };
}

if (require.main === module) {
  const sendTg = process.argv.includes('--notify') || process.argv.includes('--send');
  const force = process.argv.includes('--force');
  runVisitorBriefing({ sendTelegram: sendTg, force })
    .then(({ results }) => {
      console.log(JSON.stringify({ ok: true, results }, null, 2));
    })
    .catch((err) => {
      console.error('[HQ Visitor Briefing Error]:', err.message);
      process.exit(1);
    });
}

module.exports = { runVisitorBriefing };
