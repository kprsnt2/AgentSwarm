/**
 * Epistemic class inference — extracted from new-run.mjs so it can be unit tested.
 *
 * The class decides what counts as a valid answer, and the oracle only enforces the
 * metaphysical firewall when a domain actually carries the `metaphysical` class. An
 * inference miss is therefore not cosmetic: it silently disables a check. Two rules
 * follow from that:
 *
 *   1. Deities and religious truth claims are matched explicitly. The first version
 *      of this function missed "is Krishna real" because "krishna" was not in the
 *      keyword list — the most verdict-prone question in the corpus was classified
 *      `exploratory`, where the verdict detector never runs.
 *   2. The fallback is reported as LOW confidence. Callers must not silently accept
 *      it; new-run.mjs refuses to start without an explicit `-c <class>`.
 */

/** Religious/philosophical truth-claim markers, including named deities. */
const RELIGIOUS = /\b(god|gods|deity|deities|divine|divinity|religio|religion|religious|scripture|scriptures|veda|vedas|vedic|rigveda|rig veda|samaveda|yajurveda|atharvaveda|upanishad|upanishads|purana|puranas|bhagavad|gita|mahabharata|ramayana|bible|quran|koran|torah|gospel|afterlife|soul|souls|spiritual|spirituality|reincarnat|karma|dharma|moksha|nirvana|brahman|atman|hindu|hinduism|krishna|shiva|vishnu|rama|hanuman|ganesh|durga|laksmi|lakshmi|saraswati|parvati|kali|jesus|christ|christian|yahweh|allah|islam|muhammad|mohammed|buddha|buddhism|mahavira|jain|sikh|guru nanak|zeus|odin|thor|osiris|amaterasu|kami|consciousness (?:is|after)|meaning of life)\b/i;

/** A question about what a text says is historical/textual, not metaphysical. */
// Stem-tolerant endings (\w*) matter: "achievable", "historical" and "measurable"
// must match their stems, and a trailing \b after a bare stem silently fails on them.
const TEXTUAL = /\b(text|texts|scripture\w*|verse\w*|reference\w*|mention\w*|passage\w*|chapter\w*|hymn\w*|written|writes|say|says|said|describe\w*|document\w*|dating|histor\w*|archaeolog\w*|evidence)\b/i;

const HISTORICAL = /\b(history|historical|ancient|century|bce|dated|dating|archaeolog\w*|manuscript\w*|text|texts|empire|civilis\w*|civiliz\w*|origin of the (?:word|term|practice)|mahabharata|ramayana)\b/i;

const ENGINEERING = /\b(can we|is it possible to|feasib\w*|engineer\w*|design\w*|build\w*|construct\w*|achiev\w*|propuls\w*|reactor\w*|rocket\w*|spacecraft|travel at|faster than light|warp|terraform\w*|mine|colonis\w*|coloniz\w*)\b/i;

const EMPIRICAL = /\b(measure\w*|measur\w*|experiment\w*|data|observ\w*|detect\w*|how much|how many|what is the (?:value|mass|rate|constant)|calculat\w*|deriv\w*|equation\w*|temperature of|density of|speed of)\b/i;

const SPECULATIVE_PHYSICS = /\b(multiverse|parallel universe|string theory|quantum gravity|dark matter|dark energy|wormhole|time travel|simulation hypothesis|boltzmann brain|many worlds)\b/i;

const LIFE_ELSEWHERE = /\b(alien|aliens|extraterrest|life elsewhere|fermi|technosignature|exoplanet|habitable)\b/i;

/**
 * Infer the epistemic class from question text.
 *
 * Returns { cls, why, confidence } where confidence is 'high' for a rule match and
 * 'low' for the fallback. Callers that treat the class as load-bearing (the oracle
 * does) must refuse to proceed on 'low' unless the user overrides explicitly.
 */
export function inferClass(text) {
  const t = String(text || '').toLowerCase();

  // 1. Religious truth claims -> metaphysical, unless the question is about what a
  //    text says (then it is investigable as history/textual study).
  if (RELIGIOUS.test(t)) {
    if (TEXTUAL.test(t)) {
      return { cls: 'historical', why: 'asks what a text says -> investigable as history/textual study', confidence: 'high' };
    }
    return { cls: 'metaphysical', why: 'religious/philosophical truth claim -> not empirically decidable', confidence: 'high' };
  }

  // 2. Historical / textual.
  if (HISTORICAL.test(t)) {
    return { cls: 'historical', why: 'about documented events or texts', confidence: 'high' };
  }

  // 3. Engineering feasibility.
  if (ENGINEERING.test(t)) {
    return { cls: 'engineering', why: 'feasibility question -> needs the binding physical limit', confidence: 'high' };
  }

  // 4. Empirical.
  if (EMPIRICAL.test(t)) {
    return { cls: 'empirical', why: 'asks for measurable quantities', confidence: 'high' };
  }

  // 5. Physics-flavoured speculation.
  if (SPECULATIVE_PHYSICS.test(t)) {
    return { cls: 'exploratory', why: 'speculative physics -> must yield falsifiable predictions or concede undecidability', confidence: 'high' };
  }

  // 6. Life elsewhere.
  if (LIFE_ELSEWHERE.test(t)) {
    return { cls: 'exploratory', why: 'open search -> needs falsifiable predictions', confidence: 'high' };
  }

  return {
    cls: 'exploratory',
    why: 'no strong signal -> refusing to guess; pass -c <class> to decide explicitly',
    confidence: 'low',
  };
}
