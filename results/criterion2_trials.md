# Criterion 2 (revised): timed fresh-clone trials

| Trial | Date | Setup time | Fit cards | Failed step | Verdict | Notes |
|---|---|---|---|---|---|---|
| 1 | 2026-11-17 19:18 | 122 s | 0 of 5 | python test.py (the key was empty, length 0) | FAIL, VOID: no key was entered, so this says nothing about RUNNING.md; re-run as trial 1b | clone 2s; venv 20s; pip install 114s; key pasted 114s; test.py done (setup time) 122s; runs 9.2, 7.9, 9.1, 9, 7.8 s |
| 1b | 2026-11-17 21:22 | 130 s | 5 of 5 | none | PASS | clone 2s; venv 23s; pip install 108s; key pasted 122s; test.py done (setup time) 130s; runs 10.5, 9.2, 8.5, 8.5, 9.4 s |
| 2 | 2026-11-17 22:02 | 146 s | 5 of 5 | none | PASS | clone 1s; venv 22s; pip install 100s; key pasted 139s; test.py done (setup time) 146s; runs 9.3, 9.9, 9, 9.1, 9.4 s |
| 3 | 2026-11-17 22:13 | 174 s | 5 of 5 | none | PASS | clone 2s; venv 19s; pip install 91s; key pasted 167s; test.py done (setup time) 174s; runs 8.6, 8.7, 10.2, 8.9, 16 s |
