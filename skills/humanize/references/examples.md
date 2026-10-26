# Humanize: editing decisions

These examples were written for Scribe. Read them for the decisions, not as a house voice to impose on every passage.

## Remove the fanfare, keep the release details

Request: Make this announcement more natural.

Before:

> We are delighted to unveil a transformative improvement to the administrator experience. Starting Monday, workspace admins can export audit logs as CSV, unlocking a new level of operational visibility. It is important to note that exports cover the previous 90 days and exclude deleted records.

After:

> Starting Monday, workspace admins can export audit logs as CSV. Exports cover the previous 90 days and exclude deleted records.

The export behavior carries the announcement. The edit keeps the release timing, role restriction, format, retention window, and exclusion. It does not turn "Monday" into an invented calendar date.

## Keep uncertainty and scope

Request: Humanize this technical update.

Before:

> It is worth highlighting that retries may reduce failures caused by brief network outages. However, this behavior has not been tested under sustained load. The pilot included 18 accounts, and the reported reduction was 12%.

After:

> Retries may reduce failures caused by brief network outages. This behavior has not been tested under sustained load. The pilot included 18 accounts and reported a 12% reduction.

"May" and the untested load condition carry evidence limits. A stronger sentence such as "Retries prevent network failures" would change the claim. The edit also avoids assuming that the pilot established a causal result.

## Preserve a real contrast

Request: Make this explanation less stiff.

Before:

> It is important to understand that the import queues messages; it does not deliver them. Delivery begins only after an operator approves the batch.

After:

> The import queues messages; it does not deliver them. Delivery begins only after an operator approves the batch.

The contrast distinguishes two operations. Removing it as a stylistic reflex would lose useful information. The semicolon also works here.

## Keep the memoir's odd detail

Request: Humanize this paragraph without making it sentimental.

Before:

> Upon returning to my father's kitchen, I observed that the clock remained eleven minutes fast. He had always regarded punctuality as a moral obligation. I had always regarded his clock as a reason to check my phone.

After:

> Back in my father's kitchen, I noticed the clock was still eleven minutes fast. He had always regarded punctuality as a moral obligation. I had always regarded his clock as a reason to check my phone.

The stiff arrival changes. The eleven-minute detail, parallel phrasing, and dry joke stay. No extra memory or reconciliation is needed.

## Let a character remain unreadable

Request: Humanize this fiction excerpt.

Before:

> She put his cup in the cupboard. Then she took it out again. When he came home, it was on the table.

After:

> She put his cup in the cupboard. Then she took it out again. When he came home, it was on the table.

The sequence already works. Adding that she missed him would resolve an ambiguity the writer left open. No edit is a valid result.

## Keep functional structure

Request: Humanize the prose in a setup guide.

Source excerpt:

> It is important to note that you must set `RETRY_LIMIT=3` before starting the worker. Refer to [retry settings](https://example.com/docs/retries?mode=strict#limits) for more information. Restarting the worker is necessary after changing the value.

Possible edit:

> Set `RETRY_LIMIT=3` before starting the worker. See [retry settings](https://example.com/docs/retries?mode=strict#limits) for more information. Restart the worker after changing the value.

The setting, link destination, ordering, and restart requirement stay intact. In a file, frontmatter, code samples, and template expressions would also stay intact. A list of actual setup steps should remain a list.

## Unpack a production note

Request: Make this note easier to follow.

Before:

> Chapter-template replacement removed page numbers; footer restore required before proof export.

After:

> Replacing the chapter template removed the page numbers. Restore the footer before exporting the proof.

The edit gives the second clause a verb and makes the sequence readable. The template change, missing page numbers, and required order stay the same. No extra production step is added.

## Explain a supplied term for a new audience

Request: Make this explanation accessible to a general reader. Here, albedo means the fraction of sunlight a surface reflects.

Before:

> Ice loss lowers albedo. The surface absorbs more sunlight as a result.

After:

> Ice loss reduces albedo, the fraction of sunlight a surface reflects. The surface then absorbs more sunlight.

The writer supplied the definition, and the passage already stated the relationship. The edit places that information together while keeping the technical term. An explanation for specialists might need no definition.

## Community influences

The skill's workflow, wording, and examples are original to Scribe. These community projects informed the design:

- [blader/humanizer](https://github.com/blader/humanizer/blob/main/SKILL.md): inspecting recurring prose patterns and comparing the rewrite with the source. Scribe uses its own existing pattern catalog and returns one finished passage by default.
- [hardikpandya/stop-slop](https://github.com/hardikpandya/stop-slop/blob/main/SKILL.md): attention to repetitive rhetorical structures. Scribe keeps valid passive voice, adverbs, and genuine contrasts when they serve the passage.
- [harshaneel/humanize](https://github.com/harshaneel/humanize/blob/main/plugins/humanize/skills/humanize/SKILL.md): attention to register and rhythm. Scribe does not set statistical rhythm targets or optimize for detector outcomes.

These are design references, not runtime dependencies. No source's pattern list, scoring system, examples, or prompt text was imported.
