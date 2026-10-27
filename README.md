# Scribe

**Make AI-assisted drafts sound like you wrote them.**

Scribe is a Claude Code plugin for authors, essayists, and editors. It finds the patterns readers recognize as AI prose and rewrites them in a voice that fits your book.

```
/plugin marketplace add raymondware/kern
/plugin install scribe@raymondware
/scribe:revise
```

Paste a passage after `/scribe:revise`. Scribe returns the revised passage with before-and-after sameness scores on a 0-100 scale.

For a focused edit, use `/scribe:humanize` with a passage or file path. It removes stiffness while keeping your voice and meaning. For pasted text it returns just the edited passage; for a requested file edit it changes the prose in place. It skips the agent pipeline, pattern draw, audit log, and score, and it leaves prose that already works unchanged.

### Before

> In today's fast-paced world, leadership isn't about authority; it's about influence. Great leaders don't just manage teams, but inspire them. By leveraging empathy, clarity, and vision, they unlock the full potential of their organizations. It's important to note that this is not a destination. It is a mindset.

| Flagged | Pattern |
|---|---|
| "In today's fast-paced world" | `in-todays-fast-paced-world` |
| "isn't about authority; it's about influence" | `not-x-but-y-frame` |
| "don't just manage teams, but inspire them" | `not-just-x-but-y-reflex` |
| "empathy, clarity, and vision" | `tricolon-reflex` |
| "leveraging", "unlock the full potential" | `marketing-verb` |
| "It's important to note that" | `its-worth-noting-throat-clearing` |
| "not a destination. It is a mindset." | `negative-positive-restatement` |

### After (illustrative)

<!-- Replace with real /scribe:revise output (business-book persona) and its score before publishing. -->

> Teams follow the manager who listens before deciding. She asks what is blocking the work, says plainly which goal matters this quarter, and then lets people do it.

**18 agents · 31 anti-patterns · 5 writer personas · a different critique subset every run**

## The Problem

AI-generated writing converges on the same cadence. "Delve into the tapestry of." "It's important to note that." "Not just X, but Y." "This is not X. It is Y." Em-dashes everywhere. Three-word lists. Conclusion paragraphs that restate the previous five. Hedging openers.

Scribe combines persona-specific writing rules with critic reviews of those habits.

## Installation

Add the raymondware marketplace, then install Scribe:

```
/plugin marketplace add raymondware/kern
/plugin install scribe@raymondware
```

After you restart Claude Code, the `/scribe:*` commands are available.

## Quick Start

```text
# Generate a passage from scratch
/scribe:write opening chapter for a popular nonfiction book about how cities forget their own histories

# Audit existing prose
/scribe:audit
# (paste the manuscript section to audit)

# De-AI an existing draft
/scribe:differentiate
# (paste the draft)

# Run only the anti-pattern selector (verifies rotation)
/scribe:draw memoir essay about my year in Buenos Aires
```

## Commands

| Command | Does |
|---|---|
| `/scribe:humanize <text or path>` | Edit existing prose for naturalness while preserving voice, facts, and useful structure |
| `/scribe:write <desc>` | Full pipeline: persona detection, specialists, draft, review |
| `/scribe:audit` | Scan existing prose for anti-patterns and give it a sameness score, without rewriting it |
| `/scribe:revise` | Make targeted revisions against Scribe's standards and show before/after scores |
| `/scribe:differentiate` | Identify AI writing tells and apply heavier, structural fixes |
| `/scribe:diagnose` | Run the critics and group AI-ism findings without a score |
| `/scribe:compare [--persona <persona>] [--mode before-after \| vs-exemplar]` | Compare two supplied passages using the same pattern subset and report their sameness scores |
| `/scribe:plan <desc>` | Writing specs only (voice, rhythm, structure), no draft |
| `/scribe:review` | Most thorough audit: every critic, including pacing, and a larger pattern subset |
| `/scribe:research` | Scan writing communities for new anti-patterns and propose them in a pull request |
| `/scribe:draw <desc>` | Run the anti-pattern selector on its own (rotation verification) |

## How It Works

### 1. Persona Detection

Scribe picks a persona from your description, then loads that persona's rules for voice, rhythm, vocabulary, and structure. There are five personas:

| Persona | For |
|---|---|
| `literary-fiction` | Novels, novellas, short stories. Voice and rhythm primary. |
| `popular-nonfiction` | Books that explain ideas to a general audience. Gladwell/Lewis/Pollan register. |
| `technical-writing` | Books, docs, essays for technical readers. Precision over style. |
| `memoir` | First-person life writing. Voice is everything. |
| `business-book` | High AI-default risk. Hardest to make distinctive. |

### 2. Variation Rule

Each pipeline run checks a different subset of anti-patterns. Scribe reads the audit log (`state/draws.jsonl`) and leaves out the previous run's subset, except for three negative-parallelism patterns that are included every time. So two runs on the same prompt are critiqued against different subsets. The focused `/scribe:humanize` skill doesn't use this rotation.

### 3. Parallel Critics + Synthesizer

Rhythm, voice, cliche, and AI-ism critics run in parallel. A pacing critic joins for chapters and essays and always runs for `/scribe:review`. The synthesizer merges their output, removes duplicates, and computes a consensus sameness score.

### 4. The Sameness Score

Scored commands rate prose from 0 to 100 by how closely it resembles AI-default writing. Lower is better:

| Score | Meaning |
|---|---|
| 0-20 | Distinctive. A voice. Ship. |
| 21-40 | Has voice. Some defaults showing. |
| 41-60 | Generic. Could be any AI-generated draft. |
| 61-80 | Default AI prose. Multiple tells per page. |
| 81-100 | Unedited AI output. Do not ship. |

The score is a craft signal, not an AI-authorship detector.

## Anti-Pattern Library

Scribe ships with 31 anti-patterns across three files:

| File | Patterns |
|---|---|
| `anti-patterns/language.md` | Stock AI vocabulary, tricolons, hedge stacking, marketing verbs, em-dash overuse, self-descriptors, universal aphorisms, contrast formulas, filler intensifiers, and throat-clearing |
| `anti-patterns/rhetoric.md` | Generic openers, universalizing claims, false dichotomies, rhetorical questions, pseudo-reveals, repeated twists, and stock closing lines |
| `anti-patterns/structure.md` | Uniform paragraphs, recap openings, repeated conclusions, predictable section sequences, decorative lists, and anecdote montages |

## Agent Team

### Specialists (Haiku)
`rhythm-specialist` `voice-specialist` `vocabulary-specialist` `structure-specialist` `dialogue-specialist`

### Drafting (Sonnet)
`draft-implementer` `voice-implementer`

### Critics (parallel ensemble; Haiku, with `voice-critic` on Opus)
`rhythm-critic` `voice-critic` `cliche-detector` `ai-ism-critic` `pacing-critic`

### Orchestration
`conductor` `critique-synthesizer` (Opus), `anti-pattern-selector` (Sonnet)

### Research and Evaluation (Sonnet)
`research-scout` `external-judge` `cross-persona-audit`

## Contributing

See `CLAUDE.md` for the contributor guide.

## License

MIT. See `LICENSE`.
