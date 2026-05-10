---
file: anti-patterns/structure.md
tags: [structure, rhythm, paragraph, chapter, pacing]
affects: all
severity_default: high
pattern_count: 10
---

# Structure Anti-Patterns

Shape-of-the-page failures. Paragraph rhythm, chapter architecture, recap discipline. The patterns below show up at the structure level rather than the sentence level — and AI prose has them in nearly every chapter.

---

## Uniform Paragraph Length
_Tags: paragraph, rhythm, ai-tell · Affects: all · Severity: critical_

**What it is**: Paragraphs that are all roughly the same length. AI prose averages 4-5 sentences per paragraph and clings to that target. Real writing has wild paragraph-length variance — single-sentence paragraphs next to half-page-long ones.

**Why it fails**: Uniform paragraph length flattens prose rhythm. The reader experiences the book as a series of equally-weighted blocks. Real prose breathes — short paragraphs are fast, long ones are dense, the alternation is what reading feels like.

**Fix**: Per-page check: across any ten consecutive paragraphs, the standard deviation of sentence-counts must exceed 2.0. Fail the check by intentionally varying. Break a too-long paragraph at the strongest internal turn. Combine two too-short ones if they're saying related things.

```
// AI default (every paragraph 4-5 sentences)
The CEO walked into the boardroom. She was nervous. The numbers were bad. She had not slept the night before. She knew what was coming.

The board members looked up. Mark cleared his throat. He had prepared a statement. The statement was not friendly. He was the one who had hired her.

// Real prose
The CEO walked into the boardroom. She was nervous and the numbers were bad. She had not slept.

Mark cleared his throat — Mark, who had hired her, who had told her in 2019 that she was the only one for the job, that the board would always have her back. Mark, with the prepared statement.

She sat.
```

---

## The Chapter-Recap Opening
_Tags: recap, structure, throat-clearing · Affects: all · Severity: high_

**What it is**: Opening a chapter by summarizing the previous chapter. "In the last chapter, we explored X. Now, we will examine Y." AI default for academic-style books, business books, and popular nonfiction.

**Why it fails**: The reader just read the previous chapter. They don't need a recap. Recapping costs trust.

**Fix**: Open the new chapter with a scene, a question, a number, a person — anything except "In the last chapter." If the connection between chapters genuinely needs flagging, it should happen in the chapter title or in a single phrase woven into the first scene, not in a setup paragraph.

---

## The Chapter-End Summary
_Tags: structure, recap, ai-tell · Affects: business-book, popular-nonfiction, technical-writing · Severity: critical_

**What it is**: Closing a chapter with a summary of the chapter. "In this chapter, we have examined..." "The key takeaways from this chapter are..." Often paired with a bulleted list. The "Key Takeaways" box is the most explicit form.

**Why it fails**: The reader just read the chapter. The summary insults them. AI tools generate these reflexively because the training data over-indexes on textbook structure.

**Fix**: End the chapter on its strongest scene, image, claim, or counter-example. Trust the reader to retain the chapter. If the reader truly needs a summary, that's a sign the chapter wasn't structured well — fix the chapter, don't tape a summary on the end.

---

## "As We Will See in Chapter X" Forward Reference
_Tags: structure, throat-clearing · Affects: all · Severity: moderate_

**What it is**: Sentences that promise the reader a future chapter will resolve something. "As we will see in chapter eight, this question turns out to have a counterintuitive answer." AI prose deploys these constantly to manufacture momentum.

**Why it fails**: Every chapter is supposed to be load-bearing on its own. Forward references are an admission that the current paragraph isn't.

**Fix**: Cut the forward reference. If chapter eight matters here, mention the specific concept now. If it doesn't, don't tease.

---

## The Three-Part Chapter Skeleton
_Tags: structure, formula · Affects: business-book, popular-nonfiction · Severity: high_

**What it is**: Every chapter follows the same three-part structure: Anecdote → Principle → Application. AI tools generate book chapters from this template by default, and contemporary business books / popular nonfiction often used the template before AI.

**Why it fails**: The reader feels the formula by chapter four. Knowing the rhythm of the chapter before it starts erases its momentum.

**Fix**: Break the formula in at least one chapter per third of the book. A chapter that is all anecdote without explicit principle. A chapter that is all argument without an opening anecdote. A chapter that ends without application. Variation is what saves long-form readability.

---

## Predictable Section Sequence
_Tags: structure, pacing, ai-tell · Affects: business-book, popular-nonfiction · Severity: high_

**What it is**: Books where every section sub-heading follows the same sequence: setup, history, theory, examples, counter-examples, implications, takeaway. AI default for any book commissioned with a generic outline.

**Why it fails**: The reader can predict the next section type before opening it. The book's structure becomes its own anti-rhythm.

**Fix**: Vary section ordering across chapters. Some chapters open with examples, some with theory, some with a single long anecdote. The book's table of contents should not be guessable from its first chapter's structure.

---

## The Bullet-List Body
_Tags: structure, list, register · Affects: business-book, popular-nonfiction, technical-writing · Severity: high_

**What it is**: Long passages of prose interrupted by bulleted lists every 200-400 words. The lists are often parallel-structured ("✓ Increase efficiency, ✓ Reduce cost, ✓ Improve quality") and add nothing the prose didn't already say.

**Why it fails**: Bullet lists in narrative prose break the reading state. Every bullet list is the reader skimming. Books that bullet-list constantly read like LinkedIn posts.

**Fix**: A bullet list earns its place when the items are genuinely parallel and each item is something the reader will reference (algorithm steps, configuration options, named principles in a numbered framework). Otherwise, write the items as prose.

---

## The Three-Anecdote Montage
_Tags: structure, pacing, ai-tell · Affects: business-book, popular-nonfiction · Severity: high_

**What it is**: A chapter section that strings together three short anecdotes, all making the same point. "Take Sarah, a marketing director... Or consider Marcus, a startup founder... Then there's Amelia..." AI tools default to triple anecdotes for emphasis.

**Why it fails**: Three thin anecdotes are weaker than one thick one. The reader skims the second and third. Real popular nonfiction picks one story and stays with it for three pages.

**Fix**: Pick the strongest anecdote. Cut the other two. Spend the saved space on additional specificity in the chosen story. Quote actual people. Name the year. Show the room.

---

## The False-Question Subhead
_Tags: structure, voice · Affects: business-book, popular-nonfiction · Severity: moderate_

**What it is**: Sub-headings phrased as questions the chapter then answers. "Why Do Some Teams Outperform Others?" "What Makes a Great Leader?" "How Do Cities Forget?" AI tools generate question-subheadings reflexively.

**Why it fails**: The questions are usually rhetorical and the answers are usually unsurprising. The pattern feels like a content-marketing blog post.

**Fix**: Use declarative subheadings that compress the section's actual claim. "Some Teams Outperform Because They Have Slack" beats "Why Do Some Teams Outperform Others?" — the declarative subhead is the thesis.

---

## The Conclusion-Restating-Conclusion
_Tags: structure, recap, ai-tell · Affects: all · Severity: critical_

**What it is**: Books that end with a conclusion chapter that restates the conclusions of every previous chapter. "We have seen in this book that X, Y, and Z. We have learned that..."

**Why it fails**: The reader just read the book. Restatement feels like the author doesn't trust them. Real book endings either land on a final dramatic case, project forward into open questions, or refuse to summarize at all.

**Fix**: End on the darkest case (popular nonfiction, business books). Or on a final image (memoir, literary fiction). Or with a list of open questions (technical writing). Never with "in summary."
