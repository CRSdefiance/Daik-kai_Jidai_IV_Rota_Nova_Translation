from __future__ import annotations

import json
from pathlib import Path

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.script.mesfile import rebuild_mesfile
from dk4tool.script.translation_batch import materialize_translation_batch
from scripts.build_integrated_release import validate_ascii_guard_policy

BASE = Path("out/raphael_natural_v2_pre_lil_hodram_unified_v1_accepted_rollback.nds")
BATCH = Path("translations/common_port_departure_guard_v1.json")
STACK = Path("translations/release_stack.json")


def _load(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def test_port_departure_records_are_source_locked_and_two_byte_guarded() -> None:
    batch = _load(BATCH)
    validate_ascii_guard_policy(BATCH, batch)
    source = NdsImage.open(BASE).read_file("/COMMON/MESFILE.DK4")
    rebuilt = rebuild_mesfile(source, materialize_translation_batch(batch, source))
    records = IlnkContainer.parse(rebuilt).blocks[0].split(b"\0")

    assert records[53].rstrip().endswith(b"Continue?")
    assert records[59][45:47] == b"  "
    assert records[62][54:56] == records[62][98:100] == b"  "
    assert records[64].rstrip() == b"  About %s days at sea."
    assert records[65].rstrip() == b"  %s/%s\n  %s\n  Departed %s."


def test_shipyard_successor_includes_port_departure_guard_batch() -> None:
    profile = _load(STACK)["profiles"]["shipyard-complete-v1"]
    assert BATCH.as_posix() in profile["batches"]
