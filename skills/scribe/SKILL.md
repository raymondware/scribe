---
name: scribe
version: 1.1.1
description: Multi-agent writing harness for longform authors. Catches AI-default writing patterns (delve, tapestry, em-dash overuse, hedging openers, three-word lists, negative/positive restatement, conclusion-restating) before they ship. Five writer personas (literary fiction, popular nonfiction, technical writing, memoir, business book), persona-specific rhythm and voice rules, anti-pattern rotation per run with audit log, multi-critic synthesis. Built for authors, essayists, ghostwriters, and editors.
---

# Scribe v1.1.1

Multi-agent writing harness for authors who care about voice.

For a focused humanizing pass on existing prose, use `${CLAUDE_PLUGIN_ROOT}/skills/humanize/SKILL.md` (`/scribe:humanize`). That skill edits directly without the pipeline, a draw, an audit log entry, or a Sameness Score. Explicit requests for the pipeline commands below retain their existing behavior.

## Quick Start (5 minutes)

```bash
# Generate a passage from scratch
/scribe:write opening chapter for a popular nonfiction book about how cities forget their own histories. Should read like Patrick Radden Keefe.

# Audit existing prose
/scribe:audit
# (paste the manuscript section to audit)

# Surgical revision (preserves meaning)
/scribe:revise

# Aggressive de-AI on an LLM-generated draft
/scribe:differentiate --source claude

# Run only the anti-pattern selector (verifies rotation)
/scribe:draw memoir essay about my year in Buenos Aires

# Plan only — no draft
/scribe:plan business book chapter on why most pivots fail
```

What scribe does behind the scenes:

1. anti-pattern-selector picks a varied subset of anti-patterns for THIS run, weighted by genre + surface signals. Excludes the previous run's subset. Audits to `state/draws.jsonl`.
2. Detects one of 5 writer personas from the brief or prose
3. Loads that persona's rhythm, voice, vocabulary rules
4. Specialists work within the assigned subset (no specialist reads outside it)
5. Critic ensemble runs in parallel; synthesizer merges into a 0-100 Sameness Score
6. Score above gate threshold (40 for scribe-produced, 60 for external audit) routes to targeted rework

**Respect for stated direction:** scribe targets AI-default USES of patterns, not the user's stated voice or vocabulary preferences. If a user says "I want this to read like Cormac McCarthy with no quotation marks," scribe applies that signature WITHIN its rotation discipline.

---

## Five Writer Personas

| ID | Persona | For | Risk |
|----|---------|-----|------|
| LF | `literary-fiction` | Novels, novellas, short stories | Low — readers self-select for prose |
| PN | `popular-nonfiction` | Big-idea books for general audiences | High — heavy AI training data |
| TW | `technical-writing` | Technical books, dev essays, deep-dive docs | Medium — readers spot AI prose fast |
| MM | `memoir` | First-person life writing | Critical — voice is the product |
| BB | `business-book` | Business, leadership, productivity books | **Highest** — genre converges on AI-default |

Persona files: `${CLAUDE_PLUGIN_ROOT}/skills/scribe/references/personas/`

## The Variation Rule

The biggest failure mode of any "AI-ism checker" is that the checker becomes a template. If scribe critiqued every manuscript against the same 30 patterns, two distinct prompts would produce identical critiques.

Hard rule:

1. Vary the draw per run.
2. Never reuse the same subset two runs in a row.
3. Audit trail. Every draw appended to `state/draws.jsonl` and printed at the top of every output.
4. Brief-specific signal must influence selection.

The `anti-pattern-selector` agent enforces all four. It runs first in every pipeline command. The standalone `/scribe:humanize` skill works outside this pipeline and its draw rules.

## Agent Team

### Orchestration

| Agent | Model | Role |
|---|---|---|
| `conductor` | Opus | Pipeline orchestrator. Manages state, spawns specialists, enforces quality gates. |
| `anti-pattern-selector` | Sonnet | Picks the varied subset for this run, writes the audit log. Runs first in every pipeline. |
| `critique-synthesizer` | Opus | Merges parallel critic outputs, deduplicates, computes consensus 0-100 Sameness Score. |

### Planning Specialists (read-only, produce specs)

| Agent | Model | Role |
|---|---|---|
| `rhythm-specialist` | Haiku | Sentence-length distribution, paragraph-length variance, em-dash budget |
| `voice-specialist` | Haiku | Register, tense, POV, authorial stance, exemplar selection |
| `vocabulary-specialist` | Haiku | Domain vocabulary, banned-word list, specificity targets |
| `structure-specialist` | Haiku | Paragraph-by-paragraph skeleton, opening discipline, closing discipline |
| `dialogue-specialist` | Haiku | Speaker voices, tag rules, dialogue rhythm (when surface includes dialogue) |

### Drafting Implementers

| Agent | Model | Role |
|---|---|---|
| `draft-implementer` | Sonnet | First-pass writer. Follows specialist specs, avoids assigned subset patterns. |
| `voice-implementer` | Sonnet | Second-pass reviser. AI-ism removal, em-dash audit, rhythm tightening. |

### Review (parallel ensemble, each scoped to one slice of the subset)

| Agent | Model | Role |
|---|---|---|
| `rhythm-critic` | Haiku | Sentence/paragraph variance, em-dash density, tricolons. 0-25 |
| `voice-critic` | Opus | Voice consistency, vocabulary register, marketing-verb detection. 0-25 |
| `cliche-detector` | Haiku | Universal aphorisms, dead metaphors, content-marketing openers. 0-25 |
| `ai-ism-critic` | Haiku | Direct lexical and structural AI-fingerprint detection. 0-25 |
| `pacing-critic` | Haiku | Chapter/essay-level pacing — only for those surfaces. 0-25 |

### Independent / Research

| Agent | Model | Role |
|---|---|---|
| `external-judge` | Sonnet | Independent 0-10 sameness scorer. No shared context with critic ensemble. |
| `cross-persona-audit` | Sonnet | Audits the 5 personas for divergence. Run when persona files change. |
| `research-scout` | Sonnet | Mines writing communities for new AI-default patterns. PRs only. |

## Pipeline

```
INIT -> DRAW -> PLAN -> INTERVIEW -> DRAFT -> REVIEW -> PRESENT
                  ^                            |
                  |                            v
                  +-------- REWORK ------------+
```

Read `${CLAUDE_PLUGIN_ROOT}/skills/scribe/references/orchestration/pipeline.md` for the state machine.
Read `${CLAUDE_PLUGIN_ROOT}/skills/scribe/references/orchestration/quality-gates.md` for gate criteria.

## Anti-Pattern Pool & Manifest

The pattern pool is catalogued at `${CLAUDE_PLUGIN_ROOT}/anti-patterns/manifest.json`. Each entry has stable `id`, `categories`, `tags`, `severity_default`, `source_file`, `anchor`, `personas`, `site_signals`. Critics read the manifest to look up where to find the rule for an ID, then read only the relevant section of the source file.

The pool is grouped into three base files plus a research-sourced directory:

| File | Patterns |
|---|---|
| `${CLAUDE_PLUGIN_ROOT}/anti-patterns/language.md` | Delve / tapestry, tricolons, hedge stacking, em-dash universal connector, marketing verb, self-descriptor, universal aphorism, "not just X but Y" frames, negative/positive restatement, filler intensifiers |
| `${CLAUDE_PLUGIN_ROOT}/anti-patterns/structure.md` | Uniform paragraph length, chapter-recap opening, chapter-end summary, forward references, three-part skeleton, predictable section sequence, bullet-list body, three-anecdote montage, false-question subhead, conclusion-restating-conclusion |
| `${CLAUDE_PLUGIN_ROOT}/anti-patterns/rhetoric.md` | "In today's fast-paced world" opener, universalizing claims, false dichotomies, rhetorical question reflex, aphorism section closers, "what most don't realize" pseudo-reveal, "and yet" twist, concluding hortatory |
| `${CLAUDE_PLUGIN_ROOT}/anti-patterns/sourced-from-research/` | Filed by the research-scout agent. Each pattern requires 2+ independent complaints. |

Total at v1.0: 31 anti-patterns. Will grow through ralph-loop iterations and `/scribe:research` runs.

## Sameness Score

| Score | Meaning |
|---|---|
| 0-20 | Distinctive. Has voice. Ready to ship. |
| 21-40 | Has voice; some defaults showing but not dominant. |
| 41-60 | Generic. Could be any AI draft. |
| 61-80 | Default AI prose. Multiple tells per page. |
| 81-100 | Unedited AI output. Significant rewrite required. |

Gate threshold: **40** for scribe-produced output, **60** for `/scribe:audit` on external prose.

## Commands

| Command | Does |
|---|---|
| `/scribe:humanize <text or path>` | Focused edit preserving voice and meaning; returns the passage without pipeline scoring |
| `/scribe:write <desc>` | Full 6-phase pipeline via conductor |
| `/scribe:plan <desc>` | Plan phase only (specs, no draft) |
| `/scribe:audit` | DRAW + parallel critic ensemble + synthesizer (no rewrite) |
| `/scribe:review` | Same as audit but always runs ALL critics; verbose findings |
| `/scribe:revise` | Surgical edits preserving meaning (±10% word count) |
| `/scribe:differentiate` | Aggressive de-AI; allows structural cuts (±25% word count) |
| `/scribe:diagnose` | Read-only findings, no Sameness Score |
| `/scribe:compare` | Before/after or vs-exemplar comparison |
| `/scribe:research` | Trigger research-scout for new pattern discovery |
| `/scribe:draw <desc>` | Run the anti-pattern-selector standalone (rotation verification) |

## State

Append-only audit log lives at `${CLAUDE_PLUGIN_ROOT}/state/draws.jsonl`. Every pipeline run appends one record before any other agent runs. The standalone humanize skill does not use this log. See `${CLAUDE_PLUGIN_ROOT}/state/README.md` for the schema.

## Reference Files

| File | Purpose |
|---|---|
| `${CLAUDE_PLUGIN_ROOT}/skills/scribe/references/exemplars.md` | Author/book exemplars per persona |
| `${CLAUDE_PLUGIN_ROOT}/skills/scribe/references/rhythm-tokens.md` | Cross-persona rhythm targets and vocabulary |
| `${CLAUDE_PLUGIN_ROOT}/skills/scribe/references/reader-clarity.md` | Clarity checks for compressed and explanatory prose |
| `${CLAUDE_PLUGIN_ROOT}/skills/scribe/references/orchestration/pipeline.md` | Pipeline state machine |
| `${CLAUDE_PLUGIN_ROOT}/skills/scribe/references/orchestration/quality-gates.md` | Gate criteria |

## Tools

| File | Purpose |
|---|---|
| `${CLAUDE_PLUGIN_ROOT}/tools/draw_simulator.py` | Reference Python implementation of anti-pattern-selector for deterministic rotation testing |
| `${CLAUDE_PLUGIN_ROOT}/tools/prose_validate.sh` | Lightweight check that an output passage hits rhythm targets |

## Voice

Scribe talks writer-to-writer. No em-dashes. No marketing register. Specific recommendations over general observations.

(The voice rule applies recursively. Scribe must not exemplify what it flags.)
