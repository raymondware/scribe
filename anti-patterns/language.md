---
file: anti-patterns/language.md
tags: [vocabulary, ai-isms, register, idiom, hedging]
affects: all
severity_default: high
pattern_count: 13
---

# Language Anti-Patterns

Lexical and idiomatic AI-default tells. Word-level and phrase-level. The first thing a sophisticated reader notices.

---

## Delve / Tapestry / Realm Vocabulary
_Tags: ai-vocabulary, abstraction, hallmark · Affects: all · Severity: critical_

**What it is**: A specific cluster of abstract, slightly formal, slightly literary words that AI tools fall back on with shocking consistency. The shortlist (any of these in unedited prose is a tell):

- delve / delve into
- tapestry / rich tapestry / intricate tapestry
- realm / the realm of
- navigate (as metaphor) / navigate the complexities of
- embark / embark on a journey
- journey (as metaphor for non-physical experience)
- landscape (as metaphor)
- intricate / intricately
- myriad
- nuanced (used reflexively)
- multifaceted
- vibrant (applied to non-color things)
- robust (applied to non-physical things)
- comprehensive (used in marketing register)
- innovative (the canary)
- groundbreaking
- transformative
- holistic
- seamlessly
- effortlessly

**Why it fails**: These words have been so heavily reinforced in AI training data that their presence in unedited longform prose now signals the prose was AI-generated and unedited. Sophisticated readers identify the cluster within two pages.

**Fix**: Replace with concrete vocabulary. Instead of "delve into the topic," write "examine," "look at," "study," or — better — replace with the specific action ("read the seven case files," "interview the surgeons"). Instead of "tapestry of culture," name the actual things. Instead of "navigate the complexities," "work through the seven trade-offs" or "decide between A and B."

```
// Not this
The book delves into the rich tapestry of post-war American politics, navigating the multifaceted realm of party realignment.

// This
The book covers seven elections from 1948 to 1972. It argues that the 1968 cycle was the realignment, not the conventional 1964 answer.
```

_Community: "Every AI-written essay is set in 'the realm of' something and 'delves into' something else, no matter the topic. It's the lexical fingerprint." — r/writing. "If a book has 'delve' in the first chapter, I close it." — Hacker News thread on AI books._

---

## The Tricolon Reflex
_Tags: rhythm, rhetoric, list · Affects: all · Severity: high_

**What it is**: Three-word lists used for emphasis or rhythm. "Bold, brave, and brilliant." "Fast, cheap, and reliable." "She was tired, frustrated, hungry." AI tools default to the rule-of-three for cadence in nearly every adjective list.

**Why it fails**: Real prose uses lists of two, four, five. The tricolon is rhetorically powerful when used rarely and on purpose. Used reflexively, it's a tell.

**Fix**: Replace tricolons with two-item or four-item lists, or with one specific image. Instead of "She was tired, frustrated, and hungry" → "She was hungry. She had not slept since Tuesday." Instead of "Bold, brave, and brilliant," pick the one that's true and lose the alliteration.

```
// AI tricolon (in 80% of paragraphs)
The strategy was simple, elegant, and devastating.

// Real prose
The strategy was simple. It was also illegal.
```

_Community: "The rule-of-three is so over-used in AI prose that it's now a tell to writers, not a craft move." — Substack: Writing in the Age of GPT._

---

## Hedge Stacking
_Tags: hedging, voice, register · Affects: popular-nonfiction, business-book, technical-writing · Severity: high_

**What it is**: Multiple hedges piled into the same sentence. "Many researchers tend to suggest that there might be some evidence to support the idea that..." Each individual hedge is fine; stacked, they signal a writer (or a model) avoiding commitment.

**Why it fails**: The reader feels evasion. Even when the underlying claim is genuinely uncertain, stacking hedges reads as throat-clearing.

**Fix**: Pick ONE hedge or commit. "Recent evidence suggests X" is fine. "Many researchers tend to suggest that there might be some evidence" — cut to "Some evidence suggests" or, if the writer believes it, "Evidence shows."

The hedge inventory: many, some, several, a number of, often, sometimes, generally, typically, commonly, tends to, may, might, could, possibly, perhaps, arguably, in some cases, in many ways, to some extent.

Sentences with three or more hedges from this list are auto-flagged.

---

## The Marketing Verb
_Tags: register, marketing-speak, motivational · Affects: all (especially business-book and popular-nonfiction) · Severity: high_

**What it is**: Verbs that belong on a sales deck, not in a book. The shortlist:

- unlock, unleash, leverage (as verb), drive (as in "drive results"), revolutionize, transform, empower, elevate, optimize, streamline, supercharge, accelerate (in business contexts), pioneer, harness, amplify, catalyze, future-proof.

**Why it fails**: These verbs are not telling the reader what happened. They are selling. Real prose says what was done, who did it, and what changed.

**Fix**: Replace each marketing verb with a concrete action. "Unlock potential" → "doubled signups in eight months." "Leverage the data" → "ran the regression on the 2014 cohort." "Transform the industry" → "took 14% market share from Oracle in three years."

---

## The Em-Dash Universal Connector
_Tags: punctuation, rhythm, ai-tell · Affects: all · Severity: high_

**What it is**: Em-dashes used as the default connector between any two clauses. "She walked in — confident — and looked around." "The book — a memoir — was rejected by every press." AI prose uses em-dashes for parentheticals, asides, emphasis, list-introduction, and just-because. Often six per page.

**Why it fails**: Em-dashes are a strong punctuation. Used too often, the rhythm of the prose flattens — every clause gets the same emphasis weight, which means none of them do.

**Fix**: Per-page maximum: 2 (literary fiction, technical), 3 (popular nonfiction, business), 4 (memoir). Replace excess em-dashes with: comma (most common), period, semicolon, colon, parenthesis. Test: replace EVERY em-dash with a comma or period and see if the prose still works. If yes, the em-dash wasn't earning its place.

```
// AI prose (5 em-dashes in two sentences)
She walked into the room — quietly, almost imperceptibly — and saw him there — at the desk — typing. He looked up — surprised — and smiled.

// Edited prose
She walked into the room. He was at the desk, typing. He looked up, surprised, and smiled.
```

_Community: "I now do a find-and-replace for em-dashes when editing AI drafts. Before doing anything else." — r/writing. "The em-dash is the new comma splice — except universally and inappropriately." — Atlantic essay on AI prose._

---

## The Self-Descriptor
_Tags: voice, self-praise, marketing · Affects: all · Severity: high_

**What it is**: The author or product describing itself with adjectives that should be the reader's job to apply. "This powerful technique." "This elegant solution." "Our innovative approach." "This compelling argument."

**Why it fails**: If the technique is powerful, the reader will feel it. If it's elegant, the reader will see it. AI tools default to praising the work as it presents the work.

**Fix**: Strip every adjective that praises the thing being introduced. Let the example do the work. "This powerful technique reduces lookups from O(n) to O(log n) in our benchmarks" → "This technique reduces lookups from O(n) to O(log n) in our benchmarks."

---

## The Universal Aphorism
_Tags: rhetoric, voice, bromide · Affects: popular-nonfiction, business-book, memoir · Severity: high_

**What it is**: Short, abstract, gnomic statements that sound profound but have no specific content. "Sometimes the longest path is the shortest." "What we resist persists." "The greatest discoveries come from asking the right questions." AI tools generate these by the dozen.

**Why it fails**: These are word-shaped objects, not thought. They feel deep on first read and evaporate on second. Real aphorisms (Pascal, La Rochefoucauld, Oscar Wilde, James Baldwin) earn their gnomic compression by deriving from a specific lived observation. AI aphorisms are average-of-aphorism.

**Fix**: Replace every universal aphorism with the specific story it should have been derived from. Or cut.

---

## "It's Not About X, It's About Y" Frame
_Tags: rhetoric, contrast-construction · Affects: all · Severity: moderate_

**What it is**: Constructions that pretend to subvert one frame in favor of another. "Success is not about hard work; it's about working smart." "Leadership isn't about authority; it's about influence." AI-default contrast structure.

**Why it fails**: Almost always reductive. Real claims are messier than a binary swap. The "not X, but Y" structure is a blog-post tic that AI tools have raised to a religion.

**Fix**: Either embrace the both-and ("It's about both hard work AND working smart, and here's how the trade-off plays out"), or cut the negation ("Working smart matters more than hours after the first 50 hours per week").

---

## Filler Intensifiers
_Tags: hedging, voice · Affects: all · Severity: low_

**What it is**: "Very," "really," "quite," "rather," "actually," "essentially," "basically," "literally" (often misused), "kind of," "sort of," "in many ways," "to some degree." AI prose loads sentences with these.

**Why it fails**: They shift weight without adding meaning. "Very tired" is no more tired than "tired." Real writers earn intensity through specificity, not through "very."

**Fix**: Strip on sight. Re-read. If the sentence loses meaning, fix it some other way.

---

## "Not Just X but Also Y" Reflex
_Tags: rhythm, rhetoric · Affects: all · Severity: high_

**What it is**: The "not just X, but Y" or "not only X, but Y" construction used as default sentence-rhythm filler. "It's not just a book; it's a roadmap." "She was not only a leader, but also a teacher." AI tools default to this structure for emphasis.

**Why it fails**: It's a movie-trailer rhythm. Every clause becomes a setup for an upgrade reveal. The reader stops trusting the upgrades.

**Fix**: Convert to direct claim. "It's a roadmap" or "It's a book that works as a roadmap." Skip the negation that just sets up the affirmation.

---

## Negative/Positive Restatement
_Tags: ai-isms, rhetoric, restatement · Affects: all · Severity: high_

**What it is**: A broader cousin of the "not just X" reflex. The sentence negates a weak version of the claim, then immediately states the preferred positive version. Common forms include "This is not X. It is Y," "This is not about X. It is about Y," "Not X. Y," and stacked variants that repeat the move across a paragraph.

**Why it fails**: The negated half is usually a straw frame the reader did not need. AI prose uses the pattern to create fake decisiveness. The result sounds polished but padded: first it says what the thing is not, then it says what it meant to say.

**Fix**: State the positive claim once. Keep the negative half only when the reader probably believes the false version and the contrast is specific.

```
// AI restatement
This is not a productivity trick. It is a new operating model for teams.

// Direct claim
It changes how teams decide what work counts as finished.
```

```
// AI restatement
The goal is not to replace judgment. The goal is to put judgment in the right place.

// Direct claim
Put judgment where it belongs: use the model for context-sensitive choices and use policy for boundaries that must not drift.
```

---

## Flashlight-Hedging Adjectives
_Tags: voice, register · Affects: all · Severity: moderate_

**What it is**: Adjectives that describe a thing as having a property "in many ways" or "of sorts" or "as it were." "She was a leader of sorts." "The system was, in many ways, a museum." Hedging that retracts the claim while making it.

**Why it fails**: The hedge announces the writer's lack of conviction. Either say the thing or don't.

**Fix**: Either commit ("She was a leader") or be specific about the qualification ("She held the title of CEO but the engineering team reported to the COO").

---

## "It's Worth Noting That..." Throat-Clearing
_Tags: meta-commentary, hedging · Affects: all · Severity: moderate_

**What it is**: Sentences that begin "It's worth noting that," "It's important to note that," "It bears mentioning," "Notably," "Of course," "As one might expect." AI prose lards itself with these meta-comments.

**Why it fails**: Every sentence in a book is supposed to be worth noting. The reader didn't pick up the book to be told which paragraphs matter.

**Fix**: Cut the meta-clause. The next clause is the actual sentence.

```
// Before
It's worth noting that the team grew from 14 to 87 in six months.
// After
The team grew from 14 to 87 in six months.
```
