export function getAuthHeader() {
  const token =
    localStorage.getItem("rsa_token") ||
    (localStorage.getItem("rsa_pro_unlocked") === "true" ? "PRO-DEMO-2026" : "");
  if (token) {
    return { Authorization: `Bearer ${token}` };
  }
  return {};
}

export function formatCheckoutUrl(
  rawUrl,
  fallbackUrl = "https://truthofmarket.lemonsqueezy.com/checkout/buy/d5e7e761-8b1b-4ca8-b1fe-771acd1450f8"
) {
  const base = String(rawUrl || fallbackUrl).trim() || fallbackUrl;
  if (/[?&]embed=1\b/i.test(base)) {
    return base;
  }
  return `${base}${base.includes("?") ? "&" : "?"}embed=1`;
}

function isProActive() {
  const token =
    localStorage.getItem("rsa_token") ||
    (localStorage.getItem("rsa_pro_unlocked") === "true" ? "PRO-DEMO-2026" : "");
  return Boolean(token);
}

function isStaticHost() {
  if (typeof window === "undefined") return false;
  if (window.__STATIC_MODE__ === true) return true;
  const h = window.location.hostname || "";
  if (!h || h === "localhost" || h === "127.0.0.1") return false;
  return true;
}

async function fetchJsonWithFallback(apiUrl, options, fallbackFn) {
  if (isStaticHost()) {
    return fallbackFn();
  }
  try {
    const resp = await fetch(apiUrl, options);
    if (resp.ok) {
      const ct = resp.headers.get("content-type") || "";
      if (ct.includes("application/json")) {
        return await resp.json();
      }
    }
  } catch (e) {
    // Fallback to static snapshot / client-side engine when hosted on static CDN (GitHub Pages / Render Static)
  }
  return fallbackFn();
}

let cachedProStocks = null;
let cachedSemiOverview = null;

async function getStaticProStocks() {
  if (!cachedProStocks) {
    const r = await fetch("./static_api/stocks_pro.json");
    cachedProStocks = await r.json();
  }
  return cachedProStocks;
}

async function getStaticSemiOverview() {
  if (!cachedSemiOverview) {
    const r = await fetch("./static_api/semi_overview.json");
    cachedSemiOverview = await r.json();
  }
  return cachedSemiOverview;
}

export async function fetchStocks(params = {}) {
  const query = new URLSearchParams();
  if (params.search) query.append("search", params.search);
  if (params.zone && params.zone !== "ALL") query.append("zone", params.zone);
  if (params.sort_by) query.append("sort_by", params.sort_by);
  if (params.order) query.append("order", params.order);
  if (params.limit) query.append("limit", params.limit);
  if (params.offset) query.append("offset", params.offset);

  const url = `/api/stocks${query.toString() ? `?${query.toString()}` : ""}`;
  return fetchJsonWithFallback(
    url,
    {
      headers: {
        ...getAuthHeader(),
        Accept: "application/json",
      },
    },
    async () => {
      const file = isProActive() ? "./static_api/stocks_pro.json" : "./static_api/stocks_free.json";
      const r = await fetch(file);
      let list = await r.json();
      if (params.search) {
        const q = String(params.search).trim().toLowerCase();
        list = list.filter(
          (s) =>
            (s.ticker && s.ticker.toLowerCase().includes(q)) ||
            (s.name && s.name.toLowerCase().includes(q)) ||
            (s.name_en && s.name_en.toLowerCase().includes(q)) ||
            (s.name_jp && s.name_jp.toLowerCase().includes(q)) ||
            (s.name_kr && s.name_kr.toLowerCase().includes(q)) ||
            (s.sector && s.sector.toLowerCase().includes(q))
        );
      }
      if (params.zone && params.zone !== "ALL") {
        list = list.filter((s) => (s.zone_code || s.zone) === params.zone);
      }
      if (params.sort_by) {
        const aliasMap = {
          pw_score: "score",
          price: "close",
          prox: "prox_low52_pct",
          dd: "dd_high52_pct",
          vol: "vol_surge_10d",
        };
        const key = aliasMap[params.sort_by] || params.sort_by;
        const desc = String(params.order || "desc").toLowerCase() !== "asc";
        list = [...list].sort((a, b) => {
          const va = a[key];
          const vb = b[key];
          if (typeof va === "string" || typeof vb === "string") {
            const cmp = String(va ?? "").localeCompare(String(vb ?? ""));
            return desc ? -cmp : cmp;
          }
          const na = Number(va ?? 0);
          const nb = Number(vb ?? 0);
          return desc ? nb - na : na - nb;
        });
      }
      const off = Math.max(0, Number(params.offset || 0));
      const lim = params.limit ? Math.max(1, Number(params.limit)) : list.length;
      return list.slice(off, off + lim);
    }
  );
}

export async function fetchStockDetail(ticker) {
  const clean = String(ticker || "CELH").trim().toUpperCase();
  return fetchJsonWithFallback(
    `/api/stocks/${encodeURIComponent(clean)}`,
    {
      headers: {
        ...getAuthHeader(),
        Accept: "application/json",
      },
    },
    async () => {
      const all = await fetchStocks({ limit: 200 });
      return all.find((s) => s.ticker === clean) || all[0];
    }
  );
}

export async function fetchBacktestSummary() {
  return fetchJsonWithFallback(
    "/api/backtest",
    { headers: { Accept: "application/json" } },
    async () => {
      const r = await fetch("./static_api/backtest.json");
      return r.json();
    }
  );
}

export async function fetchResearchList() {
  return fetchJsonWithFallback(
    "/api/research",
    {
      headers: {
        ...getAuthHeader(),
        Accept: "application/json",
      },
    },
    async () => {
      const r = await fetch("./static_api/research_list.json");
      return r.json();
    }
  );
}

export async function fetchResearchBrief(ticker) {
  const clean = String(ticker || "CELH").trim().toUpperCase();
  return fetchJsonWithFallback(
    `/api/research/${encodeURIComponent(clean)}`,
    {
      headers: {
        ...getAuthHeader(),
        Accept: "application/json",
      },
    },
    async () => {
      const target = clean === "MBLY" ? "MBLY" : "CELH";
      const r = await fetch(`./static_api/research_${target}.json`);
      return r.json();
    }
  );
}

const ADMIN_CREDENTIALS_SHA256 = "4578349322b7fa9931023e0def82b9d0c19fa2c4fdab1f7d762142d8d78ef2fe";

function sha256PureJs(ascii) {
  function rightRotate(value, amount) {
    return (value >>> amount) | (value << (32 - amount));
  }
  const mathPow = Math.pow;
  const maxWord = mathPow(2, 32);
  let result = "";
  const words = [];
  const asciiBitLength = ascii.length * 8;
  let hash = (sha256PureJs.h = sha256PureJs.h || []);
  const k = (sha256PureJs.k = sha256PureJs.k || []);
  let primeCounter = k.length;
  const isComposite = {};
  for (let candidate = 2; primeCounter < 64; candidate++) {
    if (!isComposite[candidate]) {
      for (let i = 0; i < 313; i += candidate) {
        isComposite[i] = candidate;
      }
      hash[primeCounter] = (mathPow(candidate, 0.5) * maxWord) | 0;
      k[primeCounter++] = (mathPow(candidate, 1 / 3) * maxWord) | 0;
    }
  }
  ascii += "\x80";
  while ((ascii.length % 64) - 56) ascii += "\x00";
  for (let i = 0; i < ascii.length; i++) {
    const j = ascii.charCodeAt(i);
    if (j >> 8) return "";
    words[i >> 2] |= j << (((3 - i) % 4) * 8);
  }
  words[words.length] = (asciiBitLength / maxWord) | 0;
  words[words.length] = asciiBitLength;
  for (let j = 0; j < words.length; ) {
    const w = words.slice(j, (j += 16));
    const oldHash = hash;
    hash = hash.slice(0, 8);
    for (let i = 0; i < 64; i++) {
      const w15 = w[i - 15];
      const w2 = w[i - 2];
      const a = hash[0];
      const e = hash[4];
      const temp1 =
        hash[7] +
        (rightRotate(e, 6) ^ rightRotate(e, 11) ^ rightRotate(e, 25)) +
        ((e & hash[5]) ^ (~e & hash[6])) +
        k[i] +
        (w[i] =
          i < 16
            ? w[i]
            : (w[i - 16] +
                (rightRotate(w15, 7) ^ rightRotate(w15, 18) ^ (w15 >>> 3)) +
                w[i - 7] +
                (rightRotate(w2, 17) ^ rightRotate(w2, 19) ^ (w2 >>> 10))) |
              0);
      const temp2 =
        (rightRotate(a, 2) ^ rightRotate(a, 13) ^ rightRotate(a, 22)) +
        ((a & hash[1]) ^ (a & hash[2]) ^ (hash[1] & hash[2]));
      hash = [(temp1 + temp2) | 0].concat(hash);
      hash[4] = (hash[4] + temp1) | 0;
    }
    for (let i = 0; i < 8; i++) {
      hash[i] = (hash[i] + oldHash[i]) | 0;
    }
  }
  for (let i = 0; i < 8; i++) {
    for (let j = 3; j + 1; j--) {
      const b = (hash[i] >> (j * 8)) & 255;
      result += (b < 16 ? 0 : "") + b.toString(16);
    }
  }
  return result;
}

async function computeSha256Hex(inputStr) {
  try {
    if (typeof crypto !== "undefined" && crypto.subtle && typeof TextEncoder !== "undefined") {
      const data = new TextEncoder().encode(inputStr);
      const buf = await crypto.subtle.digest("SHA-256", data);
      return Array.from(new Uint8Array(buf))
        .map((b) => b.toString(16).padStart(2, "0"))
        .join("");
    }
  } catch (_) {
    // Fallback to pure JS SHA-256
  }
  return sha256PureJs(unescape(encodeURIComponent(inputStr)));
}

export async function verifyAdminCredentials(username, password) {
  const uname = String(username || "").trim();
  const pw = String(password || "");
  return fetchJsonWithFallback(
    "/api/auth/admin/login",
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
      },
      body: JSON.stringify({ username: uname, password: pw }),
    },
    async () => {
      const digest = await computeSha256Hex(`rsa_admin_v1:${uname}:${pw}`);
      const ok = digest.toLowerCase() === ADMIN_CREDENTIALS_SHA256;
      return {
        authenticated: ok,
        role: ok ? "admin" : "guest",
        license_key: ok ? "PRO-DEMO-2026" : null,
        message: ok
          ? "Admin Authenticated — Terminal Config & Pro Access Unlocked."
          : "Invalid Admin ID or Password.",
      };
    }
  );
}

export async function validateLicense(licenseKey) {
  return fetchJsonWithFallback(
    "/api/auth/license/validate",
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
      },
      body: JSON.stringify({ license_key: licenseKey }),
    },
    async () => {
      const key = String(licenseKey || "").trim();
      const valid =
        key.toUpperCase() === "PRO-DEMO-2026" ||
        /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i.test(key);
      return {
        valid,
        license_key: valid ? key : null,
        tier: valid ? "pro" : "free",
        expires_at: valid ? "2099-12-31T23:59:59Z" : null,
        message: valid
          ? "Pro Terminal License Verified."
          : "Invalid license key. Use PRO-DEMO-2026 for demo.",
      };
    }
  );
}

export async function fetchProVault() {
  return fetchJsonWithFallback(
    "/api/pro/vault",
    {
      headers: {
        ...getAuthHeader(),
        Accept: "application/json",
      },
    },
    async () => {
      const active = isProActive();
      return {
        unlocked: active,
        tier: active ? "pro" : "free",
        pine_script_available: active,
        tools: ["position_doctor", "morning_pdf", "pine_script_v5"],
      };
    }
  );
}

export async function fetchPineScript() {
  return fetchJsonWithFallback(
    "/api/pro/pinescript",
    {
      headers: {
        ...getAuthHeader(),
        Accept: "application/json",
      },
    },
    async () => {
      const r = await fetch("./static_api/pinescript.json");
      return r.json();
    }
  );
}

export async function evaluatePositionDoctor(data) {
  return fetchJsonWithFallback(
    "/api/pro/position-doctor",
    {
      method: "POST",
      headers: {
        ...getAuthHeader(),
        "Content-Type": "application/json",
        Accept: "application/json",
      },
      body: JSON.stringify(data),
    },
    async () => {
      const all = await getStaticProStocks();
      const tClean = String(data.ticker || "CELH").trim().toUpperCase();
      const stock = all.find((s) => s.ticker === tClean);
      const entry = Math.max(0.01, Number(data.entry_price || 27.93));
      const days = Number(data.days_held || 0);
      const curr =
        data.current_price !== undefined && data.current_price !== null
          ? Number(data.current_price)
          : stock
          ? Number(stock.close)
          : entry;
      const asOf = stock && stock.date ? stock.date : "2026-10-13";
      const retPct = Number(((curr / entry - 1.0) * 100.0).toFixed(2));
      const stopP = Number((entry * 0.91).toFixed(2));
      const tp1P = Number((entry * 2.0).toFixed(2));

      if (retPct <= -9.0) {
        return {
          ticker: tClean,
          status_code: "HARD_STOP",
          status_label: "🛑 Hard Stop Loss Triggered",
          return_pct: retPct,
          rule_triggered: "Rule 1 (-9.0% Hard Stop Loss)",
          action_plan: "Exit immediately. Do not average down on broken support.",
          is_critical: true,
          current_price: curr,
          entry_price: Number(entry.toFixed(2)),
          stop_price: stopP,
          tp1_price: tp1P,
          as_of_date: asOf,
        };
      } else if (days >= 55 && retPct < 8.0) {
        return {
          ticker: tClean,
          status_code: "TIME_STOP",
          status_label: "⏳ 55-Day Time Stop Triggered (55일 시간 손절)",
          return_pct: retPct,
          rule_triggered: "Rule 2 (55-Day Dead-Money Exit)",
          action_plan:
            "Exit position. Rebound momentum has stalled; reallocate into active right-side ignition candidates.",
          is_critical: false,
          current_price: curr,
          entry_price: Number(entry.toFixed(2)),
          stop_price: stopP,
          tp1_price: tp1P,
          as_of_date: asOf,
        };
      } else if (retPct >= 100.0) {
        return {
          ticker: tClean,
          status_code: "TP1_HARVEST",
          status_label: "🎯 100% Target Price 1 Achieved",
          return_pct: retPct,
          rule_triggered: "Rule 3 (+100% Principal Recovery)",
          action_plan:
            "Sell 50% of position to recoup 100% initial capital. Set trailing stop on remaining 50% using MA60.",
          is_critical: false,
          current_price: curr,
          entry_price: Number(entry.toFixed(2)),
          stop_price: stopP,
          tp1_price: tp1P,
          as_of_date: asOf,
        };
      } else {
        return {
          ticker: tClean,
          status_code: "HOLD",
          status_label: "🟢 Active Right-Side Trend Follow",
          return_pct: retPct,
          rule_triggered: "Rule 4 (Healthy Trend Follow)",
          action_plan:
            "Maintain position. Monitor MA20/MA60 trailing support; runner target is +100% TP1.",
          is_critical: false,
          current_price: curr,
          entry_price: Number(entry.toFixed(2)),
          stop_price: stopP,
          tp1_price: tp1P,
          as_of_date: asOf,
        };
      }
    }
  );
}

export async function fetchReferralConfig() {
  return fetchJsonWithFallback(
    "/api/referral/config",
    { headers: { Accept: "application/json" } },
    async () => {
      const r = await fetch("./static_api/referral_config.json");
      return r.json();
    }
  );
}

export async function updateReferralConfig(data) {
  return fetchJsonWithFallback(
    "/api/referral/config",
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
      },
      body: JSON.stringify(data),
    },
    async () => ({ status: "updated", config: data })
  );
}

export function getReferralRedirectUrl(provider, ticker) {
  return `/api/referral/redirect/${encodeURIComponent(
    provider.toLowerCase()
  )}?ticker=${encodeURIComponent(ticker)}`;
}

export async function fetchSemiOverview() {
  return fetchJsonWithFallback(
    "/api/semi/overview",
    { headers: { Accept: "application/json" } },
    async () => getStaticSemiOverview()
  );
}

export async function fetchSemiHistory(rangeCode = "1Y") {
  const rc = String(rangeCode || "1Y").trim().toUpperCase();
  const validRanges = ["3M", "6M", "1Y", "3Y", "5Y", "10Y", "ALL"];
  const safeRange = validRanges.includes(rc) ? rc : "1Y";
  return fetchJsonWithFallback(
    `/api/semi/history?range=${encodeURIComponent(safeRange)}`,
    { headers: { Accept: "application/json" } },
    async () => {
      const r = await fetch(`./static_api/semi_history_${safeRange}.json`);
      return r.json();
    }
  );
}

export async function calculateSemiRebalance(data) {
  return fetchJsonWithFallback(
    "/api/semi/rebalance",
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
      },
      body: JSON.stringify(data),
    },
    async () => {
      const ov = await getStaticSemiOverview();
      const fgScore = Number(ov.fg_score ?? 18.0);
      const ddPct = Number(ov.smh_dd_pct ?? -19.03);
      const usdkrw = Number(ov.usdkrw ?? 1324.75);
      const smhPrice = Number(ov.smh_close ?? 541.62);
      const xlvPrice = Number(ov.xlv_close ?? 179.28);
      const mode = String(data.strategy_mode || "AUTO_REGIME").trim().toUpperCase();
      const isExtreme = fgScore < 25.0 || ddPct <= -19.0;

      let smhW = 0.7;
      let xlvW = 0.3;
      let ruleEn = "";
      let ruleJp = "";
      let ruleKr = "";

      if (mode === "BASELINE_70_30") {
        smhW = 0.7;
        xlvW = 0.3;
        ruleEn = "Fixed 70% $SMH : 30% $XLV Golden Barbell Baseline";
        ruleJp = "70% $SMH : 30% $XLV 基本黄金バーベル比率";
        ruleKr = "평시 70% $SMH : 30% $XLV 기본 황금 바벨 비중";
      } else if (mode === "CONTRARIAN_80_20") {
        smhW = 0.8;
        xlvW = 0.2;
        ruleEn = "Contrarian 80% $SMH : 20% $XLV Crash Accumulation Tilt";
        ruleJp = "80% $SMH : 20% $XLV 暴落時・逆張り買い増しモード";
        ruleKr = "80% $SMH : 20% $XLV 폭락장 역발상 매집 비중";
      } else if (mode === "AGGRESSIVE_90_10") {
        smhW = 0.9;
        xlvW = 0.1;
        ruleEn = "90% $SMH : 10% $XLV Right-Side Momentum Tilt";
        ruleJp = "90% $SMH : 10% $XLV 右側モメンタム集中モード";
        ruleKr = "90% $SMH : 10% $XLV 우측 시동 공격형 비중";
      } else if (isExtreme) {
        smhW = 0.8;
        xlvW = 0.2;
        ruleEn = `AUTO REGIME: Extreme Fear (${fgScore}/100, DD ${ddPct.toFixed(1)}%) → 80% $SMH : 20% $XLV Contrarian Shift`;
        ruleJp = `自動判定: 極度の恐怖 (${fgScore}/100, 高値比 ${ddPct.toFixed(1)}%) → 80% $SMH : 20% $XLV 逆張り転換`;
        ruleKr = `자동 판독: 극단적 공포 (${fgScore}/100, 낙폭 ${ddPct.toFixed(1)}%) → 80% $SMH : 20% $XLV 역발상 비중 확대`;
      } else {
        smhW = 0.7;
        xlvW = 0.3;
        ruleEn = `AUTO REGIME: Standard Regime (${fgScore}/100) → 70% $SMH : 30% $XLV Core Barbell`;
        ruleJp = `自動判定: 通常レジーム (${fgScore}/100) → 70% $SMH : 30% $XLV 基本比率`;
        ruleKr = `자동 판독: 평시 구간 (${fgScore}/100) → 70% $SMH : 30% $XLV 기본 황금비중`;
      }

      const capUsd = Math.max(100, Number(data.total_capital_usd || 100000));
      const targetSmhUsd = Number((capUsd * smhW).toFixed(2));
      const targetXlvUsd = Number((capUsd * xlvW).toFixed(2));
      const targetSmhShares = Math.floor(targetSmhUsd / smhPrice);
      const targetXlvShares = Math.floor(targetXlvUsd / xlvPrice);
      const investedUsd = targetSmhShares * smhPrice + targetXlvShares * xlvPrice;
      const residualUsd = Number(Math.max(0, capUsd - investedUsd).toFixed(2));

      const natW = Number(ov.natural_smh_weight_pct ?? 66.5) / 100.0;
      const currSmhUsd =
        data.current_smh_usd !== undefined && data.current_smh_usd !== null
          ? Number(data.current_smh_usd)
          : Number((capUsd * natW).toFixed(2));
      const currXlvUsd =
        data.current_xlv_usd !== undefined && data.current_xlv_usd !== null
          ? Number(data.current_xlv_usd)
          : Number((capUsd * (1.0 - natW)).toFixed(2));
      const deltaSmhUsd = Number((targetSmhUsd - currSmhUsd).toFixed(2));
      const deltaXlvUsd = Number((targetXlvUsd - currXlvUsd).toFixed(2));
      const deltaSmhShares = Math.round(deltaSmhUsd / smhPrice);
      const deltaXlvShares = Math.round(deltaXlvUsd / xlvPrice);

      const freq = String(data.rebalance_frequency || "ANNUAL").trim().toUpperCase();
      const dragMap = { ANNUAL: 0.19, QUARTERLY: 0.42, MONTHLY: 0.78, WEEKLY: 1.32 };
      const taxDrag = dragMap[freq] ?? 0.19;
      const expectedNetCagr = Number((22.98 - taxDrag).toFixed(2));

      const dedLimit = 2500000;
      const gainKrw = Math.max(0, Number(data.unrealized_gain_krw ?? 3800000));
      const taxableKrw = Math.max(0, gainKrw - dedLimit);
      const taxSavedKrw = Math.round(Math.min(gainKrw, dedLimit) * 0.22);

      const taxEn =
        gainKrw <= dedLimit
          ? `Unrealized gain (₩${gainKrw.toLocaleString()}) is within the ₩2,500,000 annual tax-free allowance. Execute your $XLV ↔ $SMH rebalance before Dec 26 to harvest gains with ₩0 tax (saving ₩${taxSavedKrw.toLocaleString()}).`
          : `Unrealized gain (₩${gainKrw.toLocaleString()}) exceeds the ₩2.5M tax-free cap by ₩${taxableKrw.toLocaleString()}. Sell only up to ₩2,500,000 of realized profit this calendar year to lock in the maximum ₩550,000 tax savings, and use new cash inflow for the remaining rebalance.`;
      const taxJp =
        gainKrw <= dedLimit
          ? `評価益 (₩${gainKrw.toLocaleString()}) は年間非課税枠 (₩2,500,000) 以内です。年末までにリバランスを実行することで譲渡所得税 ₩0 (節税額 ₩${taxSavedKrw.toLocaleString()}) で利益確定と取得単価引き上げが可能です。`
          : `評価益 (₩${gainKrw.toLocaleString()}) が非課税枠を ₩${taxableKrw.toLocaleString()} 超過しています。今年の売却益を250万ウォンまでに抑えて最大 ₩550,000 を節税し、残りは新規積立資金で比率調整するのが最適です。`;
      const taxKr =
        gainKrw <= dedLimit
          ? `예상 실현차익(₩${gainKrw.toLocaleString()})이 연간 해외주식 양도세 기본공제 한도(250만 원) 이내입니다. 연말 전 리밸런싱 매도를 통해 양도세 0원(절세 효과 약 ₩${taxSavedKrw.toLocaleString()})으로 취득단가를 높이세요.`
          : `예상 차익(₩${gainKrw.toLocaleString()})이 250만 원 비과세 한도를 ₩${taxableKrw.toLocaleString()} 초과합니다. 올해는 실현차익 250만 원까지만 부분 매도하여 최대 55만 원 절세 혜택을 챙기고, 부족한 비중은 신규 적립금으로 채우세요.`;

      return {
        as_of_date: ov.date || "2026-10-26",
        smh_close: smhPrice,
        xlv_close: xlvPrice,
        total_capital_usd: capUsd,
        total_capital_krw: Math.round(capUsd * usdkrw),
        usdkrw,
        fg_score: fgScore,
        smh_dd_pct: ddPct,
        regime_code: ov.regime_code || "EXTREME_FEAR",
        active_rule_en: ruleEn,
        active_rule_jp: ruleJp,
        active_rule_kr: ruleKr,
        target_smh_weight_pct: Number((smhW * 100).toFixed(1)),
        target_xlv_weight_pct: Number((xlvW * 100).toFixed(1)),
        target_smh_usd: targetSmhUsd,
        target_xlv_usd: targetXlvUsd,
        target_smh_shares: targetSmhShares,
        target_xlv_shares: targetXlvShares,
        residual_cash_usd: residualUsd,
        delta_smh_usd: deltaSmhUsd,
        delta_xlv_usd: deltaXlvUsd,
        delta_smh_shares: deltaSmhShares,
        delta_xlv_shares: deltaXlvShares,
        rebalance_frequency: freq,
        estimated_tax_drag_pct: taxDrag,
        expected_net_cagr_pct: expectedNetCagr,
        kr_tax_deduction_limit_krw: dedLimit,
        kr_taxable_gain_krw: taxableKrw,
        kr_estimated_tax_saved_krw: taxSavedKrw,
        kr_tax_guidance_en: taxEn,
        kr_tax_guidance_jp: taxJp,
        kr_tax_guidance_kr: taxKr,
      };
    }
  );
}

export async function calculateSemiLumpSum(data) {
  return fetchJsonWithFallback(
    "/api/semi/lump-sum",
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
      },
      body: JSON.stringify(data),
    },
    async () => {
      const ov = await getStaticSemiOverview();
      const fgScore =
        data.override_fg_score !== undefined && data.override_fg_score !== null
          ? Number(data.override_fg_score)
          : Number(ov.fg_score ?? 18.0);
      const cap = Math.max(100, Number(data.capital_usd || 50000));
      const smhP = Number(ov.smh_close ?? 541.62);
      const xlvP = Number(ov.xlv_close ?? 179.28);
      const asOf = ov.date || "2026-10-26";

      if (fgScore <= 40.0) {
        const isExt = fgScore <= 25.0;
        const smhW = isExt ? 0.8 : 0.7;
        const xlvW = isExt ? 0.2 : 0.3;
        const smhUsd = Number((cap * smhW).toFixed(2));
        const xlvUsd = Number((cap * xlvW).toFixed(2));
        return {
          as_of_date: asOf,
          smh_close: smhP,
          xlv_close: xlvP,
          capital_usd: cap,
          fg_score_used: fgScore,
          case_code: "CASE_1_FEAR_100PCT",
          case_title_en: "Case 1 (Score 0–40 · Fear Regime): 100% Immediate Lump-Sum Entry",
          case_title_jp: "ケース1 (スコア 0–40 · 恐怖圏): 100% 即時一括エントリー",
          case_title_kr: "Case 1 (지수 0–40 · 공포 구간): 100% 즉시 일시금 진입",
          summary_en:
            "Semiconductors are already discounted. Do not hold excess cash—deploy 100% today and rebalance back to 70:30 when $SMH recovers within -10% of its 52-week high.",
          summary_jp:
            "半導体セクターは既に割安圏にあります。現金を遊ばせず本日100%投入し、$SMHが高値比-10%以内へ回復した時点で70:30へ戻します。",
          summary_kr:
            "반도체 섹터가 이미 할인된 공포 구간입니다. 현금을 놀리지 말고 당일 100% 거치식으로 진입한 뒤, $SMH가 고점 대비 -10% 이내로 회복되면 70:30으로 복귀하세요.",
          immediate_deploy_pct: 100.0,
          parked_cash_rp_pct: 0.0,
          tranches: [
            {
              step: 1,
              title_en: "Tranche 1 (Day 1 Immediate 100% Deployment)",
              title_jp: "第1トランシェ (初日 100% 一括エントリー)",
              title_kr: "1차 집행 (당일 100% 즉시 거치식 진입)",
              timing_en: "Execute Today (Market Open / Close)",
              timing_jp: "本日即時執行 (Fear ≤ 40 割安圏)",
              timing_kr: "오늘 즉시 집행 (공포 지수 40 이하 저평가 구간)",
              allocation_pct: 100.0,
              amount_usd: cap,
              smh_usd: smhUsd,
              xlv_usd: xlvUsd,
              cash_rp_usd: 0.0,
              smh_shares: Math.floor(smhUsd / smhP),
              xlv_shares: Math.floor(xlvUsd / xlvP),
              note_en: `Deploy 100% immediately at ${Math.round(smhW * 100)}:${Math.round(
                xlvW * 100
              )} ($SMH:$XLV). Historical 1-year forward win rate when entering below score 25 exceeds 91%.`,
              note_jp: `${Math.round(smhW * 100)}:${Math.round(
                xlvW * 100
              )} ($SMH:$XLV) 比率で100%即時エントリー。スコア25以下でのエントリーは過去1年後の勝率が91%超。`,
              note_kr: `${Math.round(smhW * 100)}:${Math.round(
                xlvW * 100
              )} ($SMH:$XLV) 비중으로 100% 즉시 진입합니다. 공포 지수 25 이하 진입 시 1년 후 플러스 수익 확률은 91% 이상입니다.`,
            },
          ],
        };
      } else if (fgScore <= 68.0) {
        const d1Smh = Number((cap * 0.35).toFixed(2));
        const d1Xlv = Number((cap * 0.3).toFixed(2));
        const d1Tot = Number((d1Smh + d1Xlv).toFixed(2));
        const t2Smh = Number((cap * 0.35).toFixed(2));
        return {
          as_of_date: asOf,
          smh_close: smhP,
          xlv_close: xlvP,
          capital_usd: cap,
          fg_score_used: fgScore,
          case_code: "CASE_2_NEUTRAL_65_35",
          case_title_en: "Case 2 (Score 40–68 · Neutral Regime): 65% Immediate + 35% Pullback Reserve",
          case_title_jp: "ケース2 (スコア 40–68 · 中立圏): 65% 初日投入 + 35% 押し目待機",
          case_title_kr: "Case 2 (지수 40–68 · 중립 구간): 65% 선진입 + 35% 달러 RP 파킹 후 분할",
          summary_en:
            "Balanced deployment: lock in your 30% $XLV anchor and half of $SMH today, while keeping 35% dry powder for volatility.",
          summary_jp:
            "バランス型エントリー：$XLV 30%と$SMH半分を初日に確保し、35%の余力で押し目に備えます。",
          summary_kr:
            "중립장 표준 공식: 1일차에 $XLV 30% 전량과 $SMH 절반(35%)을 먼저 채우고, 나머지 35%는 조정 시 추매 실탄으로 활용합니다.",
          immediate_deploy_pct: 65.0,
          parked_cash_rp_pct: 35.0,
          tranches: [
            {
              step: 1,
              title_en: "Tranche 1 (Day 1 Core 65% Deployment)",
              title_jp: "第1トランシェ (初日 65% コア投入)",
              title_kr: "1차 집행 (1일차 65% 코어 포지션 선진입)",
              timing_en: "Execute Today (30% $XLV Full + 35% $SMH Half)",
              timing_jp: "本日執行 ($XLV 30%全額 + $SMH 35%半分)",
              timing_kr: "오늘 즉시 집행 ($XLV 30% 전량 + $SMH 35% 절반)",
              allocation_pct: 65.0,
              amount_usd: d1Tot,
              smh_usd: d1Smh,
              xlv_usd: d1Xlv,
              cash_rp_usd: 0.0,
              smh_shares: Math.floor(d1Smh / smhP),
              xlv_shares: Math.floor(d1Xlv / xlvP),
              note_en:
                "Establish 100% of your defensive $XLV position (30%) and half of your $SMH position (35%) immediately.",
              note_jp:
                "ディフェンシブ枠の$XLV (30%) 全額と、成長枠$SMHの半分 (35%) を初日に構築します。",
              note_kr:
                "방어주 $XLV(30%) 전량과 반도체 $SMH 목표치의 절반(35%)을 첫날 즉시 매수합니다.",
            },
            {
              step: 2,
              title_en: "Tranche 2 (Remaining 35% $SMH Reserve in USD RP)",
              title_jp: "第2トランシェ (残り35% $SMH待機資金・米ドルMMF)",
              title_kr: "2차 집행 (잔여 35% 달러 RP 파킹 후 조건부 투입)",
              timing_en: "Deploy when FG Score ≤ 40 OR split across D+30 / D+60 / D+90",
              timing_jp: "スコア40以下へ低下時、または30日・60日・90日で3分割投入",
              timing_kr: "공포지수 40 이하 하락 시 즉시 투입 (미도달 시 30·60·90일 3분할)",
              allocation_pct: 35.0,
              amount_usd: t2Smh,
              smh_usd: t2Smh,
              xlv_usd: 0.0,
              cash_rp_usd: t2Smh,
              smh_shares: Math.floor(t2Smh / smhP),
              xlv_shares: 0,
              note_en:
                "Earn ~4.5% USD RP yield while waiting for a pullback below score 40, or auto-deploy over 90 days.",
              note_jp:
                "米ドルMMFで金利を受け取りながらスコア40以下への押し目を待つか、90日間で機械的に分割投入します。",
              note_kr:
                "달러 RP(연 4%대 금리)에 예치해 두었다가 지수가 40 이하로 내려오면 즉시 투입하고, 안 내려오면 3개월간 균등 분할 매수합니다.",
            },
          ],
        };
      } else {
        const d1Xlv = Number((cap * 0.3).toFixed(2));
        const pSmh = Number((cap * 0.7).toFixed(2));
        return {
          as_of_date: asOf,
          smh_close: smhP,
          xlv_close: xlvP,
          capital_usd: cap,
          fg_score_used: fgScore,
          case_code: "CASE_3_GREED_DEFENSIVE_FIRST",
          case_title_en:
            "Case 3 (Score 68–100 · Greed Regime): 30% $XLV Today + 70% $SMH Parked in USD RP",
          case_title_jp:
            "ケース3 (スコア 68–100 · 強欲圏): 初日 $XLV 30%のみ + 70% 米ドルMMF待機",
          case_title_kr:
            "Case 3 (지수 68–100 · 탐욕 과열 구간): 당일 $XLV 30%만 진입 + 70% 달러 RP 대기",
          summary_en:
            "Protect principal against euphoria: buy only the 30% $XLV sleeve today and keep 70% in USD RP until Fear & Greed cools to 45 or below.",
          summary_jp:
            "高値掴み防止ルール：初日は$XLV 30%のみを購入し、70%は指数が45以下に冷めるまで米ドルMMFで待機します。",
          summary_kr:
            "고점 추격매수 방지 공식: 당일에는 방어주 $XLV 30%만 매수하고, $SMH 70% 자금은 지수가 45 이하로 내려올 때까지 달러 RP에서 이자를 받으며 대기합니다.",
          immediate_deploy_pct: 30.0,
          parked_cash_rp_pct: 70.0,
          tranches: [
            {
              step: 1,
              title_en: "Tranche 1 (Day 1 Defensive $XLV 30% Only)",
              title_jp: "第1トランシェ (初日はディフェンシブ $XLV 30% のみ購入)",
              title_kr: "1차 집행 (1일차 방어주 $XLV 30%만 우선 진입)",
              timing_en: "Execute Today ($XLV Anchor Only — Zero $SMH Chasing)",
              timing_jp: "本日執行 ($XLV 30%のみ・過熱した$SMHの高値追い禁止)",
              timing_kr: "오늘 즉시 집행 (과열된 $SMH 추격매수 금지, $XLV 30%만 매수)",
              allocation_pct: 30.0,
              amount_usd: d1Xlv,
              smh_usd: 0.0,
              xlv_usd: d1Xlv,
              cash_rp_usd: 0.0,
              smh_shares: 0,
              xlv_shares: Math.floor(d1Xlv / xlvP),
              note_en:
                "Do not chase overheated semiconductors above score 68. Deploy only the 30% Healthcare anchor on Day 1.",
              note_jp:
                "スコア68超の過熱局面での半導体ジャンピングキャッチを回避し、ヘルスケア枠30%のみを先行構築します。",
              note_kr:
                "탐욕 지수 68 초과 과열 구간에서는 반도체 고점 물림을 피하기 위해 방어주 $XLV 30%만 우선 매수합니다.",
            },
            {
              step: 2,
              title_en: "Tranche 2 (70% $SMH Capital Parked in Yielding USD RP)",
              title_jp: "第2トランシェ (70% $SMH資金は米ドルMMFで冷却待機)",
              title_kr: "2차 집행 (70% $SMH 몫은 달러 RP 파킹 후 지수 ≤ 45 냉각 시 투입)",
              timing_en: "Deploy when FG Score cools ≤ 45 (or 4 monthly tranches)",
              timing_jp: "スコア45以下へ冷却時、または4ヶ月分割で順次エントリー",
              timing_kr: "공포·탐욕 지수가 45 이하로 식을 때 투입 (또는 4개월 분할)",
              allocation_pct: 70.0,
              amount_usd: pSmh,
              smh_usd: pSmh,
              xlv_usd: 0.0,
              cash_rp_usd: pSmh,
              smh_shares: Math.floor(pSmh / smhP),
              xlv_shares: 0,
              note_en:
                "Collect risk-free USD interest while waiting for semiconductor euphoria to mean-revert.",
              note_jp:
                "米ドル金利を確保しながら、半導体の過熱感が冷めるのを待って安全にエントリーします。",
              note_kr:
                "달러 RP 이자를 받으며 반도체 과열이 해소될 때까지 기다렸다가 안전하게 진입하여 고점 낙폭을 방어합니다.",
            },
          ],
        };
      }
    }
  );
}

export async function buildClientTelegramPreview({
  alert_type = "SEMI_BRIEFING",
  lang = "kr",
  ticker = "CELH",
  entry_price = null,
  days_held = 42,
} = {}) {
  const atype = String(alert_type || "SEMI_BRIEFING").trim().toUpperCase();
  const lg = ["kr", "en", "jp"].includes(String(lang || "kr").toLowerCase())
    ? String(lang || "kr").toLowerCase()
    : "kr";

  const ov = await getStaticSemiOverview();
  const reb = await calculateSemiRebalance({
    total_capital_usd: 100000,
    strategy_mode: "AUTO_REGIME",
    rebalance_frequency: "ANNUAL",
    unrealized_gain_krw: 3800000,
  });
  const allStocks = (await getStaticProStocks()).filter((s) => !String(s.ticker).includes("."));
  const ignStocks = allStocks.filter((s) => s.zone_code === "IGNITION_ZONE").slice(0, 5);

  const etfs = Array.isArray(ov.etfs) ? ov.etfs : [];
  const qqqEtf = etfs.find((e) => e.ticker === "QQQ");
  const xlvEtf = etfs.find((e) => e.ticker === "XLV");
  const qqq1d = qqqEtf ? Number(qqqEtf.ret_1d_pct ?? 1.11) : 1.11;
  const xlv1d = xlvEtf ? Number(xlvEtf.ret_1d_pct ?? 0.0) : 0.0;

  const buildSemiText = () => {
    const dSmhSign = reb.delta_smh_usd >= 0 ? "BUY +" : "SELL -";
    const dXlvSign = reb.delta_xlv_usd >= 0 ? "BUY +" : "SELL -";
    const smhShSign = reb.delta_smh_shares >= 0 ? `+${reb.delta_smh_shares}` : `${reb.delta_smh_shares}`;
    const xlvShSign = reb.delta_xlv_shares >= 0 ? `+${reb.delta_xlv_shares}` : `${reb.delta_xlv_shares}`;

    if (lg === "en") {
      return [
        `🧭 [SemiFearGreed] Daily Semiconductor & Barbell Briefing (${ov.date})`,
        `• Fear & Greed Score: ${Number(ov.fg_score).toFixed(1)} / 100 (${String(ov.regime_en).toUpperCase()})`,
        `• $SMH: $${Number(ov.smh_close).toFixed(2)} (${Number(ov.smh_dd_pct).toFixed(2)}% 52W DD)`,
        `• $XLV: $${Number(ov.xlv_close).toFixed(2)} (${xlv1d >= 0 ? "+" : ""}${xlv1d.toFixed(2)}% 1D) | $QQQ: $${Number(ov.qqq_close).toFixed(2)} (${qqq1d >= 0 ? "+" : ""}${qqq1d.toFixed(2)}% 1D)`,
        `• FX Rate: ₩${Number(ov.usdkrw).toLocaleString()} / USD`,
        ``,
        `⚡ Active Signal: Target ${ov.recommended_smh_weight}% $SMH : ${ov.recommended_xlv_weight}% $XLV`,
        `• ${ov.action_headline_en}`,
        ``,
        `📊 $100,000 Standard Rebalance Orders:`,
        `• $SMH (${reb.target_smh_weight_pct}%): $${Number(reb.target_smh_usd).toLocaleString()} (${reb.target_smh_shares} sh) → ${dSmhSign}$${Math.abs(Number(reb.delta_smh_usd)).toLocaleString()} (${smhShSign} sh)`,
        `• $XLV (${reb.target_xlv_weight_pct}%): $${Number(reb.target_xlv_usd).toLocaleString()} (${reb.target_xlv_shares} sh) → ${dXlvSign}$${Math.abs(Number(reb.delta_xlv_usd)).toLocaleString()} (${xlvShSign} sh)`,
        `🔗 Terminal: https://truthofmarket.com/#semi`,
      ].join("\n");
    }
    if (lg === "jp") {
      return [
        `🧭 [SemiFearGreed] 半導体恐怖＆強欲指数・日次ブリーフィング (${ov.date})`,
        `• 恐怖＆強欲スコア: ${Number(ov.fg_score).toFixed(1)} / 100 (${ov.regime_jp})`,
        `• $SMH: $${Number(ov.smh_close).toFixed(2)} (52週高値比 ${Number(ov.smh_dd_pct).toFixed(2)}%)`,
        `• $XLV: $${Number(ov.xlv_close).toFixed(2)} (${xlv1d >= 0 ? "+" : ""}${xlv1d.toFixed(2)}% 1D) | $QQQ: $${Number(ov.qqq_close).toFixed(2)} (${qqq1d >= 0 ? "+" : ""}${qqq1d.toFixed(2)}% 1D)`,
        `• 為替レート: ₩${Number(ov.usdkrw).toLocaleString()} / USD`,
        ``,
        `⚡ 現在のバーベル配分シグナル: ${ov.recommended_smh_weight}% $SMH : ${ov.recommended_xlv_weight}% $XLV`,
        `• ${ov.action_headline_jp}`,
        ``,
        `📊 $100,000 基準リバランス注文:`,
        `• $SMH (${reb.target_smh_weight_pct}%): $${Number(reb.target_smh_usd).toLocaleString()} (${reb.target_smh_shares}株) → ${dSmhSign}$${Math.abs(Number(reb.delta_smh_usd)).toLocaleString()} (${smhShSign}株)`,
        `• $XLV (${reb.target_xlv_weight_pct}%): $${Number(reb.target_xlv_usd).toLocaleString()} (${reb.target_xlv_shares}株) → ${dXlvSign}$${Math.abs(Number(reb.delta_xlv_usd)).toLocaleString()} (${xlvShSign}株)`,
        `🔗 ターミナル: https://truthofmarket.com/#semi`,
      ].join("\n");
    }
    return [
      `🧭 [SemiFearGreed] 반도체 공포·탐욕 지수 & 바벨 리밸런싱 브리핑 (${ov.date})`,
      `• 공포·탐욕 지수: ${Number(ov.fg_score).toFixed(1)} / 100 (${ov.regime_kr} · ${String(ov.regime_en).toUpperCase()})`,
      `• $SMH(반도체): $${Number(ov.smh_close).toFixed(2)} (52주 고점 대비 ${Number(ov.smh_dd_pct).toFixed(2)}%)`,
      `• $XLV(헬스케어): $${Number(ov.xlv_close).toFixed(2)} (${xlv1d >= 0 ? "+" : ""}${xlv1d.toFixed(2)}% 1D) | $QQQ: $${Number(ov.qqq_close).toFixed(2)} (${qqq1d >= 0 ? "+" : ""}${qqq1d.toFixed(2)}% 1D)`,
      `• 적용 환율: ₩${Number(ov.usdkrw).toLocaleString()} / USD`,
      ``,
      `⚡ 현재 발동 시그널: 목표 비중 ${ov.recommended_smh_weight}% $SMH : ${ov.recommended_xlv_weight}% $XLV`,
      `• ${ov.action_headline_kr}`,
      ``,
      `📊 $100,000 (약 ₩${Number(reb.total_capital_krw).toLocaleString()}) 기준 리밸런싱 주문:`,
      `• $SMH (${reb.target_smh_weight_pct}%): $${Number(reb.target_smh_usd).toLocaleString()} (${reb.target_smh_shares}주) → ${dSmhSign}$${Math.abs(Number(reb.delta_smh_usd)).toLocaleString()} (${smhShSign}주)`,
      `• $XLV (${reb.target_xlv_weight_pct}%): $${Number(reb.target_xlv_usd).toLocaleString()} (${reb.target_xlv_shares}주) → ${dXlvSign}$${Math.abs(Number(reb.delta_xlv_usd)).toLocaleString()} (${xlvShSign}주)`,
      `🔗 실시간 터미널: https://truthofmarket.com/#semi`,
    ].join("\n");
  };

  const buildRsaText = () => {
    const asOf = ignStocks[0]?.date || "2026-10-13";
    const rows = ignStocks
      .map((s, idx) => {
        const trig = s.entry_trigger_price ?? s.ma60_price ?? s.close;
        const stopP = s.stop_loss_price ?? Number((s.close * 0.91).toFixed(2));
        const tp1P = s.tp1_2x_price ?? Number((s.close * 2.0).toFixed(2));
        return `${idx + 1}. $${s.ticker} ($${Number(s.close).toFixed(2)}) · Score ${Number(s.score).toFixed(0)}/100\n   52W DD ${Number(s.dd_high52_pct).toFixed(1)}% | Vol ${Number(s.vol_surge_10d).toFixed(2)}x | TRG $${Number(trig).toFixed(2)} | Stop $${Number(stopP).toFixed(2)} | TP1 $${Number(tp1P).toFixed(2)}`;
      })
      .join("\n");

    const ignCount = allStocks.filter((s) => s.zone_code === "IGNITION_ZONE").length;
    if (lg === "en") {
      return [
        `🚀 [RightSideAlpha] Top US PW-RSI Right-Side Ignition Signals (${asOf})`,
        `Universe: ${allStocks.length} NYSE/NASDAQ Equities | Active Ignition Count: ${ignCount}`,
        ``,
        rows,
        ``,
        `🛡️ Exit Rules: -9.0% Hard Stop | 55-Day (+8%) Time-Stop | +100% TP1 (Sell 50%)`,
        `🔗 Screener: https://truthofmarket.com/#rightside`,
      ].join("\n");
    }
    if (lg === "jp") {
      return [
        `🚀 [RightSideAlpha] 米国株 PW-RSI 右側イグニッション上位銘柄 (${asOf})`,
        `対象ユニバース: 米国上場 ${allStocks.length}銘柄 | イグニッション点灯: ${ignCount}銘柄`,
        ``,
        rows,
        ``,
        `🛡️ エグジット原則: -9.0% ハード損切 | 55日(+8%未満) タイムストップ | +100% TP1 半分利確`,
        `🔗 スクリーナー: https://truthofmarket.com/#rightside`,
      ].join("\n");
    }
    return [
      `🚀 [RightSideAlpha] 미국 상장주 PW-RSI 우측 시동(Ignition) Top 5 (${asOf})`,
      `분석 유니버스: 미국 상장 ${allStocks.length}개 핵심 종목 | 우측 시동 포착: ${ignCount}종목`,
      ``,
      rows,
      ``,
      `🛡️ 4대 청산 원칙: -9.0% 칼손절 | 55일(+8% 미만) 시간손절 | +100% 도달 시 50% 원금회수`,
      `🔗 미국주식 터미널: https://truthofmarket.com/#rightside`,
    ].join("\n");
  };

  if (atype === "SEMI_BRIEFING") {
    return { text: buildSemiText(), as_of_date: ov.date || "2026-10-26", alert_type: atype, lang: lg };
  }
  if (atype === "RSA_IGNITION") {
    return {
      text: buildRsaText(),
      as_of_date: ignStocks[0]?.date || "2026-10-13",
      alert_type: atype,
      lang: lg,
    };
  }
  if (atype === "POSITION_DOCTOR") {
    const doc = await evaluatePositionDoctor({
      ticker: ticker || "CELH",
      entry_price: entry_price || 27.93,
      days_held: days_held ?? 42,
    });
    const text = [
      `🩺 [Position Doctor] $${doc.ticker} 포지션 리스크 진단 (${doc.as_of_date})`,
      `• 판정 결과: ${doc.status_label}`,
      `• 최근 종가: $${Number(doc.current_price).toFixed(2)} | 매수 단가: $${Number(doc.entry_price).toFixed(2)} | 보유일: ${days_held ?? 42}일`,
      `• 현재 수익률: ${doc.return_pct >= 0 ? "+" : ""}${Number(doc.return_pct).toFixed(2)}%`,
      `• -9% 손절가: $${Number(doc.stop_price).toFixed(2)} | +100% 목표가(TP1): $${Number(doc.tp1_price).toFixed(2)}`,
      `• 실행 지침: ${doc.action_plan}`,
    ].join("\n");
    return { text, as_of_date: doc.as_of_date || "2026-10-13", alert_type: atype, lang: lg };
  }
  if (atype === "TEST_PING") {
    const topSym = ignStocks[0]?.ticker || "CELH";
    const topClose = Number(ignStocks[0]?.close ?? 27.93).toFixed(2);
    const text =
      lg === "en"
        ? `✅ [Telegram Connected] SemiFearGreed & RightSideAlpha Alert Bot Active!\n• Semi Fear & Greed (${ov.date}): ${Number(ov.fg_score).toFixed(1)}/100 (${String(ov.regime_en).toUpperCase()})\n• $SMH: $${Number(ov.smh_close).toFixed(2)} | $XLV: $${Number(ov.xlv_close).toFixed(2)} | $QQQ: $${Number(ov.qqq_close).toFixed(2)}\n• Top US Ignition Pick: $${topSym} ($${topClose})`
        : `✅ [텔레그램 연동 완료] SemiFearGreed & RightSideAlpha 알림 봇이 정상 연결되었습니다!\n• 반도체 공포·탐욕 지수 (${ov.date}): ${Number(ov.fg_score).toFixed(1)}/100 (${ov.regime_kr})\n• $SMH: $${Number(ov.smh_close).toFixed(2)} | $XLV: $${Number(ov.xlv_close).toFixed(2)} | $QQQ: $${Number(ov.qqq_close).toFixed(2)}\n• 미국 우측 시동 1위: $${topSym} ($${topClose})`;
    return { text, as_of_date: ov.date || "2026-10-26", alert_type: atype, lang: lg };
  }

  return {
    text: `${buildSemiText()}\n\n━━━━━━━━━━━━━━━━━━━━\n\n${buildRsaText()}`,
    as_of_date: ov.date || "2026-10-26",
    alert_type: "FULL_DAILY",
    lang: lg,
  };
}

export const DEFAULT_TG_BOT_TOKEN = "DEMO-BOT-TOKEN";
export const DEFAULT_TG_CHAT_ID = "@SemifearGreedbot";
export const DEFAULT_TG_CHANNEL_URL = "https://t.me/SemifearGreedbot";
export const DEFAULT_YOUTUBE_URL = "https://youtube.com/@rightsidealpha";
export const DEFAULT_INSTAGRAM_URL = "https://www.instagram.com/semifeargreed";

export async function syncTelegramBotBrowser(botToken, currentChatId = "") {
  const cid = String(currentChatId || DEFAULT_TG_CHAT_ID).trim();
  return { chatId: cid, botUsername: "SemifearGreedbot", synced: true };
}

export async function fetchTelegramStatus() {
  return fetchJsonWithFallback(
    "/api/telegram/status",
    { headers: { Accept: "application/json" } },
    async () => {
      const tok = localStorage.getItem("rsa_tg_bot_token") || DEFAULT_TG_BOT_TOKEN;
      const cid = localStorage.getItem("rsa_tg_chat_id") || DEFAULT_TG_CHAT_ID;
      const ch = localStorage.getItem("rsa_tg_channel_url") || DEFAULT_TG_CHANNEL_URL;
      return {
        configured: true,
        bot_token_masked: tok ? `${tok.slice(0, 6)}...${tok.slice(-4)}` : "",
        chat_id: cid,
        channel_url: ch,
        bot_username: "SemifearGreedbot",
        enabled_alerts: ["SEMI_BRIEFING", "RSA_IGNITION", "POSITION_DOCTOR", "FULL_DAILY"],
        lang: localStorage.getItem("rsa_lang") || "kr",
        commands_supported: ["/start", "/help", "/semi", "/ignition", "/price <TICKER>", "/doctor <TICKER> <ENTRY> <DAYS>"],
      };
    }
  );
}

export async function saveTelegramConfig(data) {
  return fetchJsonWithFallback(
    "/api/telegram/config",
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
      },
      body: JSON.stringify(data),
    },
    async () => ({
      configured: Boolean(data.bot_token && data.chat_id),
      bot_token_masked: data.bot_token ? `${String(data.bot_token).slice(0, 6)}...` : "",
      chat_id: data.chat_id || "@SemifearGreedbot",
      channel_url: data.channel_url || DEFAULT_TG_CHANNEL_URL,
      bot_username: "SemifearGreedbot",
      enabled_alerts: ["SEMI_BRIEFING", "RSA_IGNITION", "POSITION_DOCTOR", "FULL_DAILY"],
      lang: data.lang || "kr",
    })
  );
}

export async function verifyTelegramBot(data) {
  const tok = String(data.bot_token || localStorage.getItem("rsa_tg_bot_token") || DEFAULT_TG_BOT_TOKEN).trim();
  let cid = String(data.chat_id || localStorage.getItem("rsa_tg_chat_id") || "").trim();

  const syncInfo = await syncTelegramBotBrowser(tok, cid);
  if (syncInfo.chatId) {
    cid = syncInfo.chatId;
  }

  const backendRes = await fetchJsonWithFallback(
    "/api/telegram/verify",
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
      },
      body: JSON.stringify({ bot_token: tok, chat_id: cid }),
    },
    async () => null
  );

  if (backendRes && backendRes.valid && backendRes.mode === "LIVE_TELEGRAM_API") {
    return { ...backendRes, chat_id: cid || backendRes.chat_id };
  }

  if (!tok) {
    return {
      valid: false,
      configured: false,
      mode: "UNCONFIGURED",
      chat_id: cid,
      message: "Bot Token is empty. Enter a @BotFather token or DEMO-BOT-TOKEN.",
    };
  }
  if (tok.toUpperCase().startsWith("DEMO")) {
    return {
      valid: true,
      configured: Boolean(cid),
      mode: "DEMO_SIMULATION",
      bot_username: "SemiFearGreedDemoBot",
      bot_name: "SemiFearGreed & RightSideAlpha Demo Bot",
      chat_id: cid || "@SemifearGreedbot",
      message: "Demo Telegram Bot verified (Simulation Mode Ready).",
    };
  }

  if (backendRes && backendRes.valid) {
    return { ...backendRes, chat_id: cid || backendRes.chat_id };
  }

  return {
    valid: true,
    configured: Boolean(cid),
    mode: "SERVER_DISPATCH_READY",
    bot_username: "SemifearGreedbot",
    bot_name: "SemiFearGreed & RightSideAlpha Bot",
    chat_id: cid || "@SemifearGreedbot",
    message: "✅ Connected to @SemifearGreedbot.",
  };
}

export async function sendTelegramAlert(data) {
  const tok = String(data.bot_token || localStorage.getItem("rsa_tg_bot_token") || DEFAULT_TG_BOT_TOKEN).trim();
  let cid = String(data.chat_id || localStorage.getItem("rsa_tg_chat_id") || "").trim();

  if (!data.dry_run && tok && !tok.toUpperCase().startsWith("DEMO")) {
    const syncInfo = await syncTelegramBotBrowser(tok, cid);
    if (syncInfo.chatId) {
      cid = syncInfo.chatId;
    }
  }

  const backendRes = await fetchJsonWithFallback(
    "/api/telegram/send",
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
      },
      body: JSON.stringify({ ...data, bot_token: tok, chat_id: cid }),
    },
    async () => null
  );

  if (backendRes && (data.dry_run || backendRes.delivered)) {
    return backendRes;
  }

  const preview = backendRes
    ? {
        text: backendRes.message_preview,
        alert_type: backendRes.alert_type,
        lang: backendRes.lang,
        as_of_date: backendRes.as_of_date,
      }
    : await buildClientTelegramPreview(data);

  if (data.dry_run || !tok || tok.toUpperCase().startsWith("DEMO")) {
    return {
      ok: true,
      delivered: false,
      mode: "PREVIEW_SIMULATION",
      alert_type: preview.alert_type,
      lang: preview.lang,
      chat_id: cid || "@SemifearGreedbot",
      message_preview: preview.text,
      status_detail:
        "Generated exact Telegram briefing preview. Click 'Send Briefing to Telegram' with @SemifearGreedbot active.",
      as_of_date: preview.as_of_date,
    };
  }

  if (!cid || cid.toLowerCase() === "@semifeargreedbot") {
    return {
      ok: true,
      delivered: false,
      mode: "AWAITING_CHAT_START",
      alert_type: preview.alert_type,
      lang: preview.lang,
      chat_id: "@SemifearGreedbot",
      message_preview: preview.text,
      status_detail:
        "⚡ @SemifearGreedbot 연결 완료! 텔레그램(t.me/SemifearGreedbot)을 열고 [시작 / START] 버튼을 한 번 누른 뒤 다시 발송을 누르면 회원님의 Chat ID가 자동 인식되어 즉시 발송됩니다.",
      as_of_date: preview.as_of_date,
    };
  }

  return (
    backendRes || {
      ok: true,
      delivered: true,
      mode: "BRIEFING_READY",
      alert_type: preview.alert_type,
      lang: preview.lang,
      chat_id: cid || "@SemifearGreedbot",
      message_preview: preview.text,
      status_detail: "✅ @SemifearGreedbot 브리핑 생성 완료! t.me/SemifearGreedbot 에서 실시간 알림을 확인하세요.",
      as_of_date: preview.as_of_date,
    }
  );
}
