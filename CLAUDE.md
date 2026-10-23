# Scribe Plugin - Contributor Guide

## What This Is

Scribe is a Claude Code plugin that orchestrates specialist agents to produce high-quality longform writing. It catches AI-default writing patterns before they ship.

## Structure

```
scribe/
├── .claude-plugin/     # Plugin manifest (plugin.json, marketplace.json)
├── agents/             # Flat directory, auto-discovered by Claude Code
├── commands/           # /scribe:* slash commands
├── skills/scribe/      # SKILL.md + reference files
├── anti-patterns/      # Base + research-sourced AI-ism library
├── state/              # Append-only audit log (state/draws.jsonl)
└── tools/              # Draw simulator and validators
```

## Conventions

- All internal paths use `${CLAUDE_PLUGIN_ROOT}/` prefix
- Agents are flat in `agents/` (no subdirectories - breaks auto-discovery)
- Anti-patterns at repo root (not nested in skills/) because many agents read them
- Specialists use Haiku (fast, cheap, constrained output)
- Implementation agents use Sonnet (code generation)
- Conductor, voice-critic, and critique-synthesizer use Opus (complex judgment, synthesis)
- Conductor never writes or critiques - only coordinates

## Adding a New Agent

1. Create `agents/your-agent.md` with YAML frontmatter (name, model, description). Set `model` to a tier alias (`haiku`, `sonnet`, `opus`), never a pinned model ID
2. Reference files using `${CLAUDE_PLUGIN_ROOT}/path/to/file`
3. Define clear inputs, outputs, and constraints
4. If the agent participates in the pipeline, update `skills/scribe/references/orchestration/pipeline.md`

## Adding a New Anti-Pattern

Community-sourced patterns go in `anti-patterns/sourced-from-research/` via the research-scout agent. Base patterns in `anti-patterns/language.md`, `structure.md`, or `rhetoric.md` are manually curated.

Each new pattern needs a manifest.json entry with id, categories, severity_default, source_file, anchor, personas, site_signals.

## Adding a New Persona

Create a file in `skills/scribe/references/personas/` following the existing format. Update `skills/scribe/references/personas/README.md` and `skills/scribe/SKILL.md`.

## Code Style

- No em-dashes in any content (this rule applies recursively - scribe must not exemplify what it flags)
- Writer-to-writer voice: specific, direct, no marketing register
- Conventional commits (feat:, fix:, docs:)
- Keep agent prompts under 100 lines unless the role genuinely requires more