from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.script.mesfile import rebuild_mesfile
from dk4tool.script.translation_batch import materialize_translation_batch
from scripts.build_integrated_release import changed_segments, resolve_release_batches
from scripts.materialize_hodram_sc2_control_probe import PROBES

BATCH = Path("translations/hodram_sc2_control_map_probe_v1.json")
CLEAN_ROM = Path("work/clean.nds")
BASE_ROM = Path("out/raphael_natural_v2_accepted_base.nds")
SC2_SHA256 = "c270e84025d6942da2dbe86ff6a0241a0874611bce0d08f80923c5fb6e75d326"


def test_hodram_control_probe_preserves_exact_leads_and_allocations() -> None:
    batch = json.loads(BATCH.read_text(encoding="utf-8"))
    clean_sc2 = NdsImage.open(CLEAN_ROM).read_file("/data/SC2.DK4")
    base_sc2 = NdsImage.open(BASE_ROM).read_file("/data/SC2.DK4")
    assert clean_sc2 == base_sc2
    assert hashlib.sha256(base_sc2).hexdigest() == SC2_SHA256
    assert batch["source_file_sha256"] == SC2_SHA256
    assert batch["research_only"] is True
    assert len(batch["records"]) == len(PROBES) == 6

    source_records = IlnkContainer.parse(base_sc2).blocks[27].split(b"\0")
    expected_segments: set[tuple[int, int]] = set()
    for record in batch["records"]:
        row_id = record["id"]
        record_index = int(row_id.rsplit("R", 1)[1])
        source = source_records[record_index]
        replacement = bytes.fromhex(record["replacement_hex"])
        expected_lead, payload = PROBES[row_id]
        assert source.hex() == record["source_hex_guard"]
        assert source[0] == replacement[0] == expected_lead
        assert len(source) == len(replacement)
        assert source[1:].decode("cp932")
        assert replacement[1:] == payload.encode("ascii")
        assert b"\n" not in replacement
        expected_segments.add((27, record_index))

    rows = materialize_translation_batch(batch, base_sc2)
    rebuilt = rebuild_mesfile(base_sc2, rows)
    assert changed_segments(base_sc2, rebuilt) == expected_segments


def test_hodram_control_probe_is_revoked_after_route_correction() -> None:
    with pytest.raises(ValueError, match="profile is revoked"):
        resolve_release_batches("hodram-sc2-control-map-probe", [])
    batch = json.loads(BATCH.read_text(encoding="utf-8"))
    macro_record = next(
        record for record in batch["records"] if record["id"] == "DK4_MES_B27_R0041"
    )
    assert bytes.fromhex(macro_record["replacement_hex"]).count(b"FI") == 1
