---
description: "Full write pipeline: persona detection, anti-pattern rotation, specialist planning, draft, voice revision, parallel critic review, synthesizer."
allowed-tools: ["Read", "Write", "Edit", "Glob", "Grep", "Bash"]
---

# /scribe:write

Full writing workflow for a passage. Persona-aware. AI-ism-resistant from the start. Uses the conductor agent to orchestrate specialists and critics through a 6-phase pipeline.

## Usage

```
/scribe:write <description>
```

The description should include:
- What you're writing (a chapter, an essay, a blurb, an opening, a dialogue scene)
- What it's about (subject matter, named persons or topics)
- Who the reader is (audience hint)
- Any voice signature (e.g., "should read like Joan Didion," "Cormac McCarthy economy")

## Pipeline

Read `${CLAUDE_PLUGIN_ROOT}/skills/scribe/references/orchestration/pipeline.md` for the full state machine.

The conductor agent manages 6 phases:

1. **DRAW**: anti-pattern-selector picks a varied subset for this run, writes the audit log to `state/draws.jsonl`. Every downstream agent receives `selected_subset`.
2. **PLAN**: Detect persona, run rhythm/voice/vocabulary specialists in parallel, then structure-specialist (and dialogue-specialist if surface includes dialogue).
3. **INTERVIEW** (conditional): Ask targeted questions if specs have gaps.
4. **DRAFT**: draft-implementer produces first draft → voice-implementer revises for voice consistency.
5. **REVIEW**: parallel critics (rhythm-critic, voice-critic, cliche-detector, ai-ism-critic, pacing-critic) → critique-synthesizer combines into Sameness Score.
6. **PRESENT**: audit_header + synthesizer report + final prose.

## Sameness Gate

The critique-synthesizer combines per-dimension scores into a 0-100 Sameness Score. For scribe-produced output the gate threshold is **40**. If the score exceeds the threshold, the conductor routes specific issues to the relevant specialist for targeted rework. Max 2 rework cycles. Score must decrease monotonically.

If after 2 rework cycles the score is still above gate, the conductor escalates — that is signal that the persona pick was wrong, not the execution.

## Example

```
/scribe:write opening chapter for a popular nonfiction book about how cities forget their own histories. Should read like Patrick Radden Keefe — scene-driven, named persons, specific dates.
```

Expected behavior:
1. DRAW: selector picks ~14 patterns weighted toward popular-nonfiction + opening signals; appends to state/draws.jsonl.
2. Persona detected: `popular-nonfiction` (confidence 1.0)
3. Voice signature noted: Keefe-style. Voice-specialist references *Empire of Pain* / *Say Nothing* sentence patterns.
4. Specialists produce: rhythm spec (high std dev, single-sentence paragraphs), voice spec (third-person reportage with light first-person where the writer's stake is honest), vocabulary spec (proper nouns, dates, named persons), structure spec (open with scene, bury thesis).
5. Draft-implementer: first prose draft.
6. Voice-implementer: revisions for cadence + AI-ism removal.
7. Critic ensemble runs in parallel: each produces 0-25 score.
8. Synthesizer: consensus 0-100 score (target ≤ 40).
9. Output: audit_header at top, then the synthesizer report, then the chapter prose.

## Notes

- For existing prose, use `/scribe:audit` instead.
- For making an existing draft less AI-looking, use `/scribe:differentiate`.
- For comparing two versions, use `/scribe:compare`.
- The workflow can be interrupted; intermediate artifacts (specialist specs, drafts) are usable independently.
