from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.dialogue.qa import audit_fixed_dialogue_record
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.script.mesfile import rebuild_mesfile
from dk4tool.script.translation_batch import materialize_translation_batch
from scripts.build_integrated_release import changed_segments
from scripts.materialize_hodram_stockholm_port_tutorials_natural_v2 import (
    BATCHES as MATERIALIZED_BATCHES,
)

BASE_ROM = Path("out/raphael_natural_v2_pre_common_accepted_rollback.nds")
SC1_SHA256 = "33981b27375cca1b9293752662d0dedb820dd310526c9dbe0612a397f38313ab"
BATCHES = {
    135: Path("translations/hodram_stockholm_dock_natural_v2_sc1_b135.json"),
    136: Path("translations/hodram_stockholm_market_natural_v2_sc1_b136.json"),
}


@pytest.mark.parametrize(("block", "batch_path"), BATCHES.items())
def test_stockholm_tutorial_is_complete_source_locked_and_qa_clean(
    block: int, batch_path: Path
) -> None:
    source_sc1 = NdsImage.open(BASE_ROM).read_file("/data/SC1.DK4")
    assert hashlib.sha256(source_sc1).hexdigest() == SC1_SHA256
    source = IlnkContainer.parse(source_sc1)
    segments = source.blocks[block].split(b"\0")
    expected_ids = set(MATERIALIZED_BATCHES[block]["records"])

    batch = json.loads(batch_path.read_text(encoding="utf-8"))
    assert batch["source_file_sha256"] == SC1_SHA256
    assert batch["encoder"] == "dialogue-fixed-v1"
    assert batch["dialogue_profile"] == "hodram-story-probe"
    assert batch["translation_policy"] == "natural-dialogue-v2"
    assert {record["id"] for record in batch["records"]} == expected_ids
    assert len(batch["records"]) == 10
    assert all(all(record["review"].values()) for record in batch["records"])

    profile = get_dialogue_profile("hodram-story-probe")
    for record in batch["records"]:
        index = int(record["id"].rsplit("R", 1)[1])
        audit = audit_fixed_dialogue_record(segments[index], record["english"], profile)
        assert not [
            issue
            for issue in audit["issues"]
            if issue["severity"] in {"warning", "error"}
        ], (record["id"], audit)

    rows = materialize_translation_batch(batch, source_sc1)
    rebuilt = rebuild_mesfile(source_sc1, rows)
    assert changed_segments(source_sc1, rebuilt) == {
        (block, int(record["id"].rsplit("R", 1)[1]))
        for record in batch["records"]
    }


@pytest.mark.parametrize("batch_path", BATCHES.values())
def test_stockholm_tutorial_choice_slots_are_exact(batch_path: Path) -> None:
    batch = json.loads(batch_path.read_text(encoding="utf-8"))
    by_id = {record["id"]: record for record in batch["records"]}
    block = int(batch["inventory"]["block"])
    assert by_id[f"DK4_MES_B{block}_R0015"]["english"] == "All right.{PAD}"
    expected_second = "You handle it.{PAD}" if block == 135 else "Don't sell it.{PAD}"
    assert by_id[f"DK4_MES_B{block}_R0017"]["english"] == expected_second
