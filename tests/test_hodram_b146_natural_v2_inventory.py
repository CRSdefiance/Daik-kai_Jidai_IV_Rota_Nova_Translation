from __future__ import annotations

import hashlib
import json
from pathlib import Path

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from scripts.materialize_hodram_b146_draft import LINES

BATCH = Path("translations/hodram_natural_v2_sc2_b146_blocked.json")
CLEAN_ROM = Path("work/clean.nds")
SC2_SHA256 = "c270e84025d6942da2dbe86ff6a0241a0874611bce0d08f80923c5fb6e75d326"


def test_hodram_b146_is_complete_source_locked_editorial_work() -> None:
    batch = json.loads(BATCH.read_text(encoding="utf-8"))
    sc2 = NdsImage.open(CLEAN_ROM).read_file("/data/SC2.DK4")
    assert hashlib.sha256(sc2).hexdigest() == SC2_SHA256
    assert batch["source_file_sha256"] == SC2_SHA256
    assert batch["records"] == []
    assert batch["inventory"] == {
        "identified_records": 35,
        "translated_drafts": 35,
        "encodable_records": 0,
        "blocked_records": 35,
        "missing_records": 0,
        "blocks": {"146": 35},
    }

    records = batch["blocked_records"]
    assert len(records) == len({record["id"] for record in records}) == 35
    assert {record["id"] for record in records} == set(LINES)
    source_records = IlnkContainer.parse(sc2).blocks[146].split(b"\0")
    for record in records:
        record_index = int(record["id"].rsplit("R", 1)[1])
        source = source_records[record_index]
        draft = record["draft_english"]
        assert record["source_prefix_hex"] == f"{source[0]:02X}"
        assert record["source_length"] == len(source)
        assert draft.endswith("{PAD}")
        assert source.count(b"FI") == draft.count("{MACRO:FI}")
        assert all(
            record["review"][gate] is True
            for gate in ("source", "context", "localization", "naturalness")
        )
        assert record["review"]["formatting"] is False
        assert "{HEX:" not in draft
        assert "{LB}" not in draft
        assert "Ã¢" not in draft

    by_id = {record["id"]: record for record in records}
    assert by_id["DK4_MES_B146_R0008"]["source_prefix_hex"] == "97"
    assert by_id["DK4_MES_B146_R0031"]["source_prefix_hex"] == "FE"
