# Demo Day: steps and what to say (about 3 minutes, four beats)

Numbers are from `results/`, `criteria.md` and the README. The dialogue is a
draft in first person: change the words, keep the numbers and the honest parts.
Each live model run takes about 9 seconds, so talk while it runs.

## Before you go on (offline)

- Terminal open in the project folder, venv active (the prompt starts with `(.venv)`).
- `.env` has your current key. Do not open `.env` on screen.
- Do one warm-up run so you know the network and key work.
- Tabs open: `criteria.md`, `logs/runs.jsonl`, `results/capstone_mine_before.md`,
  `results/capstone_mine_after.md`, `RUNNING.md`.
- Use single quotes around the query. In PowerShell, double quotes drop the `$30`.

## Beat 1: what I built (about 45 s)

**Run:**
```powershell
python app.py ask 'vintage graphic tee under $30'
```
Then show the log line it wrote:
```powershell
python -c "import runlog; print(runlog.read_runs()[-1])"
```

**Say:** "FitFindr is an agent that finds a thrifted item, suggests an outfit from
your wardrobe, and writes a fit card. For the capstone I added a run log. Every
run, including a failed one, appends one line to a file with the query, the
status, how long it took, and how many tokens it used. Here is the run I just did,
and here is its line in the log: the status is ok, and these are the tokens. I
built it this way because a failure that leaves no record looks the same as
nobody using it."

## Beat 2: the standard I set (about 30 s)

**Show:** `criteria.md`, the section marked "mine".

**Say:** "I wrote five criteria, each with a number, before I ran any results.
One: every run leaves exactly one record, a batch of five adds five lines, five
trials out of five. Two: someone can start it from the instructions alone, setup
in five minutes and at least four of five fit cards. Three: cost at most a tenth
of a cent a run, which is ten dollars a day for a hundred users making a hundred
runs each. Four: bad input never crashes it, five out of five. Five: the original
behavior still works, three of three. I wrote these myself. Claude drafted a first
set, and I replaced it. It's still in the file, marked superseded."

## Beat 3: what the test found (about 60 s)

**Run:**
```powershell
python app.py ask ' '
```
(One space inside the quotes. In PowerShell an empty `''` is dropped, and it would
open the interactive prompt instead.) Then open the before and after results files.

**Say:** "Two criteria missed. Cost: the target was a tenth of a cent, and my three
trials came out at 0.103, 0.113 and 0.114 of a cent. About 83 percent of the cost
was output tokens, because they cost more than eight times as much as input.
Bad input: an empty query didn't give an error at all. It dropped into an
interactive prompt and named no problem. My first check said five out of five,
because it only looked for any output. When I ran it by hand I saw it wasn't a
real message, tightened the check, and it was four out of five in every trial.
The other three criteria held. Criterion five is easy by design, because the item
comes from search and not from the model."

## Beat 4: what I changed and what's still broken (about 45 s)

**Show:** the 60-word line in `tools.py` (the `suggest_outfit` prompt), and the
new message from the command in beat 3.

**Say:** "I made two small changes. I capped the outfit suggestion at sixty words,
and cost dropped to about a twentieth of a cent a run,
so criterion three is met with about twice the headroom. And an empty query now
prints 'Nothing to search for' and still logs a record, so criterion four went from
four of five to five of five. For criterion two, the classmate test can only
happen at Demo Day, so I revised it underneath the original to a timed fresh
clone, and it passed three of three trials, setup under three minutes, five of
five fit cards. What's still broken: the real classmate test hasn't happened, my
self-test shows the commands work but not that a stranger can follow the text, the
price I used is from third-party pages, and I didn't re-check fit-card quality
after shortening the outfits."

## If something breaks live

- **A rate-limit pause message:** say "that's the free-tier pacing, it's normal".
- **Model or network down:** show the last line in `logs/runs.jsonl` and say what
  it would have printed. Don't re-run the cost trials live; they take 15 minutes.

## Peer testing (after the demo)

- Swap `RUNNING.md`. Your tester starts cold from the instructions alone (5 minutes
  max), then uses it for 4 minutes: an ordinary query first, then an out-of-scope one.
- They give back three things: WORKED / SURPRISED ME / COULDN'T FIGURE OUT.
- When you receive feedback: write it down and ask one question. Don't defend.
- Your testers need Python 3.12 and their own Gemini key (3.14 fails with
  `No module named 'mcp'`). Ask them their Python version before they start.
