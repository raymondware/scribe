#!/usr/bin/env python3
"""
Reference implementation of the scribe anti-pattern-selector algorithm.

The actual selector is a Claude Code agent at agents/anti-pattern-selector.md.
This simulator mirrors that algorithm in pure Python so the rotation rule and
audit-log behavior can be verified deterministically without the agent runtime.

Usage:
    python tools/draw_simulator.py "<passage description>" \\
        [--persona PERSONA] [--genre GENRE] [--audience AUDIENCE] \\
        [--command write] [--state-file PATH]

The simulator reads anti-patterns/manifest.json and the last 5 lines of the
state file (default: state/draws.jsonl). It computes a subset following the
same rules the agent follows, then appends one audit line to the state file
and prints the audit_header markdown to stdout.

Run it twice in a row with the same inputs and confirm the second subset
differs from the first. That is the rotation rule.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import random
import secrets
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

SELECTOR_VERSION = "1.0.0"
REPO_ROOT = Path(__file__).resolve().parent.parent
MANIFEST_PATH = REPO_ROOT / "anti-patterns" / "manifest.json"
DEFAULT_STATE_PATH = REPO_ROOT / "state" / "draws.jsonl"

SIGNAL_PATTERN_IDS = {
    "tricolon-reflex",
    "hedge-stacking",
    "marketing-verb",
    "em-dash-connector",
    "self-descriptor",
    "negative-positive-restatement",
}

CATEGORY_DIVERSITY_MIN = (
    "language",
    "rhythm",
    "structure",
    "rhetoric",
    "voice",
    "dialogue",
    "pacing",
)


@dataclass
class Pattern:
    id: str
    title: str
    categories: list[str]
    tags: list[str]
    severity_default: str
    source_file: str
    anchor: str
    personas: list[str]
    site_signals: list[str]
    always_include: bool = False


@dataclass
class Inputs:
    command: str
    passage: str
    persona: str
    genre: str | None
    audience: str | None


@dataclass
class Draw:
    ts: str
    run_id: str
    command: str
    selector_version: str
    input_signal: dict
    pool_size: int
    subset_size: int
    subset: list[str]
    site_specific_inclusions: list[str]
    rotation_excluded: list[str]
    previous_subsets_consulted: int
    rationale: str


def load_manifest(path: Path = MANIFEST_PATH) -> list[Pattern]:
    data = json.loads(path.read_text())
    return [
        Pattern(
            id=p["id"],
            title=p["title"],
            categories=p["categories"],
            tags=p.get("tags", []),
            severity_default=p["severity_default"],
            source_file=p["source_file"],
            anchor=p["anchor"],
            personas=p["personas"],
            site_signals=p["site_signals"],
            always_include=p.get("always_include", False),
        )
        for p in data["patterns"]
    ]


def load_history(path: Path, n: int = 5) -> list[dict]:
    if not path.exists():
        return []
    lines = [ln for ln in path.read_text().splitlines() if ln.strip()]
    return [json.loads(ln) for ln in lines[-n:]]


def derive_run_id() -> str:
    now = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%d-%H%M%S")
    return f"scribe-{now}-{secrets.token_hex(2)}"


def detect_signals(inputs: Inputs) -> Inputs:
    text = inputs.passage.lower()
    persona = inputs.persona
    genre = inputs.genre

    if persona == "unknown":
        if any(k in text for k in ["novel", "fiction", "short story", "character"]):
            persona = "literary-fiction"
        elif any(k in text for k in ["memoir", "personal", "first person", "my life"]):
            persona = "memoir"
        elif any(k in text for k in ["technical", "documentation", "code", "api"]):
            persona = "technical-writing"
        elif any(k in text for k in ["business", "leadership", "management", "strategy"]):
            persona = "business-book"
        else:
            persona = "popular-nonfiction"

    if genre is None:
        if any(k in text for k in ["fiction", "novel", "novella", "chapter"]):
            genre = "fiction"
        elif any(k in text for k in ["memoir", "essay", "personal"]):
            genre = "nonfiction-narrative"
        else:
            genre = "nonfiction"

    return Inputs(
        command=inputs.command,
        passage=inputs.passage,
        persona=persona,
        genre=genre,
        audience=inputs.audience,
    )


def must_include_set(patterns: list[Pattern], inputs: Inputs) -> list[str]:
    by_id = {p.id: p for p in patterns}

    def take(*ids: str) -> list[str]:
        return [pid for pid in ids if pid in by_id]

    forced: list[str] = []

    if inputs.genre == "fiction":
        forced += take("tricolon-reflex", "em-dash-connector", "dialogue-contracts")
    elif inputs.genre == "nonfiction":
        forced += take("hedge-stacking", "marketing-verb", "filler-openers")
    elif inputs.genre == "nonfiction-narrative":
        forced += take("universal-aphorism", "self-descriptor", "filler-openers")

    if inputs.persona == "literary-fiction":
        forced += take("tricolon-reflex", "em-dash-connector")
    elif inputs.persona == "popular-nonfiction":
        forced += take("hedge-stacking", "negative-positive-restatement", "universal-aphorism")
    elif inputs.persona == "technical-writing":
        forced += take("hedge-stacking", "marketing-verb", "negative-positive-restatement")
    elif inputs.persona == "memoir":
        forced += take("tricolon-reflex", "self-descriptor", "universal-aphorism")
    elif inputs.persona == "business-book":
        forced += take("marketing-verb", "hedge-stacking", "negative-positive-restatement")

    seen: set[str] = set()
    deduped: list[str] = []
    for pid in forced:
        if pid not in seen:
            seen.add(pid)
            deduped.append(pid)
    return deduped


def select_subset(
    patterns: list[Pattern],
    inputs: Inputs,
    history: list[dict],
    run_id: str,
) -> Draw:
    by_id = {p.id: p for p in patterns}
    pool_ids = list(by_id.keys())

    previous_subset = set(history[-1]["subset"]) if history else set()
    runs_ago_2_subset = set(history[-2]["subset"]) if len(history) >= 2 else set()
    runs_ago_3_subset = set(history[-3]["subset"]) if len(history) >= 3 else set()

    seed_int = int(hashlib.sha256(run_id.encode()).hexdigest(), 16)
    target_size = 8 + (seed_int % 7)

    # Always-on patterns are the highest-frequency AI tells. Rotating them out would
    # let them back into every other draft, so they skip the rotation rule entirely.
    always_on = [p.id for p in patterns if p.always_include]
    forced_full = [pid for pid in must_include_set(patterns, inputs) if pid not in always_on]
    forced_kept: list[str] = []
    rotation_excluded: list[str] = []

    for pid in forced_full:
        if pid in previous_subset:
            rotation_excluded.append(pid)
            continue
        forced_kept.append(pid)

    forced_kept = always_on + forced_kept[: max(1, target_size // 2)]

    rng = random.Random(seed_int)
    weights: dict[str, float] = {}
    for pid in pool_ids:
        w = 1.0
        if pid in SIGNAL_PATTERN_IDS:
            w *= 1.30
        if pid in previous_subset and pid not in forced_kept:
            w *= 0.10
        if pid in runs_ago_2_subset and pid not in previous_subset:
            w *= 1.10
        if pid in runs_ago_3_subset and pid not in previous_subset and pid not in runs_ago_2_subset:
            w *= 1.05
        weights[pid] = w

    chosen: list[str] = list(forced_kept)
    chosen_set = set(chosen)

    def category_coverage_count(ids: Iterable[str]) -> int:
        cats = set()
        for pid in ids:
            cats.update(by_id[pid].categories)
        return sum(1 for c in CATEGORY_DIVERSITY_MIN if c in cats)

    candidates = [pid for pid in pool_ids if pid not in chosen_set]

    while len(chosen) < target_size and candidates:
        coverage = category_coverage_count(chosen)
        missing_cats = [c for c in CATEGORY_DIVERSITY_MIN if c not in {x for pid in chosen for x in by_id[pid].categories}]
        if missing_cats and coverage < len(CATEGORY_DIVERSITY_MIN):
            cat_pool = [pid for pid in candidates if any(c in by_id[pid].categories for c in missing_cats)]
            if cat_pool:
                chosen_pid = weighted_choice(cat_pool, weights, rng)
                chosen.append(chosen_pid)
                chosen_set.add(chosen_pid)
                candidates.remove(chosen_pid)
                continue

        chosen_pid = weighted_choice(candidates, weights, rng)
        chosen.append(chosen_pid)
        chosen_set.add(chosen_pid)
        candidates.remove(chosen_pid)

    if set(chosen) == previous_subset and previous_subset:
        non_forced = [pid for pid in chosen if pid not in forced_kept]
        if non_forced:
            swap_out = rng.choice(non_forced)
            replacements = [pid for pid in pool_ids if pid not in chosen_set]
            if replacements:
                swap_in = weighted_choice(replacements, weights, rng)
                chosen[chosen.index(swap_out)] = swap_in
                chosen_set = set(chosen)

    rotation_excluded = [pid for pid in rotation_excluded if pid not in chosen_set]

    rationale_parts = [
        f"Genre={inputs.genre}, persona={inputs.persona}.",
        f"{len(forced_kept)} patterns forced by site-specific signals.",
    ]
    if rotation_excluded:
        rationale_parts.append(f"{len(rotation_excluded)} forced patterns deferred by rotation.")
    if previous_subset:
        rationale_parts.append("Weighted previous subset down to enforce variation.")
    rationale = " ".join(rationale_parts)

    return Draw(
        ts=dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
        run_id=run_id,
        command=inputs.command,
        selector_version=SELECTOR_VERSION,
        input_signal={
            "passage": inputs.passage[:200],
            "persona": inputs.persona,
            "genre": inputs.genre,
            "audience": inputs.audience,
        },
        pool_size=len(patterns),
        subset_size=len(chosen),
        subset=chosen,
        site_specific_inclusions=forced_kept,
        rotation_excluded=rotation_excluded,
        previous_subsets_consulted=min(len(history), 5),
        rationale=rationale,
    )


def weighted_choice(items: list[str], weights: dict[str, float], rng: random.Random) -> str:
    if not items:
        raise ValueError("no items to choose from")
    ws = [max(weights.get(pid, 1.0), 1e-6) for pid in items]
    total = sum(ws)
    r = rng.uniform(0, total)
    upto = 0.0
    for pid, w in zip(items, ws):
        upto += w
        if upto >= r:
            return pid
    return items[-1]


def render_audit_header(draw: Draw, by_id: dict[str, Pattern]) -> str:
    rows = []
    for pid in draw.subset:
        p = by_id[pid]
        rows.append(f"| `{p.id}` | {p.title} | {p.categories[0]} | {p.source_file} |")
    table = "\n".join(rows)

    forced_lines = []
    for pid in draw.site_specific_inclusions:
        forced_lines.append(f"- `{pid}`: forced by genre or persona signal")
    forced_block = "\n".join(forced_lines) if forced_lines else "- (none)"

    excluded = ", ".join(draw.rotation_excluded) if draw.rotation_excluded else "(none)"

    return (
        f"# Scribe Anti-Pattern Draw\n\n"
        f"**Run ID**: `{draw.run_id}`\n"
        f"**Command**: /{draw.command}\n"
        f"**Pool size**: {draw.pool_size}\n"
        f"**Subset size**: {draw.subset_size}\n"
        f"**Persona**: {draw.input_signal['persona']}\n"
        f"**Genre**: {draw.input_signal['genre']}\n\n"
        f"## Selected Anti-Patterns\n\n"
        f"| ID | Title | Category | Source |\n"
        f"|---|---|---|---|\n"
        f"{table}\n\n"
        f"## Site-Specific Inclusions\n\n"
        f"{forced_block}\n\n"
        f"## Rotation\n\n"
        f"Previous subsets consulted: {draw.previous_subsets_consulted}\n"
        f"Excluded this run (rotation rule): {excluded}\n\n"
        f"## Rationale\n\n"
        f"{draw.rationale}\n"
    )


def append_audit(draw: Draw, state_path: Path) -> str:
    line = json.dumps(
        {
            "ts": draw.ts,
            "run_id": draw.run_id,
            "command": draw.command,
            "selector_version": draw.selector_version,
            "input_signal": draw.input_signal,
            "pool_size": draw.pool_size,
            "subset_size": draw.subset_size,
            "subset": draw.subset,
            "site_specific_inclusions": draw.site_specific_inclusions,
            "rotation_excluded": draw.rotation_excluded,
            "previous_subsets_consulted": draw.previous_subsets_consulted,
            "rationale": draw.rationale,
        },
        separators=(",", ":"),
    )
    state_path.parent.mkdir(parents=True, exist_ok=True)
    with state_path.open("a", encoding="utf-8") as f:
        f.write(line + "\n")
    return line


def parse_args() -> tuple[Inputs, Path, str | None]:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("passage", help="Passage description string")
    p.add_argument("--command", default="write")
    p.add_argument("--persona", default="unknown")
    p.add_argument("--genre", default=None)
    p.add_argument("--audience", default=None)
    p.add_argument("--state-file", default=str(DEFAULT_STATE_PATH))
    p.add_argument("--run-id", default=None, help="Override generated run_id (useful for tests)")
    args = p.parse_args()

    inputs = Inputs(
        command=args.command,
        passage=args.passage,
        persona=args.persona,
        genre=args.genre,
        audience=args.audience,
    )
    return inputs, Path(args.state_file), args.run_id


def main() -> int:
    inputs, state_path, run_id_override = parse_args()
    inputs = detect_signals(inputs)
    patterns = load_manifest()
    by_id = {p.id: p for p in patterns}
    history = load_history(state_path)
    run_id = run_id_override or derive_run_id()
    draw = select_subset(patterns, inputs, history, run_id)
    line = append_audit(draw, state_path)
    print(render_audit_header(draw, by_id))
    print()
    print(f"Audit line written to {state_path}:")
    print(line)
    if history:
        prev = set(history[-1]["subset"])
        cur = set(draw.subset)
        diff = cur.symmetric_difference(prev)
        print()
        print(f"Rotation check: |prev|={len(prev)} |cur|={len(cur)} |symmetric_diff|={len(diff)}")
        if cur == prev:
            print("ERROR: subset matches previous run. Rotation rule violated.")
            return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())