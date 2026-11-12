"""
Where does the time in one FitFindr run go? (capstone latency breakdown)

    python stage_timing.py [n_runs]

Times each stage of the same sequence run_agent uses, n times with the cache
off: search_listings (MCP), compare_price (MCP), suggest_outfit (model) and
create_fit_card (model). It calls the stages directly, so it adds nothing to
logs/runs.jsonl. Prints mean / median / max per stage, and every slow run's
breakdown, so a tail-latency spike can be pinned on a stage.
"""

import os

os.environ["AI201_CACHE"] = "0"

import statistics
import sys
import time

import agent
from mcp_client import call_tool
from tools import create_fit_card, suggest_outfit
from utils.data_loader import get_example_wardrobe

QUERY = "vintage graphic tee under $30"
STAGES = ["search (MCP)", "compare_price (MCP)", "suggest_outfit", "create_fit_card"]


def timed(fn, *a):
    t = time.perf_counter()
    out = fn(*a)
    return out, time.perf_counter() - t


def main(n: int) -> None:
    parsed = agent._parse_query(QUERY)
    wardrobe = get_example_wardrobe()
    rows = []
    for i in range(n):
        res, t1 = timed(call_tool, "search_listings", parsed)
        item = res[0]
        _, t2 = timed(call_tool, "compare_price", {"item": item})
        outfit, t3 = timed(suggest_outfit, item, wardrobe)
        _, t4 = timed(create_fit_card, outfit, item)
        rows.append([t1, t2, t3, t4])
        print(f"  run {i + 1:>2}: " + "  ".join(f"{t:5.2f}s" for t in rows[-1])
              + f"  total {sum(rows[-1]):5.2f}s", flush=True)

    print(f"\n{'stage':<22}{'mean':>8}{'median':>8}{'max':>8}")
    for j, name in enumerate(STAGES):
        col = [r[j] for r in rows]
        print(f"{name:<22}{statistics.mean(col):8.2f}{statistics.median(col):8.2f}{max(col):8.2f}")
    totals = [sum(r) for r in rows]
    print(f"{'TOTAL':<22}{statistics.mean(totals):8.2f}{statistics.median(totals):8.2f}{max(totals):8.2f}")
    print("\nStage order in each row above: " + ", ".join(STAGES))


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 15)
