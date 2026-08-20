from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

BATCHES = (
    Path("translations/raphael_natural_v2_b43_b44.json"),
    Path("translations/raphael_natural_v2_b45_b48.json"),
    Path("translations/raphael_natural_v2_b137_b141.json"),
)
EXPECTED_BY_BLOCK = {
    43: 12,
    44: 115,
    45: 12,
    46: 26,
    47: 15,
    48: 87,
    137: 14,
    138: 7,
    139: 19,
    140: 4,
    141: 20,
}


def load_batches() -> list[dict[str, object]]:
    return [json.loads(path.read_text(encoding="utf-8")) for path in BATCHES]


def block_index(record_id: str) -> int:
    match = re.search(r"_B(\d+)_R\d+$", record_id)
    assert match is not None, record_id
    return int(match.group(1))


def test_full_raphael_v2_inventory_accounts_for_every_identified_record():
    batches = load_batches()
    safe = [record for batch in batches for record in batch["records"]]
    blocked = [
        record
        for batch in batches
        for key in ("blockers", "blocked_records")
        for record in batch.get(key, [])
    ]
    ids = [str(record["id"]) for record in safe + blocked]

    assert len(safe) == 304
    assert len(blocked) == 27
    assert len(ids) == len(set(ids)) == 331
    assert Counter(block_index(record_id) for record_id in ids) == Counter(
        EXPECTED_BY_BLOCK
    )


def test_blocked_raphael_prose_remains_translated_but_non_buildable():
    blocked_records = [
        record
        for batch in load_batches()
        for record in batch.get("blocked_records", [])
    ]

    assert len(blocked_records) == 24
    for record in blocked_records:
        draft = str(record.get("english", record.get("draft_english", "")))
        assert draft.endswith("{PAD}")
        assert str(record.get("source_meaning", "")).strip()
        assert str(record.get("context", "")).strip()
        assert record.get("review", {}).get("formatting") is False
        assert record.get("blocker")
