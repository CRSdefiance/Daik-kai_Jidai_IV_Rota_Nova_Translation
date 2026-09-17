from __future__ import annotations

import hashlib
import json
from pathlib import Path

from dk4tool.formats.ilnk import IlnkContainer

BATCHES = (
    Path("translations/lil_natural_v2_sc1_b38_b48.json"),
    Path("translations/lil_natural_v2_sc1_b66_b137.json"),
    Path("translations/lil_natural_v2_sc2_b22_blocked.json"),
    Path("translations/lil_natural_v2_sc2_b23_blocked.json"),
)


def test_all_identified_lil_drafts_are_accounted_for_and_stay_blocked():
    batches = [json.loads(path.read_text(encoding="utf-8")) for path in BATCHES]
    assert [len(batch["blocked_records"]) for batch in batches] == [64, 49, 49, 35]
    assert all(batch["records"] == [] for batch in batches)

    blocked = [record for batch in batches for record in batch["blocked_records"]]
    ids = [str(record["id"]) for record in blocked]
    assert len(blocked) == len(set(ids)) == 197
    for record in blocked:
        draft = str(record["draft_english"])
        assert draft.endswith("{PAD}")
        assert "{LB" not in draft
        assert "{ALIGN" not in draft
        assert "{SPEAKER" not in draft
        assert "{HEX" not in draft
        assert record["review"]["formatting"] is False
        assert str(record["blocker"]).strip()


def test_lil_drafts_are_not_registered_in_a_playable_release_profile():
    stack = json.loads(Path("translations/release_stack.json").read_text(encoding="utf-8"))
    registered = {
        Path(path)
        for profile in stack["profiles"].values()
        for path in profile["batches"]
    }

    assert not registered.intersection(BATCHES)


def test_lil_sc2_b23_drafts_are_source_locked_to_the_clean_route():
    source = Path("work/extracted_clean/data/SC2.DK4").read_bytes()
    assert hashlib.sha256(source).hexdigest() == (
        "c270e84025d6942da2dbe86ff6a0241a0874611bce0d08f80923c5fb6e75d326"
    )
    segments = IlnkContainer.parse(source).blocks[23].split(b"\0")
    batch = json.loads(BATCHES[-1].read_text(encoding="utf-8"))
    assert batch["inventory"] == {
        "identified_records": 35,
        "translated_drafts": 35,
        "encodable_records": 0,
        "blocked_records": 35,
        "missing_records": 0,
        "blocks": {"23": 35},
    }
    for record in batch["blocked_records"]:
        index = int(record["id"].rsplit("R", 1)[1])
        assert segments[index].hex().upper() == record["source_hex_guard"]
