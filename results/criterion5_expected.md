# Criterion 5: queries and expected item IDs (recorded before testing)

Recorded from `search_listings` alone (no model involved) before any
comparison was run. `_run_loop` and `run_agent` must both select these.

| Query | Expected selected item | Kind |
|---|---|---|
| vintage graphic tee under $30 | lst_002 | known match |
| denim jacket under $50 | lst_007 | known match |
| designer ballgown size XXS under $5 | none (no match) | no match |
