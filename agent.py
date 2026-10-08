"""
The FitFindr planning loop.

This is the file that makes FitFindr an agent rather than a script. It decides
which tool to run next based on what the last one returned.

If your loop calls all three tools no matter what comes back, you have a list
of function calls. A loop looks at the last result before it picks the next
step. **That branch is the graded part of this unit.**

Build and test your three tools in `tools.py` first. Then come here.

    python agent.py          runs both example paths below
"""

import json
import re

import config
import trace
from tools import suggest_outfit, create_fit_card, compare_price
from generate import ModelUnavailable
from mcp_client import call_tool

# Style memory (stretch): where the wardrobe gets saved between runs.
# Per-user state, not shared data, so it's gitignored.
SAVED_WARDROBE_PATH = config.DATA_DIR / "saved_wardrobe.json"


def load_saved_wardrobe(fallback: dict) -> dict:
    """Load the wardrobe saved from a previous run, or use `fallback` if none exists."""
    if SAVED_WARDROBE_PATH.exists():
        return json.loads(SAVED_WARDROBE_PATH.read_text(encoding="utf-8"))
    return fallback


def _remember_wardrobe_item(wardrobe: dict, item: dict) -> None:
    """Add the newly thrifted item to the wardrobe and persist it to disk."""
    wardrobe_item = {
        "id": f"w_{item['id']}",
        "name": item["title"],
        "category": item["category"],
        "colors": item["colors"],
        "style_tags": item["style_tags"],
        "notes": f"Thrifted from {item['platform']} for ${item['price']:.2f}",
    }
    existing_ids = {w["id"] for w in wardrobe["items"]}
    if wardrobe_item["id"] not in existing_ids:
        wardrobe["items"].append(wardrobe_item)

    config.DATA_DIR.mkdir(exist_ok=True)
    SAVED_WARDROBE_PATH.write_text(json.dumps(wardrobe, indent=2), encoding="utf-8")

# How the query is parsed: regex. Catches "under $30" / "under 30" for a
# price ceiling and "size M" / "size 8" / "size XXS" for a size. Known
# limitation: only the "under $X" phrasing is recognized — "nothing over
# $30" or "$30 max" won't parse to a price. Whatever is left after pulling
# those two out becomes the description.
_PRICE_PATTERN = re.compile(r"under\s*\$?\s*(\d+(?:\.\d+)?)", re.IGNORECASE)
_SIZE_PATTERN = re.compile(r"\bsize\s+([A-Za-z0-9./]+)", re.IGNORECASE)


def _parse_query(query: str) -> dict:
    """Pull a description, a size, and a max_price out of free-typed text."""
    max_price = None
    price_match = _PRICE_PATTERN.search(query)
    if price_match:
        max_price = float(price_match.group(1))

    size = None
    size_match = _SIZE_PATTERN.search(query)
    if size_match:
        size = size_match.group(1)

    description = _PRICE_PATTERN.sub("", query)
    description = _SIZE_PATTERN.sub("", description)
    description = re.sub(r"[,$]", " ", description)
    description = re.sub(r"\s+", " ", description).strip()

    return {"description": description, "size": size, "max_price": max_price}


# ── session state ─────────────────────────────────────────────────────────────

def new_session(query: str, wardrobe: dict) -> dict:
    """
    A fresh session for one user interaction.

    The session is the single source of truth for a run. Every tool result goes
    in here, and the next tool reads it back out.

    You could pass values straight from one call to the next. It would work,
    and you would not be able to test it — you can't print a variable you have
    already overwritten. Going through the session is what makes the state
    visible, and unit 4 has you write a criterion about exactly that.

    Add fields if you need them.
    """
    return {
        "query": query,              # what the user typed
        "parsed": {},                # description / size / max_price you pulled out of it
        "search_results": [],        # everything search_listings returned
        "selected_item": None,       # the one you chose — goes into suggest_outfit
        "wardrobe": wardrobe,        # the user's wardrobe
        "outfit_suggestion": None,   # what suggest_outfit returned
        "price_comparison": None,    # what compare_price returned (stretch)
        "fit_card": None,            # what create_fit_card returned
        "error": None,               # set when the run ended early
    }


# ── planning loop ─────────────────────────────────────────────────────────────

def run_agent(query: str, wardrobe: dict) -> dict:
    """
    Run the loop once and return the finished session.

    Args:
        query:    what the user asked for, in plain language
                  (e.g. "vintage graphic tee under $30, size M").
        wardrobe: a wardrobe dict — get_example_wardrobe() or
                  get_empty_wardrobe() from utils/data_loader.py.

    Returns:
        The session dict. **Check session["error"] first** — if it isn't None,
        the run ended early and the later fields will still be None.

    ─────────────────────────────────────────────────────────────────────────
    TODO — build this, following the branch rule you wrote in Milestone 2.

      1. Start a session with new_session().

      2. Count the times round the loop, and call trace.check_iterations(count)
         on each one before you go again. It raises when the count passes
         MAX_ITERATIONS in config.py — see trace.py.

      3. Parse the query into a description, a size, and a max_price. Regex,
         string splitting, or asking the model are all fine — say which you
         chose in your README. Put the result in session["parsed"].

      4. Call search_listings() with what you parsed.
         Put the results in session["search_results"].

         ⚠️ THIS IS THE BRANCH. If nothing came back:
              - put a message in session["error"] saying what the user could
                change — "No results" is not that message
              - return the session
              - do NOT call suggest_outfit with nothing

      5. Choose an item — the first result is fine. Put it in
         session["selected_item"].

      6. Call suggest_outfit() with the selected item and the wardrobe.
         Put the result in session["outfit_suggestion"].

      7. Call create_fit_card() with the outfit and the item.
         Put the result in session["fit_card"].

      8. Return the session.

    ─────────────────────────────────────────────────────────────────────────
    IN UNIT 4 you come back and add two things:

      • Trace calls. One per step. `trace.step("search_listings", inputs=...,
        returned=...)` — see trace.py. Your README needs the output.

      • A handler for ModelUnavailable, so a bad key produces a message rather
        than a stack trace. The import is already at the top of this file.
    """
    session = new_session(query, wardrobe)

    count = 1
    trace.check_iterations(count)

    session["parsed"] = _parse_query(query)
    parsed = session["parsed"]
    trace.step("_parse_query", inputs=query, returned=parsed)

    search_args = {
        "description": parsed["description"],
        "size": parsed["size"],
        "max_price": parsed["max_price"],
    }
    session["search_results"] = call_tool("search_listings", search_args)
    trace.step(
        "search_listings (via MCP)", inputs=search_args, returned=session["search_results"]
    )

    # ── THE BRANCH ──
    if not session["search_results"]:
        session["error"] = (
            f"No listings matched '{parsed['description']}'"
            + (f", size {parsed['size']}" if parsed["size"] else "")
            + (f", under ${parsed['max_price']:.0f}" if parsed["max_price"] else "")
            + ". Try a wider price ceiling, a different size, or a looser description."
        )
        trace.step("branch", note="empty results — stopping before suggest_outfit")
        return session

    session["selected_item"] = session["search_results"][0]

    session["price_comparison"] = compare_price(session["selected_item"])
    trace.step(
        "compare_price", inputs=session["selected_item"], returned=session["price_comparison"]
    )

    # ── SECOND BRANCH (stretch): the model being unreachable is a different
    # condition than an empty search, and needs its own stop. ──
    try:
        session["outfit_suggestion"] = suggest_outfit(
            session["selected_item"], session["wardrobe"]
        )
        trace.step(
            "suggest_outfit",
            inputs=session["selected_item"],
            returned=session["outfit_suggestion"],
        )

        session["fit_card"] = create_fit_card(
            session["outfit_suggestion"], session["selected_item"]
        )
        trace.step(
            "create_fit_card",
            inputs=session["outfit_suggestion"],
            returned=session["fit_card"],
        )
    except ModelUnavailable as exc:
        session["error"] = str(exc)
        trace.step("branch", note=f"model unavailable — stopping: {exc}")
        return session

    _remember_wardrobe_item(session["wardrobe"], session["selected_item"])

    return session


# ── running it directly ───────────────────────────────────────────────────────

def _show(session: dict) -> None:
    if session["error"]:
        print(f"  stopped: {session['error']}")
        print(f"  fit_card is {session['fit_card']!r} — it should still be None here")
        return

    item = session["selected_item"] or {}
    print(f"  found:    {item.get('title')} — ${item.get('price')} on {item.get('platform')}")
    print(f"  outfit:   {session['outfit_suggestion']}")
    print(f"  fit card: {session['fit_card']}")


if __name__ == "__main__":
    from utils.data_loader import get_example_wardrobe

    print("=== A query the data can match ===")
    _show(run_agent(
        query="looking for a vintage graphic tee under $30",
        wardrobe=get_example_wardrobe(),
    ))

    print("\n=== A query it can't ===")
    _show(run_agent(
        query="designer ballgown size XXS under $5",
        wardrobe=get_example_wardrobe(),
    ))

    print(
        "\nThe second one should stop before the fit card. If both paths look "
        "the same,\nthe branch isn't doing anything yet."
    )
