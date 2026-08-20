from __future__ import annotations

import json
from pathlib import Path

BATCHES = (
    Path("translations/lil_natural_v2_sc1_b38_b48.json"),
    Path("translations/lil_natural_v2_sc1_b66_b137.json"),
    Path("translations/lil_natural_v2_sc2_b22_blocked.json"),
)


def test_all_identified_lil_drafts_are_accounted_for_and_stay_blocked():
    batches = [json.loads(path.read_text(encoding="utf-8")) for path in BATCHES]
    assert [len(batch["blocked_records"]) for batch in batches] == [64, 49, 49]
    assert all(batch["records"] == [] for batch in batches)

    blocked = [record for batch in batches for record in batch["blocked_records"]]
    ids = [str(record["id"]) for record in blocked]
    assert len(blocked) == len(set(ids)) == 162
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
