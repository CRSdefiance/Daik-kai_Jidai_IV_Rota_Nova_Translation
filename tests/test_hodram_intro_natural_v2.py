from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.script.mesfile import rebuild_mesfile
from dk4tool.script.translation_batch import materialize_translation_batch
from scripts.build_integrated_release import changed_segments, resolve_release_batches
from scripts.materialize_hodram_intro_natural_v2 import EXCLUDED, LINES

BATCH = Path("translations/hodram_intro_natural_v2_sc1_b42_b44.json")
CLEAN_ROM = Path("work/clean.nds")
BASE_ROM = Path("out/raphael_natural_v2_pre_common_accepted_rollback.nds")
SC1_SHA256 = "33981b27375cca1b9293752662d0dedb820dd310526c9dbe0612a397f38313ab"


def test_hodram_intro_is_complete_source_locked_and_qa_ready() -> None:
    batch = json.loads(BATCH.read_text(encoding="utf-8"))
    clean_sc1 = NdsImage.open(CLEAN_ROM).read_file("/data/SC1.DK4")
    base_sc1 = NdsImage.open(BASE_ROM).read_file("/data/SC1.DK4")
    assert clean_sc1 == base_sc1
    assert hashlib.sha256(base_sc1).hexdigest() == SC1_SHA256
    assert batch["source_file_sha256"] == SC1_SHA256
    assert batch["encoder"] == "dialogue-fixed-v1"
    assert batch["dialogue_profile"] == "hodram-story-probe"
    assert batch["excluded_records"] == EXCLUDED
    assert len(batch["records"]) == len(LINES) == 67
    assert {record["id"] for record in batch["records"]} == set(LINES)
    assert all(record["review"]["formatting"] is True for record in batch["records"])

    source = IlnkContainer.parse(base_sc1)
    expected_segments: set[tuple[int, int]] = set()
    for record in batch["records"]:
        block = int(record["id"].split("_B", 1)[1].split("_", 1)[0])
        index = int(record["id"].rsplit("R", 1)[1])
        assert source.blocks[block].split(b"\0")[index]
        expected_segments.add((block, index))

    rows = materialize_translation_batch(batch, base_sc1)
    rebuilt = rebuild_mesfile(base_sc1, rows)
    assert changed_segments(base_sc1, rebuilt) == expected_segments


def test_hodram_intro_profile_fails_closed_for_unmeasured_future_macros() -> None:
    profile = get_dialogue_profile("hodram-story-probe")
    assert profile.guard_linebreaks is True
    assert profile.pair_phase_safe_breaks is True
    assert profile.leading_speaker_bytes == frozenset({0x10, 0x12, 0x17, 0xFE})
    assert profile.macro_ascii_lengths == {}


def test_hodram_intro_replaces_the_revoked_wrong_route_probe() -> None:
    with pytest.raises(ValueError, match="accepted-baked"):
        resolve_release_batches("hodram-intro-english-probe", [])
    with pytest.raises(ValueError, match="profile is revoked"):
        resolve_release_batches("hodram-sc2-control-map-probe", [])
