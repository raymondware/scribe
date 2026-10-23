#!/usr/bin/env python3
"""Validate Scribe plugin packaging and deterministic draw behavior."""

from __future__ import annotations

import json
import importlib.util
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import NoReturn

ROOT = Path(__file__).resolve().parents[1]


def fail(message: str) -> NoReturn:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def read_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # pragma: no cover - diagnostic path
        fail(f"{path.relative_to(ROOT)} is not valid JSON: {exc}")


def slugify_heading(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"[`*_]", "", text)
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    text = re.sub(r"\s+", "-", text)
    text = re.sub(r"-+", "-", text)
    return text.strip("-")


def validate_plugin_manifests() -> None:
    plugin = read_json(ROOT / ".claude-plugin" / "plugin.json")
    marketplace = read_json(ROOT / ".claude-plugin" / "marketplace.json")

    if plugin.get("name") != "scribe":
        fail("plugin.json name must be scribe")
    if plugin.get("version") != "1.0.0":
        fail("plugin.json version must stay aligned with release docs")
    if plugin.get("license") != "MIT":
        fail("plugin.json license must be MIT")
    if plugin.get("repository") != "https://github.com/raymondware/scribe":
        fail("plugin.json repository URL is not the public repo")

    plugins = marketplace.get("plugins")
    if not isinstance(plugins, list) or len(plugins) != 1:
        fail("marketplace.json must expose exactly one plugin")
    entry = plugins[0]
    for key in ["name", "version", "description", "category", "source"]:
        if key not in entry:
            fail(f"marketplace plugin entry missing {key}")
    if entry["name"] != plugin["name"] or entry["version"] != plugin["version"]:
        fail("marketplace plugin name/version must match plugin.json")
    if entry["source"] != "./":
        fail("marketplace plugin source must remain ./ for repo-root plugin install")


def frontmatter(path: Path) -> dict[str, str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0] != "---":
        fail(f"{path.relative_to(ROOT)} missing YAML frontmatter fence")
    end = None
    for i, line in enumerate(lines[1:], start=1):
        if line == "---":
            end = i
            break
    if end is None:
        fail(f"{path.relative_to(ROOT)} missing closing frontmatter fence")
    data: dict[str, str] = {}
    for line in lines[1:end]:
        if not line.strip() or ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip('"')
    return data


def validate_agents_and_commands() -> None:
    agent_dir = ROOT / "agents"
    command_dir = ROOT / "commands"
    agents = sorted(agent_dir.glob("*.md"))
    commands = sorted(command_dir.glob("*.md"))
    if len(agents) < 10:
        fail("expected at least 10 Scribe agents")
    if len(commands) < 8:
        fail("expected at least 8 Scribe commands")

    names: set[str] = set()
    for path in agents:
        fm = frontmatter(path)
        for key in ["name", "model", "description"]:
            if not fm.get(key):
                fail(f"{path.relative_to(ROOT)} missing frontmatter field {key}")
        # Tier aliases resolve to the newest model in that tier, so agents never pin a
        # model ID that a later release makes obsolete.
        if fm["model"] not in {"haiku", "sonnet", "opus", "inherit"}:
            fail(f"{path.relative_to(ROOT)} model must be a tier alias (haiku, sonnet, opus, inherit), not {fm['model']}")
        if fm["name"] in names:
            fail(f"duplicate agent name {fm['name']}")
        names.add(fm["name"])

    for path in commands:
        fm = frontmatter(path)
        if not fm.get("description"):
            fail(f"{path.relative_to(ROOT)} missing command description")


def validate_antipattern_manifest() -> None:
    manifest = read_json(ROOT / "anti-patterns" / "manifest.json")
    patterns = manifest.get("patterns")
    if not isinstance(patterns, list) or len(patterns) < 20:
        fail("anti-pattern manifest must include the public pattern catalog")

    seen: set[str] = set()
    for pattern in patterns:
        for key in ["id", "title", "categories", "severity_default", "source_file", "anchor", "personas", "site_signals"]:
            if key not in pattern:
                fail(f"pattern entry missing {key}: {pattern}")
        pid = pattern["id"]
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", pid):
            fail(f"pattern id is not kebab-case: {pid}")
        if pid in seen:
            fail(f"duplicate pattern id {pid}")
        if not isinstance(pattern.get("always_include", False), bool):
            fail(f"pattern {pid} always_include must be a boolean")
        seen.add(pid)
        source = ROOT / pattern["source_file"]
        if not source.exists():
            fail(f"pattern {pid} source file missing: {pattern['source_file']}")
        headings = []
        for line in source.read_text(encoding="utf-8").splitlines():
            if line.startswith("#"):
                headings.append(slugify_heading(line.lstrip("#")))
        anchor = pattern["anchor"]
        normalized_anchor = re.sub(r"-+", "-", anchor)
        normalized_headings = {re.sub(r"-+", "-", heading) for heading in headings}
        if anchor not in headings and normalized_anchor not in normalized_headings:
            fail(f"pattern {pid} anchor {anchor} not found in {pattern['source_file']}")


def validate_personas() -> None:
    persona_dir = ROOT / "skills" / "scribe" / "references" / "personas"
    expected = {
        "literary-fiction.md",
        "popular-nonfiction.md",
        "technical-writing.md",
        "memoir.md",
        "business-book.md",
    }
    actual = {p.name for p in persona_dir.glob("*.md") if p.name != "README.md"}
    if actual != expected:
        fail(f"persona set mismatch: {sorted(actual)}")
    readme = (persona_dir / "README.md").read_text(encoding="utf-8")
    for filename in sorted(expected):
        persona_id = filename.removesuffix(".md")
        if persona_id not in readme:
            fail(f"personas README does not mention {persona_id}")


def validate_draw_rotation() -> None:
    simulator = ROOT / "tools" / "draw_simulator.py"
    with tempfile.TemporaryDirectory(prefix="scribe-validate-") as tmp:
        state = Path(tmp) / "draws.jsonl"
        base = [
            sys.executable,
            str(simulator),
            "business book chapter on why most pivots fail",
            "--persona",
            "business-book",
            "--command",
            "write",
            "--state-file",
            str(state),
        ]
        first = subprocess.run(base + ["--run-id", "scribe-ci-20260725-0001"], cwd=ROOT, text=True, capture_output=True)
        if first.returncode != 0:
            fail(f"first draw simulator run failed: {first.stderr or first.stdout}")
        second = subprocess.run(base + ["--run-id", "scribe-ci-20260725-0002"], cwd=ROOT, text=True, capture_output=True)
        if second.returncode != 0:
            fail(f"second draw simulator run failed: {second.stderr or second.stdout}")
        lines = [json.loads(line) for line in state.read_text(encoding="utf-8").splitlines() if line.strip()]
        if len(lines) != 2:
            fail("draw simulator should append exactly two audit lines")
        if set(lines[0]["subset"]) == set(lines[1]["subset"]):
            fail("draw simulator reused the same subset twice")
        if not 8 <= lines[0]["subset_size"] <= 14 or not 8 <= lines[1]["subset_size"] <= 14:
            fail("draw simulator subset size outside expected range")
        manifest = read_json(ROOT / "anti-patterns" / "manifest.json")
        always_on = {p["id"] for p in manifest["patterns"] if p.get("always_include")}
        for line in lines:
            missing = always_on - set(line["subset"])
            if missing:
                fail(f"draw {line['run_id']} dropped always_include patterns: {sorted(missing)}")


def validate_negative_positive_detector() -> None:
    module_path = ROOT / "tools" / "prose_fingerprints.py"
    spec = importlib.util.spec_from_file_location("prose_fingerprints", module_path)
    if spec is None or spec.loader is None:
        fail("could not load prose_fingerprints detector")
    module = importlib.util.module_from_spec(spec)
    sys.modules["prose_fingerprints"] = module
    spec.loader.exec_module(module)

    positive_cases = [
        "This is not a productivity trick. It is a new operating model for teams.",
        "The goal is not about replacing judgment. The goal is about putting judgment in the right place.",
        "It is not just a checklist, but a complete operating model.",
        "It's not about speed, it's about impact.",
        "Leadership isn't about authority; it's about influence.",
        "We don't need more speed. We need impact.",
    ]
    for case in positive_cases:
        findings = module.detect_negative_positive_restatement(case)
        if not findings:
            fail(f"negative/positive detector missed: {case}")

    negative_case = "The job did not finish because the database was unavailable. The retry queue preserved the failed work item."
    if module.detect_negative_positive_restatement(negative_case):
        fail("negative/positive detector flagged a specific non-restatement failure sentence")


def main() -> int:
    validate_plugin_manifests()
    validate_agents_and_commands()
    validate_antipattern_manifest()
    validate_personas()
    validate_draw_rotation()
    validate_negative_positive_detector()
    print("Scribe plugin validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
