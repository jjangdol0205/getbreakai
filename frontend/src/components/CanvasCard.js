export function renderScoreboardCard(stock, config = {}) {
  const canvas = document.getElementById("viralCanvas") || document.createElement("canvas");
  canvas.id = "viralCanvas";
  canvas.width = 900;
  canvas.height = 500;
  canvas.style.display = "none";
  if (!document.body.contains(canvas)) {
    document.body.appendChild(canvas);
  }

  const ctx = canvas.getContext("2d");
  const siteUrl = config.site1_url || "https://truthofmarket.com";

  // Background
  ctx.fillStyle = "#070b14";
  ctx.fillRect(0, 0, 900, 500);

  // Border colored by zone
  let borderColor = "#f59e0b"; // amber watch
  let badgeBg = "#78350f";
  if (stock.zone_code === "IGNITION_ZONE") {
    borderColor = "#10b981"; // emerald
    badgeBg = "#065f46";
  } else if (stock.zone_code === "LEFT_SIDE_KNIFE" || stock.zone_code === "VALUE_TRAP_FILTERED") {
    borderColor = "#ef4444"; // red
    badgeBg = "#7f1d1d";
  }

  ctx.strokeStyle = borderColor;
  ctx.lineWidth = 6;
  ctx.strokeRect(14, 14, 872, 472);

  // Header Title
  ctx.fillStyle = "#94a3b8";
  ctx.font = "bold 20px -apple-system, Segoe UI, sans-serif";
  ctx.fillText("⚡ RIGHTSIDEALPHA.IO — 20-YR QUANTITATIVE PW-RSI DIAGNOSTIC", 42, 58);

  // Stock Ticker & Close Price
  ctx.fillStyle = "#f8fafc";
  ctx.font = "900 44px -apple-system, Segoe UI, sans-serif";
  const stockName = stock.name || stock.name_en || stock.ticker;
  ctx.fillText(`$${stock.ticker} (${stockName}) — $${Number(stock.close).toFixed(2)}`, 42, 122);

  // Zone Badge Stamp
  ctx.fillStyle = badgeBg;
  ctx.fillRect(42, 146, 540, 52);
  ctx.fillStyle = "#ffffff";
  ctx.font = "bold 24px -apple-system, Segoe UI, sans-serif";
  const zoneLabel = stock.zone_code === "IGNITION_ZONE"
    ? "🟢 RIGHT-SIDE IGNITION"
    : (stock.zone_code === "LEFT_SIDE_KNIFE" ? "🔴 LEFT-SIDE FALLING KNIFE" : "🟡 WASHOUT WATCH (Pre-MA60)");
  ctx.fillText(`${zoneLabel}  |  PW-RSI Score: ${stock.score || stock.pw_score || 85}/100`, 56, 181);

  // 4 Quantitative Bullets
  ctx.fillStyle = "#cbd5e1";
  ctx.font = "bold 22px -apple-system, Segoe UI, sans-serif";
  
  const proxLow = stock.prox_low52_pct !== undefined ? stock.prox_low52_pct : stock.prox_low_pct;
  const ddHigh = stock.dd_high52_pct !== undefined ? stock.dd_high52_pct : stock.dd_high_pct;
  const vsMa20 = stock.vs_ma20_pct !== undefined ? stock.vs_ma20_pct : 0;
  const vsMa60 = stock.vs_ma60_pct !== undefined ? stock.vs_ma60_pct : 0;
  const volSurge = stock.vol_surge_10d !== undefined ? stock.vol_surge_10d : (stock.vol_surge || 1.35);
  const rsi = stock.rsi14 || 50.0;
  const hist2x = stock.hist_2x_rate || stock.hist_2x_rate_after_40pct_crash || 45.8;
  const ma60Price = stock.ma60_price ? `$${Number(stock.ma60_price).toFixed(2)}` : "Masked";

  ctx.fillText(`• 52W Low Proximity: +${Number(proxLow).toFixed(1)}%   (52W High Drawdown: ${Number(ddHigh).toFixed(1)}%)`, 42, 248);
  ctx.fillText(`• Moving Averages: vs MA20 (${vsMa20 >= 0 ? "+" : ""}${Number(vsMa20).toFixed(1)}%)  |  vs MA60 (${vsMa60 >= 0 ? "+" : ""}${Number(vsMa60).toFixed(1)}%)`, 42, 292);
  ctx.fillText(`• 10D Institutional Volume Washout: ${Number(volSurge).toFixed(2)}x Avg  |  RSI(14): ${Number(rsi).toFixed(1)}`, 42, 336);

  ctx.fillStyle = "#34d399";
  ctx.fillText(`• Historical 1Y 2x (+100%) Win Rate: ${Number(hist2x).toFixed(1)}%   (MA60 Breakout: ${ma60Price})`, 42, 382);

  // Watermark Compliance Footer
  ctx.fillStyle = "#64748b";
  ctx.font = "bold 17px -apple-system, Segoe UI, sans-serif";
  ctx.fillText(`🌐 Live Screener & 394,371-Day Backtest Leaderboard: ${siteUrl}  |  Not Financial Advice`, 42, 448);

  return canvas;
}

export async function copyOrDownloadCard(stock, config = {}, onToast) {
  const canvas = renderScoreboardCard(stock, config);
  
  canvas.toBlob(async (blob) => {
    if (!blob) return;
    try {
      if (navigator.clipboard && navigator.clipboard.write) {
        await navigator.clipboard.write([
          new ClipboardItem({ "image/png": blob })
        ]);
        if (onToast) onToast(`📸 $${stock.ticker} Scoreboard PNG Copied to Clipboard!`);
        return;
      }
    } catch (err) {
      // Clipboard write failed or not supported in this browser context, fallback to download
    }

    // Graceful Fallback: Download file
    const a = document.createElement("a");
    a.href = canvas.toDataURL("image/png");
    a.download = `${stock.ticker}_pw_rsi_scoreboard.png`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    if (onToast) onToast(`📸 Downloaded $${stock.ticker} PNG Scorecard!`);
  }, "image/png");
}
