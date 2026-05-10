# State

## draws.jsonl

Append-only audit log. Every scribe run that involves an anti-pattern selector appends one JSONL record before any other agent runs. The line is also printed at the top of every scribe output.

Schema (per line):

```json
{
  "run_id": "scribe-YYYYMMDD-HHMMSS-XXXX",
  "ts": "ISO-8601",
  "command": "write|audit|revise|differentiate|diagnose|research|draw|plan|review",
  "selector_version": "1.0.0",
  "manifest_version": "0.1.0",
  "inputs": {
    "product": "user description string",
    "persona": "literary-fiction|popular-nonfiction|technical-writing|memoir|business-book|unknown",
    "surface": "chapter|essay|blurb|opening|conclusion|dialogue|exposition|any",
    "audience": "free text",
    "voice_signature": "free text optional"
  },
  "subset": ["pattern-id-1", "pattern-id-2", "..."],
  "previous_subset_excluded": true
}
```

## Why append-only

Two distinct manuscripts MUST produce different anti-pattern subsets. The selector reads the most recent draws.jsonl line and excludes that subset from this run. If the file is truncated or rewritten, rotation breaks.

Treat draws.jsonl as immutable. Add new lines. Never edit or delete past lines.
