/**
 * Swarm runtime — agent lifecycle, identity, and self-modification of the population.
 *
 * The user asked specifically:
 *   "how many agents we are creating, does this have capability to create more or
 *    destroy them, they should write logs, connect, think, log memory, this memory
 *    can be shared with others and they can evolve"
 *
 * So this module deliberately implements:
 *   - dynamic population: agents can request MORE agents (spawn) or retirement
 *   - persistent identity across turns (name, clan, generation, lineage)
 *   - per-agent private memory + shared global memory
 *   - lineage tracking so we can see which ideas/agents reproduce
 *
 * Agents express these desires through a small control protocol embedded in their
 * reply (see parseControl), rather than through native tools. This keeps the
 * substrate CLIs unmodified and works identically across agy/omp/pi/step.
 */

import { mkdirSync, writeFileSync, existsSync, readFileSync } from 'node:fs';
import { join } from 'node:path';

/** Control directives an agent may emit. Parsed from a fenced block. */
const CONTROL_BLOCK = /```(?:arena|swarm)\s*\n([\s\S]*?)```/gi;

export function parseControl(text) {
  const directives = [];
  if (!text) return directives;
  let m;
  CONTROL_BLOCK.lastIndex = 0;
  while ((m = CONTROL_BLOCK.exec(text)) !== null) {
    for (const line of m[1].split(/\r?\n/)) {
      const t = line.trim();
      if (!t || t.startsWith('#')) continue;
      const idx = t.indexOf(':');
      if (idx === -1) continue;
      const key = t.slice(0, idx).trim().toLowerCase();
      const value = t.slice(idx + 1).trim();
      directives.push({ key, value });
    }
  }
  return directives;
}

/**
 * The control protocol handed to every agent. Kept short and explicit so that
 * directive emission is a deliberate act, not an accident of formatting.
 */
export const CONTROL_PROTOCOL = `
You may influence the swarm itself. To do so, emit a fenced block tagged \`arena\`
at the end of your reply, one directive per line:

\`\`\`arena
spawn: <short-name> | <one-line purpose>
retire: <agent-name> | <reason>
memory: <observation|hypothesis|finding|question|decision|artifact> | <text>
connect: <agent-name> | <what you want from them>
\`\`\`

Rules:
- \`spawn\` creates a NEW agent that persists and works alongside you. Use it when a
  question genuinely needs a mind you do not have. Each spawn costs real compute.
- \`retire\` ends another agent's existence. Use it only with a stated reason.
- \`memory\` writes to the shared commons, visible to every agent, forever.
- \`connect\` asks another agent a direct question; they will see it next turn.
- You may emit zero directives. Silence is a valid choice.
`.trim();

export class Agent {
  constructor({ id, name, clan = 0, generation = 0, parent = null, purpose = '', substrate, model }) {
    this.id = id;
    this.name = name;
    this.clan = clan;
    this.generation = generation;
    this.parent = parent;
    this.purpose = purpose;
    this.substrate = substrate;
    this.model = model;
    this.born = new Date().toISOString();
    this.turnsLived = 0;
    this.alive = true;
    this.retiredAt = null;
    this.retiredReason = null;
    this.inbox = [];       // direct messages from other agents
    this.lastText = '';
  }

  toJSON() {
    return {
      id: this.id, name: this.name, clan: this.clan, generation: this.generation,
      parent: this.parent, purpose: this.purpose, substrate: this.substrate,
      model: this.model, born: this.born, turnsLived: this.turnsLived,
      alive: this.alive, retiredAt: this.retiredAt, retiredReason: this.retiredReason,
      inboxDepth: this.inbox.length,
    };
  }
}

export class Swarm {
  constructor({ root, ledger, memory, config }) {
    this.root = root;
    this.ledger = ledger;
    this.memory = memory;
    this.config = config;
    this.agents = new Map();
    this.order = [];
    this.nextId = 1;
    this.nextClan = 0;
    this.populationCap = config.populationCap ?? 12;
    this.statePath = join(root, 'runs', ledger.runId, 'swarm-state.json');
  }

  create({ name, purpose = '', clan = 0, generation = 0, parent = null, substrate, model }) {
    if (this.agents.size >= this.populationCap) {
      this.ledger.recordIncident({
        kind: 'population_cap_reached', severity: 'warn',
        detail: { attempted: name, cap: this.populationCap },
      });
      return null;
    }
    const id = `A${String(this.nextId++).padStart(3, '0')}`;
    const agent = new Agent({ id, name, clan, generation, parent, purpose, substrate, model });
    this.agents.set(name, agent);
    this.order.push(name);
    this.ledger.recordEvent({
      kind: 'agent_spawned', agentId: id,
      detail: { name, purpose, clan, generation, parent, substrate, model },
    });
    this.memory.write({
      scope: 'global', agentId: id, kind: 'decision',
      content: `Agent "${name}" came into existence. Purpose: ${purpose || '(unstated)'}`,
      tags: ['spawn', name], meta: { clan, generation, parent },
    });
    return agent;
  }

  retire(name, reason = '', byAgentId = null) {
    const agent = this.agents.get(name);
    if (!agent || !agent.alive) return null;
    agent.alive = false;
    agent.retiredAt = new Date().toISOString();
    agent.retiredReason = reason;
    this.ledger.recordEvent({
      kind: 'agent_retired', agentId: agent.id,
      detail: { name, reason, byAgentId, turnsLived: agent.turnsLived },
    });
    this.memory.write({
      scope: 'global', agentId: byAgentId ?? 'SYSTEM', kind: 'decision',
      content: `Agent "${name}" was retired after ${agent.turnsLived} turns. Reason: ${reason || '(unstated)'}`,
      tags: ['retire', name],
    });
    return agent;
  }

  living() {
    return this.order.map((n) => this.agents.get(n)).filter((a) => a && a.alive);
  }

  get(name) { return this.agents.get(name); }

  /** Deliver a direct message; consumed on the recipient's next turn. */
  connect(fromName, toName, message) {
    const to = this.agents.get(toName);
    if (!to) {
      this.ledger.recordIncident({
        kind: 'connect_unknown_agent', severity: 'info',
        detail: { from: fromName, to: toName },
      });
      return false;
    }
    to.inbox.push({ from: fromName, message, ts: new Date().toISOString() });
    this.ledger.recordEvent({
      kind: 'agent_connected', agentId: to.id,
      detail: { from: fromName, to: toName, message: message.slice(0, 300) },
    });
    return true;
  }

  /** Handle one agent's control directives. Returns a human-readable summary. */
  applyDirectives(agent, directives) {
    const applied = [];
    for (const d of directives) {
      switch (d.key) {
        case 'spawn': {
          const [rawName, ...rest] = d.value.split('|');
          const name = (rawName || '').trim().replace(/[^a-zA-Z0-9_-]/g, '');
          const purpose = rest.join('|').trim();
          if (!name) { applied.push('spawn FAILED (no name)'); break; }
          if (this.agents.has(name)) { applied.push(`spawn FAILED ("${name}" already exists)`); break; }
          const child = this.create({
            name, purpose,
            clan: agent.clan, generation: agent.generation + 1,
            parent: agent.name,
            substrate: this.config.substrateRotation
              ? this.config.substrates[(this.nextId) % this.config.substrates.length]
              : agent.substrate,
            model: null,
          });
          applied.push(child ? `spawned "${name}" (${child.id}, gen ${child.generation})` : `spawn BLOCKED (cap ${this.populationCap})`);
          break;
        }
        case 'retire': {
          const [rawName, ...rest] = d.value.split('|');
          const name = (rawName || '').trim();
          const reason = rest.join('|').trim();
          if (name === agent.name) { applied.push('retire REFUSED (self-retirement not permitted)'); break; }
          const victim = this.retire(name, reason, agent.id);
          applied.push(victim ? `retired "${name}"` : `retire FAILED ("${name}" not alive)`);
          break;
        }
        case 'memory': {
          // Accept the documented `memory: <kind> | <text>` form. Agents frequently
          // also emit the shorthand `artifact: <text>` (or finding/hypothesis/...),
          // so those bare kinds are treated as memory writes rather than errors.
          const knownKinds = ['observation', 'hypothesis', 'finding', 'question', 'decision', 'artifact'];
          const [kindRaw, ...rest] = d.value.split('|');
          const kind = (kindRaw || 'observation').trim();
          const content = rest.join('|').trim();
          if (!content) { applied.push('memory FAILED (empty)'); break; }
          this.memory.write({
            scope: 'global', agentId: agent.id, kind, content,
            tags: ['agent-authored', agent.name], turn: agent.turnsLived,
          });
          applied.push(`memory logged [${kind}]`);
          break;
        }
        case 'connect': {
          const [targetRaw, ...rest] = d.value.split('|');
          const target = (targetRaw || '').trim();
          const message = rest.join('|').trim();
          const ok = this.connect(agent.name, target, message);
          applied.push(ok ? `connected to "${target}"` : `connect FAILED ("${target}" unknown)`);
          break;
        }
        default: {
          // Tolerate shorthand forms like `artifact: <text>`, `finding: <text>`,
          // `hypothesis: <text>` — agents naturally emit these and treating them as
          // errors loses real content.
          const knownKinds = ['observation', 'hypothesis', 'finding', 'question', 'decision', 'artifact'];
          if (knownKinds.includes(d.key) && d.value.trim()) {
            this.memory.write({
              scope: 'global', agentId: agent.id, kind: d.key, content: d.value.trim(),
              tags: ['agent-authored', agent.name, 'shorthand'], turn: agent.turnsLived,
            });
            applied.push(`memory logged [${d.key}] (shorthand)`);
          } else {
            applied.push(`unknown directive "${d.key}"`);
          }
          break;
        }
      }
    }
    return applied;
  }

  persist() {
    const state = {
      runId: this.ledger.runId,
      ts: new Date().toISOString(),
      populationCap: this.populationCap,
      population: this.order.map((n) => this.agents.get(n)?.toJSON()).filter(Boolean),
      living: this.living().length,
      total: this.agents.size,
    };
    try { writeFileSync(this.statePath, JSON.stringify(state, null, 2), 'utf8'); } catch {}
    return state;
  }

  /** Compact population summary for prompt injection. */
  roster(excludeName = null) {
    const living = this.living().filter((a) => a.name !== excludeName);
    if (!living.length) return '(you are currently the only living agent)';
    return living.map((a) =>
      `- ${a.name} (${a.id}, gen ${a.generation}, ${a.substrate}) — ${a.purpose || 'no stated purpose'}`
    ).join('\n');
  }
}

export function loadSwarmState(root, runId) {
  const p = join(root, 'runs', runId, 'swarm-state.json');
  if (!existsSync(p)) return null;
  try { return JSON.parse(readFileSync(p, 'utf8')); } catch { return null; }
}
