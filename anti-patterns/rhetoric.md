---
file: anti-patterns/rhetoric.md
tags: [rhetoric, voice, hedging, framing, register]
affects: all
severity_default: high
pattern_count: 8
---

# Rhetoric Anti-Patterns

The way prose argues, frames, and turns. AI-default rhetorical moves that signal generic synthesis rather than authored thought.

---

## "In Today's Fast-Paced World..." Opener
_Tags: opener, register, ai-tell · Affects: all (especially business-book, popular-nonfiction) · Severity: critical_

**What it is**: Opening sentences that gesture at the contemporary moment with no specifics. "In today's increasingly complex world..." "In an era of unprecedented change..." "Now more than ever..." "In the digital age..." The reader is being framed for an argument that has not yet started.

**Why it fails**: These openers are content-marketing-blog signatures. They have been mocked enough by serious editors that their presence is now an explicit AI-tell.

**Fix**: Open with a specific scene, person, number, or sentence-length-question. Cut the framing.

```
// AI default
In today's increasingly complex business landscape, leaders must navigate a multitude of challenges.

// Real prose
On the morning of November 4, 2008, Stripe had four employees and a Stripe-issued credit card with a $30,000 limit.
```

_Community: "If a book opens with 'in today's,' I close it." — multiple Goodreads reviews aggregated. "The 'fast-paced world' opener is the prose equivalent of stock photography." — Atlantic._

---

## Universalizing Claims About "We" or "Many People"
_Tags: rhetoric, voice, vagueness · Affects: all · Severity: high_

**What it is**: Claims that begin with "Many people..." or "We all know that..." or "Most of us have experienced..." or "Every entrepreneur knows..." The author is assigning belief to an unspecified group.

**Why it fails**: The unspecified group is a dodge. Either name the group ("38% of CEOs in our survey") or speak for yourself ("In my experience"). AI prose hides behind "we" because synthesis is easier than specificity.

**Fix**: Replace every "we / they / many people / most of us" with: a named group with a number, a personal first-person claim with the writer accepting accountability, or a deletion.

---

## False Dichotomies Used Rhetorically
_Tags: rhetoric, framing · Affects: business-book, popular-nonfiction · Severity: high_

**What it is**: Setup sentences that pose a binary and then resolve it. "It's not about working harder; it's about working smarter." "There are two kinds of people in the world: those who plan and those who do."

**Why it fails**: Most binaries are false. The "two kinds of people" frame is one of the most-mocked AI-default patterns. Presented as wisdom, deployed as filler.

**Fix**: Either commit to the both-and ("Working hard and working smart compound; the right ratio depends on field maturity") or skip the binary altogether.

---

## The Rhetorical Question That Gets Answered
_Tags: rhetoric, voice · Affects: business-book, popular-nonfiction · Severity: moderate_

**What it is**: Asking a question whose answer is going to be in the next paragraph. "Why does this happen?" "What's the lesson here?" "What can we learn from this?" AI prose uses these as transitions.

**Why it fails**: The reader is reading specifically because they want answers; they don't need to be asked the questions first. The pattern infantilizes.

**Fix**: Replace the rhetorical question with a declarative claim or with the answer itself. "Why does this happen? The answer is X." → "X happens because..." Or skip the meta-question entirely.

---

## Aphorism-as-Section-Closer
_Tags: aphorism, ai-tell · Affects: popular-nonfiction, business-book, memoir · Severity: high_

**What it is**: Section endings that resolve into a short, gnomic, abstract aphorism. "Sometimes, the answer is in the question itself." "What we hold onto holds us." "The journey is the destination." AI tools generate these by the dozen.

**Why it fails**: The aphorism is doing emotional work the section's specifics should have done. Every section ending in a manufactured aphorism is a section that didn't earn its conclusion through evidence.

**Fix**: End sections on the strongest concrete image, scene, or quote. If the section's argument is genuinely aphoristic, let the reader feel it without packaging the takeaway.

---

## "What Most People Don't Realize..." Pseudo-Reveal
_Tags: rhetoric, voice · Affects: business-book, popular-nonfiction · Severity: high_

**What it is**: Claiming a hidden insight that the audience supposedly missed. "What most people don't realize is..." "Few people understand that..." "The truth is..." AI tools love this rhythm because it manufactures the impression of authority.

**Why it fails**: Real hidden insights don't need announcing. They emerge from evidence. Claiming hiddenness is a tell.

**Fix**: State the claim plainly. If the claim is genuinely counter-intuitive, let the evidence demonstrate the counter-intuition. Don't pre-announce the reveal.

---

## "And Yet..." Twist Reflex
_Tags: rhythm, rhetoric · Affects: popular-nonfiction, business-book · Severity: high_

**What it is**: Setup, evidence, then a sentence beginning with "And yet..." to introduce a counter-intuitive turn. This rhythm became Malcolm Gladwell's signature in 2008 and an AI-default in 2023.

**Why it fails**: The literal phrase "and yet" announces the turn before delivering it. Real counter-intuitive turns work better when they arrive without flagging.

**Fix**: Cut the literal phrase. If the counter-intuitive content is right, the reader will feel the turn without "and yet." Replace with: "But," ".", or just the new sentence cold.

---

## The Concluding Hortatory
_Tags: rhetoric, voice, motivational · Affects: business-book, popular-nonfiction, memoir · Severity: high_

**What it is**: A book or chapter ending that pivots to direct address: "Now it's your turn." "What will YOU do?" "The choice is yours." AI tools default to motivational closings because the training data over-indexes on self-help.

**Why it fails**: The hortatory ending is an admission that the prose didn't trust the reader to draw the conclusion themselves. It's also the most-mocked move in the genre.

**Fix**: End on a specific image, a darkest case, an open question, or simply stop. The reader will infer the call-to-action; let them.
