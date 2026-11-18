# My capstone criteria, trials - after - 2026-11-17 18:27

Criterion 2 (classmates) is scored by hand, not here.

| Criterion | Target | Results per trial | Verdict |
|---|---|---|---|
| 1. Exactly one record per run | 5 of 5 trials add 5 lines | PASS (5 lines), PASS (5 lines), PASS (5 lines), PASS (5 lines), PASS (5 lines) | MET |
| 3. Cost per run | at most $0.001/run | $0.00051/run (10/10 ok), $0.00052/run (10/10 ok), $0.00050/run (10/10 ok) | MET |
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
{"timestamp": "2026-11-18T00:20:42+00:00", "query": "vintage graphic tee under $30", "status": "ok", "output": "That butterfly print is straight out of 2003, and at just $18 on Depop, I had to grab it. I'm balancing the sweet graphic with baggy dark denim and combat boots for an edgy look, or going full off-duty with khaki trousers and a zip hoodie. Which vibe are we leaning toward?", "error": nul
{"timestamp": "2026-11-18T00:20:48+00:00", "query": "90s track jacket in size M", "status": "ok", "output": "There is truly nothing better than crisp navy-and-white piping on a 90s Champion piece. Snagged this vintage track jacket on Poshmark for $45, and it’s already doing all the heavy lifting in my wardrobe. Throwing it on with baggy denim and chunky sneakers for an easy sporty look, or layerin
{"timestamp": "2026-11-18T00:20:53+00:00", "query": "silk slip dress in midi length under $40", "status": "ok", "output": "That 90s floral silk midi hanging in my closet is finally getting its moment. Scooped this gem up on Depop for just $30 and instantly knew I had to play with the contrasts. Either throwing a beat-up grey crewneck and combat boots over it for effortless grunge, or zipping it un
{"timestamp": "2026-11-18T00:21:00+00:00", "query": "platform sneakers size 8", "status": "ok", "output": "Elevate literally any outfit with these chunky white platform sneakers—total Y2K model-off-duty energy. I just snagged them on Poshmark for $48 and I'm already planning two ways to wear them on repeat. Dress 'em up with wide-leg khakis and a denim jacket, or lean into the streetwear vibe with
{"timestamp": "2026-11-18T00:21:06+00:00", "query": "denim jacket under $50", "status": "ok", "output": "Nothing beats a boxy, perfectly broken-in light wash denim jacket, especially when it's already cropped to the ideal length. I snagged this Wrangler piece on Poshmark for $42 and honestly haven't stopped planning outfits around it. Whether I'm going for high-contrast double denim with chunky sn
{"timestamp": "2026-11-18T00:21:25+00:00", "query": "vintage graphic tee under $30", "status": "ok", "output": "That nostalgic little butterfly graphic immediately took me straight back to 2003, and for $18 on Depop, I couldn't leave her behind. I'm leaning all the way into the effortless everyday vibe by pairing it with baggy dark-wash denim and chunky white sneakers. But if I want to switch it u
{"timestamp": "2026-11-18T00:21:31+00:00", "query": "90s track jacket in size M", "status": "ok", "output": "Nothing beats finding a crisp navy-and-white striped collar that actually holds its shape. Snagged this vintage 90s Champion track jacket on Poshmark for $45, and I’m already planning two ways to wear it. First up: keeping it casual with baggy dark denim and chunky sneakers, or leaning into
{"timestamp": "2026-11-18T00:21:42+00:00", "query": "silk slip dress in midi length under $40", "status": "ok", "output": "That 90s floral midi drape is everything, especially for just $30 on Depop. I'm leaning hard into the grunge contrast by layering it with a white ribbed tank, combat boots, and a beat-up denim jacket for Outfit 1. Or, I can flip the script for Outfit 2 by throwing an oversized
{"timestamp": "2026-11-18T00:21:47+00:00", "query": "platform sneakers size 8", "status": "ok", "output": "These cloud-like platform sneakers give me major 90s model-off-duty energy. I snagged them on Poshmark for just $48, and honestly, they instantly elevate everything in my closet. I'm obsessed with pairing them with baggy dark-wash denim and a vintage jacket for daytime, or dressing them down 
{"timestamp": "2026-11-18T00:21:52+00:00", "query": "denim jacket under $50", "status": "ok", "output": "Nothing beats a perfectly worn-in, cropped Wrangler denim jacket for throwing over literally everything in my closet. Snagged this light wash beauty on Poshmark for just $42, and honestly, the vintage fade is unmatched. Thinking a ribbed tank and baggy dark denim for an effortless off-duty look

### C4 (label, no Traceback, has message, exit code, ok, output)
- ('empty query', True, True, 0, True, "Nothing to search for. Type what you're looking for, for example: vintage graphic tee under $30 |  | 0 model calls this session")
- ('3,000 characters', True, False, 0, True, '[1] _parse_query |       in:  vintage graphic tee vintage graphic tee vintage graphic tee vintage graphic tee vintage graphic tee vintage gr… |       out: dict ')
- ('symbols only', True, True, 0, True, '[1] _parse_query |       in:  !!!@@@###$$$%%%^^^&&&*** |       out: dict with keys: description, size, max_price | [2] search_listings (via MCP) |       in:  di')
- ('unsupported language', True, True, 0, True, '[1] _parse_query |       in:  古着のグラフィックTシャツを探しています |       out: dict with keys: description, size, max_price | [2] search_listings (via MCP) |       in:  dict w')
- ('invalid API key', True, True, 0, True, '[1] _parse_query |       in:  vintage graphic tee under $30 |       out: dict with keys: description, size, max_price | [2] search_listings (via MCP) |       in')

### C5 (query, expected id, [_run_loop id, run_agent id], ok)
- ('vintage graphic tee under $30', 'lst_002', ['lst_002', 'lst_002'], True)
- ('denim jacket under $50', 'lst_007', ['lst_007', 'lst_007'], True)
- ('designer ballgown size XXS under $5', None, [None, None], True)
