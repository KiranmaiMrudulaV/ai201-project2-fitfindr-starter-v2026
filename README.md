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
| 1.  |  |  |  |  |  |  |  |
| 2.  |  |  |  |  |  |  |  |
| 3.  |  |  |  |  |  |  |  |
| 4.  |  |  |  |  |  |  |  |
| 5.  |  |  |  |  |  |  |  |

**Real output from one try**, pasted as text, naming the file and function
that produced it:

```

```

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
| 1 |  |  |  |  |
| 2 |  |  |  |  |
| 3 |  |  |  |  |
| 4 |  |  |  |  |
| 5 |  |  |  |  |

**Diagnoses**



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

**What I changed:**

**Which failure it was meant to fix:**

### Run Log — After

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |  |  |
| 2.  |  |  |  |  |  |  |  |
| 3.  |  |  |  |  |  |  |  |
| 4.  |  |  |  |  |  |  |  |
| 5.  |  |  |  |  |  |  |  |

**Did it help, and how do I know:**

<!-- If it made things worse, say that. Honestly reported, that earns full
     credit and is more interesting than one that worked. -->



---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped where
     you did. "I ran out of time" is fine if it's true. Pretending nothing is
     left is not. -->



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
