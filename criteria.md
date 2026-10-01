# Acceptance criteria — FitFindr

Five criteria that say what "working" means for this agent, written in unit 3
**before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. *"The agent handles errors"* is an opinion.
*"When search returns nothing, the agent stops before calling the second tool,
in 5 of 5 tries"* is a criterion.

Under each one, write a sentence or two on **why that target** and not a
stricter one. A reason that says something about your tools, your loop, or the
data earns credit; *"80% seemed reasonable"* does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

**Two are written for you. You write three.**

---

## 1. A matching query completes all three tools

Given a query that matches at least one listing, the agent completes all three
tool calls and returns a fit card — in at least 4 of 5 tries.

**Why this target:** `search_listings` scores by exact token overlap after
stop-word removal — it has no synonym or stemming logic. A query using
"shoes" won't match a listing tagged "sneakers," and "tee" won't match
"shirt." That's a real, known gap in phrasing coverage, not a bug, so I'd
expect an occasional miss rather than a perfect 5 of 5.

---

## 2. An impossible query stops before the second tool

Given a query that matches no listings, the agent stops before calling
`suggest_outfit` and returns a message naming what to change — 5 of 5 tries.

**Why this target:** Calling `suggest_outfit` without a real item would
crash it outright — it indexes into `new_item['title']`,
`new_item['category']`, etc., and there's nothing to index into when the
search came back empty. I hit exactly this error while testing. On top of
that, the check itself (`if not session["search_results"]:`) is a plain
`if` on a list — unlike `search_listings`' keyword matching, there's no
ambiguity it has to resolve, so there's no plausible reason for it to work
4 times and fail the 5th.

---

## 3. The item that search found is the item suggest_outfit uses

The item in `session["selected_item"]` is the same item `suggest_outfit`
receives as `new_item` — in 5 of 5 tries.

**Why this target:** Unlike `suggest_outfit` and `create_fit_card`, picking
`selected_item` is plain code with no model call involved — my loop always
takes `search_results[0]` with no randomness or fallback branch that could
pick something else. I ran it 5 times and checked by hand that
`selected_item` matched `search_results[0]` every time, so I'd expect 5 of 5
rather than leaving room for the slack I gave the model-calling tools.

---

## 4. The fit card names the item correctly without repeating itself

Given the same item, each of 5 fit cards is checked individually for whether
it mentions both the item's price and its platform — this passes in at
least 4 of 5 tries. Separately, across all 5 captions, no two are
word-for-word identical.

**Why this target:** `TEMPERATURE` is 0.9 (config.py), so the model varies
its wording almost every call — at that setting, two identical captions
back to back would essentially never happen, so zero duplicates is a fair
bar. Mentioning the price and platform is a smaller detail the model could
plausibly drop in a sentence once in a while, so 4 of 5 leaves room for
that without excusing a pattern of it.

---

## 5. Size matching never produces a mismatch

Across 5 size-filtered searches, including the known edge cases (size `S`
against shoe listings like `US 9`, size `L` against `XL`, and waist size
`W30L30` against the data's `W30 L30`), no returned listing's size fails to
share a token with the requested size — 5 of 5 tries.

**Why this target:** `search_listings` has no model call and no
randomness — the size-matching logic is plain code, so there's no
reasonable excuse for a miss. Unlike the criteria that depend on the
model's output, this one should hold 5 of 5 every time, not 4 of 5.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 4 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it, like this:

         ## 4. Something about the fit card

         The fit card is different every time.

         **Why this target:** ...

         > **Revised in unit 4:** For 5 different items, the 5 fit cards share
         > no opening sentence.
         >
         > **Why revised:** "different" wasn't checkable — two cards that
         > differed by one word still counted. The new version is something I
         > can actually score.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "I said the empty search stops it 5 of 5 times, but I got 3 of 5,
            so 3 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
