---
description: "Run only the anti-pattern-selector. Verifies rotation by producing a subset and writing the audit log. Use to test the rotation rule."
allowed-tools: ["Read", "Write", "Bash"]
---

# /scribe:draw

Run only the anti-pattern-selector. No critique, no writing, no synthesis. Just the draw.

## Usage

```
/scribe:draw <description>
```

## When to Use

- Verifying the rotation rule (run `/scribe:draw` with the same brief twice; the second draw must differ from the first)
- Inspecting which patterns the rotation system would apply for a given brief
- Debugging the manifest (does the new pattern you added show up in the right context?)
- Testing the audit-log integrity

## Pipeline

1. anti-pattern-selector reads the manifest, the brief, and the last 5 lines of `state/draws.jsonl`.
2. Computes brief-specific must-include patterns.
3. Picks subset (12-14 patterns, target).
4. Excludes the previous run's subset.
5. Appends a JSON line to `state/draws.jsonl`.
6. Returns the audit_header.

## Output

Just the audit_header. No further pipeline runs.

## Reproducibility Test

```bash
# Run 1
/scribe:draw landing chapter for a memoir about my year in Buenos Aires

# Run 2 (same brief)
/scribe:draw landing chapter for a memoir about my year in Buenos Aires

# Verify
diff <(tail -2 state/draws.jsonl | head -1 | jq -c '.subset' | tr ',' '\n' | sort) \
     <(tail -1 state/draws.jsonl | jq -c '.subset' | tr ',' '\n' | sort)
# Should show non-empty diff (subsets differ)
```

The Python reference implementation `${CLAUDE_PLUGIN_ROOT}/tools/draw_simulator.py` mirrors this command's algorithm for deterministic CI testing.
