# Out of Scope

What scribe does NOT do, and why. If you wish it did one of these things, that is a separate project.

## Not in scope

### Grammar and punctuation correction
Scribe is not Grammarly. It does not fix subject-verb disagreement, missing commas, or homophones. Run a copy editor or an existing grammar tool first. Scribe assumes the prose is mechanically correct and audits voice, rhythm, and AI-defaultness.

### Plagiarism detection
Scribe does not check whether prose was lifted from another source. Use Originality, GPTZero, Copyscape, or similar.

### AI-vs-human authorship classification
Scribe does not output a probability that a passage was written by AI. Scribe assumes the user is editing AI-influenced or AI-generated prose deliberately and wants it to read as if written by a human author with a specific voice. The Sameness Score is a craft signal, not a forensic one.

### Plot, character, or story structure
Scribe critiques sentences and paragraphs. It does not evaluate whether a story arc works, whether a character is well-developed, or whether a chapter advances plot. That is a developmental editor's job. Scribe is line-level.

### Fact checking
Scribe does not verify claims, statistics, or quotes. Use a research assistant or fact-checking workflow.

### SEO or marketing optimization
Scribe specifically refuses to apply marketing register to prose. Headlines that "convert" or "engage" are out of scope; in fact, scribe flags them as anti-patterns.

### Publishing, formatting, distribution
Scribe is concerned with the prose itself, not the EPUB, the cover, the blurb (well, the blurb might be in scope as a `blurb` surface — but typesetting and distribution are not).

### Translation between languages
Scribe is English-only at v0.1. Other languages may come later but require their own anti-pattern catalogs and persona definitions. Each language has its own AI-default tells.

### Poetry
Scribe's rhythm rules assume prose. Verse has different cadence rules. A `poetry` persona would require its own architecture branch.

### Screenplays and stage plays
Different format conventions, different anti-pattern set. A `screenplay` persona may come later but is not in v0.1.

## Maybe later (if traction justifies it)

- Per-language packs (Spanish, French, Mandarin)
- Poetry persona
- Screenplay persona
- Academic-paper persona (closer to technical-writing but with citation and structure rules of its own)
- Email/cold-outreach persona (anti-AI for B2B sales writing)
- Newsletter persona (Substack-aware)
