/**
 * ValueTracker — JS port of entroly/value_tracker.py
 *
 * Persistent, lifetime-savings accounting with the self-funded evolution
 * budget invariant:
 *
 *     C_spent(t)  ≤  τ · S(t)         (τ = 5%)
 *
 * Any token-costing evolution step MUST gate on `getEvolutionBudget().canEvolve`.
 * The tracker is atomic-write safe and survives process restarts.
 */

'use strict';

const fs = require('fs');
const path = require('path');
const os = require('os');

const EVOLUTION_TAX_RATE = 0.05;
const FILE_NAME = 'value_tracker.json';

// Per-model $/1M tokens — kept in sync with entroly/value_tracker.py (×1000).
const COST_PER_M = {
  default: 3.0,
  // OpenAI
  'gpt-4o': 2.5,
  'gpt-4o-mini': 0.15,
  'gpt-4-turbo': 10.0,
  'gpt-4': 30.0,
  'gpt-3.5-turbo': 0.5,
  'o1': 15.0,
  'o1-mini': 3.0,
  'o3': 10.0,
  'o3-mini': 1.1,
  'o4-mini': 1.1,
  // Anthropic
  'claude-opus-4': 15.0,
  'claude-sonnet-4': 3.0,
  'claude-haiku-4': 0.8,
  'claude-3-5-sonnet': 3.0,
  'claude-3-5-haiku': 0.8,
  // Google
  'gemini-2.5-pro': 1.25,
  'gemini-2.5-flash': 0.075,
  'gemini-1.5-pro': 1.25,
  'gemini-1.5-flash': 0.075,
};

// Old→new name aliases so 'claude-3-opus' hits the same rate as Python.
const MODEL_ALIASES = {
  'claude-3-opus': 'claude-opus-4',
  'claude-3-sonnet': 'claude-sonnet-4',
  'claude-3-haiku': 'claude-haiku-4',
  'claude-3.5-sonnet': 'claude-3-5-sonnet',
  'claude-3.5-haiku': 'claude-3-5-haiku',
};

function estimateCost(tokens, model = '') {
  let m = (model || '').toLowerCase();
  for (const [alias, canonical] of Object.entries(MODEL_ALIASES)) {
    if (m.startsWith(alias)) { m = canonical + m.slice(alias.length); break; }
  }
  // Longest-prefix match — prevents 'gpt-4o' eating 'gpt-4o-mini'.
  const keys = Object.keys(COST_PER_M).filter(k => k !== 'default').sort((a, b) => b.length - a.length);
  const key = (m && keys.find(k => m.startsWith(k)));
  if (!key && model) {
    // One-time warning per unknown model — stderr, doesn't pollute stdout.
    if (!estimateCost._warned) estimateCost._warned = new Set();
    if (!estimateCost._warned.has(model)) {
      estimateCost._warned.add(model);
      try { console.warn(`[entroly] unknown model '${model}'; using default $${COST_PER_M.default}/M`); } catch (_) {}
    }
  }
  return (tokens / 1_000_000) * COST_PER_M[key || 'default'];
}

function atomicWrite(filePath, content) {
  const tmp = filePath + '.tmp-' + process.pid;
  fs.writeFileSync(tmp, content, 'utf8');
  fs.renameSync(tmp, filePath);
}

class ValueTracker {
  constructor(dataDir = null) {
    this._dir = dataDir || path.join(os.homedir(), '.entroly');
    fs.mkdirSync(this._dir, { recursive: true });
    this._path = path.join(this._dir, FILE_NAME);
    this._data = this._load();
  }

  _load() {
    if (fs.existsSync(this._path)) {
      try {
        const raw = JSON.parse(fs.readFileSync(this._path, 'utf8'));
        if (raw && typeof raw === 'object' && 'version' in raw) return raw;
      } catch (_) { /* fall through */ }
    }
    return this._defaults();
  }

  _defaults() {
    const now = Date.now() / 1000;
    return {
      version: 2,
      lifetime: {
        tokens_saved: 0,
        cost_saved_usd: 0.0,
        requests_optimized: 0,
        first_seen: now,
        last_seen: now,
        evolution_spent_usd: 0.0,
        evolution_attempts: 0,
        evolution_successes: 0,
      },
    };
  }

  _save() {
    try { atomicWrite(this._path, JSON.stringify(this._data, null, 2)); }
    catch (_) { /* best-effort */ }
  }

  record({ tokensSaved = 0, model = '', optimized = true } = {}) {
    const cost = estimateCost(tokensSaved, model);
    const lt = this._data.lifetime;
    lt.tokens_saved += tokensSaved;
    lt.cost_saved_usd = +(lt.cost_saved_usd + cost).toFixed(6);
    if (optimized) lt.requests_optimized += 1;
    lt.last_seen = Date.now() / 1000;
    this._save();
    return { tokensSaved, costSaved: cost };
  }

  getEvolutionBudget() {
    const lt = this._data.lifetime;
    const lifetimeSaved = lt.cost_saved_usd || 0;
    const totalSpent = lt.evolution_spent_usd || 0;
    const totalEarned = lifetimeSaved * EVOLUTION_TAX_RATE;
    const available = Math.max(0, totalEarned - totalSpent);
    return {
      availableUsd: +available.toFixed(6),
      totalEarnedUsd: +totalEarned.toFixed(6),
      totalSpentUsd: +totalSpent.toFixed(6),
      canEvolve: available > 0.001,
      taxRate: EVOLUTION_TAX_RATE,
    };
  }

  recordEvolutionSpend(costUsd, success = false) {
    const lt = this._data.lifetime;
    const lifetimeSaved = lt.cost_saved_usd || 0;
    const currentSpent = lt.evolution_spent_usd || 0;
    const totalEarned = lifetimeSaved * EVOLUTION_TAX_RATE;
    const available = totalEarned - currentSpent;

    if (costUsd > available + 0.001) {
      return {
        status: 'rejected',
        remainingUsd: +Math.max(0, available).toFixed(6),
      };
    }

    lt.evolution_spent_usd = +(currentSpent + costUsd).toFixed(6);
    lt.evolution_attempts = (lt.evolution_attempts || 0) + 1;
    if (success) lt.evolution_successes = (lt.evolution_successes || 0) + 1;
    this._save();
    return {
      status: 'recorded',
      remainingUsd: +Math.max(0, available - costUsd).toFixed(6),
    };
  }

  stats() {
    return {
      lifetime: { ...this._data.lifetime },
      budget: this.getEvolutionBudget(),
    };
  }
}

module.exports = { ValueTracker, EVOLUTION_TAX_RATE, estimateCost };
