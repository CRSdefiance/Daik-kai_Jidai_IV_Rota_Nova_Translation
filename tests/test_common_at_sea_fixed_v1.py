from __future__ import annotations

import importlib.util
import json
import re
from pathlib import Path

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.script.mesfile import rebuild_mesfile
from dk4tool.script.translation_batch import materialize_translation_batch


BASE = Path("out/raphael_natural_v2_pre_lil_hodram_unified_v1_accepted_rollback.nds")
CLEAN = Path("work/files/COMMON/MESFILE.DK4")
BATCH = Path("translations/common_at_sea_fixed_v1.json")
MATERIALIZER = Path("scripts/materialize_common_at_sea_fixed_v1.py")
STACK = Path("translations/release_stack.json")


def load(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def module():
    spec = importlib.util.spec_from_file_location("common_at_sea_fixed_v1", MATERIALIZER)
    assert spec is not None and spec.loader is not None
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value


def test_all_14_surviving_generic_at_sea_records_are_source_based_and_fixed_size() -> None:
    generated = module().materialize(BASE, CLEAN)
    checked_in = load(BATCH)
    assert generated == checked_in
    assert len(checked_in["records"]) == 14

    clean_blocks = [block.split(b"\0") for block in IlnkContainer.parse(CLEAN.read_bytes()).blocks]
    for record in checked_in["records"]:
        index = int(str(record["id"]).rsplit("R", 1)[1])
        replacement = bytes.fromhex(str(record["replacement_hex"]))
        assert len(replacement) == len(clean_blocks[7][index])
        starts = [int(value) for value in record["entry_offsets"]]
        for position, start in enumerate(starts):
            end = starts[position + 1] if position + 1 < len(starts) else len(replacement)
            assert all(len(line) <= 31 for line in replacement[start:end].rstrip().split(b"\n"))
        assert re.findall(rb"%[-+0-9.*]*[sd]", replacement) == re.findall(
            rb"%[-+0-9.*]*[sd]", clean_blocks[7][index]
        )


def test_at_sea_batch_removes_the_canned_marine_captain_sentence_and_preserves_entries() -> None:
    source = NdsImage.open(BASE).read_file("/COMMON/MESFILE.DK4")
    batch = load(BATCH)
    rebuilt = rebuild_mesfile(source, materialize_translation_batch(batch, source))
    block = IlnkContainer.parse(rebuilt).blocks[7].split(b"\0")
    assert all(b"crew needs a marine captain" not in record.lower() for record in block)

    for record in batch["records"]:
        index = int(str(record["id"]).rsplit("R", 1)[1])
        for offset in record["entry_offsets"]:
            assert block[index][int(offset) :].lstrip(b" ")
    assert block[17][33:].startswith(b"Right. Leave it to me.")
    assert block[19][66:].startswith(b"Admiral! A leak!")
    assert block[52][44:].startswith(b"%s\nhas run out.")
    assert block[74][33:].startswith(b"No surveyor is assigned,")


def test_v2_profile_extends_the_complete_market_and_inn_set() -> None:
    profiles = load(STACK)["profiles"]
    previous = profiles["hodram-market-inn-v1"]["batches"]
    current = profiles["hodram-market-inn-sea-v2"]["batches"]
    assert current[:-1] == previous
    assert current[-1] == BATCH.as_posix()
