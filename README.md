# FitFindr

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, every
> command, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> python app.py listings --full -n 6      # read the data (Milestone 1)
> python app.py fields                    # what you can filter on
> python app.py ask 'vintage graphic tee under $30'
> ```
>
> All three tools are stubs, so that last command will do nothing useful yet.
> That's the starting position.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     This is your submission. Fill each section in as you finish the milestone
     it belongs to — don't leave it all to the end.

     Unit 3 asks for the first five sections. Unit 4 adds the five below them.
     Leave the unit 4 sections alone until then; they're here so you know
     what's coming.

     Everything is pasted as TEXT. No screenshots, no images, no video links.
     A typed block of output gets full credit; a picture of the same output
     gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 3 — THE BUILD ═══════════════════════ -->

## What This Does

You tell FitFindr what you're after in plain English — something like "a
vintage graphic tee under $30, size M" — and it goes and finds the single
best-matching listing for you. From there it figures out how that piece
would actually work with clothes you already own (or gives general styling
advice if you haven't saved a wardrobe yet), and wraps it all up in a short
caption you could post without editing. If nothing in the listings matches
what you asked for, it tells you that plainly instead of pretending to find
something.

---

## Tool Inventory

<!-- Four lines per tool. This is worth 2 points and it's the single most
     common place students lose them.

     "Returns a list" earns NOTHING. The description has to say what is IN
     the list.

     The empty case isn't optional either — it's the thing your loop branches
     on, and if you don't decide it here you'll discover it as a crash in
     Milestone 5. -->

### `search_listings`

- **What it does:** Searches the listings data for items matching a text
  description, filtered by size and a price ceiling.
- **Inputs:** `description` (str), `size` (str or None — None skips the size
  filter), `max_price` (float or None — None skips the price filter).
- **Returns:** A list of matching listing dicts, best match first. Each dict
  has `id`, `title`, `description`, `category`, `style_tags` (list), `size`,
  `condition`, `price` (float), `colors` (list), `brand` (str or None — most
  listings have no brand), `platform`.
- **When it has nothing:** Returns an empty list — never `None`, never an
  exception.

### `suggest_outfit`

- **What it does:** Given a thrifted item and the user's wardrobe, suggests
  one or two outfit ideas.
- **Inputs:** `new_item` (dict — a listing dict from `search_listings`),
  `wardrobe` (dict with an `items` key, which may be empty).
- **Returns:** A non-empty string with outfit suggestions, naming specific
  pieces from the wardrobe when there are any.
- **When it has nothing:** If the wardrobe's `items` list is empty, returns
  general styling advice for the item instead of raising or returning an
  empty string.

### `create_fit_card`

- **What it does:** Writes a short caption (2-4 sentences) someone would
  actually post about the thrifted find.
- **Inputs:** `outfit` (str — the suggestion from `suggest_outfit`),
  `new_item` (dict — the listing dict).
- **Returns:** A postable caption that mentions the item's price and
  platform once each.
- **When it has nothing:** If `outfit` is empty or whitespace-only, returns
  `"No outfit suggestion to caption yet."` instead of raising.

---

## Planning Loop

<!-- Your branch rule, stated as a rule — the condition AND both paths — plus
     the file and function that holds it.

     Like this:
       "If search_listings returns an empty list, put a message in the session
        and stop. Otherwise take the first result and go to suggest_outfit."
        — agent.py::run_agent

     The grader checks your code against what you claim here, so the file and
     function have to be real. -->

**Branch rule:** If `search_listings` returns an empty list, put a message
in `session["error"]` naming what to try differently (a wider price, a
different size, a looser description) and stop — `suggest_outfit` is never
called. Otherwise, take the first item from `search_results` as
`selected_item`, pass it with the wardrobe to `suggest_outfit` to get an
outfit suggestion, then pass that outfit and the item to `create_fit_card`
to get the caption.

**Where it lives:** `agent.py::run_agent`

**How the query is parsed:** Regex. `_parse_query()` searches the text for
known patterns — "under $X" for a price ceiling, "size X" for a size —
extracts those values, and treats whatever text is left after removing them
as the description. Known limitation: only the "under $X" phrasing is
recognized, so something like "nothing over $30" or "$30 max" won't parse
to a price ceiling.

**What moves through the session:** `query` and `wardrobe` are set
immediately when the session starts. Then, in order: `parsed`
(description/size/max_price pulled from the query) → `search_results`
(what `search_listings` returned) → `selected_item` (the first result,
chosen from `search_results`) → `outfit_suggestion` (what `suggest_outfit`
returned) → `fit_card` (what `create_fit_card` returned). `error` stays
`None` unless the branch stops the run early — if it's set,
`selected_item`, `outfit_suggestion`, and `fit_card` are still `None`.

---

## Sample Run

<!-- Two things go here.

     1. One FULL query and its output, pasted as text.
     2. Your three per-tool terminal tests — the command and what it printed. -->

**One full query**

```
$ python app.py ask 'vintage graphic tee under $30, size M'

  Found:    Y2K Baby Tee — Butterfly Print — $18.0 on depop

  Outfit:   Here are two outfit suggestions that seamlessly integrate the Y2K butterfly baby tee into their existing wardrobe:

### Outfit 1: High-Contrast Y2K Streetwear (Balanced Proportions)
This outfit plays on the classic Y2K silhouette of a tight top paired with loose, baggy bottoms, using contrast to make the pink, purple, and white butterfly print pop against the dark wash.

*   **Top:** Y2K Butterfly Baby Tee
*   **Bottoms:** Baggy straight-leg jeans (dark wash)
*   **Outerwear:** Vintage black denim jacket (worn off the shoulders or open)
*   **Shoes:** Chunky white sneakers
*   **Accessories:** Black crossbody bag

### Outfit 2: Retro Casual Prep (Soft & Sporty)
This look leans into a softer, retro-casual palette by pairing the pastel tones of the baby tee with warm neutrals, tied together with classic footwear.

*   **Top:** Y2K Butterfly Baby Tee
*   **Bottoms:** Wide-leg khaki trousers
*   **Accessories:** Brown leather belt (to define the waist with the tucked-in tee)
*   **Outerwear:** Black cropped zip hoodie (carried or layered over the shoulders)
*   **Shoes:** Chunky white sneakers

  Fit card: Found my ultimate Y2K butterfly baby tee on Depop for just $18 and I'm officially obsessed 🦋✨ Thinking of styling it either wayyy baggy with dark denim for that classic streetwear contrast, or tucked into wide-leg khakis for a sporty-prep moment. Which vibe are we leaning towards today? 👇

0 model calls this session, 2 served from cache
```

**The three tools, tested one at a time**

```
$ python -c "from tools import search_listings; print(search_listings('graphic tee', max_price=30))"

[{'id': 'lst_002', 'title': 'Y2K Baby Tee — Butterfly Print', 'description': 'Super cute early 2000s baby tee with butterfly graphic. Fitted crop length. Tag says medium but fits like a small.', 'category': 'tops', 'style_tags': ['y2k', 'vintage', 'graphic tee', 'cottagecore'], 'size': 'S/M', 'condition': 'excellent', 'price': 18.0, 'colors': ['white', 'pink', 'purple'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_006', 'title': 'Graphic Tee — 2003 Tour Bootleg Style', 'description': 'Vintage-style bootleg tee with faded graphic. Slightly boxy fit. 100% cotton, soft and worn-in.', 'category': 'tops', 'style_tags': ['graphic tee', 'vintage', 'grunge', 'streetwear', 'band tee'], 'size': 'L', 'condition': 'good', 'price': 24.0, 'colors': ['black'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_017', 'title': 'Mesh Long-Sleeve Top — Black', 'description': 'Sheer black mesh long-sleeve. Great for layering under a graphic tee or over a bralette. Stretchy material, fits true to size.', 'category': 'tops', 'style_tags': ['y2k', 'grunge', 'goth', 'layering'], 'size': 'S/M', 'condition': 'excellent', 'price': 15.0, 'colors': ['black'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_033', 'title': 'Vintage Band Tee — Faded Grey', 'description': 'Faded grey band-style tee with distressed graphic. Crew neck. Fits boxy. Well-loved but no holes or major damage.', 'category': 'tops', 'style_tags': ['vintage', 'grunge', 'band tee', 'graphic tee', 'streetwear'], 'size': 'L', 'condition': 'fair', 'price': 19.0, 'colors': ['grey', 'charcoal'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_011', 'title': 'Low-Rise Cargo Pants — Khaki', 'description': 'Y2K era low-rise cargo pants. Lots of pockets. Khaki color, slightly distressed at the hems. Great for layering with a long tee.', 'category': 'bottoms', 'style_tags': ['y2k', 'cargo', '2000s', 'streetwear'], 'size': 'W29', 'condition': 'fair', 'price': 27.0, 'colors': ['khaki', 'tan'], 'brand': None, 'platform': 'poshmark'}, {'id': 'lst_015', 'title': 'Vintage Graphic Hoodie — Faded Black', 'description': 'Faded black pullover hoodie with barely-visible vintage graphic on the chest. Cozy interior. Some pilling but adds to the worn-in look.', 'category': 'tops', 'style_tags': ['vintage', 'grunge', 'graphic', 'streetwear'], 'size': 'L', 'condition': 'fair', 'price': 26.0, 'colors': ['black', 'charcoal'], 'brand': None, 'platform': 'depop'}]
```

```
$ python -c "from tools import suggest_outfit; from utils.data_loader import get_example_wardrobe, load_listings; print(suggest_outfit(load_listings()[0], get_example_wardrobe()))"

Here are two outfit ideas that seamlessly integrate the vintage Levi's 501 medium wash jeans into your existing wardrobe, creating distinct looks using only pieces you already own:

### Outfit 1: Casual & Sporty (Everyday Uniform)
This look leans into a classic, effortless off-duty aesthetic, balancing the structured medium-wash denim with cozy, relaxed layers.

*   **Bottoms:** Vintage Levi's 501 Jeans (Medium Wash)
*   **Top:** White ribbed tank top
*   **Outerwear:** Oversized grey crewneck sweatshirt (worn over the shoulders or layered on top)
*   **Shoes:** Chunky white sneakers
*   **Accessories:** Black crossbody bag

**Why it works:** The white ribbed tank tucked into the medium-wash 501s creates a clean, timeless silhouette. Throwing on the oversized grey crewneck adds texture and comfort, while the chunky white sneakers and black crossbody tie the casual, street-style elements together.

### Outfit 2: Edgy & Textured (Cool-Weather Contrast)
This look plays with contrasting textures and colors, pairing the vintage blue denim with darker, bolder pieces for an effortlessly cool vibe.

*   **Bottoms:** Vintage Levi's 501 Jeans (Medium Wash)
*   **Top:** Black cropped zip hoodie
*   **Outerwear:** Vintage black denim jacket (layered over the hoodie)
*   **Shoes:** Black combat boots
*   **Accessories:** Brown leather belt

**Why it works:** Layering the black cropped zip hoodie under the vintage black denim jacket creates a great "double-black" contrast against the brighter, medium-wash blue of the jeans. The black combat boots ground the outfit with a rugged edge, and the brown leather belt adds a subtle, earthy accent that breaks up the black-and-blue color palette.
```

```
$ python -c "from tools import create_fit_card; from utils.data_loader import load_listings; print(create_fit_card('jeans and white sneakers', load_listings()[0]))"

Scored these vintage Levi's 501s on Depop for just $38 and I am officially obsessed. The medium wash has that *exact* broken-in, effortless 90s vibe I've been hunting for. Honestly, nothing beats throwing them on with crisp white sneakers and calling it a day. ✨
```

---

## How I Used AI

<!-- Two specific moments. What you asked, what came back, what you changed.

     "I used Claude to help me code" is not enough.

     "I gave Claude my search_listings spec. It returned None on no match
     instead of an empty list, so I changed it" is the level we want. -->

**Moment 1**

- *What I asked for:* Help writing `search_listings`' size-matching logic
  so it wouldn't have the substring bug the stub warns about (`"s" in
  "us 9"` being `True`).
- *What came back:* A token-based matcher that split both the requested
  size and the listing's size on plain alphanumeric runs. It fixed the
  original substring bug, but lecture that same night used an example
  (`W32L30`, no space) that exposed a second bug: a fused waist+length size
  like `"W30L30"` tokenized differently than the data's spaced version
  `"W30 L30"`, so they'd never match even though they mean the same size.
- *What I changed:* We tested the fused-size case directly
  (`_size_matches('W30L30', 'W30 L30')` came back `False`), then rewrote
  the regex to match letter+digit runs first (`[A-Za-z]+\d+`) before
  falling back to plain letters or plain digits, so `"W30L30"` and
  `"W30 L30"` both tokenize to `{"W30", "L30"}`. I re-ran all the earlier
  size tests (`S` vs `US 9`, `L` vs `XL`) to confirm the fix didn't break
  anything that was already working.

**Moment 2**

- *What I asked for:* Feedback on my draft for acceptance criterion 4 (the
  fit card one): *"4 of 5 should give different captions, mentioning
  price platform completely different sentences of same garment."*
- *What came back:* A specific objection, not a rewrite — the sentence
  couldn't be tested as written because "all of them should be different"
  and "in at least 4 of 5 tries" contradict each other (one says every
  caption must be unique, the other implies some can fail). I was asked to
  pick one of two concrete interpretations before going further.
- *What I changed:* I picked the interpretation where price/platform
  mentions are judged per-try at 4 of 5, and uniqueness across all 5 is
  judged separately with zero tolerance. I rewrote the criterion as two
  explicit checks instead of one vague "different captions" claim, and
  tied the "why" to something concrete — `TEMPERATURE = 0.9` in
  `config.py` — instead of the vague "it's user experience" reasoning I
  started with.

---

## Stretch Features

<!-- Declared before being built, per the rubric's all-or-nothing rule. -->

**A fourth tool — `compare_price(item)`:** Compares a listing's price to
the average price of other listings in the same category (e.g. "$4 below
the $22 average for tops"). Called right after an item is selected; the
result is stored in `session["price_comparison"]`. If the item is the only
listing in its category, returns a message saying there's nothing to
compare against instead of dividing by zero.

**A second branch — model failure stops the run cleanly:** If
`suggest_outfit` or `create_fit_card` raises `ModelUnavailable` (bad key,
no network), `run_agent` catches it, puts a message in `session["error"]`,
and returns early — the same pattern as the empty-search branch, but
triggered by a completely different condition (the model being unreachable,
not the search coming up empty).

**Style memory — the wardrobe persists between runs:** After a successful
run, the newly thrifted item is added to the wardrobe and saved to
`data/saved_wardrobe.json` (gitignored — it's per-user state, not shared
data). On the next run, if that file exists, it's loaded instead of
starting from the example wardrobe, so `suggest_outfit` can reference items
found in earlier runs.

### Run showing the fourth tool

The `Price:` line below is `compare_price`'s output, called automatically
right after an item is selected:

```
$ python app.py ask 'vintage graphic tee under $30, size M'

  Found:    Y2K Baby Tee — Butterfly Print — $18.0 on depop
  Price:    $4.00 below the $22.00 average for tops.
  ...
```

### Run showing the second branch

With the API key temporarily broken, `run_agent` stops cleanly instead of
crashing with a stack trace:

```
>>> session = run_agent('vintage graphic tee under $30, size M', get_example_wardrobe())
error: The model rejected your API key. Check GEMINI_API_KEY in your .env file, or create a fresh key at aistudio.google.com.
fit_card: None
```

### Run showing style memory — two runs, the second shaped by the first

Run 1 — wardrobe starts at 10 items, finds the Y2K Baby Tee, saves it:

```
$ python app.py ask 'vintage graphic tee under $30, size M'

  Found:    Y2K Baby Tee — Butterfly Print — $18.0 on depop
  Price:    $4.00 below the $22.00 average for tops.
  ...
```

After run 1, `data/saved_wardrobe.json` has 11 items (the original 10 plus
the Y2K Baby Tee).

Run 2 — a different query, loading the saved wardrobe from run 1:

```
$ python app.py ask 'denim jacket under $50'

  Found:    Denim Jacket — Light Wash, Cropped — $42.0 on poshmark
  Price:    $2.29 below the $44.29 average for outerwear.

  Outfit:   Here are two outfit suggestions using the new light wash cropped denim jacket and pieces from their existing wardrobe:

### Outfit 1: The Contrast Denim Look
* **Top:** White ribbed tank top
* **Bottoms:** Baggy straight-leg jeans (dark wash)
* **Outerwear:** Denim Jacket — Light Wash, Cropped (the new item)
* **Accessories & Shoes:** Brown leather belt, chunky white sneakers, and black crossbody bag

### Outfit 2: Y2K Casual Cool
* **Top:** Y2K Baby Tee (Butterfly Print)
* **Bottoms:** Wide-leg khaki trousers
* **Outerwear:** Denim Jacket — Light Wash, Cropped (the new item)
* **Accessories & Shoes:** Black combat boots and black crossbody bag

**Why it works:** The light wash denim and butterfly baby tee lean into a playful 2000s aesthetic...
  ...
```

"Outfit 2" names the **Y2K Baby Tee (Butterfly Print)** — the item found in
run 1, not part of the original example wardrobe. After run 2, the saved
wardrobe file has 12 items (10 original + the tee from run 1 + the jacket
from run 2).

<!-- ═══════════════════════ UNIT 4 — THE TEST ═══════════════════════

     Don't fill these in during unit 3.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Run Log — Before

<!-- Five criteria, five tries each, in this exact format.

     Five, because your criteria are written out of five. Mark each try PASS
     or FAIL, count the passes, and read that count against your target — a
     row targeting 4 of 5 with three PASS cells is MISSED (3/5).

     `python run_eval.py --label before` runs everything and writes the table
     into results/. Paste it here and fill in the verdicts. -->

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1. matching query completes all three tools | 4 of 5 | FAIL | PASS | FAIL | PASS | PASS | MISSED (3/5) |
| 2. impossible query stops before suggest_outfit | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 3. selected item matches what suggest_outfit receives | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 4. fit card mentions price+platform (4/5), zero duplicate captions | 4/5 + 0 dup | PASS | PASS | PASS | PASS | PASS | MET (5/5, 0 duplicates) |
| 5. size L search excludes XL listings | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |

Full output for all 25 tries: `results/run_2026-10-07_1936_before.md`,
produced by `run_eval.py::main` calling `agent.py::run_agent`.

**Real output from one try** — criterion 1, Try 1, a real miss (not staged):

```
$ python run_eval.py --label before
(scenario: matching query completes, query: "vintage graphic tee under $30")

[1] _parse_query
      in:  vintage graphic tee under $30
      out: dict with keys: description, size, max_price
[2] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: 10 items: Y2K Baby Tee — Butterfly Print, Graphic Tee — 2003 Tour Bootleg Style, Vintage Band Tee — Faded Grey … +7 more
[3] compare_price
      in:  Y2K Baby Tee — Butterfly Print ($18.0, depop)
      out: $4.00 below the $22.00 average for tops.
[4] suggest_outfit
      in:  Y2K Baby Tee — Butterfly Print ($18.0, depop)
      out: Here are two outfit suggestions that pair the Y2K butterfly baby tee with pieces from the existing wardrobe: …
[5] branch
      →    model unavailable — stopping: Couldn't reach the model: 503 UNAVAILABLE. {'error': {'code': 503, 'message': 'This model is currently experiencing high demand. Spikes in demand are usually temporary. Please try again later.', 'status': 'UNAVAILABLE'}}

try 1: stopped early — Couldn't reach the model: 503 UNAVAILABLE...
```

Produced by `run_eval.py::run_once` calling `agent.py::run_agent`.

---

## Verdicts and Diagnoses

<!-- MET or MISSED per criterion against LAST UNIT's target, plus a sentence on
     how you decided.

     Then, for every miss: which of the four places it happened — a tool, the
     loop's branch, the session, or the model's output — AND the mechanism.

     Not a diagnosis:  "The fit card was bad."
     A diagnosis:      "The fit card criterion missed on 2 of 5 items. Both had
                        an empty brand field. My prompt puts the brand in the
                        first sentence, so the card opened with a blank and read
                        like a fragment. The tool worked; the prompt assumed a
                        field that isn't always there."

     Look for a pattern. Three misses on the same tool is one problem, not
     three. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 | Matching query completes all three tools | 4 of 5 | **MISSED (3/5)** | Counted the 5 tries in the run log: 2 stopped early before reaching `create_fit_card`, both with `ModelUnavailable` stopping the run. 3 completed. 3 is below the 4-of-5 target, so this is a miss, not a borderline pass. |
| 2 | Impossible query stops before suggest_outfit | 5 of 5 | **MET (5/5)** | All 5 tries show `stopped early: yes` with a message naming what to change, `selected_item: (none)`, and 0 model calls in the trace. |
| 3 | Selected item matches what suggest_outfit receives | 5 of 5 | **MET (5/5)** | For all 5 tries, `session["selected_item"]`'s title/price/platform exactly match the `in:` value on the `[4] suggest_outfit` trace line. No mismatch in any try. |
| 4 | Fit card mentions price+platform (4/5), zero duplicate captions | 4/5 + 0 dup | **MET (5/5, 0 duplicates)** | All 5 captions mention both `$18` and `Depop` — stronger than the 4/5 required. Comparing all 5 texts pairwise, none are word-for-word identical (tries 1 and 4 open with a near-identical sentence before diverging, which isn't a duplicate by my own criterion's wording, but is a pattern worth watching). |
| 5 | Size L search excludes XL listings | 5 of 5 | **MET (5/5)** | All 5 tries returned the identical 6-item list (expected — no model call, no randomness). None of the 3 XL-only listings that also match "vintage"/"streetwear" keywords appear in any try. |

**Diagnoses**

**Criterion 1 — the only miss.** Place: the model's output, by way of the
`ModelUnavailable` branch — not `search_listings`, not the session, not the
branch logic itself. Mechanism: both failing tries hit a real
`503 UNAVAILABLE` ("This model is currently experiencing high demand")
error from the Gemini API, on the *second* model call of the run (after
`suggest_outfit` had already succeeded once, in try 1's case) or on the
first call (try 3). My `except ModelUnavailable` branch caught both
correctly and stopped the run with a clean message instead of crashing —
the agent did exactly what it was built to do. The tool worked; the model's
own availability didn't.

This is a different mechanism than the one I reasoned about when I set the
4-of-5 target. My original "why" for this criterion was about
`search_listings`' exact-token-overlap matching occasionally missing a
valid phrasing — a problem in my own code. What actually caused both
misses this run was the external API being temporarily overloaded, which
has nothing to do with my search logic. Both misses share the identical
mechanism (a `503` from the same call), so this is one problem occurring
twice, not two separate ones — and it's a problem with the dependency, not
with anything I built.

---

## Loop Trace

<!-- One full run, printed step by step, with the MCP call visible in it.

     `python app.py ask '...' --trace` once you've added the trace.step()
     calls in Milestone 2.

     Worth pasting BOTH the happy path and the empty-search path. The empty
     one should be visibly shorter, because it stops. If your two traces are
     the same length, your branch isn't working — and this is the fastest way
     anyone will ever find that out. -->

**Happy path**

```
$ python app.py ask 'vintage graphic tee under $30, size M' --trace

[1] _parse_query
      in:  vintage graphic tee under $30, size M
      out: dict with keys: description, size, max_price
[2] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: 8 items: Y2K Baby Tee — Butterfly Print, Mesh Long-Sleeve Top — Black, 90s Silk Slip Dress — Floral, Midi Length … +5 more
[3] compare_price
      in:  Y2K Baby Tee — Butterfly Print ($18.0, depop)
      out: $4.00 below the $22.00 average for tops.
[4] suggest_outfit
      in:  Y2K Baby Tee — Butterfly Print ($18.0, depop)
      out: Here are two outfit ideas that pair the Y2K Butterfly Baby Tee with your light wash, cropped denim jacket: …
[5] create_fit_card
      in:  Here are two outfit ideas that pair the Y2K Butterfly Baby Tee with your light wash, cropped denim jacket: …
      out: Found this absolute gem on depop for just $18 and I am never taking it off. 🦋✨ Giving major Y2K street style w…
```

**Empty search**

```
$ python app.py ask 'designer ballgown size XXS under $5' --trace

[1] _parse_query
      in:  designer ballgown size XXS under $5
      out: dict with keys: description, size, max_price
[2] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: [] (empty)
[3] branch
      →    empty results — stopping before suggest_outfit
```

The happy path takes 5 steps; the empty-search path stops at 3 and never
reaches `suggest_outfit` or `create_fit_card` — the branch is visibly doing
something, not just present in the code.

**On the MCP move:** Moved `search_listings` onto MCP (`mcp_server.py`),
with the tool description naming the size-matching behavior (token-based,
not substring), stating `max_price` as a USD ceiling, and stating the
empty-list case explicitly — since that description is now a contract read
by something that can't see my code. `run_agent` calls it through
`mcp_client.call_tool("search_listings", {...})` instead of a direct
import. Nothing behaved differently afterward: the same matching query
found the same item, and the empty-search branch still stopped with 0
model calls, exactly as before the move. `suggest_outfit` and
`create_fit_card` are untouched.

**Failure modes triggered on purpose:**

1. **Empty search** — `python app.py ask 'designer ballgown size XXS under $5'`
   → `No listings matched 'designer ballgown', size XXS, under $5. Try a
   wider price ceiling, a different size, or a looser description.` Stops
   before `suggest_outfit`, 0 model calls. No new handler needed — this is
   `search_listings` returning `[]` plus the existing branch.
2. **Empty wardrobe** — `python app.py ask 'denim jacket under $50'
   --empty-wardrobe` → `suggest_outfit` returned two full general-styling
   outfit suggestions (not a crash, not an empty string) despite having no
   saved items to reference. No new handler needed — this was already
   `suggest_outfit`'s designed behavior from unit 3.
3. **Model unavailable** — corrupted one character of `GEMINI_API_KEY` in
   `.env`, then ran a query never asked before (`'leather belt brown
   braided under $15'`, to rule out a cached answer) → `The model rejected
   your API key. Check GEMINI_API_KEY in your .env file, or create a fresh
   key at aistudio.google.com.` No raw stack trace, no hang. No new handler
   needed — `run_agent`'s `except ModelUnavailable` catch (built as unit
   3's stretch second branch) already covers this. Key was restored
   immediately after, confirmed by `python test.py` passing 10/10 again.

---

## The Improvement

<!-- What you changed, why your diagnosis pointed at it, and the after-run in
     the same table format. One change, measured properly.

     `python run_eval.py --label after` -->

**What I changed:** In `generate.py`'s `generate()`, broadened the retry
condition from rate-limit errors only (`429`, "resource exhausted", "rate
limit") to also include `503`/"unavailable"/"high demand" errors. Before
this change, a `503` went straight to `ModelUnavailable` and killed the
run on the first occurrence; now it retries with the same backoff logic
already used for rate limits.

**Which failure it was meant to fix:** Criterion 1's diagnosed miss —
both failing tries in the "before" run hit a real `503 UNAVAILABLE` from
the Gemini API, which the old code treated as a permanent failure (same
bucket as a bad API key) instead of a transient one worth retrying.

### Run Log — After

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1. matching query completes all three tools | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 2. impossible query stops before suggest_outfit | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 3. selected item matches what suggest_outfit receives | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 4. fit card mentions price+platform (4/5), zero duplicate captions | 4/5 + 0 dup | PASS | PASS | PASS | PASS | PASS | MET (5/5, 0 duplicates) |
| 5. size L search excludes XL listings | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |

Full output: `results/run_2026-10-12_0029_after.md`, produced by
`run_eval.py::main` calling `agent.py::run_agent`.

**Did it help, and how do I know:** Yes. Criterion 1 went from 3/5 to
5/5 — the only criterion that was missing its target before is now
meeting it, and nothing else regressed (criteria 2-5 are identical,
5/5, to the before run). This isn't just the API behaving better this
time by luck: the "after" run's raw output shows the new retry path
firing for real —

```
[service unavailable] service pushed back. Waiting 1s (attempt 1 of 5). This is the limiter doing its job, not a bug.
```

— four separate times during the run. Each time, the old code would have
raised `ModelUnavailable` immediately and ended that scenario's run early;
the new code waited 1 second, retried, and succeeded. The fix is doing
exactly what the diagnosis said it should.

---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped where
     you did. "I ran out of time" is fine if it's true. Pretending nothing is
     left is not. -->

Nothing is currently missed — all five criteria are MET (5/5) after the
improvement. Two things worth naming honestly rather than papering over:

- **The fix doesn't eliminate `503`s, it just rides through them.** If the
  Gemini API went down for longer than `MAX_RETRIES` (5 attempts) worth of
  backoff, the run would still fail with a `RuntimeError`. I haven't
  tested that longer-outage case — doing so would mean simulating an
  extended outage, which isn't something I can trigger on the real
  service on demand.
- **Criterion 4's near-duplicate pattern** (tries 1 and 4 in the "before"
  run opened with nearly the same sentence) didn't reappear verbatim in
  the "after" run, but I didn't dig into *why* the model favors certain
  openings at `TEMPERATURE = 0.9`. It's not a miss against my criterion as
  written, but if I tightened criterion 4 to check opening-sentence
  similarity instead of exact duplication, I'd expect to find more of
  this pattern. I didn't chase it because it's outside what my current
  criterion actually measures, not because I think it's a non-issue.

---

## Stretch Features — Unit 4

<!-- Declared before being built, per the rubric's all-or-nothing rule. -->

**A second tool moved onto MCP:** `compare_price` gets registered on
`mcp_server.py` alongside `search_listings`. `run_agent` calls it through
`mcp_client.call_tool` instead of a direct import.

**Retry with looser constraints:** When `search_listings` (via MCP) comes
back empty and a size was specified, `run_agent` retries once without the
size filter. If that retry finds something, the run continues with those
results and the message says the size filter was dropped. If it's still
empty, the existing empty-search message and branch apply unchanged.

**A second measured improvement:** The diagnosis in "What's Still Broken"
names a real pattern — two fit cards in the "before" run opened with
nearly identical sentences. The change: tighten `create_fit_card`'s prompt
to explicitly ask for a distinct opening line, instead of letting the
model default to a favorite phrasing. Re-run the full eval afterward and
report honestly whether the pattern actually goes away.

### Run showing the second MCP tool and the retry

```
$ python app.py ask 'denim jacket size XXL'

[1] _parse_query
      in:  denim jacket size XXL
      out: dict with keys: description, size, max_price
[2] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: [] (empty)
[3] search_listings (via MCP, retry without size)
      in:  dict with keys: description, size, max_price
      out: 8 items: Denim Jacket — Light Wash, Cropped, Vintage Levi's 501 Jeans — Medium Wash, 90s Track Jacket — Navy/White Stripe … +5 more
      →    dropped size filter ('XXL') after empty search
[4] compare_price (via MCP)
      in:  Denim Jacket — Light Wash, Cropped ($42.0, poshmark)
      out: $2.29 below the $44.29 average for outerwear.
[5] suggest_outfit
      ...
[6] create_fit_card
      ...

  (no exact match — dropped size XXL and retried)
  Found:    Denim Jacket — Light Wash, Cropped — $42.0 on poshmark
```

No size `XXL` exists in the data for a denim jacket, so the sized search
correctly comes back empty; the retry drops the size filter, finds the
jacket by description alone, and both the trace and the printed output
name exactly what was dropped. Confirmed the retry doesn't paper over a
truly impossible query: `'designer ballgown size XXS under $5'` still
retries, is still empty, and still stops with the normal message and 0
model calls — the same result as before this stretch was added.

### Run Log — Second Improvement

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1. matching query completes all three tools | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 2. impossible query stops before suggest_outfit | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 3. selected item matches what suggest_outfit receives | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 4. fit card mentions price+platform (4/5), zero duplicate captions | 4/5 + 0 dup | PASS | PASS | PASS | PASS | PASS | MET (5/5, 0 duplicates) |
| 5. size L search excludes XL listings | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |

Full output: `results/run_2026-10-12_0103_after2.md`.

**Did it help, and how do I know:** Mostly yes, with an honest caveat. On
the actual criterion-4 scenario (5 tries on the Y2K Baby Tee), the fix
worked cleanly — all 5 opening sentences are now genuinely distinct
("Pulled this pastel butterfly baby tee...", "Pastel butterflies and a
tiny cropped fit...", "That rhinestone butterfly graphic...", "That
butterfly print is straight out of 2003...", "Channeling my inner 2003
pop star..."), with zero shared openers, compared to the "before" run
where two captions opened almost identically.

But I also ran three quick extra captions on a *different* item (the
Levi's jeans) to double check, and two of those three opened with
"Nothing beats a broken-in pair of 501s..." / "Nothing beats that
perfectly broken-in vintage denim..." — a new near-duplicate pattern,
just a different sentence than before. So the fix removed the specific
opener I diagnosed ("Found this... and I'm obsessed"), but it didn't
remove the model's general tendency to settle into a favorite phrasing
at `TEMPERATURE = 0.9` — it just moved which phrasing that is. My actual
criterion 4, as written, only checks for word-for-word duplicates (which
still passes 5/5 both before and after), so this doesn't show up as a
regression against what I measured — but it's a real limit of the fix
worth naming honestly rather than claiming a cleaner win than I actually
got.

<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 3

       [ ] criteria.md has five numbered criteria, each with a target
       [ ] Each criterion has a reason underneath it
       [ ] All five unit 3 sections above have real content
       [ ] Tool Inventory: all three tools, inputs WITH TYPES, a specific
           return value, and the empty case
       [ ] Planning Loop names the branch rule and agent.py::run_agent
       [ ] Sample Run: one full query plus the three per-tool tests, as text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN, you submit the same one
           next unit

     SUBMISSION CHECKLIST — unit 4

       [ ] mcp_server.py exists with one tool registered
           (or a written record of exactly where the rewire broke)
       [ ] Run Log — Before, five criteria, five tries each
       [ ] Real output pasted underneath, naming file and function
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, naming a place AND a mechanism
       [ ] Loop Trace, with the MCP call visible in it
       [ ] All three failure modes triggered and handled
       [ ] One improvement, with Run Log — After in the same format
       [ ] What's Still Broken
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository. Your commit history is what
     shows your criteria existed before your results did.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**


---

## Capstone

**What This Extends**

This extends **FitFindr** (the multi-tool thrifting agent from units 3 and 4: `search_listings` over MCP, `compare_price`, `suggest_outfit`, `create_fit_card`, wired together by the loop in `agent.py::run_agent`). What's new is an operational layer around that existing agent: a structured run log (`logs/runs.jsonl`) that records every run, including failed ones, a measured cost per run, and a run path that someone else can follow from `RUNNING.md` alone. The agent's tools and planning loop are unchanged.

**The Shape**

**Shape A — deploy and instrument, on Path B (local with logs).** Every run of the agent writes one JSON record with a timestamp, the query that came in, what came out, how long it took, token usage and a status. A run that ends early or crashes writes a record too. The system is started by one documented command and I include a committed log from real runs. I chose Path B because the agent only calls a hosted model API (nothing local) but hosting would add a signup and a card for no grading benefit.

Out of scope, on purpose:
- No new tools and no changes to the planning loop's branching. The agent's behavior stays as unit 4 left it.
- No hosting (Path A), no web UI work, and no changes to `serve.py`.
- No changes to the parsing or search logic, even though the regex parser has known limits (see What's Still Broken in the unit 4 sections above).


**Running It**

**Path B — local with logs.** FitFindr runs on my machine and calls a hosted model API, so there is nothing to deploy and no model file to download. The exact start command, the Python version (tested on 3.12.3, not 3.14), the pinned dependencies and the `.env` setup are in [RUNNING.md](RUNNING.md). I tested it by cloning the repo into a fresh folder, creating a new venv, running `pip install -r requirements.txt`, then `python test.py` (10 of 10 passed) and `python app.py ask 'vintage graphic tee under $30'`, which produced a fit card and a log record (`status ok, 12.2 s, 551 + 307 tokens`). I expected the instructions to fail the first time; they didn't, so I found nothing to fix. Without a real key `python test.py` says "no key to test with", which is a clear message for a reader. The only environment trap I hit was running the system Python instead of the venv, which fails with `No module named 'mcp'`; RUNNING.md now says so.

**Instrumentation**

`runlog.py::log_run` appends one JSON line per run to `logs/runs.jsonl`. It is called from `agent.py::run_agent`, which wraps the unchanged loop (`_run_loop`) in a try/except, so runs that crash write a record too. Fields: `timestamp` (UTC), `query` (what came in), `status` (`ok`, `empty_search`, `model_unavailable` or `exception`), `output` (the fit card or the stop message), `error`, `selected_item_id`, `dropped_constraint`, `duration_s`, `cache_enabled`, `model_calls`, `prompt_tokens`, `output_tokens`. Token counts are the difference in `generate.token_counts()` before and after the run.

Twelve real entries, copied from `logs/runs.jsonl` in order. Only `output` and `error` are shortened to 70 characters here for readability; the file has them in full. The first entry is a crash (system Python without the `mcp` package), the fourth is a wrong-key run, and the second is an impossible query:

```
{"timestamp": "2026-11-12T02:23:22+00:00", "query": "designer ballgown size XXS under $5", "status": "exception", "output": null, "error": "MCPError: Couldn't call 'search_listings' over MCP: No module named 'm…", "duration_s": 0.004, "cache_enabled": true, "model_calls": 0, "prompt_tokens": 0, "output_tokens": 0}
{"timestamp": "2026-11-12T02:24:00+00:00", "query": "designer ballgown size XXS under $5", "status": "empty_search", "output": "No listings matched 'designer ballgown', size XXS, under $5. Try a wid…", "error": "No listings matched 'designer ballgown', size XXS, under $5. Try a wid…", "selected_item_id": null, "dropped_constraint": null, "duration_s": 8.915, "cache_enabled": true, "model_calls": 0, "prompt_tokens": 0, "output_tokens": 0}
{"timestamp": "2026-11-12T02:24:17+00:00", "query": "vintage graphic tee under $30", "status": "ok", "output": "That pink and purple butterfly graphic is straight out of a 2000s musi…", "error": null, "selected_item_id": "lst_002", "dropped_constraint": null, "duration_s": 11.625, "cache_enabled": false, "model_calls": 2, "prompt_tokens": 569, "output_tokens": 332}
{"timestamp": "2026-11-12T02:24:33+00:00", "query": "oversized wool coat under $60", "status": "model_unavailable", "output": "The model rejected your API key. Check GEMINI_API_KEY in your .env fil…", "error": "The model rejected your API key. Check GEMINI_API_KEY in your .env fil…", "selected_item_id": "lst_003", "dropped_constraint": null, "duration_s": 9.633, "cache_enabled": false, "model_calls": 1, "prompt_tokens": 0, "output_tokens": 0}
{"timestamp": "2026-11-12T02:29:17+00:00", "query": "vintage graphic tee under $30", "status": "ok", "output": "Pastel butterflies and the exact kind of tiny baby tee fit I’ve been h…", "error": null, "selected_item_id": "lst_002", "dropped_constraint": null, "duration_s": 12.823, "cache_enabled": false, "model_calls": 2, "prompt_tokens": 629, "output_tokens": 375}
{"timestamp": "2026-11-12T02:29:23+00:00", "query": "90s track jacket in size M", "status": "ok", "output": "That crisp navy and white piping is doing all the 90s heavy lifting. S…", "error": null, "selected_item_id": "lst_004", "dropped_constraint": null, "duration_s": 5.609, "cache_enabled": false, "model_calls": 2, "prompt_tokens": 566, "output_tokens": 309}
{"timestamp": "2026-11-12T02:29:29+00:00", "query": "silk slip dress in midi length under $40", "status": "ok", "output": "Scored this dreamy 90s floral midi silk slip dress on Depop for just $…", "error": null, "selected_item_id": "lst_013", "dropped_constraint": null, "duration_s": 5.696, "cache_enabled": false, "model_calls": 2, "prompt_tokens": 631, "output_tokens": 405}
{"timestamp": "2026-11-12T02:29:35+00:00", "query": "platform sneakers size 8", "status": "ok", "output": "These chunky platform sneakers are giving major '90s model-off-duty en…", "error": null, "selected_item_id": "lst_019", "dropped_constraint": null, "duration_s": 6.071, "cache_enabled": false, "model_calls": 2, "prompt_tokens": 585, "output_tokens": 361}
{"timestamp": "2026-11-12T02:29:40+00:00", "query": "denim jacket under $50", "status": "ok", "output": "That vintage Wrangler denim fit is finally hitting the sweet spot with…", "error": null, "selected_item_id": "lst_007", "dropped_constraint": null, "duration_s": 5.714, "cache_enabled": false, "model_calls": 2, "prompt_tokens": 611, "output_tokens": 352}
{"timestamp": "2026-11-12T02:29:46+00:00", "query": "vintage graphic tee under $30", "status": "ok", "output": "Channeling total 2000s mall-rat energy with this tiny butterfly tee I …", "error": null, "selected_item_id": "lst_002", "dropped_constraint": null, "duration_s": 5.585, "cache_enabled": false, "model_calls": 2, "prompt_tokens": 550, "output_tokens": 318}
{"timestamp": "2026-11-12T02:29:52+00:00", "query": "90s track jacket in size M", "status": "ok", "output": "Nothing beats that crisp 90s athletic drape, especially when you find …", "error": null, "selected_item_id": "lst_004", "dropped_constraint": null, "duration_s": 5.697, "cache_enabled": false, "model_calls": 2, "prompt_tokens": 527, "output_tokens": 280}
{"timestamp": "2026-11-12T02:30:16+00:00", "query": "silk slip dress in midi length under $40", "status": "ok", "output": "Nothing beats a dreamy 90s floral silk midi when you want to lean into…", "error": null, "selected_item_id": "lst_013", "dropped_constraint": null, "duration_s": 24.421, "cache_enabled": false, "model_calls": 2, "prompt_tokens": 630, "output_tokens": 389}
```

Failed runs are in the list above: entry 1 is `status exception` (a crash, re-raised after logging), entry 2 is `empty_search`, and entry 4 is `model_unavailable` (wrong API key, 0 tokens, because the request was rejected).

**What It Costs**

Measured with `measure_cost.py`: 10 runs through `agent.run_agent` with the cache off (so every token is real), five different queries run twice, each run given the same fresh example wardrobe so style memory could not lengthen the prompts. All 10 finished `ok`. Numbers come from the service's own usage report (`generate.token_counts()`), summed per run in the log, not from a pricing page.

| Measure | Mean | Min | Max |
|---|---|---|---|
| Model calls per run | 2.00 | 2 | 2 |
| Prompt tokens | 590.4 | 527 | 631 |
| Output tokens | 352.3 | 280 | 405 |
| Total tokens | 942.7 | | |
| Seconds per run | 8.54 | 5.58 | 24.42 |

The mean of 8.5 s is pulled up by one slow run; the typical run is about 6.2 s (see the stage breakdown under The Improvement, which also explains the slow runs).

Dollars need a price, and a price is not something I can measure. The listed price for this model is $0.30 per million input tokens and $2.50 per million output tokens (from several third-party price pages, e.g. [eesel.ai](https://eesel.ai/blog/gemini-3-5-flash-lite-pricing) and [pricepertoken.com](https://pricepertoken.com/pricing-page/model/google-gemini-3.5-flash-lite); I could not open Google's own page, so treat the rate as unconfirmed). On the free tier the real bill is $0.

- Input: 590.4 × $0.30 / 1,000,000 = $0.000177
- Output: 352.3 × $2.50 / 1,000,000 = $0.000881
- **One run ≈ $0.00106**
- 100 people a day, one run each: 100 × $0.00106 = **$0.106 a day**, about $3.17 over 30 days.

Output tokens are about 83% of the cost, even though there are fewer of them than input tokens, because they are priced more than eight times higher.

**What It Costs, after my improvement**

Same method, from the log, priced at $0.30 in and $2.50 out per million tokens (third-party pages, unconfirmed; the real free-tier bill is $0). Before the improvement an average two-call run used 602.7 prompt and 369.3 output tokens, which is $0.00110. After capping the outfit suggestion at 60 words it used 403.1 prompt and 157.6 output tokens, which is $0.00052. At my budget of 100 users making 100 runs each (10,000 runs) that is about $5 a day instead of about $11. (Means are over every `ok` two-call run in each batch of trials, 53 before and 48 after.)

**Run Log and Verdicts (my criteria)**

These are the five criteria I wrote myself in `criteria.md` ("Capstone criteria (unit 9) - mine"). They were committed in `57f3c0e`, before any of these results. They are scored by `capstone_trials_mine.py`. Criterion 2 is scored by hand with two classmates and **has not been scored yet** (see What's Still Broken). Criterion 1 runs 5 trials because it says "5 of 5 trials"; the others run 3. Raw output: `results/capstone_mine_before.md`, `results/capstone_mine_after.md`.

| Criterion | Target | Before | After |
|---|---|---|---|
| 1. Every run leaves exactly one record | batch of 5 adds 5 lines, 5 of 5 trials | 5 of 5 trials MET | 5 of 5 trials MET |
| 2. A classmate starts it alone from RUNNING.md | 2 of 2 testers | not scored yet | not scored yet |
| 3. Cost per run | at most $0.001 | $0.00103, $0.00113, $0.00114 **MISSED** | $0.00051, $0.00052, $0.00050 MET |
| 4. Bad input does not crash | 5 of 5 | 4/5 in all three trials **MISSED** (strict check) | 5/5 in all three trials MET |
| 5. Original behavior preserved | 3 of 3 comparisons | 3/3 in all three trials MET | 3/3 in all three trials MET |

One honest detail about criterion 4. The first "before" run reported 5/5, because my script counted any non-empty output as "a message naming the problem". I then ran the CLI by hand and saw that `python app.py ask ""` does not run the agent. It drops into the interactive prompt and prints "Ask for something, or press Enter on an empty line to quit.", which names no problem. I tightened the check to require a real problem message ("No listings matched", "rejected your API key" or "Nothing to search for") and re-scored. The before verdict above is the strict one (4/5, the empty query failing each time). The loose 5/5 is still in `results/capstone_mine_before.md`.

**Diagnoses.**
- **Criterion 3 (cost).** Output tokens were about 83% of the cost, because they are priced more than eight times higher than input. The longest and least bounded output was `suggest_outfit` ("one or two outfits", no length limit), and its text is also the input to `create_fit_card`, so it inflated both calls. That is the stage to change.
- **Criterion 4 (empty query).** The failing stage is `app.py::cmd_ask`. An empty argument is falsy, so `if args.query:` skipped the agent and fell into the interactive prompt branch. The agent itself was fine.
- **Criteria 1 and 5** held in every trial. Criterion 5 is a regression check that is easy by design: the selected item comes from search, not from the model, so it was never likely to fail.

**The Improvement (my criteria)**

Two small changes, one per missed criterion, each followed by a full re-run.
1. **Cost** (`tools.py`): both `suggest_outfit` prompts now end with "Keep the whole answer under 60 words." Result: $0.0011 to $0.0005 per run, and criterion 3 went from MISSED to MET with about 2x headroom. That is a bigger drop than I expected. I only needed about 10%.
2. **Empty query** (`app.py::cmd_ask`): an empty or whitespace-only `ask` argument now prints "Nothing to search for. Type what you're looking for, for example: vintage graphic tee under $30" and writes one record (status `empty_search`, 0 model calls), so it still counts as one run with one record. Result: criterion 4 went from 4/5 to 5/5.

What it cost, and what I did not check: outfits are shorter, and I only looked at samples. They still name specific pieces and the fit cards still mention price and platform, and `test.py` still passes 10 of 10, but I did **not** re-run the unit 3 criteria, so I cannot say the shorter outfits did not hurt fit-card quality in general. Also, the empty-query check lives in the CLI, so a caller using `run_agent("")` directly gets the original "No listings matched" message instead.

**What's Still Broken (my criteria)**
- **Criterion 2 is unscored.** It needs two classmates following RUNNING.md alone, with a timer. I should also do a dry run on a fresh clone first, because their other projects may not have `mcp` installed. This is the most important gap.
- **Criterion 3 rests on an unconfirmed price.** The rates come from third-party pages, not Google's own, and on the free tier my real bill is $0.
- **Criterion 4's check is tied to three exact phrases.** A reworded error message would fail the harness even if it were fine for a user.
- **My criteria are inconsistent about trials.** The section intro says 3 trials each, but criterion 1 says "5 of 5 trials". I ran 5 for criterion 1 and 3 for the rest.
- **The timeout change from the first draft is still in the code** (`generate.py::_call_with_timeout`) with no demonstrated benefit (see below). I still think it should be reverted.
- **About 58% of a normal run is MCP startup**, unchanged.

---

*The sections below were written against Claude's first draft of the criteria, which I superseded. They are kept as a record of what happened, not as my verdicts.*

**Run Log and Verdicts (superseded draft criteria)**

> **Scored against Claude's first draft of the criteria, not mine.** These five criteria were drafted by Claude, not by me, and have since been superseded (see How I Used AI). The tables below are kept as a record. The results for my own criteria are further down.

Five criteria from `criteria.md` ("Capstone criteria (unit 9) — Claude's first draft"), three trials each, run by `capstone_trials.py --label before` with the cache off. Each criterion is scored from the records the logger wrote.

| Criterion | Target | Trial 1 | Trial 2 | Trial 3 | Verdict |
|---|---|---|---|---|---|
| 1. Every run leaves exactly one complete record | 10 of 10 | 10/10 | 10/10 | 10/10 | MET |
| 2. Bad input and a failing model never crash or look like success | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 3. Normal run under 10 s (cache off, 10 runs in a row) | 9 of 10 | 9/10 | 9/10 | 9/10 | MET (at the edge) |
| 4. Tokens per run: mean ≤ 1,200, max ≤ 2,000 | both | mean 960, max 1098 | mean 952, max 1070 | mean 941, max 1114 | MET |
| 5. A matching query still returns a fit card | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |

Real output underneath. All of it is from `results/capstone_before.md` and the harness output, produced by `capstone_trials.py` (functions `trial_1` to `trial_5`) calling `agent.py::run_agent`.

Criterion 1, trial 1 (per input: query, bad key?, new log lines, outcome, ok):

```
('vintage graphic tee under $30', False, 1, 'returned', True)
('90s track jacket in size M', False, 1, 'returned', True)
('denim jacket under $50', False, 1, 'returned', True)
('silk slip dress in midi length under $40', False, 1, 'returned', True)
('designer ballgown size XXS under $5', False, 1, 'returned', True)
('designer ballgown size XXS under $5', False, 1, 'returned', True)
('vintage graphic tee under $30', True, 1, 'returned', True)
('vintage graphic tee under $30', True, 1, 'returned', True)
('', False, 1, 'returned', True)
('vintage graphic tee vintage graphic tee …', False, 1, 'returned', True)
```

Criterion 2, trial 1 (per case; the CLI was run as a subprocess to check for a Traceback):

```
('empty string', 'raised=False', 'no_traceback=True', 'status=empty_search', True)
('whitespace only', 'raised=False', 'no_traceback=True', 'status=empty_search', True)
('3,000 characters', 'raised=False', 'no_traceback=True', 'status=ok', True)
('wrong API key', 'raised=False', 'no_traceback=True', 'status=model_unavailable', True)
('impossible query', 'raised=False', 'no_traceback=True', 'status=empty_search', True)
```

Criteria 3 and 4, harness output (`trial_3_4`, runs over 10 s as `(duration_s, model_calls)`):

```
trial 1:
  C3 9/10 under 10s, slow=[(15.293, 2)]
  C4 mean 960 max 1098
trial 2:
  C3 9/10 under 10s, slow=[(20.436, 2)]
  C4 mean 952 max 1070
trial 3:
  C3 9/10 under 10s, slow=[(21.645, 2)]
  C4 mean 941 max 1114
```

Criterion 5, trial 1: 5 of 5 runs returned a non-empty `session["fit_card"]` with `session["error"] is None` (the five records are in `results/capstone_before.md`).

**Verdicts and diagnoses.** I met all five in all three trials, so there is no miss to diagnose, and I looked hard at whether the targets were just easy.

- **Criteria 1, 2 and 5** passed legitimately. I checked what the malformed inputs actually did: an empty string and whitespace both stop at `empty_search` with a message, and the 3,000-character query matches a listing and completes. So criterion 2 was a real test, and the agent held up.
- **Criterion 3 is the weak pass.** It came out exactly 9 of 10 in every trial, and every trial had exactly one run of 15 to 22 s while the other nine mostly took 5.6 to 7.8 s (the longest of them, 9.7 s, was still under the limit). The slow runs are not random model latency. They are the free-tier quota: `generate.py` allows 15 requests per minute (`REQUESTS_PER_MINUTE`), and the test fires one run every ~6 s at 2 model calls each, about 20 calls a minute. The slow run comes when the 15th call of the minute lands, and the harness output has the matching pauses (`[rate limit] 15 requests used this minute. Waiting 16s / 13s / 10s`). So the stage is the pacing in `generate.py::_wait_for_slot`, and the mechanism is that the criterion's "10 runs in a row" pattern exceeds the quota by itself. A single user asking one question a minute would never see it. I never changed the criterion because it was met.
- **Criterion 4 was set too low.** Means were 941 to 992 against a 1,200 target, and the max was 1,070 to 1,218 against 2,000. I would tighten it to a mean of at most 1,000 and a maximum of 1,250.
- **Pattern:** the one real weakness (latency under repeated use) comes from a single stage, the request pacing, and it makes the latency criterion measure the quota, not the system.

**The Improvement (superseded draft criteria)**

*What I first thought, and what I changed.* A stage breakdown (`stage_timing.py`, 15 runs, cache off) gave a typical run of about 6.2 s: the two MCP calls cost about 1.8 s each (about 58% of a normal run, because each call starts a new server process in `mcp_client.py::_call`), and the two model calls about 1.5 s and 0.9 s. The one slow run, 23 s, had `create_fit_card` at 17.6 s against a 0.9 s median. I read that as a hung model request and changed `generate.py` to stop waiting after `MODEL_TIMEOUT_S = 6.0` s and retry (`_call_with_timeout`, a daemon thread; commit "Improvement: abandon and retry a model call that takes over 6s"). My first version used the SDK's own timeout, and testing it showed the API rejects any deadline under 10 s (`Minimum allowed deadline is 10s`), which would have broken every call, so I enforce the timeout in our own code. I verified both the forced-timeout path (5 retries, then a clean error) and a normal call.

*Run log after the change* (`capstone_trials.py --label after`, same harness, same format):

| Criterion | Target | Trial 1 | Trial 2 | Trial 3 | Verdict |
|---|---|---|---|---|---|
| 1. Every run leaves exactly one complete record | 10 of 10 | 10/10 | 10/10 | 10/10 | MET |
| 2. Bad input and a failing model never crash or look like success | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 3. Normal run under 10 s | 9 of 10 | 9/10 | 9/10 | 9/10 | MET (at the edge) |
| 4. Tokens per run | mean ≤ 1,200, max ≤ 2,000 | mean 992, max 1218 | mean 992, max 1073 | mean 949, max 1038 | MET |
| 5. A matching query still returns a fit card | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |

Side by side with "Run Log and Verdicts" above: identical verdicts, and the slow run in each batch is still there (before: 15.3, 20.4, 21.6 s; after: 22.4, 47.3, 25.6 s).

*Did it help? No.* The timeout fired zero times in the whole after-run (no `[timeout]` message anywhere), which is the giveaway: if the slow runs were hung model requests, a 6 s timeout would have caught them. They were the rate limiter instead. The after-run output lists `[rate limit] 15 requests used this minute. Waiting 21s / 19s / 16s / 12s`, and a real server-side 429 (`Waiting 39s`) accounts for the 47 s run, which also shows 3 model calls instead of 2. The same pauses appear in the before-run. I had misread the 17.6 s in my timing run: that was the 16th request inside a minute. So I aimed the fix at the wrong stage. The corrected diagnosis is the one in "Verdicts and diagnoses": the stage is `generate.py`'s request pacing, and the lesson is that one slow sample told me where to look but not why.

*What it cost.* Nothing measurable in this data, but the change has a downside I can name: an abandoned request may still be billed by the service, and its tokens never reach the log, so the log can under-count cost whenever a timeout fires.

**What's Still Broken (superseded draft criteria)**

- **Criterion 3 (MET, but only because of the 9-of-10 allowance).** A strict 10-of-10 would have missed in all three trials, because the test itself exceeds the free-tier quota. What I would do: re-measure latency with runs spaced about 9 seconds apart (7 runs a minute is the limit at 2 calls per run), and write the criterion that way. I stopped because the unit was out of time and the honest fix is a new measurement, not more code. I left the original criterion in place.
- **The timeout change did not help.** I would revert it. It adds a thread and a billing risk with no demonstrated benefit. I kept it in the history, with the evidence above, because removing it would erase the diagnosis.
- **58% of a normal run is MCP startup** (two server processes at about 1.8 s each). A single long-lived MCP session would remove about 3.6 s of a 6.2 s run. I scoped it out because it changes `mcp_client.py`, and the scope I declared was a log, not a speed-up.
- **Criterion 4 was set too low** (see above): tighten to a mean of at most 1,000 and a max of 1,250.
- **Not built:** hosting (Path A), and the per-call token log does not include abandoned requests.

*The one thing I would do first:* the spaced-out latency measurement. Every other speed decision (reverting the timeout, persisting the MCP session) depends on knowing the real per-run latency, and right now my only number includes the quota pauses.

*Stretch, not claimed.* I built a latency breakdown (`stage_timing.py`) but did not declare it in the README before building it, so I am not claiming the extra credit; the results are used in the diagnosis above.

**How I Used AI**

I worked in Claude Code, and at my request it wrote the capstone code and the first version of these README sections. The brief asks for criteria written by the student, and that is where this went wrong, so here is what happened and what I did about it.

**What went wrong.** When I asked for help with the capstone, Claude drafted the five criteria in `criteria.md` itself, using the cost numbers it had already measured. It chose the targets, wrote the reasons, ran three trials against them, and I committed the results. All of that was committed under criteria that were not mine. I did not catch it until I read them and asked why Claude had drafted them. Two consequences: the criteria were not my own work, and, because the targets were set knowing the measured averages, criterion 4 (tokens) was easy to meet and criterion 3 (latency) was written knowing it would just pass.

**What I did to fix it.**
1. I wrote five new criteria myself (one record per run, a classmate starting it alone, cost per run, bad input not crashing, original behavior preserved), with my own numbers and reasons. Claude only gave feedback on whether each one could be tested, for example that "duplicate" needed a definition about log lines and not listings, and that a 3,000-character query might succeed instead of failing. Claude typed my wording into `criteria.md` at my request.
2. I did not delete the first draft. It stays in `criteria.md`, marked "Claude's first draft, SUPERSEDED", so the history is visible, and my criteria are committed in a separate commit before any new results.
3. The trials and verdict tables in "Run Log and Verdicts" and "The Improvement" above were scored against that first draft. I am keeping them as a record of what happened, but they are not the verdicts for my criteria. The results for my own criteria are in the sections marked as such, run after my criteria were committed.

Two specific moments:

1. **The timeout.** I asked for a fix for the slow runs. Claude first proposed the SDK's `http_options` timeout of 8 s. Before committing it, Claude tested the failure path and found the API returns `400 INVALID_ARGUMENT: Manually set deadline 1s is too short. Minimum allowed deadline is 10s`. That would have failed every call, and the retry check would have retried each one. I switched to a client-side timeout in a daemon thread (`generate.py::_call_with_timeout`) and kept the 6 s value.
2. **The diagnosis.** Claude's first diagnosis, from one slow `create_fit_card` in the timing run, was a hung model request. The after-run contradicted it: no timeout ever fired, and the output was full of `[rate limit] 15 requests used this minute` pauses that matched the slow runs. I replaced the diagnosis with the quota explanation and reported the improvement as not helping.
