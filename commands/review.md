---
description: "Review existing prose with the full critic ensemble. Same as /scribe:audit but always runs ALL critics including pacing-critic, even for non-chapter surfaces. Use when you want the most thorough audit."
allowed-tools: ["Read", "Glob", "Grep"]
---

# /scribe:review

Maximum-coverage audit. Runs ALL critics regardless of surface. Use when you want a thorough verdict on a finished manuscript section.

## Usage

```
/scribe:review [--persona <persona>]
```

## Pipeline

Same as `/scribe:audit` except:
- pacing-critic runs even for short or non-chapter surfaces
- A larger anti-pattern subset (16-18 instead of 12-14)
- Synthesizer reports findings at low + moderate severities too (audit usually filters those out)

## When to Use

- Final pass before a manuscript ships to a publisher or agent
- After multiple `/scribe:revise` cycles, when you need to be sure nothing has crept back
- Auditing a colleague's draft you're going to ghost-edit
- Compiling an editing report for a client

## Output

Same format as `/scribe:audit`, but more verbose. Includes low/moderate findings as a separate section.

## Notes

- This is the most expensive command (most critics, biggest subset). Don't run it on every draft — use `/scribe:audit` for routine passes.
- For a quick sanity check, use `/scribe:diagnose` (no score, just findings).
