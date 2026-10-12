"""
The three FitFindr tools.

Each one is a standalone function you can call and test on its own, before any
of them are wired into the loop. Build and test them one at a time — three
untested tools joined by a loop is one problem that looks like six, because you
can't tell which layer is lying to you.

    search_listings(description, size, max_price)  → list[dict]
    suggest_outfit(new_item, wardrobe)             → str
    create_fit_card(outfit, new_item)              → str

All three are stubs right now. They run and they do nothing — that's the
starting position and it's deliberate.

⚠️ Before you write any of them, fill in the **Tool Inventory** section of your
README (Milestone 2). Four lines per tool: what it does, each input with its
type, exactly what it returns, and what it returns when it has nothing to give.
That last line is what your loop branches on. "Returns a list" earns nothing —
the description has to say what is *in* the list.
"""

import re

import config
from generate import generate
from utils.data_loader import load_listings

# Filler words that carry no search signal in a thrift query — without
# dropping these, every listing scores at least 1 on "a" or "under" alone,
# and the "drop anything scoring 0" step stops doing anything.
STOP_WORDS = {
    "a", "an", "the", "for", "with", "under", "over", "in", "of", "to",
    "and", "or", "size", "looking", "like", "me", "my", "is", "are",
}


def _tokenize(text: str) -> set[str]:
    """Lowercase, split on word boundaries, drop stop words."""
    words = re.findall(r"\w+", text.lower())
    return {w for w in words if w not in STOP_WORDS}


# Matches a letter+digit run first ("W30"), then a plain letter run ("XL"),
# then a plain number ("9", "8.5") — in that order, so a waist+length size
# like "W30L30" splits into {"W30", "L30"} instead of one fused token, and a
# plain shoe size like "US 9" still splits into {"US", "9"}.
_SIZE_TOKEN_PATTERN = r"[A-Za-z]+\d+(?:\.\d+)?|[A-Za-z]+|\d+(?:\.\d+)?"


def _size_tokens(size: str) -> set[str]:
    return set(re.findall(_SIZE_TOKEN_PATTERN, size.upper()))


def _size_matches(query_size: str, listing_size: str) -> bool:
    """
    Compare sizes by exact token, not substring.

    A plain `"s" in "us 9"` is True, and so is `"l" in "xl"` — both wrong.
    Splitting each side into tokens and checking for an exact overlap avoids
    both false matches, and also makes "W30L30" (no space) match "W30 L30"
    (with space) in the data, since both split into the same {"W30", "L30"}.
    """
    return bool(_size_tokens(query_size) & _size_tokens(listing_size))


# ── Tool 1: search_listings ───────────────────────────────────────────────────

def search_listings(
    description: str,
    size: str | None = None,
    max_price: float | None = None,
) -> list[dict]:
    """
    Search the listings data for items matching a description, and optionally a
    size and a price ceiling.

    This is the tool that doesn't call the model, which makes it the easiest one
    to test and the one to move onto MCP in unit 4.

    Args:
        description: keywords describing what the user wants
                     (e.g. "vintage graphic tee").
        size:        a size string to filter by, or None to skip size filtering.
                     Match case-insensitively — "M" should match "S/M".

                     ⚠️ Read the sizes in the data before you reach for a plain
                     substring test. `"s" in "us 9"` is True, and so is
                     `"l" in "xl"`. A filter that returns shoes when someone
                     asked for a small top reads like a broken search, and it
                     will quietly cost you in unit 4 when you test criterion 1.
                     What counts as a size match is part of your spec — decide
                     it and write it into your Tool Inventory.
        max_price:   maximum price, inclusive, or None to skip price filtering.

    Returns:
        A list of matching listing dicts, best match first.
        **Returns an empty list when nothing matches — an empty list, not None,
        and not an exception.** Your loop branches on this.

    Each listing dict has these fields:
        id, title, description, category, style_tags (list), size,
        condition, price (float), colors (list), brand (str or None), platform

    Note that `brand` is None for most listings. That is deliberate and
    realistic — thrift listings often have no brand. If something you write
    assumes a brand is always there, you will find out in unit 4.

    TODO:
        1. Load every listing with load_listings().
        2. Filter by max_price and by size, when each is provided.
        3. Score what's left by keyword overlap with `description`.
        4. Drop anything scoring zero.
        5. Sort by score, highest first, and return the listing dicts —
           at most config.SEARCH_RESULT_LIMIT of them.

    Test it from a terminal before you move on:
        python -c "from tools import search_listings; print(search_listings('graphic tee', max_price=30))"
    """
    listings = load_listings()

    candidates = []
    for listing in listings:
        if max_price is not None and listing["price"] > max_price:
            continue
        if size is not None and not _size_matches(size, listing["size"]):
            continue
        candidates.append(listing)

    query_keywords = _tokenize(description)

    scored = []
    for listing in candidates:
        text = " ".join([
            listing["title"],
            listing["description"],
            " ".join(listing["style_tags"]),
        ])
        listing_keywords = _tokenize(text)
        score = len(query_keywords & listing_keywords)
        if score > 0:
            scored.append((score, listing))

    scored.sort(key=lambda pair: pair[0], reverse=True)
    return [listing for _, listing in scored[: config.SEARCH_RESULT_LIMIT]]


# ── Tool 2: suggest_outfit ────────────────────────────────────────────────────

def suggest_outfit(new_item: dict, wardrobe: dict) -> str:
    """
    Given a thrifted item and the user's wardrobe, suggest one or two outfits.

    This one calls the model, through `generate()`. You don't need to think
    about rate limits — the adapter handles pacing for you.

    Args:
        new_item: a listing dict — the item the user is considering.
        wardrobe: a wardrobe dict with an 'items' key holding a list of items.
                  **It may be empty.** Handle that.

    Returns:
        A non-empty string with outfit suggestions.
        With an empty wardrobe, return general styling advice rather than
        raising or returning "". Unit 4 has you trigger the empty wardrobe on
        purpose, so decide now what it should do.

    TODO:
        1. Check whether wardrobe['items'] is empty.
        2. If it is, ask the model for general styling ideas for this item.
        3. If it isn't, format the wardrobe items into the prompt and ask for
           specific combinations naming pieces the user already owns.
        4. Return the model's response.

    Test it from a terminal before you move on:
        python -c "from tools import suggest_outfit; from utils.data_loader import get_example_wardrobe, load_listings; print(suggest_outfit(load_listings()[0], get_example_wardrobe()))"
    """
    item_desc = (
        f"{new_item['title']} ({new_item['category']}, {new_item['size']}, "
        f"colors: {', '.join(new_item['colors'])})"
    )

    items = wardrobe.get("items", [])
    if not items:
        prompt = (
            f"Someone is considering thrifting this item: {item_desc}.\n"
            "They don't have any wardrobe saved yet. Give general styling "
            "advice for one or two outfits this item could work in."
        )
    else:
        wardrobe_lines = "\n".join(
            f"- {w['name']} ({w['category']}, colors: {', '.join(w['colors'])})"
            for w in items
        )
        prompt = (
            f"Someone is considering thrifting this item: {item_desc}.\n"
            f"Here is their existing wardrobe:\n{wardrobe_lines}\n\n"
            "Suggest one or two outfits that pair the new item with specific "
            "pieces they already own. Name the pieces."
        )

    return generate(prompt)


# ── Tool 3: create_fit_card ───────────────────────────────────────────────────

def create_fit_card(outfit: str, new_item: dict) -> str:
    """
    Write a short caption someone would actually post about the find.

    This calls the model too.

    Args:
        outfit:   the outfit suggestion string from suggest_outfit().
        new_item: the listing dict for the item.

    Returns:
        A two-to-four sentence caption.
        If `outfit` is empty or whitespace, return a descriptive message rather
        than raising.

    The caption should read like a real post rather than a product description,
    mention the item and its price and platform once each, and be specific about
    the vibe.

    It should also come out **differently for different inputs**. If you run
    this three times on the same item and get three word-for-word identical
    strings, it's one of two things, and both are near the top of `config.py`:

        • CACHE_ENABLED — the adapter handed back an answer it already had
        • TEMPERATURE   — at 0.0 the model gives the same words every time

    TODO:
        1. Guard against an empty or whitespace-only `outfit`.
        2. Build a prompt with the item details and the outfit.
        3. Call generate() and return the response.

    Test it from a terminal before you move on:
        python -c "from tools import create_fit_card; from utils.data_loader import load_listings; print(create_fit_card('jeans and white sneakers', load_listings()[0]))"
    """
    if not outfit or not outfit.strip():
        return "No outfit suggestion to caption yet."

    # Unit 4, second improvement: the "before" run showed two captions
    # opening with nearly the same sentence ("Found the ultimate ... and I
    # am *obsessed*"). The added line below asks the model to avoid its
    # default opener instead of leaving that to chance.
    brand = f"{new_item['brand']} " if new_item.get("brand") else ""
    prompt = (
        f"Write a short, casual social-media caption (2-4 sentences) for a "
        f"thrift find: {brand}{new_item['title']}, ${new_item['price']:.0f} "
        f"on {new_item['platform']}. Here's how I'd style it: {outfit}\n\n"
        "Write it like a real post, not a product listing. Mention the price "
        "and platform once, and be specific about the vibe. Avoid a generic "
        "opener like 'Found this ... and I'm obsessed' or 'Scored this ... "
        "for just $X' — write a first sentence specific to this exact item."
    )
    return generate(prompt)


# ── Tool 4 (stretch): compare_price ───────────────────────────────────────────

def compare_price(item: dict) -> str:
    """
    Compare a listing's price to the average price of other listings in the
    same category.

    This is the fourth, stretch tool. It doesn't call the model — it's a
    plain calculation over the listings data, same spirit as search_listings.

    Args:
        item: a listing dict — the item to compare.

    Returns:
        A string describing how the item's price compares to the category
        average (e.g. "$4.00 below the $22.00 average for tops").
        If item is the only listing in its category, returns a message
        saying there's nothing to compare against — never divides by zero.
    """
    others = [
        listing
        for listing in load_listings()
        if listing["category"] == item["category"] and listing["id"] != item["id"]
    ]

    if not others:
        return (
            f"No other {item['category']} listings to compare "
            f"${item['price']:.2f} against."
        )

    average = sum(listing["price"] for listing in others) / len(others)
    diff = abs(item["price"] - average)

    if item["price"] < average:
        return f"${diff:.2f} below the ${average:.2f} average for {item['category']}."
    if item["price"] > average:
        return f"${diff:.2f} above the ${average:.2f} average for {item['category']}."
    return f"Right at the ${average:.2f} average for {item['category']}."
