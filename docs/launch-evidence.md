# Launch evidence

Scribe is a public Claude Code plugin. Before a release, the repo needs evidence that the plugin package is internally consistent and the anti-pattern draw rule works without the Claude runtime.

## Current automated gate

Run from the repo root:

```bash
python3 tools/validate_plugin.py
```

The validator checks:

- `.claude-plugin/plugin.json` parses and points at `https://github.com/raymondware/scribe`
- `.claude-plugin/marketplace.json` exposes exactly one `scribe` plugin entry aligned with `plugin.json`
- every agent file has `name`, `model`, and `description` frontmatter
- every command file has `description` frontmatter
- every anti-pattern manifest entry has a unique kebab-case id, required metadata, an existing source file, and a matching markdown heading anchor
- the five persona files are present and listed in the persona README
- `tools/draw_simulator.py` can run twice against a temporary audit log and produce different subsets

## CI

`.github/workflows/plugin-validation.yml` runs the same validator on pull requests and pushes to `main`.

## Local smoke transcript

Expected successful output:

```text
Scribe plugin validation passed
```

This is package and deterministic-selector evidence only. It is not a Claude Code marketplace install transcript, release tag, demo recording, paid usage proof, or public launch approval.

## Remaining launch evidence gaps

- Run an actual Claude Code plugin install smoke after Ray approves a release candidate.
- Record a `/scribe:draw` command transcript from a real plugin install.
- Create a release tag only with explicit approval.
- Keep public launch, external posts, marketplace changes, and branch protection changes approval-gated.
