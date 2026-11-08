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

module.exports = {
  calculateSMA,
  calculateRSI,
  calculateDonchianHigh,
  calculatePwRsi,
  calculateRiskProfile,
  evaluateBreakoutSignal,
  updatePositionStatus
};
