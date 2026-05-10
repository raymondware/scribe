# Pipeline State Machine

The conductor agent manages the scribe writing pipeline. This document defines the state transitions, parallel execution groups, and termination conditions.

## States

```
INIT -> DRAW -> PLAN -> INTERVIEW -> DRAFT -> REVIEW -> PRESENT
                  ^                            |
                  |                            v
                  +-------- REWORK ------------+
```

DRAW always runs first. The selected_subset is locked once the audit log line is written. Rework operates within the original draw.

## Phase 0: DRAW

**Purpose**: Pick a varied anti-pattern subset for this run and write the audit log. This is the rotation rule that keeps two distinct manuscripts from producing identical critiques.

**Sequence**:

1. Generate `run_id` (timestamp + 4 hex chars).
2. Spawn `anti-pattern-selector` with: command, brief, persona (or "unknown"), surface, audience, voice_signature.
3. Selector reads `${CLAUDE_PLUGIN_ROOT}/anti-patterns/manifest.json` and the last 5 lines of `${CLAUDE_PLUGIN_ROOT}/state/draws.jsonl`.
4. Selector picks subset (12-14 patterns), appends one JSON line to `state/draws.jsonl`, returns audit_header + subset.
5. Conductor verifies the append happened (last line of draws.jsonl matches the selector's output).

**Artifacts produced**:
- `audit_header`: markdown block printed at top of every output
- `selected_subset`: list of anti-pattern IDs threaded through every downstream agent
- One appended line in `state/draws.jsonl`

**Gate to PLAN**: Audit log line written and verified. Selector returned a non-empty subset spanning at least 2 of the 3 base files. If either fails, abort the run with a hard error.

## Phase 1: PLAN

**Purpose**: Detect persona, build specialist specs that constrain the draft.

**Sequence**:

1. Detect persona from the brief. If confidence < 0.7 (interactive mode), ask the user. If subagent mode, proceed with detected persona and flag.
2. Spawn the planning specialists in parallel:
   - `rhythm-specialist`
   - `voice-specialist`
   - `vocabulary-specialist`
3. After parallel specialists return, spawn `structure-specialist` with all three outputs as input.
4. If the surface includes dialogue (chapter, essay with dialogue, or explicit `dialogue` surface), spawn `dialogue-specialist` after structure-specialist.

**Gate to INTERVIEW**: All required specialists returned non-empty specs.

## Phase 2: INTERVIEW (conditional)

**Purpose**: Fill gaps in the brief that would lead to vague prose.

**Trigger**: Specialist specs flag missing inputs (no specific scene named for an opening; no specific person named for popular-nonfiction; no specific year for a chapter that needs grounding).

**Sequence**:

1. Conductor spawns up to 3 targeted questions to the user.
2. Wait for response.
3. Update specialist specs with the new inputs.

In subagent mode, INTERVIEW is skipped entirely — the conductor proceeds with whatever the brief provided and the specs accept gaps.

## Phase 3: DRAFT

**Purpose**: Produce the prose.

**Sequence**:

1. Spawn `draft-implementer` with all specialist specs + persona file + selected_subset. Returns first draft.
2. Spawn `voice-implementer` with the first draft + selected_subset + persona file. Returns revised draft.

**Gate to REVIEW**: Voice-implementer returned a non-empty draft within ±10% of the structure-specialist's target word count.

## Phase 4: REVIEW

**Purpose**: Score the draft against the assigned subset.

**Sequence**:

1. Spawn the critic ensemble in parallel:
   - `rhythm-critic`
   - `voice-critic`
   - `cliche-detector`
   - `ai-ism-critic`
   - `pacing-critic` (only if surface is chapter or essay; for `/scribe:review`, runs always)
2. Each critic returns a 0-25 score and findings.
3. After all critics return, spawn `critique-synthesizer` with all critic outputs.
4. Synthesizer returns 0-100 Sameness Score, deduped findings, rework routing.

**Gate to PRESENT**: Sameness Score below gate threshold (40 for `/scribe:write`, 60 for `/scribe:audit`).

**Gate to REWORK**: Sameness Score at or above gate.

## Phase 5: REWORK (conditional)

**Purpose**: Targeted re-draft based on synthesizer findings.

**Sequence**:

1. Synthesizer routes findings to the relevant specialists (vocabulary, voice, structure, voice-implementer).
2. Conductor re-runs only the affected specialists with their specs updated by the findings.
3. Re-run draft-implementer (or voice-implementer alone if the issue is voice/vocabulary, not structure).
4. Re-run only the relevant critics (the ones whose dimension scored above 12).
5. Synthesizer re-computes Sameness Score.

**Gate to PRESENT**: Score below gate.

**Cycle limit**: 2 rework cycles maximum. After 2 cycles still above gate, escalate to user with the recommendation: "Score is stuck above gate. Persona pick may be wrong. Consider switching to runner-up persona [Y]."

**Monotonic rule**: Each rework cycle's score MUST be lower than the previous cycle's. If it is not (score stagnates or increases), abort and escalate.

## Phase 6: PRESENT

**Purpose**: Output to user.

**Sequence**:

1. Print `audit_header` from anti-pattern-selector at the top of output.
2. Print synthesizer report (Sameness Score, breakdown, findings).
3. Print the final prose.

## State Diagram (textual)

```
INIT
 │
 v
DRAW ──> [audit log written?]
 │            │
 │ yes        │ no
 │            v
 │         ABORT
 v
PLAN ──> [all specialists returned?]
 │            │
 │ yes        │ no
 │            v
 │         ABORT
 v
INTERVIEW (conditional, skip if subagent or no gaps)
 │
 v
DRAFT ──> [draft non-empty?]
 │            │
 │ yes        │ no
 │            v
 │         ABORT
 v
REVIEW ──> [score < gate?]
 │            │
 │ yes        │ no
 │            v
 │         REWORK ──> [cycles < 2 AND score decreasing?]
 │            │           │
 │            │           │ yes
 │            │           v
 │            │        DRAFT (re-enter)
 │            │           │
 │            │ no        │
 │            v           │
 │         ESCALATE       │
 v                        │
PRESENT <─────────────────┘
```
