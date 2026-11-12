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


---

# Capstone criteria (unit 9)

Five criteria for the capstone extension: the structured run log, the run
path, and the cost measurement around the FitFindr agent. Written before any
capstone trial was run. Each trial below means one full pass of the described
batch with the response cache off (`AI201_CACHE=0`), and each criterion is
scored over **3 trials**. "A run" means one call to `agent.run_agent`, started
the way RUNNING.md says (`python app.py ask '...'`).

Note on order: the 10 cost-measurement runs in the README were done before
these were written, because the brief puts cost measurement (Milestone 3)
before criteria (Milestone 4). Criterion 4 and criterion 3's number were set
knowing those averages; criteria 1, 2 and 5 were not.

## 1. Every run leaves exactly one complete record

Run a batch of 10 mixed inputs: 4 queries that match a listing, 2 impossible
queries (e.g. `designer ballgown size XXS under $5`), 2 runs with a deliberately
wrong `GEMINI_API_KEY`, and 2 malformed queries (an empty string and a
3,000-character string). After the batch, `logs/runs.jsonl` must have gained
**exactly 10 new lines**, each parseable as JSON and each containing the fields
`timestamp`, `query`, `status`, `output`, `duration_s`. **10 of 10 per trial.**

**Why this target:** The log is the only record I'll have once this runs
where I'm not watching, so a missing line is a failure I would never see.
`run_agent` writes the record in one wrapper that also catches exceptions, so
I expect the logging itself to be solid, which is why the target is all 10 and
not 9. The malformed inputs are where I don't know what happens, and that is
the point of including them; looser than 10 of 10 would let a silent gap pass.

## 2. Bad input and a failing model never crash the run or look like success

For each of these 5 inputs: an empty string, a whitespace-only string, a
3,000-character string, a query with a wrong API key, and an impossible
query. `run_agent` must **return without raising**, the CLI output must
contain **no `Traceback`**, and the log record's `status` must **not be `ok`**
for the wrong-key and impossible-query cases (they must be `model_unavailable`
and `empty_search` respectively). **5 of 5 per trial.**

**Why this target:** A run that fails with a stack trace is worse than a
run that stops politely, and a failure logged as `ok` is worse again, because
the log would then lie. The wrong-key and impossible-query paths already have
handlers from unit 4, so I expect them to hold; the empty, whitespace-only and
enormous strings never had a test, so they are the real risk. 5 of 5 because
each of these is a plain yes or no on a deterministic code path (no model is
involved in the three malformed cases), unlike model output, which can vary.

## 3. A normal run is fast enough, measured from the log

Run the query `vintage graphic tee under $30` 10 times in a row, cache off.
Using `duration_s` from the 10 log records, **at least 9 of 10 finish in under
10 seconds.** This counts every run, not only warm ones: there is no cold start
to excuse a slow one, because nothing sleeps, and each run includes starting a
fresh MCP server subprocess and two model calls.

**Why this target:** My first measured runs averaged about 8.5 seconds, so
10 seconds is under 2 seconds above the mean, not a comfortable margin. I chose 9 of 10
and not 10 of 10 because model latency varies and one slow call or rate-limit
pause should not fail the whole criterion; I chose 10 seconds and not 20 because
a person waiting at a terminal feels anything past 10 seconds as stuck.

## 4. One run stays cheap, measured in tokens from the log

Across the same 10 runs as criterion 3, the **mean of `prompt_tokens +
output_tokens` per `ok` run is at most 1,200, and no single run exceeds
2,000.** Both numbers come from the log records, not from a pricing page.

**Why this target:** The measured mean was about 943 tokens, so 1,200 leaves
roughly a quarter of headroom for model wording changes without letting the
cost drift unnoticed. Output tokens are about 83% of the dollar cost (output is
priced much higher than input), so the real risk is the model writing longer
outfit suggestions. The 2,000 per-run cap exists because a mean can hide one
runaway answer.

## 5. The original behavior still works: a matching query returns a fit card

Run `vintage graphic tee under $30` 5 times. In each, `session["fit_card"]`
is a non-empty string and `session["error"]` is `None`. **5 of 5 per trial.**

**Why this target:** This is the regression check, because an extension that
breaks what it extends has failed. Unit 3's version of this criterion was 4 of
5; I'm asking for 5 of 5 now because unit 4 added retry on 503 errors, which
was aimed at exactly the failures that used to cost me the fifth run. It can
still miss if the service stays unavailable through all retries, and if it
does, that's a finding about the model dependency and not about my code.
