# Scribe

**Make AI-assisted drafts sound like you wrote them.**

Scribe is a Claude Code plugin for authors, essayists, and editors. It finds the patterns readers recognize as AI prose and rewrites them in a voice that fits your book.

```
/plugin marketplace add raymondware/kern
/plugin install scribe@raymondware
/scribe:revise
```

Paste a passage after `/scribe:revise`. Scribe returns the rewrite, a diff, and a 0-100 sameness score.

For a focused edit, use `/scribe:humanize` with a passage or file path. It keeps your voice and meaning, removes stiffness where needed, and returns the edited passage. It runs directly without the agent pipeline, pattern draw, audit log, or score. Already-effective prose can stay unchanged.

### Before

> In today's fast-paced world, leadership isn't about authority; it's about influence. Great leaders don't just manage teams, but inspire them. By leveraging empathy, clarity, and vision, they unlock the full potential of their organizations. It's important to note that this is not a destination. It is a mindset.

| Flagged | Pattern |
|---|---|
| "In today's fast-paced world" | `in-todays-fast-paced-world` |
| "isn't about authority; it's about influence" | `negative-positive-restatement` |
| "don't just manage teams, but inspire them" | `not-just-x-but-y-reflex` |
| "empathy, clarity, and vision" | `tricolon-reflex` |
| "leveraging", "unlock the full potential" | `marketing-verb` |
| "It's important to note that" | `its-worth-noting-throat-clearing` |
| "not a destination. It is a mindset." | `negative-positive-restatement` |

### After

<!-- Replace with real /scribe:revise output (business-book persona) and its score before publishing. -->

> Teams follow the manager who listens before deciding. She asks what is blocking the work, says plainly which goal matters this quarter, and then lets people do it.

**18 agents · 31 anti-patterns · 5 writer personas · a different critique subset every run**

## The Problem

AI-generated writing converges on the same cadence. "Delve into the tapestry of." "It's important to note that." "Not just X, but Y." "This is not X. It is Y." Em-dashes everywhere. Three-word lists. Conclusion paragraphs that restate the previous five. Hedging openers.

Scribe fixes this with persona-first generation and a sameness score that quantifies how close prose is to the AI default.

## Installation

Add the raymondware marketplace, then install Scribe:

```
/plugin marketplace add raymondware/kern
/plugin install scribe@raymondware
```

Restart Claude Code and the `/scribe:*` commands are available.

## Quick Start

```bash
# Generate a passage from scratch
/scribe:write opening chapter for a popular nonfiction book about how cities forget their own histories

# Audit existing prose
/scribe:audit
# (paste the manuscript section to audit)

# De-AI an existing draft
/scribe:differentiate

# Run only the anti-pattern selector (verifies rotation)
/scribe:draw memoir essay about my year in Buenos Aires
```

## Commands

| Command | Does |
|---|---|
| `/scribe:humanize <text or path>` | Edit existing prose for naturalness while preserving voice, facts, and useful structure |
| `/scribe:write <desc>` | Full pipeline: persona detection, specialists, draft, review |
| `/scribe:audit` | Anti-pattern scan with sameness score against existing prose |
| `/scribe:revise` | Rewrite a passage against Scribe's standards, show diff |
| `/scribe:differentiate` | Identify AI writing tells and apply targeted fixes |
| `/scribe:diagnose` | Single-pass AI-ism detection, fast turnaround |
| `/scribe:compare <a> <b>` | Side-by-side prose comparison with similarity score |
| `/scribe:plan <desc>` | Writing specs only (voice, rhythm, structure) -- no draft |
| `/scribe:review` | Full review pass: critic ensemble, voice editor |
| `/scribe:research` | Scan writing communities for new anti-patterns |
| `/scribe:draw <desc>` | Run the anti-pattern selector standalone (rotation verification) |

## How It Works

### 1. Persona Detection

Scribe picks a persona from your description, then loads that persona's rules for voice, rhythm, vocabulary, and structure. Five personas:

| Persona | For |
|---|---|
| `literary-fiction` | Novels, novellas, short stories. Voice and rhythm primary. |
| `popular-nonfiction` | Books that explain ideas to a general audience. Gladwell/Lewis/Pollan register. |
| `technical-writing` | Books, docs, essays for technical readers. Precision over style. |
| `memoir` | First-person life writing. Voice is everything. |
| `business-book` | High AI-default risk. Hardest to make distinctive. |

### 2. Variation Rule

Every pipeline run picks a different subset of anti-patterns. Scribe reads the audit log (`state/draws.jsonl`) and excludes the previous run's subset. Two runs on the same prompt produce different critiques. The focused `/scribe:humanize` skill works outside this pipeline.

### 3. Parallel Critics + Synthesizer

Five critics run in parallel (rhythm, voice, cliche, AI-ism, pacing). The synthesizer merges their output, removes duplicates, and computes a consensus sameness score.

### 4. The Sameness Score

Every draft gets a 0-100 score on AI-default similarity:

| Score | Meaning |
|---|---|
| 0-20 | Distinctive. A voice. Ship. |
| 21-40 | Has voice. Some defaults showing. |
| 41-60 | Generic. Could be any AI-generated draft. |
| 61-80 | Default AI prose. Multiple tells per page. |
| 81-100 | Unedited AI output. Do not ship. |

## Anti-Pattern Library

Scribe ships with anti-patterns across three files:

| File | Patterns |
|---|---|
| `anti-patterns/language.md` | Delve/tapestry/realm vocabulary, tricolon reflex, hedge stacking, marketing verbs, em-dash overuse, self-descriptors, negative/positive restatement, filler intensifiers |
| `anti-patterns/rhetoric.md` | Universal aphorisms, "not just X but Y" frames, throat-clearing openers, flashlight-hedging adjectives |
| `anti-patterns/structure.md` | Conclusion-restating, predictable section sequence, thesis-delay syndrome |

## Agent Team

### Specialists (Haiku)
`rhythm-specialist` `voice-specialist` `vocabulary-specialist` `structure-specialist` `dialogue-specialist`

### Drafting (Sonnet)
`draft-implementer` `voice-implementer`

### Critics (parallel ensemble)
`rhythm-critic` `voice-critic` `cliche-detector` `ai-ism-critic` `pacing-critic`

### Orchestration
`conductor` `critique-synthesizer` (Opus), `anti-pattern-selector` (Sonnet)

## Contributing

See `CLAUDE.md` for the contributor guide.

## License

MIT. See `LICENSE`.
