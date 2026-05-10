---
description: "Full anti-pattern scan with Sameness Score. Persona-aware. Audits prose without rewriting it."
allowed-tools: ["Read", "Glob", "Grep"]
---

# /scribe:audit

Full anti-pattern scan of existing prose. Severity-bucketed output. Persona-aware. Computes a 0-100 Sameness Score from 4-5 parallel critics.

## When to Use

Run `/scribe:audit` when:
- Reviewing AI-generated drafts before integrating them
- Editing your own writing and want a fresh second opinion on AI-default tells
- Before submitting a manuscript to an agent or publisher
- Auditing ghostwritten content for an author who needs to maintain a recognizable voice
- After a fast generation pass that prioritized output over craft

## How to Run

```
/scribe:audit [--persona <persona>]
```

Paste the manuscript section to audit after the command. Accepted inputs:
- A chapter (any length)
- An essay
- A book blurb
- A dialogue scene
- Marketing copy that was supposed to read as longform

Persona flag is optional. If omitted, scribe infers the persona from the input. If inference is ambiguous, scribe asks.

Valid personas: `literary-fiction`, `popular-nonfiction`, `technical-writing`, `memoir`, `business-book`

## What Scribe Does

1. **DRAW**: Spawns the `anti-pattern-selector`. The selector reads `${CLAUDE_PLUGIN_ROOT}/anti-patterns/manifest.json` and rotation history at `${CLAUDE_PLUGIN_ROOT}/state/draws.jsonl`. Picks varied subset weighted by brief signals. Appends draw to audit log.
2. **REVIEW** (parallel ensemble): Spawns rhythm-critic, voice-critic, cliche-detector, ai-ism-critic, and pacing-critic (if surface is chapter or essay) in parallel. Each reads only the subset slice assigned. Each returns 0-25 score and specific findings.
3. **SYNTHESIZE**: Spawns critique-synthesizer. Deduplicates across critics, computes consensus Sameness Score, emits the final report.
4. **PRESENT**: audit_header at top, then synthesizer report.

External `/scribe:audit` runs use a gate threshold of **60** (vs **40** for scribe-produced output). The synthesizer applies the threshold based on the command.

## Output Format

Audit header (from anti-pattern-selector) followed by the synthesizer report. See `${CLAUDE_PLUGIN_ROOT}/agents/critique-synthesizer.md` for the format.

## Sameness Score Thresholds

**0-20**: Distinctive. Has voice. Ready to ship.
**21-40**: Has voice; some defaults showing but not dominant.
**41-60**: Generic. Could be any AI draft. Moderate fixes required.
**61-80**: Default AI prose. Multiple tells per page. Run `/scribe:differentiate` before continuing.
**81-100**: Unedited AI output. Significant rewrite required.

## Notes

- Scribe does NOT rewrite the prose. For revision, use `/scribe:revise` or `/scribe:differentiate`.
- Scribe does NOT do grammar correction. Run a copy editor first.
- Scribe does NOT detect plagiarism or classify AI authorship — Sameness Score is a craft signal, not a forensic one.
