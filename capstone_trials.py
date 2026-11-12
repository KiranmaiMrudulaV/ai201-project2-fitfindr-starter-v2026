"""
Run the five capstone criteria three times each (criteria.md, "Capstone criteria").

    python capstone_trials.py --label before

Writes results/capstone_<label>.md with the summary table and the real log
records behind trial 1. Every run also appends to logs/runs.jsonl as usual.

Each function below scores ONE trial of ONE criterion, exactly as the sentence
in criteria.md describes it. Nothing changes between trials.
"""

import os

os.environ["AI201_CACHE"] = "0"  # before `import config`: five tries = five real answers

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

REQUIRED_FIELDS = ("timestamp", "query", "status", "output", "duration_s")
TEE = "vintage graphic tee under $30"
LONG_QUERY = ("vintage graphic tee " * 150).strip()  # about 3,000 characters


@contextmanager
def bad_key():
    """Make the model reject the key, then put everything back."""
    old = os.environ.get("GEMINI_API_KEY")
    old_client = generate._client
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
    """Run the agent once. Returns (session or None, exception or None, new log records)."""
    before = len(runlog.read_runs())
    session, exc = None, None
    try:
        if use_bad_key:
            with bad_key():
                session = agent.run_agent(query, get_example_wardrobe())
        else:
            session = agent.run_agent(query, get_example_wardrobe())
    except Exception as e:  # noqa: BLE001 — scoring it, not hiding it
        exc = e
    return session, exc, runlog.read_runs()[before:]


# ── criterion 1: every run leaves exactly one complete record ────────────────

def trial_1():
    inputs = (
        [(q, False) for q in (
            TEE, "90s track jacket in size M", "denim jacket under $50",
            "silk slip dress in midi length under $40",
        )]
        + [("designer ballgown size XXS under $5", False)] * 2
        + [(TEE, True)] * 2
        + [("", False), (LONG_QUERY, False)]
    )
    good, details = 0, []
    for query, key_is_bad in inputs:
        _, exc, new = run_one(query, key_is_bad)
        ok = len(new) == 1 and all(f in new[0] for f in REQUIRED_FIELDS)
        good += ok
        details.append((query[:40] + ("…" if len(query) > 40 else ""), key_is_bad,
                        len(new), "exception" if exc else "returned", ok, new))
    return good, 10, details


# ── criterion 2: bad input never crashes, a failure never looks like success ─

def cli(query, env_extra=None):
    env = {**os.environ, **(env_extra or {})}
    return subprocess.run(
        [sys.executable, "app.py", "ask", query],
        capture_output=True, text=True, env=env, timeout=300,
        stdin=subprocess.DEVNULL, encoding="utf-8", errors="replace",
    )


def trial_2():
    cases = [  # (label, query, bad key?, required status or None)
        ("empty string", "", False, None),
        ("whitespace only", "   ", False, None),
        ("3,000 characters", LONG_QUERY, False, None),
        ("wrong API key", TEE, True, "model_unavailable"),
        ("impossible query", "designer ballgown size XXS under $5", False, "empty_search"),
    ]
    good, details = 0, []
    for label, query, key_is_bad, want in cases:
        _, exc, new = run_one(query, key_is_bad)
        env = {"GEMINI_API_KEY": "badkey-for-capstone-trial"} if key_is_bad else None
        proc = cli(query, env)
        no_trace = "Traceback" not in proc.stdout + proc.stderr
        status = new[0]["status"] if new else None
        status_ok = (status != "exception") and (want is None or status == want)
        ok = exc is None and no_trace and status_ok
        good += ok
        details.append((label, f"raised={exc is not None}", f"no_traceback={no_trace}",
                        f"status={status}", ok, new))
    return good, 5, details


# ── criteria 3 and 4: 10 runs, same query — latency and tokens from the log ──

def trial_3_4():
    records = []
    for _ in range(10):
        _, _, new = run_one(TEE)
        records.extend(new)
    fast = sum(1 for r in records if r["duration_s"] < 10)
    oks = [r for r in records if r["status"] == "ok"]
    totals = [r["prompt_tokens"] + r["output_tokens"] for r in oks]
    mean_tokens = statistics.mean(totals) if totals else float("inf")
    max_tokens = max(totals) if totals else float("inf")
    slow = [(r["duration_s"], r["model_calls"]) for r in records if r["duration_s"] >= 10]
    return fast, mean_tokens, max_tokens, records, slow


# ── criterion 5: the original behavior still works ────────────────────────────

def trial_5():
    good, records = 0, []
    for _ in range(5):
        session, exc, new = run_one(TEE)
        records.extend(new)
        good += bool(session and session["fit_card"] and session["error"] is None)
    return good, 5, records


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--label", default="before")
    args = parser.parse_args()

    # Style memory writes data/saved_wardrobe.json on every ok run; protect the user's.
    saved = agent.SAVED_WARDROBE_PATH
    backup = saved.with_suffix(".json.bak")
    had_saved = saved.exists()
    if had_saved:
        shutil.copy(saved, backup)

    rows = {n: [] for n in range(1, 6)}
    sample = {}
    try:
        for t in (1, 2, 3):
            print(f"=== trial {t} ===", flush=True)
            g, n, d = trial_1()
            rows[1].append(f"{g}/{n}")
            print(f"  C1 {g}/{n}", flush=True)
            if t == 1:
                sample[1] = d

            g, n, d = trial_2()
            rows[2].append(f"{g}/{n}")
            print(f"  C2 {g}/{n}", flush=True)
            if t == 1:
                sample[2] = d

            fast, mean_t, max_t, recs, slow = trial_3_4()
            rows[3].append(f"{fast}/10")
            rows[4].append(f"mean {mean_t:.0f}, max {max_t:.0f}")
            rows.setdefault("slow", []).append(slow)
            rows.setdefault("c4pass", []).append(mean_t <= 1200 and max_t <= 2000)
            print(f"  C3 {fast}/10 under 10s, slow={slow}", flush=True)
            print(f"  C4 mean {mean_t:.0f} max {max_t:.0f}", flush=True)
            if t == 1:
                sample[3] = recs

            g, n, recs = trial_5()
            rows[5].append(f"{g}/{n}")
            print(f"  C5 {g}/{n}", flush=True)
            if t == 1:
                sample[5] = recs
    finally:
        if had_saved:
            shutil.move(backup, saved)
        elif saved.exists():
            saved.unlink()

    def count(cell):
        return int(cell.split("/")[0])

    verdicts = {
        1: all(count(c) == 10 for c in rows[1]),
        2: all(count(c) == 5 for c in rows[2]),
        3: all(count(c) >= 9 for c in rows[3]),
        4: all(rows["c4pass"]),
        5: all(count(c) == 5 for c in rows[5]),
    }
    targets = {1: "10 of 10", 2: "5 of 5", 3: "9 of 10 under 10s",
               4: "mean ≤1200, max ≤2000", 5: "5 of 5"}
    names = {
        1: "Every run leaves exactly one complete record",
        2: "Bad input / failing model: no crash, no false ok",
        3: "Normal run under 10 s, 9 of 10",
        4: "Tokens per run: mean ≤1,200, max ≤2,000",
        5: "Matching query still returns a fit card",
    }

    config.RESULTS_DIR.mkdir(exist_ok=True)
    out = config.RESULTS_DIR / f"capstone_{args.label}.md"
    with out.open("w", encoding="utf-8") as f:
        f.write(f"# Capstone trials — {args.label} — {datetime.now():%Y-%m-%d %H:%M}\n\n")
        f.write("| Criterion | Target | Trial 1 | Trial 2 | Trial 3 | Verdict |\n|---|---|---|---|---|---|\n")
        for n in range(1, 6):
            v = "MET" if verdicts[n] else "MISSED"
            f.write(f"| {n}. {names[n]} | {targets[n]} | "
                    + " | ".join(rows[n]) + f" | {v} |\n")
        f.write(f"\nTrial-by-trial runs over 10 s (duration_s, model_calls): {rows['slow']}\n")
        f.write("\n## Raw records from trial 1\n")
        f.write("\n### Criterion 1 (per input: query, bad key?, new lines, outcome, ok)\n")
        for line in sample[1]:
            f.write(f"- {line[:5]}\n")
            for r in line[5]:
                f.write("  " + json.dumps(r, ensure_ascii=False)[:600] + "\n")
        f.write("\n### Criterion 2\n")
        for line in sample[2]:
            f.write(f"- {line[:5]}\n")
            for r in line[5]:
                f.write("  " + json.dumps(r, ensure_ascii=False)[:600] + "\n")
        f.write("\n### Criteria 3 and 4 (the 10 log records)\n")
        for r in sample[3]:
            f.write(json.dumps(r, ensure_ascii=False)[:500] + "\n")
        f.write("\n### Criterion 5\n")
        for r in sample[5]:
            f.write(json.dumps(r, ensure_ascii=False)[:500] + "\n")
    print(f"\nWrote {out}")


if __name__ == "__main__":
    main()
