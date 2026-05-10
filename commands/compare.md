---
description: "Compare two prose passages for sameness. Useful for before/after editing comparisons, or for comparing a draft against a known-good exemplar."
allowed-tools: ["Read", "Glob", "Grep"]
---

# /scribe:compare

Compare two passages. Returns side-by-side Sameness Scores plus a divergence analysis.

## Usage

```
/scribe:compare [--persona <persona>] [--mode before-after | vs-exemplar]
```

Provide two passages: passage A and passage B.

Modes:
- `before-after` (default): A is the original, B is the revised version. Output: Δ score (lower is better) + which AI-tells were resolved + which remain.
- `vs-exemplar`: A is the user's draft, B is an exemplar passage. Output: structural diff in rhythm, voice, vocabulary; specific deltas the user would need to close to match the exemplar.

## Pipeline

1. **DRAW**: anti-pattern-selector picks subset (one draw covers both passages — same subset for fair comparison).
2. **AUDIT EACH**: critic ensemble runs against passage A, then passage B. Each critic scores both.
3. **DIVERGE**: synthesizer computes per-passage Sameness Scores and identifies which findings are unique to A vs B vs both.
4. **PRESENT**: audit header + side-by-side comparison.

## Output (before-after mode)

```markdown
## /scribe:compare — Before/After

[audit_header]

### Sameness Score
- Passage A (before): 67 / 100
- Passage B (after): 28 / 100
- Δ: -39 (improvement)

### Resolved (issues in A, fixed in B)
- delve-tapestry-realm
- em-dash-overuse
- chapter-end-summary

### Remaining (still flagged in B)
- universal-aphorism (paragraph 7)

### Newly Introduced (only in B)
- [none]

### Verdict
B is significantly more distinctive than A. The remaining aphorism is the next high-value edit.
```

## Output (vs-exemplar mode)

```markdown
## /scribe:compare — vs Exemplar

[audit_header]

### Sameness Score
- Passage A (your draft): 51 / 100
- Passage B (exemplar): 12 / 100

### Rhythm Comparison
- Mean wd/sentence: A = 17.2, B = 14.8
- Std dev: A = 4.1, B = 9.3 ← exemplar has much higher variance
- Single-sentence paragraphs: A = 0, B = 4 per page

### Vocabulary Comparison
- Lexical canaries in A: [list]; in B: [none]
- Specific proper nouns per 200 words: A = 1, B = 4

### Structural Comparison
- Opening type: A = framing, B = scene
- Thesis location: A = paragraph 1, B = paragraph 3
- Closing type: A = recap, B = single concrete image

### Specific Deltas to Close
- Vary sentence-length more aggressively (target std dev: 9+)
- Open with a scene; bury the thesis to paragraph 3
- Cut: lexical canaries, em-dash overuse
- Add: proper nouns, specific numbers, named scenes
```

## Notes

- For comparing across personas, results may be misleading because the rhythm/voice rules differ. Stick to within-persona comparisons for fair scores.
- The exemplar passage in vs-exemplar mode should be from a published author the user trusts. Quotes from the persona file's "Exemplars" section are good starting points.
