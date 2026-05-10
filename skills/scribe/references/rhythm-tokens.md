# Rhythm Tokens

Cross-persona reference for rhythm targets. The rhythm-specialist consults this file plus the active persona file to set targets for a run.

## Sentence-length distribution

| Persona | Mean wd/sent | Min std dev | Min sentences ≤ 6 wd / 250 wd | Min sentences ≥ 30 wd / 250 wd |
|---|---|---|---|---|
| literary-fiction | 16 | 8 | 1 | 1 |
| popular-nonfiction | 17 | 7 | 1 | 1 |
| technical-writing | 15 | 6 | 0-1 | optional |
| memoir | 18 | 9 | 1-2 | 1 |
| business-book | 17 | 6 | 1 | 1 |

## Paragraph-length distribution

| Persona | Mean sent/para | Min std dev | Min single-sentence paras / page |
|---|---|---|---|
| literary-fiction | 4 | 2.5 | 1 (often more) |
| popular-nonfiction | 5 | 2 | 1 |
| technical-writing | 4 | 2 | 0 (lists carry rhythm) |
| memoir | 5 | 3 | 1-2 |
| business-book | 5 | 2 | 1 |

A "page" = ~250 words of running prose. Lists do not count toward paragraph rhythm.

## Em-dash budget (per page)

| Persona | Budget |
|---|---|
| literary-fiction | 2 |
| popular-nonfiction | 3 |
| technical-writing | 1 |
| memoir | 4 |
| business-book | 2 |

If a page exceeds budget, the rhythm-critic flags. The voice-implementer reduces by replacing half with periods, half with commas. Remaining em-dashes must each signal genuine interruption (parenthetical, abrupt redirect, dialogue break).

## Tricolon budget (per chapter)

| Persona | Budget |
|---|---|
| literary-fiction | 1 (very rare; must be deliberate rhetorical move) |
| popular-nonfiction | 2 |
| technical-writing | 1 |
| memoir | 2 |
| business-book | 2 |

Tricolons are three-word adjective lists used for emphasis ("bold, brave, brilliant"). The default form is the AI-default rhythm. A tricolon used WITHIN budget should be earning its place — typically as a single rhetorical highlight, not as background filler.

## Hedging budget (per 200 words)

| Persona | Budget |
|---|---|
| literary-fiction | 2 |
| popular-nonfiction | 3 (more than other personas because the genre allows "many," "often," "some" with named-evidence) |
| technical-writing | 1 |
| memoir | 4 (memoir tolerates "I think," "I'm not sure" — these are part of voice) |
| business-book | 2 |

Hedge inventory: many, some, several, a number of, often, sometimes, generally, typically, commonly, tends to, may, might, could, possibly, perhaps, arguably, in some cases, in many ways, to some extent.

Sentences with 3+ hedges from this list trigger the hedge-stack anti-pattern.

## Dialogue cadence

For surfaces that include dialogue:

- "Said" is the default verb (≥80% of tags). Other verbs allowed when the action is genuinely required: whispered, shouted, replied, asked.
- Adverbial tags banned (no "she said angrily").
- Dialogue line lengths must vary. A 30-word speech can be followed by "No.". Uniform back-and-forth is an AI-default.
- Beats (action between dialogue lines) replace tags 30-50% of the time in literary fiction; less in technical/business.

## Variance test

The simplest rhythm health check: across any 10-sentence span, the standard deviation of word counts must exceed the persona's `Min std dev` value. If it does not, the rhythm-critic flags "uniform-sentence-length" — the most common AI-default rhythm signature.

## When to override

If the user's voice signature explicitly references an author whose rhythm violates these defaults — e.g., "Cormac McCarthy economy" pushes mean wd/sentence DOWN and disables most em-dashes — apply the user's signature, not the table. The table is a starting point.
