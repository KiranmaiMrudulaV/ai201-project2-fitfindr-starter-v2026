# Demo Day script (about 3 minutes, four beats)

Written from the real numbers in `results/` and `criteria.md`. Say it in your own
words; these are the facts to hit, with the time budget. Have open: the system
ready to run, `criteria.md`, `logs/runs.jsonl`, `RUNNING.md`.

## 1. What I built (about 45 s)

FitFindr is an agent that finds a thrifted item, suggests an outfit from your
wardrobe, and writes a fit card. For the capstone I extended it with a run log:
every run appends one JSON line to `logs/runs.jsonl` with the query, status,
output, duration and token counts, and failed runs are logged too. Run it live:
`python app.py ask 'vintage graphic tee under $30'`, then show the new line in the log.

## 2. The standard I set (about 30 s)

Read the criteria with the number:
1. Every run leaves exactly one record: a batch of 5 adds 5 lines, 5 of 5 trials.
2. A classmate starts it alone from RUNNING.md: 2 of 2 testers, setup in 5 minutes, five runs in another 5, at least 4 of 5 fit cards.
3. Cost: at most $0.001 per run, which is $10 a day for 100 users making 100 runs each.
4. Bad input does not crash: 5 of 5 inputs, no Traceback, a message naming the problem.
5. The original behavior still works: 3 of 3 comparisons.

Say that I wrote them myself (Claude's first draft was superseded, see the README).

## 3. What the test found (about 60 s)

Name the real misses:
- **Cost missed.** $0.00103, $0.00113 and $0.00114 a run against $0.001. About 83% of the cost was output tokens.
- **Empty query.** `ask ""` fell into an interactive prompt and named no problem. My first check said 5 of 5, but it only checked for any output; the strict check showed 4 of 5 in every trial.
- Criteria 1 and 5 held. Criterion 5 is easy by design (the item comes from search, not the model).

## 4. What I changed, whether it helped, what's still broken (about 45 s)

- Capped the outfit suggestion at 60 words: cost fell to about $0.0005 a run, criterion 3 met with about 2x headroom.
- `ask ""` now prints "Nothing to search for..." and still logs one record: criterion 4 went from 4/5 to 5/5.
- Still broken, say it plainly: criterion 2 is not scored yet (my dry run: 143 s setup, 5 of 5 fit cards, but that is not a test by a stranger); the price is from third-party pages; I did not re-check fit-card quality after shortening outfits.

## Peer testing (after the demo)

- Swap RUNNING.md; start cold from the instructions alone (5 minutes max); then use it for 4 minutes: an ordinary input first, then an out-of-scope one.
- Give back three things: WORKED / SURPRISED ME / COULDN'T FIGURE OUT.
- When receiving feedback: write it down and ask one question. Do not defend.
- Your testers need Python 3.12 and their own Gemini key (3.14 fails with `No module named 'mcp'`).
