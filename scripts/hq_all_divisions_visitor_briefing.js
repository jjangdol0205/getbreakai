#!/usr/bin/env node
/**
 * scripts/hq_all_divisions_visitor_briefing.js
 * 1·2·3사업부 통합 홈페이지 실방문자(UV/PV) & 사업부별 핵심 목표(1·2사업부: 유료회원 전환 / 3사업부: 상품 레퍼럴 클릭) 정기 브리핑 엔진
 */

'use strict';

const fs = require('fs');
const https = require('https');

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

function getKstDateString(offsetDays = 0) {
  const ms = Date.now() + 9 * 3600 * 1000 + offsetDays * 86400 * 1000;
  return new Date(ms).toISOString().slice(0, 10);
}

function getKstNowFormatted() {
  return new Date(Date.now() + 9 * 3600 * 1000).toISOString().replace('T', ' ').slice(0, 19) + ' KST';
}

function getAbacusCount(ns, key) {
  return new Promise((resolve) => {
    const url = `https://abacus.jasoncameron.dev/get/${ns}/${key}`;
    const req = https.get(url, { timeout: 5000 }, (res) => {
      let raw = '';
      res.on('data', (c) => (raw += c));
      res.on('end', () => {
        if (res.statusCode === 200) {
          try {
            const parsed = JSON.parse(raw);
            resolve(Number(parsed.value) || 0);
            return;
          } catch (_) {}
        }
        resolve(0);
      });
    });
    req.on('error', () => resolve(0));
    req.on('timeout', () => {
      req.destroy();
      resolve(0);
    });
  });
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

async function fetchDivisionMetrics(div) {
  const today = getKstDateString(0);
  const yesterday = getKstDateString(-1);
  const [
    uvToday,
    pvToday,
    uvYest,
    pvYest,
    uvTotal,
    pvTotal,
    paidClickToday,
    paidClickTotal,
    paidMemberToday,
    paidMemberTotal,
    refClickToday,
    refClickTotal,
    health
  ] = await Promise.all([
    getAbacusCount(div.ns, `uv_${today}`),
    getAbacusCount(div.ns, `pv_${today}`),
    getAbacusCount(div.ns, `uv_${yesterday}`),
    getAbacusCount(div.ns, `pv_${yesterday}`),
    getAbacusCount(div.ns, 'uv_total'),
    getAbacusCount(div.ns, 'pv_total'),
    getAbacusCount(div.ns, `paid_click_${today}`),
    getAbacusCount(div.ns, 'paid_click_total'),
    getAbacusCount(div.ns, `paid_member_${today}`),
    getAbacusCount(div.ns, 'paid_member_total'),
    getAbacusCount(div.ns, `ref_click_${today}`),
    getAbacusCount(div.ns, 'ref_click_total'),
    checkSiteHealth(div.url)
  ]);

  return {
    ...div,
    uvToday,
    pvToday,
    uvYest,
    pvYest,
    uvTotal: Math.max(uvTotal, uvToday),
    pvTotal: Math.max(pvTotal, pvToday),
    paidClickToday,
    paidClickTotal: Math.max(paidClickTotal, paidClickToday),
    paidMemberToday,
    paidMemberTotal: Math.max(paidMemberTotal, paidMemberToday),
    refClickToday,
    refClickTotal: Math.max(refClickTotal, refClickToday),
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

  const results = await Promise.all(divisions.map(fetchDivisionMetrics));
  const nowStr = getKstNowFormatted();

  const lines = [
    `📊 <b>[1·2·3사업부 방문 현황 &amp; 핵심 목표(유료회원·상품레퍼럴) 브리핑]</b>`,
    `⏰ <b>집계 시각</b>: <code>${nowStr}</code> (봇·크롤러 제외 순수 실방문자 기준)`,
    `━━━━━━━━━━━━━━━━━━`
  ];

  for (const r of results) {
    const statusBadge = r.health.ok ? `🟢 정상 (${r.health.ms}ms)` : `🔴 점검필요`;
    const kpiLine =
      r.kpiType === 'PAID'
        ? `• <b>💳 [목표: 유료회원 증대]</b>: 오늘 결제창 클릭 <b>${r.paidClickToday}회</b> (누적 ${r.paidClickTotal}회) · 신규 유료전환 <b>${r.paidMemberToday}명</b> (누적 <b>${r.paidMemberTotal}명</b>)`
        : `• <b>🛍️ [목표: 상품 레퍼럴 확대]</b>: 오늘 상품구매 클릭 <b>${r.refClickToday}회</b> (누적 레퍼럴 클릭 <b>${r.refClickTotal}회</b>)`;

    lines.push(
      `🏢 <b>${r.code} | ${r.name}</b> (<code>${r.domain}</code>)`,
      `• <b>핵심 목표</b>: 🎯 <b>${r.kpiGoal}</b>`,
      kpiLine,
      `• <b>오늘 실방문자(UV)</b>: <b>${r.uvToday.toLocaleString()}명</b> (페이지뷰 PV: <b>${r.pvToday.toLocaleString()}회</b> / 누적 UV: <b>${r.uvTotal.toLocaleString()}명</b>)`,
      `• <b>서버 &amp; 서치콘솔</b>: ${statusBadge} | ✅ <code>${r.gscStatus}</code>`,
      `━━━━━━━━━━━━━━━━━━`
    );
  }

  lines.push(
    `🔔 <b>정기 자동 브리핑 &amp; 24시간 교대근무</b>`,
    `• <b>새벽 05:00</b>: 유료전환(1·2사업부) &amp; 상품구매클릭(3사업부) 최우선 강화학습(RL) 자가개선`,
    `• <b>오전 08:30 &amp; 밤 21:00</b>: 전 사업부 방문자·유료전환·상품레퍼럴 정기 결산 보고`
  );

  const html = lines.join('\n');
  if (options.sendTelegram) {
    await sendTelegramHtml(html);
  }
  return { results, html };
}

if (require.main === module) {
  const sendTg = process.argv.includes('--notify') || process.argv.includes('--send');
  runVisitorBriefing({ sendTelegram: sendTg })
    .then(({ results }) => {
      console.log(JSON.stringify({ ok: true, results }, null, 2));
    })
    .catch((err) => {
      console.error('[HQ Visitor Briefing Error]:', err.message);
      process.exit(1);
    });
}

module.exports = { runVisitorBriefing };
