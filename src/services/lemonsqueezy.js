/**
 * GetBreakAI - Lemon Squeezy USD SaaS Subscription Integration
 * Store ID: #296100 (KIDS-FIT Global Studio / TruthOfMarket / GetBreakAI)
 * Contact Desk: beable9489@gmail.com
 */

'use strict';

const crypto = require('crypto');

const CHECKOUT_URLS = {
  monthly: 'https://truthofmarket.lemonsqueezy.com/checkout/buy/9a7fe220-ad63-4119-a9f8-59e3d5fb978d?embed=1&checkout[redirect_url]=https://getbreakai.com/confirmation.html',
  annual: 'https://truthofmarket.lemonsqueezy.com/checkout/buy/d01ca3fb-f4d9-4a13-b888-8b208f5ca6d3?embed=1&checkout[redirect_url]=https://getbreakai.com/confirmation.html',
  enterprise: 'mailto:beable9489@gmail.com'
};

const STORE_CONFIG = {
  storeId: '296100',
  storeName: 'GetBreakAI & TruthOfMarket Analytics',
  checkoutBaseUrl: 'https://truthofmarket.lemonsqueezy.com/checkout/buy',
  supportEmail: 'beable9489@gmail.com',
  youtubeChannelUrl: 'https://www.youtube.com/@GetBreakAI',
  plans: {
    starter_monthly: {
      id: 'plan_starter_monthly',
      name: 'Starter Breakout Scanner ($29/月)',
      priceUsd: 29.00,
      interval: 'month',
      variantId: '9a7fe220-ad63-4119-a9f8-59e3d5fb978d',
      checkoutUrl: CHECKOUT_URLS.monthly,
      features: [
        'Daily Top 10 Breakout Scanner (TSE Prime & US Tech)',
        'Mechanical -9.0% & 2.0x ATR Stop-Loss Calculator',
        'End-of-Day Watchlist CSV Download',
        'Web Browser & Email Instant Signal Delivery',
        'TruthOfMarket.com Sister VIP Access Included'
      ]
    },
    pro_annual: {
      id: 'plan_pro_annual',
      name: 'Pro Institutional Annual Pass ($199/年 · 43%OFF)',
      priceUsd: 199.00,
      interval: 'year',
      variantId: 'd01ca3fb-f4d9-4a13-b888-8b208f5ca6d3',
      checkoutUrl: CHECKOUT_URLS.annual,
      features: [
        'Real-time Intraday Ignition & SEC 8-K Alerts',
        'Price-Weighted RSI (PW-RSI) Volume Engine',
        'Dynamic 2.0x / 2.5R Take-Profit Trajectory Alerts',
        'Web Browser & Email Instant VIP Signal Feed',
        'TradingView Pine Script v5 Full Source Code'
      ]
    },
    institutional_enterprise: {
      id: 'plan_institutional_enterprise',
      name: 'Institutional Alpha Terminal (法人・機関投資家プラン)',
      priceUsd: null,
      interval: 'custom',
      variantId: 'enterprise-inquiry',
      checkoutUrl: CHECKOUT_URLS.enterprise,
      features: [
        'Full REST & WebSocket Signal API Access',
        'SEC 10-K Forensic Accounting Risk Feed',
        'Dark-Pool Block Trade Flow Imbalance',
        'Multi-seat Team License (Up to 5 seats)',
        '1-on-1 Dedicated Support Desk (beable9489@gmail.com)'
      ]
    }
  }
};

// Backward-compatible aliases so existing callers passing 'pro_monthly' or 'institutional_annual' resolve cleanly
STORE_CONFIG.plans.pro_monthly = STORE_CONFIG.plans.pro_annual;
STORE_CONFIG.plans.institutional_annual = STORE_CONFIG.plans.institutional_enterprise;

/**
 * Generate Lemon Squeezy Hosted / Overlay Checkout URL
 * @param {string} planKey Key in STORE_CONFIG.plans or variantId
 * @param {object} [options]
 * @param {string} [options.userEmail]
 * @param {string} [options.userId]
 * @param {string} [options.redirectUrl]
 * @param {boolean} [options.embed=true]
 * @returns {string} Checkout URL
 */
function createCheckoutUrl(planKey, options = {}) {
  let plan = STORE_CONFIG.plans[planKey];
  if (!plan) {
    plan = Object.values(STORE_CONFIG.plans).find(p => p.variantId === planKey || p.id === planKey);
  }
  if (!plan) {
    throw new Error(`Invalid plan key: ${planKey}. Available: ${Object.keys(STORE_CONFIG.plans).join(', ')}`);
  }

  if (plan.checkoutUrl && plan.checkoutUrl.startsWith('mailto:')) {
    return plan.checkoutUrl;
  }

  const url = new URL(`${STORE_CONFIG.checkoutBaseUrl}/${plan.variantId}`);
  if (options.embed !== false) {
    url.searchParams.set('embed', '1');
  }
  const redirectUrl = options.redirectUrl !== undefined ? options.redirectUrl : 'https://getbreakai.com/confirmation.html';
  if (redirectUrl) {
    url.searchParams.set('checkout[redirect_url]', redirectUrl);
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
  CHECKOUT_URLS,
  STORE_CONFIG,
  createCheckoutUrl,
  verifyWebhookSignature,
  parseWebhookEvent
};
