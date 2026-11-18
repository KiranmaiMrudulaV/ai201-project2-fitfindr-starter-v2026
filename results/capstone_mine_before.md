# My capstone criteria, trials - before - 2026-11-17 17:18

Criterion 2 (classmates) is scored by hand, not here.

| Criterion | Target | Results per trial | Verdict |
|---|---|---|---|
| 1. Exactly one record per run | 5 of 5 trials add 5 lines | PASS (5 lines), PASS (5 lines), PASS (5 lines), PASS (5 lines), PASS (5 lines) | MET |
| 3. Cost per run | at most $0.001/run | $0.00103/run (10/10 ok), $0.00113/run (10/10 ok), $0.00114/run (10/10 ok) | MISSED |
| 4. Bad input does not crash | 5 of 5 | 5/5, 5/5, 5/5 | MET |
| 5. Original behavior preserved | 3 of 3 | 3/3, 3/3, 3/3 | MET |

## Raw output, trial 1

### C1 (query, bad key?, new lines)
- ('vintage graphic tee under $30', False, 1)
- ('denim jacket under $50', False, 1)
- ('90s track jacket in size M', False, 1)
- ('(empty)', False, 1)
- ('vintage graphic tee under $30', True, 1)

### C3 log records
{"timestamp": "2026-11-17T23:11:39+00:00", "query": "vintage graphic tee under $30", "status": "ok", "output": "That little pastel butterfly print on this baby tee is just peak 2000s, and I grabbed it on Depop for $18. I’ve been wearing it on heavy rotation by styling it two ways: either contrasted against dark baggy denim and chunky sneakers for full streetwear energy, or dressed down with wide-l
{"timestamp": "2026-11-17T23:11:44+00:00", "query": "90s track jacket in size M", "status": "ok", "output": "Zip-up track jackets are officially doing the heavy lifting in my wardrobe right now. Snagged this navy and white 90s Champion piece on Poshmark for $45, and it’s about to live over a white ribbed tank and my favorite baggy dark wash jeans. Add some chunky sneakers and a black crossbody, an
{"timestamp": "2026-11-17T23:11:51+00:00", "query": "silk slip dress in midi length under $40", "status": "ok", "output": "There is seriously nothing better than a 90s floral midi that feels like actual liquid silk. Snagged this beauty on Depop for just $30, and honestly, styling it is half the fun. Swipe to see how I'm wearing it two ways: grungy with a cropped zip hoodie and combat boots, and fu
{"timestamp": "2026-11-17T23:11:59+00:00", "query": "platform sneakers size 8", "status": "ok", "output": "Chunky white platforms are officially my new everyday uniform, especially after scoring these for just $48 on Poshmark. I'm leaning all the way into the effortless streetwear vibe with baggy denim and a vintage jacket, or dressing them up with tailored khaki trousers and a cropped hoodie. Hon
{"timestamp": "2026-11-17T23:12:06+00:00", "query": "denim jacket under $50", "status": "ok", "output": "That perfectly faded vintage wash hits different when you find it online for just $42 on Poshmark. I've been living in this cropped Wrangler jacket lately—whether I'm leaning into a double-denim moment with dark baggy jeans or throwing it over a grey crewneck and khakis for that high-low street
{"timestamp": "2026-11-17T23:12:20+00:00", "query": "vintage graphic tee under $30", "status": "ok", "output": "Nothing screams butterfly-clip summer quite like this pink and purple graphic. Snagged it on Depop for just $18 and I'm already stuck between styling it with baggy dark wash denim or grounding it with some wide-leg khaki trousers. Which vibe are we leaning into today? 🦋✨", "error": null,
{"timestamp": "2026-11-17T23:12:27+00:00", "query": "90s track jacket in size M", "status": "ok", "output": "That deep navy and white stripe hits that exact 90s athletic sweet spot without trying too hard. Snagged this vintage Champion track jacket on Poshmark for $45, and it’s already doing all the heavy lifting in my rotation. Throw it over baggy dark denim and chunky sneakers for an easy retro 
{"timestamp": "2026-11-17T23:12:37+00:00", "query": "silk slip dress in midi length under $40", "status": "ok", "output": "That dreamy floral silk slip dress I snagged on Depop for $30 has officially unlocked my inner 90s indie-sleaze icon. I’m leaning all the way into the delicate-meets-edgy juxtaposition by throwing on a beat-up denim jacket and combat boots. Or, when I'm feeling lazy, I just pu
{"timestamp": "2026-11-17T23:12:43+00:00", "query": "platform sneakers size 8", "status": "ok", "output": "Those chunky white platforms instantly add that perfect late-90s height to everything in my closet. I just grabbed them on Poshmark for $48, and they’re already pulling their weight—pairing just as easily with baggy indigo denim and a black jacket as they do dressed up with tailored khaki tro
{"timestamp": "2026-11-17T23:12:49+00:00", "query": "denim jacket under $50", "status": "ok", "output": "That perfect 90s boxy fit is impossible to fake, which is why I couldn't pass up this cropped Wrangler jacket for $42 on Poshmark. Planning to lean into the proportions by throwing it over baggy dark denim or styling it high-low with tailored khaki trousers. Sustainable style just hits differen

### C4 (label, no Traceback, has message, exit code, ok, output)
- ('empty query', True, True, 0, True, 'Ask for something, or press Enter on an empty line to quit. |  | >  | 0 model calls this session')
- ('3,000 characters', True, True, 0, True, '[1] _parse_query |       in:  vintage graphic tee vintage graphic tee vintage graphic tee vintage graphic tee vintage graphic tee vintage gr… |       out: dict ')
- ('symbols only', True, True, 0, True, '[1] _parse_query |       in:  !!!@@@###$$$%%%^^^&&&*** |       out: dict with keys: description, size, max_price | [2] search_listings (via MCP) |       in:  di')
- ('unsupported language', True, True, 0, True, '[1] _parse_query |       in:  古着のグラフィックTシャツを探しています |       out: dict with keys: description, size, max_price | [2] search_listings (via MCP) |       in:  dict w')
- ('invalid API key', True, True, 0, True, '[1] _parse_query |       in:  vintage graphic tee under $30 |       out: dict with keys: description, size, max_price | [2] search_listings (via MCP) |       in')

### C5 (query, expected id, [_run_loop id, run_agent id], ok)
- ('vintage graphic tee under $30', 'lst_002', ['lst_002', 'lst_002'], True)
- ('denim jacket under $50', 'lst_007', ['lst_007', 'lst_007'], True)
- ('designer ballgown size XXS under $5', None, [None, None], True)
