---
description: "Revise existing prose for voice consistency, rhythm precision, and AI-ism removal. Surgical edits only — does not rewrite from scratch."
allowed-tools: ["Read", "Write", "Edit", "Glob", "Grep"]
---

# /scribe:revise

Revise existing prose for voice consistency, rhythm precision, and AI-ism removal. Targeted edits only — content meaning is preserved; the writer-DNA fingerprint is what changes.

## Usage

```
/scribe:revise [--persona <persona>]
```

Paste in the prose to revise.

## Pipeline

This is a slimmer pipeline than `/scribe:write`. Skips DRAFT (the prose already exists). Skips initial PLAN specialists (the existing prose is the constraint).

1. **DRAW**: anti-pattern-selector picks subset.
2. **AUDIT**: critic ensemble runs against the existing prose (rhythm-critic, voice-critic, cliche-detector, ai-ism-critic).
3. **REVISE**: voice-implementer takes the critique-synthesizer's findings and applies surgical revisions. Does NOT rewrite paragraphs from scratch unless a paragraph is unrescuable.
4. **RE-AUDIT**: critic ensemble re-runs on the revised prose. Synthesizer produces before-and-after scores.
5. **PRESENT**: audit header + before/after comparison + revised prose.

## What "Surgical" Means

- Replace banned vocabulary with concrete alternatives (delve → examine; tapestry → name the actual things).
- Cut throat-clearing phrases ("It's worth noting that," "It's important to understand").
- Reduce em-dash density to budget by replacing half with periods, half with commas.
- Break uniform paragraph runs by splitting one too-long paragraph at its strongest internal turn.
- Replace tricolons with two-item or four-item lists.
- Cut rhetorical questions whose answer is in the next paragraph.
- Vary sentence-length distribution by intentionally shortening or extending one sentence per affected stretch.

## What `/scribe:revise` Does NOT Do

- Reorder paragraphs or sections.
- Add new claims, examples, or named persons.
- Change tense or POV.
- Change the meaning of any sentence.
- Lengthen the passage by more than 10% or shorten by more than 10%.

If the prose needs structural surgery (paragraph reordering, replacing a thin anecdote with a thick one, re-pacing the chapter), use `/scribe:differentiate` instead.

## Output

```markdown
## /scribe:revise Output

[audit_header from anti-pattern-selector]

### Before/After Sameness Score
- Before: 67 / 100
- After: 28 / 100

### Revised Prose

[the prose, edited inline]

### Edit Summary

[Optional, if requested. Bullet list of edit categories: vocabulary substitutions, em-dash reductions, paragraph splits, etc.]
```

## Notes

- For full rewriting, use `/scribe:write` from scratch.
- For deeper structural overhauls, use `/scribe:differentiate`.
- For just an audit without changes, use `/scribe:audit`.
