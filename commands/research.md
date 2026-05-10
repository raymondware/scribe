---
description: "Trigger the research-scout agent to mine writing communities for emerging AI-default patterns. Files dated patterns to anti-patterns/sourced-from-research/. Opens PRs only — never pushes to main."
allowed-tools: ["Read", "Write", "Edit", "Glob", "Grep", "Bash", "WebFetch", "WebSearch"]
---

# /scribe:research

Mine the public web for new AI-default writing patterns. Each new pattern requires 2+ independent sources.

## Usage

```
/scribe:research [--platform <platform>] [--since <date>]
```

`--platform` (optional): focus on one source. Choices: reddit, hn, x, substack, goodreads, all (default).
`--since` (optional): ISO date. Only consider posts after this date.

## What Happens

1. The `research-scout` agent searches the configured sources for editor / writer / reader complaints about AI-default writing.
2. Candidates are deduplicated against the existing manifest.
3. Each new candidate must have 2+ independent sources and at least one direct quote.
4. The scout files dated markdown files to `${CLAUDE_PLUGIN_ROOT}/anti-patterns/sourced-from-research/YYYY-MM-DD-pattern-slug.md`.
5. The scout indexes each new pattern in `manifest.json`.
6. The scout opens a PR titled "research: add [pattern title] from [platforms] community signals" — does NOT push to main.

## Configuration

Source list and search scopes live at `${CLAUDE_PLUGIN_ROOT}/research/sources.json`. Edit that file to add platforms, change search radii, etc.

History of past research runs lives at `${CLAUDE_PLUGIN_ROOT}/research/findings.jsonl`.

## What This Command Does NOT Do

- Generate anti-patterns from the model's intuition. Sources are required.
- Push directly to main. Always opens PRs.
- Update existing patterns silently — additions to existing pattern citations are also PR-only.

## Notes

- Run weekly via cron (when integrated). Each run typically yields 0-3 new patterns; manuscripts of "new AI-isms" stabilize over time as model defaults stabilize.
- Old patterns can become stale (a model update changes defaults). The research scout flags candidates for retirement when the original sources are withdrawn or contradicted.
