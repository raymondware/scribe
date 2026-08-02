# Scribe

A Claude Code plugin that catches AI-default writing patterns before they ship.

Scribe routes every draft through a persona system, picks a varied subset of anti-patterns per run (so two runs never produce the same critique), scores prose on a 0-100 sameness scale, and fixes voice, rhythm, vocabulary, structure, and rhetoric before the book goes to print.

Built for longform authors, essayists, ghostwriters, and editors. Runs a team of specialist agents that plan, draft, edit, and review collaboratively.

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

Every run picks a different subset of anti-patterns. Scribe reads the audit log (`state/draws.jsonl`) and excludes the previous run's subset. Two runs on the same prompt produce different critiques.

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

### Orchestration (Opus 4.8)
`conductor` `anti-pattern-selector` `critique-synthesizer`

## Contributing

See `CLAUDE.md` for the contributor guide.

## License

MIT. See `LICENSE`.