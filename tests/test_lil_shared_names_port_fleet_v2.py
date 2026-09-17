from __future__ import annotations

import json
import struct
from pathlib import Path

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.script.arm9_profiles import GLOBAL_NAME_ENTRIES
from dk4tool.script.mesfile import rebuild_mesfile
from dk4tool.script.translation_batch import materialize_translation_batch
from scripts.build_integrated_release import apply_arm9_fixed_batch

BASE = Path("out/raphael_natural_v2_pre_lil_hodram_unified_v1_accepted_rollback.nds")
ARM9_BATCH = Path("translations/lil_shared_names_port_fleet_arm9_v1.json")
CREW_BATCH = Path("translations/common_crew_join_leading_guard_v2.json")
STACK = Path("translations/release_stack.json")
ARM9_LOAD_ADDRESS = 0x02000000


def _load(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def test_global_name_and_port_catchup_is_source_locked_and_terminated() -> None:
    source = NdsImage.open(BASE).read_file("/__arm9__.bin")
    rebuilt, ids = apply_arm9_fixed_batch(ARM9_BATCH, source)
    assert len(ids) == 9

    assert rebuilt[0x15E96C : 0x15E977] == b"Overijssel\0"
    assert rebuilt[0x15E977 : 0x15E980] == b"%s Fleet\0"
    fleet_pointer = ARM9_LOAD_ADDRESS + 0x15E977
    for pointer_offset in (0x35288, 0x36B4C, 0x82E70, 0x9AE84):
        assert struct.unpack_from("<I", rebuilt, pointer_offset)[0] == fleet_pointer

    assert rebuilt[0x15E674 : 0x15E680] == b"Ardelknatts\0"
    assert rebuilt[0x15E680 : 0x15E685] == b"Hemp\0"
    assert struct.unpack_from("<I", rebuilt, 0x15F158)[0] == ARM9_LOAD_ADDRESS + 0x15E680
    assert rebuilt[0x15D1F0 : 0x15D1FC].split(b"\0", 1)[0] == b"Flanders"
    assert rebuilt[0x157088 : 0x157090].split(b"\0", 1)[0] == b"Target"

    assert len(GLOBAL_NAME_ENTRIES) == 190
    for entry in GLOBAL_NAME_ENTRIES:
        visible = rebuilt[entry.offset : entry.offset + entry.source_length].split(b"\0", 1)[0]
        assert visible.decode("ascii"), entry.row_id


def test_crew_join_template_guards_the_first_expanded_letter() -> None:
    source = NdsImage.open(BASE).read_file("/COMMON/MESFILE.DK4")
    rows = materialize_translation_batch(_load(CREW_BATCH), source)
    rebuilt = rebuild_mesfile(source, rows)
    record = IlnkContainer.parse(rebuilt).blocks[4].split(b"\0")[59]

    assert len(record) == 43
    assert record[20:23] == b" %s"
    assert record.find(b"%s", 1) == 21
    assert record[20] == 0x20
    expanded = record[20:].replace(b"%s", b"Fernando", 1).rstrip()
    assert expanded == b" Fernando joined your crew!"
    assert expanded.lstrip().startswith(b"Fernando")


def test_lil_shared_data_profile_keeps_every_required_layer_together() -> None:
    profile = _load(STACK)["profiles"]["lil-b22-intro-shared-data-v2"]
    assert profile["status"] == "experimental"
    assert profile["batches"] == [
        "translations/lil_sc2_b22_intro_natural_v2.json",
        ARM9_BATCH.as_posix(),
        CREW_BATCH.as_posix(),
    ]
