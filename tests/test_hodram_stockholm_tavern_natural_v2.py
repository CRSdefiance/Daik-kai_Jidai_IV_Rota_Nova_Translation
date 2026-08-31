from __future__ import annotations

import hashlib
import json
from pathlib import Path

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.script.mesfile import rebuild_mesfile
from dk4tool.script.translation_batch import materialize_translation_batch
from scripts.build_integrated_release import changed_segments
from scripts.materialize_hodram_stockholm_tavern_natural_v2 import LINES

BATCH = Path("translations/hodram_stockholm_tavern_natural_v2_sc1_b134.json")
BASE_ROM = Path("out/raphael_natural_v2_pre_common_accepted_rollback.nds")
SC1_SHA256 = "33981b27375cca1b9293752662d0dedb820dd310526c9dbe0612a397f38313ab"


def test_stockholm_tavern_batch_is_complete_source_locked_and_fixed() -> None:
    batch = json.loads(BATCH.read_text(encoding="utf-8"))
    source_sc1 = NdsImage.open(BASE_ROM).read_file("/data/SC1.DK4")
    assert hashlib.sha256(source_sc1).hexdigest() == SC1_SHA256
    assert batch["source_file_sha256"] == SC1_SHA256
    assert batch["encoder"] == "dialogue-fixed-v1"
    assert batch["dialogue_profile"] == "hodram-story-probe"
    assert batch["translation_policy"] == "natural-dialogue-v2"
    assert {record["id"] for record in batch["records"]} == set(LINES)
    assert len(batch["records"]) == 7
    assert all(all(record["review"].values()) for record in batch["records"])

    source = IlnkContainer.parse(source_sc1)
    source_lengths = {
        int(record["id"].rsplit("R", 1)[1]): len(
            source.blocks[134].split(b"\0")[int(record["id"].rsplit("R", 1)[1])]
        )
        for record in batch["records"]
    }
    rows = materialize_translation_batch(batch, source_sc1)
    rebuilt = rebuild_mesfile(source_sc1, rows)
    assert changed_segments(source_sc1, rebuilt) == {
        (134, index) for index in source_lengths
    }
    rebuilt_block = IlnkContainer.parse(rebuilt).blocks[134].split(b"\0")
    assert all(len(rebuilt_block[index]) == length for index, length in source_lengths.items())


def test_stockholm_tavern_choices_preserve_exact_allocations() -> None:
    batch = json.loads(BATCH.read_text(encoding="utf-8"))
    by_id = {record["id"]: record for record in batch["records"]}
    assert by_id["DK4_MES_B134_R0015"]["english"] == "All right.{PAD}"
    assert by_id["DK4_MES_B134_R0017"]["english"] == "You handle it.{PAD}"
