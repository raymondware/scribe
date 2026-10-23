# Quality Gates

The conductor enforces these gates between phases. Failing a gate either aborts the run, escalates to the user, or routes to REWORK.

## DRAW → PLAN gate

**Pass condition (all required)**:
- Selector wrote one new line to `state/draws.jsonl`
- The new line's `subset` array is non-empty
- The subset contains at least 2 patterns of severity `critical` (`delve-tapestry-realm`, `uniform-paragraph-length`, `chapter-end-summary`, `in-todays-fast-paced-world`, `conclusion-restating-conclusion`)
- The subset spans at least 2 of the 3 base source files (`language.md`, `structure.md`, `rhetoric.md`)
- The subset does NOT match the previous run's subset
- The subset contains every manifest pattern with `"always_include": true`

**Fail action**: ABORT. The audit-log discipline is non-negotiable.

## PLAN → INTERVIEW gate

**Pass condition**:
- All required specialists returned non-empty specs
- Persona is resolved (either by detection or by user confirmation)
- Specialist specs are mutually consistent (e.g., voice-spec's tense matches structure-skeleton's opening tense)

**Fail action**: ABORT, surface to user.

## INTERVIEW → DRAFT gate

**Pass condition**:
- Either INTERVIEW was skipped (subagent mode), or
- All targeted questions were answered, or
- Conductor explicitly accepted the gaps and noted them in the run record

**Fail action**: Loop back into INTERVIEW with one more question. Maximum 3 questions per run.

## DRAFT → REVIEW gate

**Pass condition**:
- voice-implementer returned a draft within ±10% of structure-specialist's target word count
- Draft contains no banned vocabulary (the persona's banned list — sanity check; the specialists should have caught this)
- Draft does not start with any forbidden opener from the persona file

**Fail action**: Re-run voice-implementer with explicit findings. If second attempt fails the same way, escalate.

## REVIEW → PRESENT gate

**Pass condition (for `/scribe:write`)**:
- Synthesized Sameness Score < 40
- No critical-severity finding remains unaddressed

**Pass condition (for `/scribe:audit`)**:
- Score is reported as-is; PRESENT runs regardless because audit is read-only

**Fail action**: Route to REWORK.

## REWORK gate

**Pass condition (continuing rework)**:
- Cycle count < 2
- Previous cycle's score is higher than the projected re-draft's score (monotonic improvement)

**Fail action**: Escalate. Recommend persona reconsideration.

## Score Floors and Ceilings

These constraints prevent gaming or runaway:

- A critic CANNOT return a score below 0 or above 25.
- The synthesizer CANNOT return a score below the maximum critic score (i.e., if any critic returns 24, synthesized score is at least 24/100).
- The synthesizer CANNOT return a score that conflicts with the critic findings — every critical-severity finding must contribute at least +5 to the score.
- The synthesizer CANNOT lower a score after a rework cycle if the same finding is still present.

## Escalation Behavior

When the conductor escalates:

1. Halt the pipeline.
2. Output the latest audit_header and synthesizer report.
3. Show the user the rework history (cycle 1 score, cycle 2 score).
4. Show the current draft (whatever the latest voice-implementer output was).
5. Recommend: "Score stuck at [N] / 100. Try one of: (a) switch to runner-up persona [Y], (b) provide a more specific voice signature, (c) abandon this brief and start over."

## Hard Aborts

Some failures are not recoverable mid-run:

- DRAW append failed: ABORT
- Selector returned an empty or single-source-file subset: ABORT
- Specialist returned empty spec: ABORT (after one retry)
- Voice-implementer produced output 50%+ different in word count: ABORT (the model is not following instructions)
- Synthesizer score increased after rework: ABORT (rework is making things worse)

ABORT means: print whatever was produced, log the failure to the synthesizer report, do NOT recommend retrying without the user changing inputs.
