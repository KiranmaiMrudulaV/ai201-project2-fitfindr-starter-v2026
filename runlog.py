"""
Structured run log (capstone, shape A).

One call to `log_run()` appends one JSON object, on one line, to
logs/runs.jsonl. That format is called JSONL: a file you can read back with
`json.loads(line)` for each line, and filter or average without any parsing
tricks. Named fields, not sentences.

Why this is its own module and not part of agent.py: the logger should never
be able to change what the agent does. It only appends to a file.
"""

import json
from datetime import datetime, timezone

import config


def log_run(**fields) -> dict:
    """Append one record to the run log and return it.

    `timestamp` is added here, in UTC, so every record has one in the same
    format. Everything else is whatever the caller passes in.

    A logging failure (disk full, permissions) must never kill a run that
    already worked, so write errors are swallowed after a note on stderr.
    """
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        **fields,
    }
    try:
        config.LOG_FILE.parent.mkdir(exist_ok=True)
        with config.LOG_FILE.open("a", encoding="utf-8") as f:
            # ensure_ascii=False keeps emoji in fit cards readable in the file
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    except OSError as exc:
        import sys

        print(f"  [runlog] could not write log: {exc}", file=sys.stderr)
    return entry


def read_runs() -> list[dict]:
    """Read every record back. Used by the cost and criteria measurements."""
    if not config.LOG_FILE.exists():
        return []
    runs = []
    for line in config.LOG_FILE.read_text(encoding="utf-8").splitlines():
        if line.strip():
            runs.append(json.loads(line))
    return runs
