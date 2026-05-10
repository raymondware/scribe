---
description: "De-AI an existing draft. Heavy-handed surgical revision targeting tool-specific fingerprints (ChatGPT, Claude, Gemini default cadences). Goes beyond /scribe:revise into structural editing."
allowed-tools: ["Read", "Write", "Edit", "Glob", "Grep"]
---

# /scribe:differentiate

The most aggressive de-AI command. For prose that came directly out of an LLM and needs to be made publishable.

`/scribe:revise` does surgical voice + rhythm tightening within meaning preservation. `/scribe:differentiate` goes further: it will restructure paragraphs, replace thin anecdotes with prompts for thick ones, kill entire passages that are unrescuable, and swap an entire opening for a different opening.

## Usage

```
/scribe:differentiate [--persona <persona>] [--source <tool>]
```

`--source` (optional) tells scribe which tool the prose came from. Each tool has its own fingerprint. If omitted, scribe infers.

Recognized sources:
- `chatgpt` — heavy on "delve," "tapestry," tricolons, conclusion-restating
- `claude` — heavier on hedging, on "of course" / "it's worth noting"
- `gemini` — heavier on bulleted lists in narrative passages, on "Key Takeaways" boxes
- `gpt-4` (older) — em-dash overuse + "And yet" twists at higher density
- `unknown` — apply union of all fingerprints

## What's Different From /scribe:revise

| Action | /scribe:revise | /scribe:differentiate |
|---|---|---|
| Vocabulary substitution | yes | yes |
| Em-dash reduction | yes | yes |
| Cut throat-clearing | yes | yes |
| Tricolon replacement | yes | yes |
| Paragraph splitting/joining | sparingly | yes |
| Paragraph reordering | no | yes |
| Replace anecdote with prompt for new anecdote | no | yes |
| Rewrite chapter opening from scratch | no | yes if opener is unrescuable |
| Cut entire passages | no | yes |
| Word count change | ±10% | ±25% |

## Pipeline

1. **DRAW**: anti-pattern-selector picks subset weighted toward tool-specific fingerprints from the named source.
2. **DIAGNOSE**: critics audit existing prose. Synthesizer flags critical/high findings with paragraph anchors.
3. **STRUCTURAL TRIAGE**: For each critical finding, decide:
   - Surgical revision (most cases)
   - Paragraph-level rewrite (when a paragraph has 3+ critical findings)
   - Cut + replace with prompt for the user (when an anecdote is too thin to rescue, e.g., generic three-anecdote montage)
4. **VOICE-IMPLEMENTER**: applies surgical revisions.
5. **STRUCTURAL EDITOR** (a special mode of voice-implementer): handles paragraph rewrites and cuts. Marks any cut-and-replace gap with `[GAP: please supply a specific anecdote about X]`.
6. **RE-AUDIT**: critic ensemble + synthesizer.
7. **PRESENT**: audit header + before/after Sameness Scores + revised prose with marked gaps.

## Output Format

```markdown
## /scribe:differentiate Output

[audit_header]

### Before/After Sameness Score
- Before: 78 / 100
- After: 31 / 100

### Word Count
- Before: [N]
- After: [N]
- Δ: [-N]%

### Cuts and Marked Gaps

The following passages were cut as unrescuable. Each is marked with a [GAP] tag where you should supply specific content:

- Paragraph 4: "The three-anecdote montage of Sarah, Marcus, and Amelia is generic." [GAP: replace with one thick anecdote — a real named person you have firsthand knowledge of who exemplifies this pattern, with specific year, place, and outcome.]

- Paragraph 9: "Conclusion paragraph restated chapter argument." [Cut entirely. End instead on the paragraph 8 case study. The reader will retain the argument.]

### Revised Prose

[Full revised prose with [GAP] markers in place where structural cuts happened.]
```

## Notes

- `/scribe:differentiate` is meant for AI-generated drafts being prepared for publication. For your own writing that's drifted toward AI-default, use `/scribe:revise` first.
- The `[GAP]` tag is intentional — the writer (not scribe) supplies the specific replacement. Scribe will not invent fictional named persons.
- Output may be 10-25% shorter than input. That is the point.
