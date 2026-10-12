"""
The runs your test needs. ← UNIT 4, MILESTONE 3

Each of your five criteria needs something run against it. A criterion about
the empty-search branch needs an impossible query. One about the fit card needs
the same item run more than once. Working that out is Milestone 3's first step,
and this file is where you write it down.

`run_eval.py` runs everything here five times and writes the run log — five
because your criteria are written out of five.

Three scenarios are filled in to show the shape. Add or change whatever your
own criteria need — these are a starting point, not a fixed set.
"""

SCENARIOS = [
    {
        # A query the data can match. Criterion 1.
        "name": "matching query completes",
        "query": "vintage graphic tee under $30",
        "wardrobe": "example",
        "criterion": 1,
    },
    {
        # A query nothing can match. Criterion 2 — the branch.
        "name": "impossible query stops early",
        "query": "designer ballgown size XXS under $5",
        "wardrobe": "example",
        "criterion": 2,
    },
    {
        # A user with nothing saved. One of unit 4's three failure modes.
        "name": "empty wardrobe",
        "query": "denim jacket under $50",
        "wardrobe": "empty",
        "criterion": None,
    },
    {
        # Criterion 3: state. Any matching query works — what's checked is
        # whether session["selected_item"] is the same item suggest_outfit
        # received, not what the user typed.
        "name": "selected item matches what suggest_outfit receives",
        "query": "denim jacket under $50",
        "wardrobe": "example",
        "criterion": 3,
    },
    {
        # Criterion 4: the fit card. Same query every try, so the SAME item
        # gets a new caption each of the 5 tries (cache is off during
        # run_eval) — checking price/platform mentions and no duplicates.
        "name": "fit card mentions price and platform, no duplicates",
        "query": "vintage graphic tee under $30, size M",
        "wardrobe": "example",
        "criterion": 4,
    },
    {
        # Criterion 5: size matching. "vintage streetwear" matches several
        # L-sized AND several XL-sized listings by keyword — a real test of
        # whether size="L" wrongly pulls in the XL ones (the substring bug
        # the criterion names). Deterministic (no model call), so all 5
        # tries should come back identical.
        "name": "size L search excludes XL listings",
        "query": "vintage streetwear size L",
        "wardrobe": "example",
        "criterion": 5,
    },
]

WARDROBES = ("example", "empty")


def validate() -> list[str]:
    """Complain about anything malformed, before a long run rather than during."""
    problems = []
    for i, scenario in enumerate(SCENARIOS, 1):
        if not scenario.get("query", "").strip():
            problems.append(f"scenario {i} has no query")
        if scenario.get("wardrobe") not in WARDROBES:
            problems.append(
                f"scenario {i} has wardrobe {scenario.get('wardrobe')!r} — "
                f"it should be one of {WARDROBES}"
            )
    return problems
