---
description: "Diagnose-only mode. Reads prose and identifies AI-default tells without producing a Sameness Score. Returns categorized findings. Useful for understanding why a passage feels off."
allowed-tools: ["Read", "Glob", "Grep"]
---

# /scribe:diagnose

Read-only diagnostic. Does NOT compute a Sameness Score. Returns categorized findings the user can act on.

Useful when:
- A passage feels off but you cannot articulate why
- You're learning to recognize AI-default patterns and want examples from your own prose
- You want a finding list without the verdict pressure

## Usage

```
/scribe:diagnose [--persona <persona>]
```

Paste prose to diagnose.

## Pipeline

1. **DRAW**: anti-pattern-selector picks subset.
2. **DIAGNOSE**: critic ensemble runs in parallel. Each critic returns findings WITH NO SCORE.
3. **CATEGORIZE**: synthesizer groups findings by class (lexical, structural, voice, rhythm, rhetoric) without computing a 0-100 score.
4. **PRESENT**: audit header + categorized findings.

## Output Format

```markdown
## /scribe:diagnose Output

[audit_header]

### Lexical Tells

| Pattern | Where | Example |
|---|---|---|
| delve-tapestry-realm | paragraph 3 | "delves into the rich tapestry of..." |
| ... | ... | ... |

### Rhythm Tells

| Pattern | Where | Measurement |
|---|---|---|
| Uniform paragraph length | whole passage | std dev = 0.8 (target ≥ 2.0) |

### Voice Tells

| Pattern | Where | Example |
|---|---|---|
| Self-descriptor | paragraph 1 | "this powerful framework" |

### Structural Tells

| Pattern | Where | Example |
|---|---|---|
| Chapter-end summary | last paragraph | "In this chapter we have explored..." |

### Rhetorical Tells

| Pattern | Where | Example |
|---|---|---|
| Universal aphorism | paragraph 9 | "Sometimes the longest path is the shortest." |

### Suggestions for Action

If you want to fix these, run:
- `/scribe:revise` for surgical fixes (preserves meaning)
- `/scribe:differentiate` for structural overhaul (allows cuts)
- `/scribe:write` to start over from a brief
```

## Notes

- This is the lowest-friction command. It doesn't pressure you to act on findings.
- Useful for editors triaging a manuscript before deciding how to proceed.
- Can be run on the same passage multiple times — the rotation system varies which patterns are checked.
