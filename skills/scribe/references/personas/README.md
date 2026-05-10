# Persona Registry

Five writing personas. Each defines voice, rhythm, vocabulary, forbidden openers, em-dash discipline, persona-specific anti-patterns (PSI-XX-N), signature moves, and exemplar authors.

| ID | Persona | For | Risk |
|----|---------|-----|------|
| LF | `literary-fiction.md` | Novels, novellas, short stories | Low — readers self-select for prose |
| PN | `popular-nonfiction.md` | Big-idea books for general audiences | High — heavy AI training data |
| TW | `technical-writing.md` | Technical books, dev essays, deep-dive docs | Medium — readers spot AI prose fast |
| MM | `memoir.md` | First-person life writing | Critical — voice is the product |
| BB | `business-book.md` | Business, leadership, productivity books | **Highest** — genre converges on AI-default |

## How critics use these files

Every scribe critic and specialist agent reads the persona file before generating or critiquing. The persona constrains:

- Sentence-length distribution targets
- Acceptable em-dash density
- Vocabulary register (banned/required word categories)
- Forbidden opener patterns
- Persona-specific anti-patterns (PSI flags)
- Exemplar authors to reference for direction

## Adding a sixth persona

This is a major version bump. Adding a new persona means every critic and specialist must be updated to handle it. Don't add casually. Genuine candidates being considered for v1.0:

- `screenplay` — different format, different cadence rules
- `poetry` — verse rules, not prose rules
- `academic-paper` — citation discipline, IMRaD structure
- `email` — cold-outreach, B2B sales writing (anti-AI for selling)
- `newsletter` — Substack-aware longform email

Each requires its own file following the existing template. Do not stub — write all sections fully.

## Persona detection

`anti-pattern-selector` infers persona from the user's brief if not stated. The selector looks for genre signals (story, character, plot → literary-fiction; founder, CEO, framework → business-book; engineer, system, code → technical-writing; mother, grandmother, hospital → memoir; researcher, scientist, study → popular-nonfiction).

If signals are mixed (confidence < 0.7), the conductor escalates with the top two options.
