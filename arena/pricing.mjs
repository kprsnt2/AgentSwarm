/**
 * Pricing — real, per-provider list rates used for accurate cost comparison.
 *
 * WHY: the CLIs report inconsistent cost data. `agy` and `step` report $0.00
 * because they are covered by a subscription / promo, and `pi`/`omp` report
 * whatever their own pricing table says. That makes cross-substrate cost
 * comparison meaningless as reported.
 *
 * This module computes cost from TOKEN COUNTS at published list rates, so every
 * substrate is priced on the same basis. Three numbers are produced per turn:
 *
 *   reportedCost  - what the CLI claimed (may be 0 due to subscription/promo)
 *   listCost      - what the tokens would cost at list API rates
 *   effectiveCost - listCost, i.e. the comparable figure across substrates
 *
 * Rates are USD per 1,000,000 tokens as [freshInput, cachedInput, output].
 * Verify against the provider's current pricing page before publishing numbers;
 * these are the values known at the time of writing.
 */

export const PRICING = {
  // Google Gemini (via Antigravity CLI or the Antigravity provider)
  'gemini-3.8-flash-high': { fresh: 0.30, cached: 0.075, out: 2.50, provider: 'Google', plan: 'Google AI plan' },
  'gemini-3.8-flash': { fresh: 0.30, cached: 0.075, out: 2.50, provider: 'Google', plan: 'Google AI plan' },
  'google-antigravity/gemini-3.8-flash': { fresh: 0.30, cached: 0.075, out: 2.50, provider: 'Google', plan: 'Google AI plan' },
  'google-antigravity/gemini-3.8-flash:high': { fresh: 0.30, cached: 0.075, out: 2.50, provider: 'Google', plan: 'Google AI plan' },
  'gemini-3.7-flash': { fresh: 0.30, cached: 0.075, out: 2.50, provider: 'Google', plan: 'Google AI plan' },
  'gemini-3.1-pro-high': { fresh: 1.25, cached: 0.31, out: 10.00, provider: 'Google', plan: 'Google AI plan' },

  // Anthropic (reachable through the Antigravity provider)
  'claude-opus-4-6': { fresh: 15.00, cached: 1.50, out: 75.00, provider: 'Anthropic', plan: 'Google AI plan' },
  'google-antigravity/claude-opus-4-6': { fresh: 15.00, cached: 1.50, out: 75.00, provider: 'Anthropic', plan: 'Google AI plan' },
  'claude-sonnet-4-6': { fresh: 3.00, cached: 0.30, out: 15.00, provider: 'Anthropic', plan: 'Google AI plan' },

  // Step (preview promo at time of writing)
  'step/step-5-preview': { fresh: 0.20, cached: 0.05, out: 1.00, provider: 'Step', plan: 'Preview promo' },
  'step-5-preview': { fresh: 0.20, cached: 0.05, out: 1.00, provider: 'Step', plan: 'Preview promo' },
  'step/step-3.7-flash': { fresh: 0.10, cached: 0.025, out: 0.40, provider: 'Step', plan: 'Pay-as-you-go' },

  // DeepSeek via Fireworks
  'fireworks/accounts/fireworks/models/deepseek-v4p1-flash': {
    fresh: 0.15, cached: 0.02, out: 0.60, provider: 'Fireworks', plan: 'Pay-as-you-go',
  },
  'accounts/fireworks/models/deepseek-v4p1-flash': {
    fresh: 0.15, cached: 0.02, out: 0.60, provider: 'Fireworks', plan: 'Pay-as-you-go',
  },

  // OpenAI (reachable through omp)
  'gpt-5.4-mini': { fresh: 0.25, cached: 0.025, out: 2.00, provider: 'OpenAI', plan: 'Pay-as-you-go' },
  'gpt-oss-120b-medium': { fresh: 0.15, cached: 0.02, out: 0.60, provider: 'OpenAI', plan: 'Open weights' },
};

/** Fallback used when a model is not in the table, so cost is never silently 0. */
const FALLBACK = { fresh: 0.30, cached: 0.075, out: 2.50, provider: 'unknown', plan: 'estimated' };

export function rateFor(model) {
  if (!model) return FALLBACK;
  if (PRICING[model]) return PRICING[model];
  // fuzzy: match on the distinctive tail of the id
  const key = Object.keys(PRICING).find((k) =>
    model.includes(k) || k.includes(model.split('/').pop()));
  return key ? PRICING[key] : FALLBACK;
}

/** Normalise the many usage shapes the CLIs emit into {fresh, cached, out}. */
export function normalizeUsage(usage) {
  if (!usage) return { fresh: 0, cached: 0, out: 0 };
  return {
    fresh: usage.input ?? usage.input_tokens ?? usage.prompt_tokens ?? 0,
    cached: usage.cacheRead ?? usage.cache_read_tokens ?? usage.cached_tokens ?? 0,
    out: usage.output ?? usage.output_tokens ?? usage.completion_tokens ?? 0,
  };
}

/**
 * Compute list-rate cost for one turn.
 * Returns a full breakdown so the UI can show how the number was derived.
 */
export function costOfTurn({ model, usage, reportedCost = 0 }) {
  const rate = rateFor(model);
  const u = normalizeUsage(usage);
  const freshCost = (u.fresh / 1e6) * rate.fresh;
  const cachedCost = (u.cached / 1e6) * rate.cached;
  const outCost = (u.out / 1e6) * rate.out;
  const listCost = freshCost + cachedCost + outCost;
  const totalIn = u.fresh + u.cached;

  return {
    model,
    provider: rate.provider,
    plan: rate.plan,
    rate,
    tokens: u,
    cacheHitRate: totalIn ? u.cached / totalIn : 0,
    breakdown: { freshCost, cachedCost, outCost },
    listCost,
    reportedCost,
    // How much a subscription/promo is absorbing for this turn.
    absorbed: Math.max(0, listCost - reportedCost),
    // What caching saved versus billing all input at the fresh rate.
    cacheSavings: (u.cached / 1e6) * (rate.fresh - rate.cached),
  };
}
