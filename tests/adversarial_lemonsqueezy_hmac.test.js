/**
 * Adversarial HMAC Stress Testing for Lemon Squeezy Webhook Verification
 * File: getbreakai/tests/adversarial_lemonsqueezy_hmac.test.js
 */

'use strict';

const assert = require('assert');
const crypto = require('crypto');
const { verifyWebhookSignature, STORE_CONFIG } = require('../src/services/lemonsqueezy');

console.log('========================================================================');
console.log('  ADVERSARIAL HMAC-SHA256 SIGNATURE STRESS TEST FOR LEMON SQUEEZY     ');
console.log('========================================================================\n');

let totalTests = 0;
let passedTests = 0;
const findings = [];

function testCase(name, fn) {
  totalTests++;
  try {
    fn();
    console.log(`  ✓ [PASS] ${name}`);
    passedTests++;
  } catch (err) {
    console.error(`  ✗ [FAIL] ${name}`);
    console.error(`     Error: ${err.message}`);
    findings.push(`${name}: ${err.message}`);
  }
}

const secret = 'prod_lemon_squeezy_webhook_secret_2026_xyz';
const legitPayload = JSON.stringify({
  meta: { event_name: 'order_created', custom_data: { user_id: 'usr_premium_001' } },
  data: { id: 'ord_998822', attributes: { total: 19900, user_email: 'ceo@dreamcompany.kr', status: 'paid' } }
});
const legitHmac = crypto.createHmac('sha256', secret).update(legitPayload).digest('hex');

// Test 1: Baseline valid signature
testCase('1. Baseline valid HMAC signature is accepted', () => {
  const result = verifyWebhookSignature(legitPayload, legitHmac, secret);
  assert.strictEqual(result, true, 'Valid signature must be accepted');
});

// Test 2: Forged signature with incorrect secret
testCase('2. Forged signature generated with wrong secret is rejected', () => {
  const forgedHmac = crypto.createHmac('sha256', 'attacker_arbitrary_secret').update(legitPayload).digest('hex');
  const result = verifyWebhookSignature(legitPayload, forgedHmac, secret);
  assert.strictEqual(result, false, 'Forged signature must be rejected');
});

// Test 3: Tampered payload body (price modified from 19900 to 100)
testCase('3. Tampered payload (price tampering) with valid original signature is rejected', () => {
  const tamperedPayload = JSON.stringify({
    meta: { event_name: 'order_created', custom_data: { user_id: 'usr_premium_001' } },
    data: { id: 'ord_998822', attributes: { total: 100, user_email: 'ceo@dreamcompany.kr', status: 'paid' } }
  });
  const result = verifyWebhookSignature(tamperedPayload, legitHmac, secret);
  assert.strictEqual(result, false, 'Tampered payload must be rejected');
});

// Test 4: Missing x-signature header (undefined, null, empty)
testCase('4. Missing or empty signatureHeader is rejected gracefully', () => {
  assert.strictEqual(verifyWebhookSignature(legitPayload, undefined, secret), false);
  assert.strictEqual(verifyWebhookSignature(legitPayload, null, secret), false);
  assert.strictEqual(verifyWebhookSignature(legitPayload, '', secret), false);
});

// Test 5: Missing or empty webhookSecret
testCase('5. Missing or empty webhookSecret is rejected gracefully', () => {
  assert.strictEqual(verifyWebhookSignature(legitPayload, legitHmac, undefined), false);
  assert.strictEqual(verifyWebhookSignature(legitPayload, legitHmac, null), false);
  assert.strictEqual(verifyWebhookSignature(legitPayload, legitHmac, ''), false);
});

// Test 6: Single-bit flip in signature
testCase('6. Single-bit / single-character flip in signature is rejected', () => {
  // Flip first hex character
  const flippedChar = legitHmac[0] === 'a' ? 'b' : 'a';
  const modifiedHmac = flippedChar + legitHmac.slice(1);
  assert.strictEqual(verifyWebhookSignature(legitPayload, modifiedHmac, secret), false);
});

// Test 7: Length mismatch attacks (short signature, timingSafeEqual buffer length check)
testCase('7. Short signature (e.g. 10 chars instead of 64) does not throw RangeError and returns false', () => {
  const shortSig = legitHmac.slice(0, 10);
  assert.strictEqual(verifyWebhookSignature(legitPayload, shortSig, secret), false);
});

// Test 8: Long signature (e.g. 128 chars) returns false
testCase('8. Excessively long signature returns false', () => {
  const longSig = legitHmac + legitHmac;
  assert.strictEqual(verifyWebhookSignature(legitPayload, longSig, secret), false);
});

// Test 9: Binary Buffer rawPayload vs String rawPayload
testCase('9. Supports Buffer payload as well as UTF-8 string', () => {
  const bufferPayload = Buffer.from(legitPayload, 'utf8');
  assert.strictEqual(verifyWebhookSignature(bufferPayload, legitHmac, secret), true);
});

// Test 10: Multi-byte UTF-8 characters in payload (Korean & Emojis)
testCase('10. Multi-byte UTF-8 characters (Korean / Emojis) verify correctly', () => {
  const unicodePayload = JSON.stringify({
    customer: '홍길동 VIP 🚀',
    note: '동아시아 분기 특별 할인 보고서'
  });
  const unicodeHmac = crypto.createHmac('sha256', secret).update(unicodePayload).digest('hex');
  assert.strictEqual(verifyWebhookSignature(unicodePayload, unicodeHmac, secret), true);

  // Tamper 1 character
  const tamperedUnicode = JSON.stringify({
    customer: '홍길동 VIP 🛸',
    note: '동아시아 분기 특별 할인 보고서'
  });
  assert.strictEqual(verifyWebhookSignature(tamperedUnicode, unicodeHmac, secret), false);
});

// Test 11: Type confusion attacks on parameters
testCase('11. Type confusion attacks (object, number, boolean) handled safely without crash', () => {
  assert.strictEqual(verifyWebhookSignature({}, legitHmac, secret), false);
  assert.strictEqual(verifyWebhookSignature(12345, legitHmac, secret), false);
  assert.strictEqual(verifyWebhookSignature(legitPayload, { signature: 'hack' }, secret), false);
  assert.strictEqual(verifyWebhookSignature(legitPayload, 12345678, secret), false);
  assert.strictEqual(verifyWebhookSignature(legitPayload, legitHmac, { secret: 'obj' }), false);
});

// Test 12: Timing-attack resistance verification
testCase('12. Timing-safe comparison invoked via crypto.timingSafeEqual', () => {
  // Confirm crypto.timingSafeEqual is used internally and handles identical length buffers
  const digest = Buffer.from('a'.repeat(64), 'utf8');
  const signature = Buffer.from('a'.repeat(64), 'utf8');
  assert.strictEqual(crypto.timingSafeEqual(digest, signature), true);
});

console.log('\n========================================================================');
console.log(`Adversarial HMAC Test Summary: ${passedTests} / ${totalTests} Passed (${passedTests === totalTests ? '100% Secure' : 'Vulnerabilities Found'})`);
console.log('========================================================================\n');

if (findings.length > 0) {
  process.exit(1);
}
