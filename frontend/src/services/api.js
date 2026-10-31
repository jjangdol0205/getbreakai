function getAuthHeader() {
  const token =
    localStorage.getItem("rsa_token") ||
    (localStorage.getItem("rsa_pro_unlocked") === "true" ? "PRO-DEMO-2026" : "");
  if (token) {
    return { Authorization: `Bearer ${token}` };
  }
  return {};
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
            (s.sector && s.sector.toLowerCase().includes(q))
        );
      }
      if (params.zone && params.zone !== "ALL") {
        list = list.filter((s) => s.zone === params.zone);
      }
      if (params.sort_by) {
        const key = params.sort_by;
        const desc = String(params.order || "desc").toLowerCase() !== "asc";
        list = [...list].sort((a, b) => {
          const va = Number(a[key] ?? 0);
          const vb = Number(b[key] ?? 0);
          return desc ? vb - va : va - vb;
        });
      }
      return list;
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
        (key.length >= 10 && key.includes("-"));
      return {
        valid,
        tier: valid ? "pro" : "free",
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
      const r = await fetch("./static_api/pinescript.json");
      return r.json();
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
      const curr = stock ? Number(stock.close) : entry;
      const asOf = stock && stock.date ? stock.date : "2026-10-13";
      const retPct = Number((((curr / entry) - 1.0) * 100.0).toFixed(2));
      const stopP = Number((entry * 0.91).toFixed(2));
      const tp1P = Number((entry * 2.0).toFixed(2));

      if (retPct <= -9.0) {
        return {
          ticker: tClean,
          status_code: "CRITICAL_STOP",
          status_label: "🛑 Hard Stop Loss Triggered",
          return_pct: retPct,
          rule_triggered: "Rule 1 (-9.0% Hard Stop Loss)",
          action_plan: "Execute immediate market exit. Do not average down on broken support.",
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
          status_code: "DEAD_MONEY",
          status_label: "⏳ 55-Day Time Stop Triggered",
          return_pct: retPct,
          rule_triggered: "Rule 2 (55-Day Dead-Money Exit)",
          action_plan: "Exit position. Rebound momentum has stalled; reallocate into active right-side ignition candidates.",
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
          status_code: "TP1_REACHED",
          status_label: "🎯 100% Target Price 1 Achieved",
          return_pct: retPct,
          rule_triggered: "Rule 3 (+100% Principal Recovery)",
          action_plan: "Sell 50% of position to recoup 100% initial capital. Set trailing stop on remaining 50% using MA60.",
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
          status_code: "ACTIVE_HOLD",
          status_label: "🟢 Active Right-Side Trend Follow",
          return_pct: retPct,
          rule_triggered: "Rule 4 (Healthy Trend Follow)",
          action_plan: "Maintain position. Monitor MA20/MA60 trailing support; runner target is +100% TP1.",
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
  return `/api/referral/redirect/${encodeURIComponent(provider.toLowerCase())}?ticker=${encodeURIComponent(ticker)}`;
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

      const natW = Number(ov.natural_smh_weight_pct ?? 64.9) / 100.0;
      const currSmhUsd = Number((capUsd * natW).toFixed(2));
      const currXlvUsd = Number((capUsd * (1.0 - natW)).toFixed(2));
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
          summary_en: "Semiconductors are already discounted. Do not hold excess cash—deploy 100% today and rebalance back to 70:30 when $SMH recovers within -10% of its 52-week high.",
          summary_jp: "半導体セクターは既に割安圏にあります。現金を遊ばせず本日100%投入し、$SMHが高値比-10%以内へ回復した時点で70:30へ戻します。",
          summary_kr: "반도체 섹터가 이미 할인된 공포 구간입니다. 현금을 놀리지 말고 당일 100% 거치식으로 진입한 뒤, $SMH가 고점 대비 -10% 이내로 회복되면 70:30으로 복귀하세요.",
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
              note_en: `Deploy 100% immediately at ${Math.round(smhW * 100)}:${Math.round(xlvW * 100)} ($SMH:$XLV). Historical 1-year forward win rate when entering below score 25 exceeds 91%.`,
              note_jp: `${Math.round(smhW * 100)}:${Math.round(xlvW * 100)} ($SMH:$XLV) 比率で100%即時エントリー。スコア25以下でのエントリーは過去1年後の勝率が91%超。`,
              note_kr: `${Math.round(smhW * 100)}:${Math.round(xlvW * 100)} ($SMH:$XLV) 비중으로 100% 즉시 진입합니다. 공포 지수 25 이하 진입 시 1년 후 플러스 수익 확률은 91% 이상입니다.`,
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
          summary_en: "Balanced deployment: lock in your 30% $XLV anchor and half of $SMH today, while keeping 35% dry powder for volatility.",
          summary_jp: "バランス型エントリー：$XLV 30%と$SMH半分を初日に確保し、35%の余力で押し目に備えます。",
          summary_kr: "중립장 표준 공식: 1일차에 $XLV 30% 전량과 $SMH 절반(35%)을 먼저 채우고, 나머지 35%는 조정 시 추매 실탄으로 활용합니다.",
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
              note_en: "Establish 100% of your defensive $XLV position (30%) and half of your $SMH position (35%) immediately.",
              note_jp: "ディフェンシブ枠の$XLV (30%) 全額と、成長枠$SMHの半分 (35%) を初日に構築します。",
              note_kr: "방어주 $XLV(30%) 전량과 반도체 $SMH 목표치의 절반(35%)을 첫날 즉시 매수합니다.",
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
              note_en: "Earn ~4.5% USD RP yield while waiting for a pullback below score 40, or auto-deploy over 90 days.",
              note_jp: "米ドルMMFで金利を受け取りながらスコア40以下への押し目を待つか、90日間で機械的に分割投入します。",
              note_kr: "달러 RP(연 4%대 금리)에 예치해 두었다가 지수가 40 이하로 내려오면 즉시 투입하고, 안 내려오면 3개월간 균등 분할 매수합니다.",
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
          case_title_en: "Case 3 (Score 68–100 · Greed Regime): 30% $XLV Today + 70% $SMH Parked in USD RP",
          case_title_jp: "ケース3 (スコア 68–100 · 強欲圏): 初日 $XLV 30%のみ + 70% 米ドルMMF待機",
          case_title_kr: "Case 3 (지수 68–100 · 탐욕 과열 구간): 당일 $XLV 30%만 진입 + 70% 달러 RP 대기",
          summary_en: "Protect principal against euphoria: buy only the 30% $XLV sleeve today and keep 70% in USD RP until Fear & Greed cools to 45 or below.",
          summary_jp: "高値掴み防止ルール：初日は$XLV 30%のみを購入し、70%は指数が45以下に冷めるまで米ドルMMFで待機します。",
          summary_kr: "고점 추격매수 방지 공식: 당일에는 방어주 $XLV 30%만 매수하고, $SMH 70% 자금은 지수가 45 이하로 내려올 때까지 달러 RP에서 이자를 받으며 대기합니다.",
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
              note_en: "Do not chase overheated semiconductors above score 68. Deploy only the 30% Healthcare anchor on Day 1.",
              note_jp: "スコア68超の過熱局面での半導体ジャンピングキャッチを回避し、ヘルスケア枠30%のみを先行構築します。",
              note_kr: "탐욕 지수 68 초과 과열 구간에서는 반도체 고점 물림을 피하기 위해 방어주 $XLV 30%만 우선 매수합니다.",
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
              note_en: "Collect risk-free USD interest while waiting for semiconductor euphoria to mean-revert.",
              note_jp: "米ドル金利を確保しながら、半導体の過熱感が冷めるのを待って安全にエントリーします。",
              note_kr: "달러 RP 이자를 받으며 반도체 과열이 해소될 때까지 기다렸다가 안전하게 진입하여 고점 낙폭을 방어합니다.",
            },
          ],
        };
      }
    }
  );
}
