/**
 * GetBreakAI - Lemon Squeezy USD SaaS Subscription Integration
 * Store ID: #296100 (KIDS-FIT Global Studio / TruthOfMarket / GetBreakAI)
 * Contact Desk: beable9489@gmail.com
 */

'use strict';

const crypto = require('crypto');

const STORE_CONFIG = {
  storeId: '296100',
  storeName: 'GetBreakAI & TruthOfMarket Analytics',
  checkoutBaseUrl: 'https://truthofmarket.lemonsqueezy.com/checkout/buy',
  supportEmail: 'beable9489@gmail.com',
  plans: {
    starter_monthly: {
      id: 'plan_starter_monthly',
      name: 'Starter Breakout Scanner',
      priceUsd: 29.00,
      interval: 'month',
      variantId: 'gb-starter-29',
      features: [
        'Daily Top 10 Breakout Scanner',
        'Mechanical -9.0% Stop-Loss Calculator',
        'End-of-Day Watchlist CSV Download',
        'Standard Email Support'
      ]
    },
    pro_monthly: {
      id: 'plan_pro_monthly',
      name: 'Pro Institutional Breakout',
      priceUsd: 49.00,
      interval: 'month',
      variantId: 'gb-pro-49',
      features: [
        'Real-time Intraday Ignition Alerts',
        'Price-Weighted RSI (PW-RSI) Volume Engine',
        'Dynamic 2x Take-Profit Trajectory Alerts',
        'Direct VIP Telegram Signal Feed',
        'TradingView Pine Script v5 Source Code'
      ]
    },
    institutional_annual: {
      id: 'plan_institutional_annual',
      name: 'Institutional Alpha Terminal',
      priceUsd: 1499.00,
      interval: 'year',
      variantId: 'gb-inst-1499',
      features: [
        'Full REST & WebSocket Signal API Access',
        'SEC 10-K Forensic Accounting Risk Feed',
        'Dark-Pool Block Trade Flow Imbalance',
        'Multi-seat Team License (Up to 5 seats)',
        '1-on-1 Dedicated Support Desk'
      ]
    }
  }
};

/**
 * Generate Lemon Squeezy Hosted / Overlay Checkout URL
 * @param {string} planKey Key in STORE_CONFIG.plans
 * @param {object} [options]
 * @param {string} [options.userEmail]
 * @param {string} [options.userId]
 * @param {boolean} [options.embed=true]
 * @returns {string} Checkout URL
 */
function createCheckoutUrl(planKey, options = {}) {
  const plan = STORE_CONFIG.plans[planKey];
  if (!plan) {
    throw new Error(`Invalid plan key: ${planKey}. Available: ${Object.keys(STORE_CONFIG.plans).join(', ')}`);
  }

  const url = new URL(`${STORE_CONFIG.checkoutBaseUrl}/${plan.variantId}`);
  if (options.embed !== false) {
    url.searchParams.set('embed', '1');
  }
  if (options.userEmail) {
    url.searchParams.set('checkout[email]', options.userEmail);
  }
  if (options.userId) {
    url.searchParams.set('checkout[custom][user_id]', options.userId);
  }
  url.searchParams.set('checkout[custom][source]', 'getbreakai_app');

  return url.toString();
}

/**
 * Verify Lemon Squeezy Webhook Signature using HMAC-SHA256
 * @param {string|Buffer} rawPayload 
 * @param {string} signatureHeader Value from 'x-signature'
 * @param {string} webhookSecret 
 * @returns {boolean}
 */
function verifyWebhookSignature(rawPayload, signatureHeader, webhookSecret) {
  if (!signatureHeader || !webhookSecret) {
    return false;
  }

  try {
    const hmac = crypto.createHmac('sha256', webhookSecret);
    const digest = Buffer.from(hmac.update(rawPayload).digest('hex'), 'utf8');
    const signature = Buffer.from(signatureHeader, 'utf8');

    if (digest.length !== signature.length) {
      return false;
    }
    return crypto.timingSafeEqual(digest, signature);
  } catch (err) {
    return false;
  }
}

/**
 * Parse and Route Webhook Event Payload
 * @param {object} event Lemon Squeezy webhook JSON payload
 * @returns {object} Actionable event summary
 */
function parseWebhookEvent(event) {
  const eventName = event?.meta?.event_name;
  const data = event?.data;

  switch (eventName) {
    case 'subscription_created':
      return {
        action: 'ACTIVATE_SUBSCRIPTION',
        userId: data?.attributes?.user_email || event?.meta?.custom_data?.user_id,
        subscriptionId: data?.id,
        status: data?.attributes?.status,
        planName: data?.attributes?.product_name,
        renewsAt: data?.attributes?.renews_at
      };
    case 'subscription_updated':
      return {
        action: 'UPDATE_SUBSCRIPTION',
        subscriptionId: data?.id,
        status: data?.attributes?.status,
        cardLastFour: data?.attributes?.card_last_four
      };
    case 'subscription_cancelled':
      return {
        action: 'CANCEL_SUBSCRIPTION',
        subscriptionId: data?.id,
        endsAt: data?.attributes?.ends_at
      };
    case 'order_created':
      return {
        action: 'ORDER_CONFIRMED',
        orderId: data?.id,
        totalUsd: (data?.attributes?.total || 0) / 100,
        customerEmail: data?.attributes?.user_email
      };
    default:
      return {
        action: 'UNKNOWN_EVENT',
        eventName
      };
  }
}

module.exports = {
  STORE_CONFIG,
  createCheckoutUrl,
  verifyWebhookSignature,
  parseWebhookEvent
};
