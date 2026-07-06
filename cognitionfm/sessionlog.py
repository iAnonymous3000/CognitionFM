"""Append listening-protocol session rows to logs/listening-log.csv.

Column layout matches docs/03-testing-protocol.md:
date,playlist,condition,focus,state,friction,anchor,notes
"""

import csv
import datetime
import os

HEADER = ["date", "playlist", "condition", "focus", "state", "friction",
          "anchor", "notes"]


def append_session(path: str, playlist: str, condition: str, focus: int,
                   state: int, friction: int, anchor: str = "",
                   notes: str = "") -> dict:
    condition = condition.upper()
    if condition not in ("A", "B"):
        raise ValueError("condition must be A (playlist) or B (control)")
    for name, v in (("focus", focus), ("state", state), ("friction", friction)):
        if not 1 <= v <= 5:
            raise ValueError(f"{name} must be 1-5, got {v}")
    row = {"date": datetime.date.today().isoformat(), "playlist": playlist,
           "condition": condition, "focus": focus, "state": state,
           "friction": friction, "anchor": anchor, "notes": notes}
    os.makedirs(os.path.dirname(path), exist_ok=True)
    new_file = not os.path.exists(path) or os.path.getsize(path) == 0
    with open(path, "a", newline="") as f:
        w = csv.DictWriter(f, fieldnames=HEADER)
        if new_file:
            w.writeheader()
        w.writerow(row)
    return row
