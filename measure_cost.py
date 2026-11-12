"""
Measure what one FitFindr run costs (capstone, "What It Costs").

    python measure_cost.py

Runs 10 queries through run_agent with the response cache OFF, so every token
counted is a real one. Each run writes its own record to logs/runs.jsonl, and
this script averages those records. The numbers come from the service's own
usage report, not from a pricing page.

Two things it protects you from:
  * Style memory saves every found item into data/saved_wardrobe.json, which
    makes later prompts longer. Every run here gets the same fresh example
    wardrobe, and your saved file is backed up and restored afterwards.
  * The cache. AI201_CACHE is set to 0 before config is imported.
"""

import os

os.environ["AI201_CACHE"] = "0"  # must happen before `import config`

import shutil
import statistics

import agent
import config
import runlog
from utils.data_loader import get_example_wardrobe

# Five different queries that each find a listing, run twice = 10 runs.
QUERIES = [
    "vintage graphic tee under $30",
    "90s track jacket in size M",
    "silk slip dress in midi length under $40",
    "platform sneakers size 8",
    "denim jacket under $50",
] * 2


def main() -> None:
    saved = agent.SAVED_WARDROBE_PATH
    backup = saved.with_suffix(".json.bak")
    had_saved = saved.exists()
    if had_saved:
        shutil.copy(saved, backup)

    start_count = len(runlog.read_runs())
    try:
        for i, query in enumerate(QUERIES, 1):
            session = agent.run_agent(query, get_example_wardrobe())
            print(f"  run {i:>2}/10  {'ok' if not session['error'] else 'STOPPED'}  {query}")
    finally:
        # Put the user's saved wardrobe back exactly as it was.
        if had_saved:
            shutil.move(backup, saved)
        elif saved.exists():
            saved.unlink()

    runs = runlog.read_runs()[start_count:]
    ok = [r for r in runs if r["status"] == "ok"]
    print(f"\n{len(ok)} of {len(runs)} runs finished ok. Averages over the ok runs:")
    for field in ("duration_s", "model_calls", "prompt_tokens", "output_tokens"):
        values = [r[field] for r in ok]
        print(
            f"  {field:<14} mean {statistics.mean(values):8.2f}   "
            f"min {min(values):8.2f}   max {max(values):8.2f}"
        )
    total = [r["prompt_tokens"] + r["output_tokens"] for r in ok]
    print(f"  {'total_tokens':<14} mean {statistics.mean(total):8.2f}")
    print(f"\nModel: {config.MODEL}. Records are in {config.LOG_FILE}.")


if __name__ == "__main__":
    main()
