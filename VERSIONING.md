# Versioning

Scribe follows semantic versioning.

## Current

v1.1.1 - Refines humanize and voice revision to unpack compressed prose and check reader understanding while preserving meaning and genre.

v1.1.0 - Adds the focused `/scribe:humanize` skill, original editing examples, and skill packaging validation. Existing pipeline commands keep their behavior.

v1.0.0 -- Initial public release. 5 personas, anti-pattern library, conductor + 11 agents wired.

## Bump rules

**Major (X.0.0)** -- Breaking change to:
- `manifest.json` schema (renamed fields, removed required keys)
- Agent invocation contract (new required input/output fields)
- Persona file structure (a critic stops being able to parse a persona)
- The 5-persona set itself (adding a 6th, removing one, renaming any)

**Minor (0.X.0)** -- New capability:
- New agent
- New command
- Persona file expansion that changes critic behavior
- New anti-pattern category in manifest
- Significant rewrites of any persona file

**Patch (0.0.X)** -- Refinement:
- New anti-pattern indexed without changing categories
- Tightening or clarifying agent prompts
- Documentation
- Bug fixes in tools

## Anti-pattern manifest version

The `manifest.json` has its own `version` field for the pattern catalog itself. It bumps independently:
- Major: schema change
- Minor: new patterns added or recategorized
- Patch: edited descriptions or anchor fixes
