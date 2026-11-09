/**
 * GetBreakAI - Core Quantitative Algorithmic Engine (src/engine/breakout_engine.js)
 * 
 * Disciplines:
 * 1. Donchian 20-Day Channel Breakout + SMA60 Right-Side Filter
 * 2. Institutional Volume Factor & Price-Weighted RSI (PW-RSI)
 * 3. Non-Negotiable -9.0% Hard Stop-Loss & Dynamic 2x Take-Profit (2:1 R:R)
 */

'use strict';

/**
 * Calculate Simple Moving Average
 * @param {Array<number>} values 
 * @param {number} period 
 * @returns {Array<number>}
 */
function calculateSMA(values, period) {
  const sma = [];
  let sum = 0;
  for (let i = 0; i < values.length; i++) {
    sum += values[i];
    if (i >= period) {
      sum -= values[i - period];
    }
    if (i >= period - 1) {
      sma.push(sum / period);
    } else {
      sma.push(null);
    }
  }
  return sma;
}

/**
 * Calculate Wilder's Relative Strength Index (RSI 14)
 * @param {Array<number>} closes 
 * @param {number} period 
 * @returns {Array<number>}
 */
function calculateRSI(closes, period = 14) {
  if (closes.length < period + 1) {
    return closes.map(() => 50.0);
  }

  const rsi = new Array(closes.length).fill(null);
  let gains = 0;
  let losses = 0;

  for (let i = 1; i <= period; i++) {
    const diff = closes[i] - closes[i - 1];
    if (diff >= 0) gains += diff;
    else losses += Math.abs(diff);
  }

  let avgGain = gains / period;
  let avgLoss = losses / period;

  rsi[period] = avgLoss === 0 ? 100 : 100 - (100 / (1 + avgGain / avgLoss));

  for (let i = period + 1; i < closes.length; i++) {
    const diff = closes[i] - closes[i - 1];
    const gain = diff > 0 ? diff : 0;
    const loss = diff < 0 ? Math.abs(diff) : 0;

    avgGain = (avgGain * (period - 1) + gain) / period;
    avgLoss = (avgLoss * (period - 1) + loss) / period;

    if (avgLoss === 0) {
      rsi[i] = 100.0;
    } else {
      const rs = avgGain / avgLoss;
      rsi[i] = Number((100 - (100 / (1 + rs))).toFixed(2));
    }
  }

  return rsi;
}

/**
 * Calculate Donchian Channel High (N-period highest high of previous bars)
 * @param {Array<{high: number}>} bars 
 * @param {number} period 
 * @returns {Array<number>}
 */
function calculateDonchianHigh(bars, period = 20) {
  const highs = [];
  for (let i = 0; i < bars.length; i++) {
    if (i < period) {
      highs.push(null);
      continue;
    }
    let maxHigh = -Infinity;
    for (let k = 1; k <= period; k++) {
      if (bars[i - k].high > maxHigh) {
        maxHigh = bars[i - k].high;
      }
    }
    highs.push(maxHigh);
  }
  return highs;
}

/**
 * Calculate Price-Weighted RSI (PW-RSI)
 * Formula: PW_RSI = RSI * min(Volume / MA20_Volume, 3.0)
 * @param {number} rsi 
 * @param {number} currentVolume 
 * @param {number} ma20Volume 
 * @returns {number}
 */
function calculatePwRsi(rsi, currentVolume, ma20Volume) {
  if (!ma20Volume || ma20Volume <= 0) return rsi;
  const volFactor = Math.min(currentVolume / ma20Volume, 3.0);
  return Number((rsi * volFactor).toFixed(2));
}

/**
 * Calculate Institutional Risk Profile for a given Entry Price
 * @param {number} entryPrice 
 * @param {number} [stopPercent=9.0] 
 * @param {number} [rrRatio=2.0] 
 */
function calculateRiskProfile(entryPrice, stopPercent = 9.0, rrRatio = 2.0) {
  if (typeof entryPrice !== 'number' || entryPrice <= 0) {
    throw new Error('Valid positive entry price is required.');
  }

  const stopLoss = Number((entryPrice * (1 - stopPercent / 100)).toFixed(2));
  const riskAmount = Number((entryPrice - stopLoss).toFixed(2));
  const takeProfit = Number((entryPrice + riskAmount * rrRatio).toFixed(2));
  const breakevenTrigger = Number((entryPrice * 1.15).toFixed(2)); // +15%
  const trailingBreakevenStop = Number((entryPrice * 1.01).toFixed(2)); // +1% net gain

  return {
    entryPrice,
    stopLoss,
    stopPercent,
    riskAmount,
    takeProfit,
    takeProfitPercent: Number(((takeProfit - entryPrice) / entryPrice * 100).toFixed(2)),
    rewardToRiskRatio: rrRatio,
    breakevenTrigger,
    trailingBreakevenStop
  };
}

/**
 * Evaluate Bar for Breakout Signal & Institutional Ignition
 * @param {object} params
 * @param {number} params.close 
 * @param {number} params.high 
 * @param {number} params.low 
 * @param {number} params.volume 
 * @param {number} params.donchianHigh 
 * @param {number} params.sma60 
 * @param {number} params.sma20Vol 
 * @param {number} params.rsi 
 * @returns {object} Breakout evaluation result
 */
function evaluateBreakoutSignal({ close, high, volume, donchianHigh, sma60, sma20Vol, rsi }) {
  const volFactor = sma20Vol && sma20Vol > 0 ? Number((volume / sma20Vol).toFixed(2)) : 1.0;
  const pwRsi = calculatePwRsi(rsi, volume, sma20Vol);

  const priceBreakout = donchianHigh !== null && close > donchianHigh;
  const rightSideConfirmed = sma60 !== null && close > sma60;
  const volumeExpansion = volFactor >= 1.5;
  const pwRsiIgnition = pwRsi >= 90.0;

  let signal = 'NEUTRAL';
  let reason = 'Consolidation / Below Breakout Level';

  if (priceBreakout) {
    if (!rightSideConfirmed) {
      signal = 'SUPPRESSED_LEFT_SIDE';
      reason = 'Price is below SMA60 (Falling Knife Risk)';
    } else if (!volumeExpansion) {
      signal = 'LOW_VOLUME_TRAP';
      reason = `Volume factor (${volFactor}x) is below institutional threshold (1.5x)`;
    } else if (pwRsiIgnition) {
      signal = 'INSTITUTIONAL_IGNITION';
      reason = 'Confirmed Donchian Breakout + Volume Surge + PW-RSI Ignition';
    } else {
      signal = 'STANDARD_BREAKOUT';
      reason = 'Confirmed Breakout with Moderate Momentum';
    }
  }

  const risk = calculateRiskProfile(close);

  return {
    signal,
    isActionable: signal === 'INSTITUTIONAL_IGNITION' || signal === 'STANDARD_BREAKOUT',
    price: close,
    high,
    donchianHigh,
    sma60,
    volume,
    volFactor,
    rsi,
    pwRsi,
    riskProfile: risk,
    reason
  };
}

/**
 * Track an Active Position Against Live Price Bar
 * @param {object} position Active position with riskProfile & status
 * @param {{high: number, low: number, close: number}} currentBar 
 * @returns {object} Updated position status
 */
function updatePositionStatus(position, currentBar) {
  const pos = { ...position };
  if (pos.status === 'CLOSED_STOP_LOSS' || pos.status === 'CLOSED_TAKE_PROFIT') {
    return pos;
  }

  // 1. Check Hard Stop-Loss Hit
  if (currentBar.low <= pos.currentStopLoss) {
    pos.status = 'CLOSED_STOP_LOSS';
    pos.exitPrice = pos.currentStopLoss;
    pos.pnlPercent = Number(((pos.exitPrice - pos.entryPrice) / pos.entryPrice * 100).toFixed(2));
    pos.exitReason = `Hard Stop Hit at ${pos.exitPrice} (-${pos.riskProfile.stopPercent}%)`;
    return pos;
  }

  // 2. Check Take-Profit Hit
  if (currentBar.high >= pos.takeProfit) {
    pos.status = 'CLOSED_TAKE_PROFIT';
    pos.exitPrice = pos.takeProfit;
    pos.pnlPercent = Number(((pos.exitPrice - pos.entryPrice) / pos.entryPrice * 100).toFixed(2));
    pos.exitReason = `2x Take-Profit Target Reached at ${pos.exitPrice} (+${pos.riskProfile.takeProfitPercent}%)`;
    return pos;
  }

  // 3. Check Dynamic Trailing Breakeven Trigger (+15% gain)
  if (!pos.isBreakevenArmed && currentBar.high >= pos.riskProfile.breakevenTrigger) {
    pos.isBreakevenArmed = true;
    pos.currentStopLoss = Math.max(pos.currentStopLoss, pos.riskProfile.trailingBreakevenStop);
    pos.notes = 'Dynamic Breakeven Armed (+1% protected stop)';
  }

  pos.status = 'ACTIVE';
  pos.unrealizedPnlPercent = Number(((currentBar.close - pos.entryPrice) / pos.entryPrice * 100).toFixed(2));
  return pos;
}

/**
 * Calculate Options-Implied Expected Move & Gamma Walls around an Event/Earnings Catalyst
 * Formula: ExpectedMove = Spot * (IV / 100) * sqrt(Days / 252)
 * @param {number} spotPrice
 * @param {number} impliedVolatilityPct Annualized IV percentage (e.g. 68.5 for 68.5%)
 * @param {number} [daysToEvent=1] Trading days across event window
 * @returns {object}
 */
function calculateExpectedMove(spotPrice, impliedVolatilityPct, daysToEvent = 1) {
  if (typeof spotPrice !== 'number' || spotPrice <= 0) {
    throw new Error('Valid positive spotPrice is required.');
  }
  const iv = Math.max(0, Number(impliedVolatilityPct) || 0);
  const days = Math.max(1, Number(daysToEvent) || 1);
  const moveFraction = (iv / 100.0) * Math.sqrt(days / 252.0);
  const expectedMoveDollar = Number((spotPrice * moveFraction).toFixed(2));
  const expectedMovePct = Number((moveFraction * 100.0).toFixed(2));

  return {
    spotPrice,
    impliedVolatilityPct: iv,
    daysToEvent: days,
    expectedMoveDollar,
    expectedMovePct,
    upperGammaWall: Number((spotPrice + expectedMoveDollar).toFixed(2)),
    lowerPutWall: Number(Math.max(0.01, spotPrice - expectedMoveDollar).toFixed(2))
  };
}

/**
 * Calculate Volatility-Adjusted ATR Position Size & Dynamic Catalyst Risk Profile
 * @param {object} params
 * @param {number} params.accountBalance Total portfolio equity in USD
 * @param {number} [params.riskPercent=1.5] Max account equity risked on this catalyst (%)
 * @param {number} params.entryPrice Stock entry price
 * @param {number} params.atr 14-day Average True Range in USD
 * @param {number} [params.atrMultiplier=2.0] Stop distance in ATR units
 * @returns {object}
 */
function calculateAtrPositionSize({
  accountBalance,
  riskPercent = 1.5,
  entryPrice,
  atr,
  atrMultiplier = 2.0
}) {
  if (!accountBalance || accountBalance <= 0 || !entryPrice || entryPrice <= 0 || !atr || atr <= 0) {
    throw new Error('Valid positive accountBalance, entryPrice, and atr are required.');
  }
  const maxRiskDollars = Number((accountBalance * (riskPercent / 100.0)).toFixed(2));
  const stopDistance = Number((atr * atrMultiplier).toFixed(2));
  const atrStopLoss = Number(Math.max(0.01, entryPrice - stopDistance).toFixed(2));
  const target25R = Number((entryPrice + stopDistance * 2.5).toFixed(2));
  const rawShares = Math.floor(maxRiskDollars / stopDistance);
  const maxAffordableShares = Math.floor(accountBalance / entryPrice);
  const optimalShares = Math.max(0, Math.min(rawShares, maxAffordableShares));
  const positionNotional = Number((optimalShares * entryPrice).toFixed(2));

  return {
    accountBalance,
    riskPercent,
    maxRiskDollars,
    entryPrice,
    atr,
    atrMultiplier,
    stopDistance,
    atrStopLoss,
    target25R,
    optimalShares,
    positionNotional,
    portfolioAllocationPct: Number(((positionNotional / accountBalance) * 100.0).toFixed(2))
  };
}

/**
 * Evaluate AI Multi-Factor Event Catalyst & Unusual Institutional Flow Score (0-100)
 * Distinct from truthofmarket.com's macro/trend engine: focuses on SEC 8-K/Earnings NLP,
 * Form-4 Executive Cluster Buying, Dark Pool Prints, and Options Call/Put Gamma Flow.
 * @param {object} params
 * @returns {object}
 */
function evaluateCatalystScore({
  earningsSurprisePct = 0,
  nlpGuidanceScore = 50,
  insiderClusterBuys = 0,
  darkPoolPrintPct = 35,
  callPutRatio = 1.0
}) {
  const earningsComponent = Math.min(25, Math.max(0, (earningsSurprisePct + 5) * 1.25));
  const nlpComponent = Math.min(25, Math.max(0, (nlpGuidanceScore / 100.0) * 25.0));
  const insiderComponent = Math.min(25, Math.max(0, insiderClusterBuys * 8.0));
  const flowComponent = Math.min(
    25,
    Math.max(0, ((darkPoolPrintPct - 30) * 0.45) + ((callPutRatio - 1.0) * 8.5))
  );

  const catalystScore = Number((earningsComponent + nlpComponent + insiderComponent + flowComponent).toFixed(1));

  let classification = 'NO_CATALYST_EDGE';
  if (catalystScore >= 82 && callPutRatio >= 2.2) {
    classification = 'GAMMA_SQUEEZE_IGNITION';
  } else if (catalystScore >= 75 && insiderClusterBuys >= 2) {
    classification = 'INSIDER_WHALE_CLUSTER';
  } else if (catalystScore >= 70) {
    classification = 'EARNINGS_PEAD_BREAKOUT';
  }

  return {
    catalystScore,
    classification,
    isHighConviction: catalystScore >= 70,
    breakdown: {
      earningsComponent: Number(earningsComponent.toFixed(1)),
      nlpComponent: Number(nlpComponent.toFixed(1)),
      insiderComponent: Number(insiderComponent.toFixed(1)),
      flowComponent: Number(flowComponent.toFixed(1))
    }
  };
}

module.exports = {
  calculateSMA,
  calculateRSI,
  calculateDonchianHigh,
  calculatePwRsi,
  calculateRiskProfile,
  evaluateBreakoutSignal,
  updatePositionStatus,
  calculateExpectedMove,
  calculateAtrPositionSize,
  evaluateCatalystScore
};
