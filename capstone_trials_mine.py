"""
Score MY capstone criteria (criteria.md, "Capstone criteria (unit 9) - mine").

    python capstone_trials_mine.py --label before

Criterion 2 (a classmate starts it alone) cannot be scripted; it is scored with
real testers and is not in here.

C1 runs 5 trials (the criterion says "5 of 5 trials"); C3, C4, C5 run 3.
Writes results/capstone_mine_<label>.md. Every run also appends to logs/runs.jsonl.
"""

import os

os.environ["AI201_CACHE"] = "0"  # before `import config`: every run is a real one

import argparse
import json
import shutil
import statistics
import subprocess
import sys
from contextlib import contextmanager
from datetime import datetime

import agent
import config
import generate
import runlog
from utils.data_loader import get_example_wardrobe

# Prices from criteria.md criterion 3 (third-party pages, per million tokens).
PRICE_IN, PRICE_OUT = 0.30, 2.50
COST_CEILING = 0.001

TEE = "vintage graphic tee under $30"
LONG_QUERY = ("vintage graphic tee " * 150).strip()  # about 3,000 characters

# Criterion 5: recorded in results/criterion5_expected.md before any test.
C5_CASES = [
    ("vintage graphic tee under $30", "lst_002"),
    ("denim jacket under $50", "lst_007"),
    ("designer ballgown size XXS under $5", None),
]


@contextmanager
def bad_key():
    old, old_client = os.environ.get("GEMINI_API_KEY"), generate._client
    os.environ["GEMINI_API_KEY"] = "badkey-for-capstone-trial"
    generate._client = None
    try:
        yield
    finally:
        if old is None:
            os.environ.pop("GEMINI_API_KEY", None)
        else:
            os.environ["GEMINI_API_KEY"] = old
        generate._client = old_client


def run_one(query, use_bad_key=False):
    """One agent run. Returns (session or None, exception or None, new log lines)."""
    before = len(runlog.read_runs())
    session, exc = None, None
    try:
        if use_bad_key:
            with bad_key():
                session = agent.run_agent(query, get_example_wardrobe())
        else:
            session = agent.run_agent(query, get_example_wardrobe())
    except Exception as e:  # noqa: BLE001 - scoring it, not hiding it
        exc = e
    return session, exc, runlog.read_runs()[before:]


# -- criterion 1: each run adds exactly one line; a batch of 5 adds 5 ----------

def trial_1():
    batch = [(TEE, False), ("denim jacket under $50", False),
             ("90s track jacket in size M", False),
             ("", False),                       # the bad input
             (TEE, True)]                       # the wrong key
    before_total = len(runlog.read_runs())
    per_run = []
    for query, key_bad in batch:
        _, _, new = run_one(query, key_bad)
        per_run.append((query[:30] or "(empty)", key_bad, len(new)))
    added = len(runlog.read_runs()) - before_total
    ok = added == 5 and all(n == 1 for _, _, n in per_run)
    return ok, added, per_run


# -- criterion 3: cost per run from the log, 10 uncached runs -------------------

COST_QUERIES = [TEE, "90s track jacket in size M",
                "silk slip dress in midi length under $40",
                "platform sneakers size 8", "denim jacket under $50"] * 2


def trial_3():
    recs = []
    for q in COST_QUERIES:
        _, _, new = run_one(q)
        recs.extend(new)
    ok = [r for r in recs if r["status"] == "ok"]
    costs = [r["prompt_tokens"] * PRICE_IN / 1e6 + r["output_tokens"] * PRICE_OUT / 1e6
             for r in ok]
    mean = statistics.mean(costs) if costs else float("inf")
    return mean, len(ok), len(recs), recs


# -- criterion 4: bad input never gives a Traceback -----------------------------

def cli(query, env_extra=None):
    env = {**os.environ, **(env_extra or {})}
    return subprocess.run(
        [sys.executable, "app.py", "ask", query],
        capture_output=True, text=True, env=env, timeout=300,
        stdin=subprocess.DEVNULL, encoding="utf-8", errors="replace",
    )


C4_CASES = [  # (label, query, bad key?, must print a message naming the problem?)
    ("empty query", "", False, True),
    ("3,000 characters", LONG_QUERY, False, False),  # valid query: only no Traceback
    ("symbols only", "!!!@@@###$$$%%%^^^&&&***", False, True),
    ("unsupported language", "古着のグラフィックTシャツを探しています", False, True),
    ("invalid API key", TEE, True, True),
]


def trial_4():
    ok_count, details = 0, []
    for label, query, key_bad, needs_message in C4_CASES:
        proc = cli(query, {"GEMINI_API_KEY": "badkey-for-capstone-trial"} if key_bad else None)
        out = proc.stdout + proc.stderr
        no_trace = "Traceback" not in out
        # Strict: a real problem message, not just any output (the first
        # "before" run counted any non-empty output and let the empty query pass).
        has_message = any(p in out for p in (
            "No listings matched", "rejected your API key", "Nothing to search for"))
        ok = no_trace and (has_message or not needs_message)
        ok_count += ok
        details.append((label, no_trace, has_message, proc.returncode, ok,
                        out.strip().replace("\n", " | ")[:160]))
    return ok_count, details


# -- criterion 5: run_agent behaves exactly like the original _run_loop --------

def trial_5():
    good, details = 0, []
    for query, expected in C5_CASES:
        orig = agent._run_loop(query, get_example_wardrobe())
        wrapped = agent.run_agent(query, get_example_wardrobe())
        got = [(s["selected_item"] or {}).get("id") for s in (orig, wrapped)]
        if expected:
            ok = (got == [expected, expected]
                  and bool(orig["fit_card"]) and bool(wrapped["fit_card"]))
        else:
            ok = got == [None, None] and bool(orig["error"]) and bool(wrapped["error"])
        good += ok
        details.append((query, expected, got, ok))
    return good, details


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--label", default="before")
    args = parser.parse_args()

    saved = agent.SAVED_WARDROBE_PATH  # style memory writes here; protect the user's
    backup = saved.with_suffix(".json.bak")
    had_saved = saved.exists()
    if had_saved:
        shutil.copy(saved, backup)

    res = {1: [], 3: [], 4: [], 5: []}
    samples = {}
    try:
        for t in range(1, 6):
            print(f"=== C1 trial {t} ===", flush=True)
            ok, added, per_run = trial_1()
            res[1].append(f"{'PASS' if ok else 'FAIL'} ({added} lines)")
            print(f"  C1 added {added} lines, per-run {[n for _,_,n in per_run]}", flush=True)
            if t == 1:
                samples[1] = per_run
        for t in range(1, 4):
            print(f"=== trial {t} (C3, C4, C5) ===", flush=True)
            mean, n_ok, n, recs = trial_3()
            res[3].append(f"${mean:.5f}/run ({n_ok}/{n} ok)")
            print(f"  C3 mean ${mean:.5f}/run over {n_ok} ok of {n}", flush=True)
            if t == 1:
                samples[3] = recs
            n4, d4 = trial_4()
            res[4].append(f"{n4}/5")
            print(f"  C4 {n4}/5", flush=True)
            if t == 1:
                samples[4] = d4
            n5, d5 = trial_5()
            res[5].append(f"{n5}/3")
            print(f"  C5 {n5}/3", flush=True)
            if t == 1:
                samples[5] = d5
    finally:
        if had_saved:
            shutil.move(backup, saved)
        elif saved.exists():
            saved.unlink()

    def met(cells, want):
        return all(c.startswith(want) for c in cells)

    c3_met = all(float(c.split("$")[1].split("/")[0]) <= COST_CEILING for c in res[3])
    verdict = {1: met(res[1], "PASS"), 3: c3_met, 4: met(res[4], "5/"), 5: met(res[5], "3/")}

    config.RESULTS_DIR.mkdir(exist_ok=True)
    out = config.RESULTS_DIR / f"capstone_mine_{args.label}.md"
    with out.open("w", encoding="utf-8") as f:
        f.write(f"# My capstone criteria, trials - {args.label} - {datetime.now():%Y-%m-%d %H:%M}\n\n")
        f.write("Criterion 2 (classmates) is scored by hand, not here.\n\n")
        f.write("| Criterion | Target | Results per trial | Verdict |\n|---|---|---|---|\n")
        f.write(f"| 1. Exactly one record per run | 5 of 5 trials add 5 lines | {', '.join(res[1])} | {'MET' if verdict[1] else 'MISSED'} |\n")
        f.write(f"| 3. Cost per run | at most ${COST_CEILING}/run | {', '.join(res[3])} | {'MET' if verdict[3] else 'MISSED'} |\n")
        f.write(f"| 4. Bad input does not crash | 5 of 5 | {', '.join(res[4])} | {'MET' if verdict[4] else 'MISSED'} |\n")
        f.write(f"| 5. Original behavior preserved | 3 of 3 | {', '.join(res[5])} | {'MET' if verdict[5] else 'MISSED'} |\n")
        f.write("\n## Raw output, trial 1\n\n### C1 (query, bad key?, new lines)\n")
        for row in samples[1]:
            f.write(f"- {row}\n")
        f.write("\n### C3 log records\n")
        for r in samples[3]:
            f.write(json.dumps(r, ensure_ascii=False)[:400] + "\n")
        f.write("\n### C4 (label, no Traceback, has message, exit code, ok, output)\n")
        for row in samples[4]:
            f.write(f"- {row}\n")
        f.write("\n### C5 (query, expected id, [_run_loop id, run_agent id], ok)\n")
        for row in samples[5]:
            f.write(f"- {row}\n")
    print(f"\nWrote {out}")


if __name__ == "__main__":
    main()
