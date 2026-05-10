---
description: "Plan-only mode. Runs persona detection + specialist planning without producing a draft. Returns specs the user can review or hand to a different writer."
allowed-tools: ["Read", "Write", "Edit", "Glob", "Grep", "Bash"]
---

# /scribe:plan

Plan only. No prose, no critique. Returns the specialist specs (rhythm, voice, vocabulary, structure, optionally dialogue) that would constrain a draft.

Useful when:
- You want to write the draft yourself but want scribe's plan as a constraint
- You want to see what scribe would constrain before committing to a full run
- You're a ghostwriter handing the plan to another writer
- You're an editor who wants to see the plan before approving the draft brief

## Usage

```
/scribe:plan <description>
```

## Pipeline

1. **DRAW**: anti-pattern-selector picks subset.
2. **PLAN**: persona detection → rhythm-specialist + voice-specialist + vocabulary-specialist (parallel) → structure-specialist → optional dialogue-specialist.
3. **PRESENT**: audit header + persona detection result + all specialist specs.

No draft. No critique. No synthesis. Stops at the end of PLAN phase.

## Output

```markdown
## /scribe:plan Output

[audit_header]

### Persona Detection
- Persona: popular-nonfiction
- Confidence: 0.9
- Runner-up: business-book

### Rhythm Spec
[from rhythm-specialist]

### Voice Spec
[from voice-specialist]

### Vocabulary Spec
[from vocabulary-specialist]

### Structure Skeleton
[from structure-specialist]

### Dialogue Spec (if applicable)
[from dialogue-specialist]
```

## Notes

- After running `/scribe:plan`, you can hand the specs to your own draft (just write following the specs). Or run `/scribe:write` with the same brief — the conductor will recompute the plan.
- The persona detection in `/scribe:plan` does NOT escalate on low confidence (subagent mode). The specs include a confidence note when persona is ambiguous.
