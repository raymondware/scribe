#!/usr/bin/env python3
"""Lightweight prose fingerprint detectors for Scribe validation."""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class Finding:
    pattern_id: str
    kind: str
    line: int
    excerpt: str


# Building blocks shared by the restatement patterns. Contractions are matched with
# both straight and curly apostrophes because drafts arrive in either form.
_APOS = r"['’]"
_NEG_SUBJECT = r"\b(?:it|this|that|the\s+\w+|\w+(?:\s+\w+){0,2})"
_POS_SUBJECT = r"(?:it|this|that|they|the\s+\w+(?:\s+\w+)?)"
_NEG_BE = (
    rf"(?:\s+(?:is|was|are|were)\s+(?:not|never)|{_APOS}s\s+(?:not|never)"
    rf"|\s+(?:is|was|are|were)n{_APOS}t)"
)
_POS_BE = rf"(?:\s+(?:is|was|are|were)|{_APOS}s|{_APOS}re)"

NEGATIVE_POSITIVE_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    (
        "not_just_but",
        re.compile(
            r"\bnot\s+(?:just|only|merely)\b[^.!?;]{0,160}\bbut(?:\s+also)?\b[^.!?]{0,160}",
            re.IGNORECASE,
        ),
    ),
    (
        "not_about_about",
        re.compile(
            rf"{_NEG_SUBJECT}{_NEG_BE}\s+about\b[^.!?]{{0,140}}?"
            rf"[.!?;,]\s*{_POS_SUBJECT}{_POS_BE}\s+(?:all\s+|really\s+)?about\b[^.!?]{{0,140}}",
            re.IGNORECASE,
        ),
    ),
    (
        "not_x_it_is_y",
        re.compile(
            rf"\b(?:it|this|that|the\s+goal|the\s+point|the\s+work|the\s+system){_NEG_BE}\b[^.!?]{{3,140}}?"
            rf"[.!?;,]\s*(?:it|this|that|the\s+goal|the\s+point|the\s+work|the\s+system){_POS_BE}\b[^.!?]{{3,140}}",
            re.IGNORECASE,
        ),
    ),
    (
        # "We don't need X. We need Y." The backreferences require the same subject and
        # verb on both sides, which keeps ordinary negative sentences out.
        "not_do_x_do_y",
        re.compile(
            rf"\b(we|you|they|i)\s+(?:don{_APOS}t|do\s+not|didn{_APOS}t|did\s+not)\s+(\w+)\b[^.!?]{{0,120}}?"
            r"[.!?;,]\s*\1\s+\2\b[^.!?]{0,140}",
            re.IGNORECASE,
        ),
    ),
    (
        "not_fragment_then_claim",
        re.compile(
            r"(?:^|[.!?]\s+)Not\s+(?:a\s+|an\s+|the\s+)?[^.!?]{3,100}[.!?]\s+[A-Z][^.!?]{3,140}",
        ),
    ),
)


def line_for_offset(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def compact_excerpt(value: str, limit: int = 220) -> str:
    excerpt = re.sub(r"\s+", " ", value).strip()
    if len(excerpt) <= limit:
        return excerpt
    return excerpt[: limit - 1].rstrip() + "..."


def detect_negative_positive_restatement(text: str) -> list[Finding]:
    """Find negated claim followed by immediate positive restatement."""
    findings: list[Finding] = []
    seen: set[tuple[int, int, str]] = set()

    for kind, pattern in NEGATIVE_POSITIVE_PATTERNS:
        for match in pattern.finditer(text):
            key = (match.start(), match.end(), kind)
            if key in seen:
                continue
            seen.add(key)
            findings.append(
                Finding(
                    pattern_id="negative-positive-restatement",
                    kind=kind,
                    line=line_for_offset(text, match.start()),
                    excerpt=compact_excerpt(match.group(0)),
                )
            )

    findings.sort(key=lambda item: (item.line, item.excerpt))
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description="Detect Scribe AI-default prose fingerprints.")
    parser.add_argument("path", help="Text or Markdown file to inspect")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable findings")
    args = parser.parse_args()

    text = Path(args.path).read_text(encoding="utf-8")
    findings = detect_negative_positive_restatement(text)
    if args.json:
        print(json.dumps([asdict(item) for item in findings], indent=2))
    else:
        for item in findings:
            print(f"{item.pattern_id}:{item.line}:{item.kind}: {item.excerpt}")
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
