from __future__ import annotations

import json
from pathlib import Path

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage


CANDIDATE = Path("out/all_routes_unified_v5_candidate.nds")


def _record(file_path: str, block: int, record: int) -> bytes:
    data = NdsImage.open(CANDIDATE).read_file(file_path)
    return IlnkContainer.parse(data).blocks[block].split(b"\0")[record]


def test_common_renderer_specific_guards_match_cold_boot_evidence() -> None:
    assert _record("/COMMON/MESFILE.DK4", 0, 34).startswith(
        b"  Resupply? %s coins."
    )
    crew = _record("/COMMON/MESFILE.DK4", 4, 59)
    assert crew[:20].startswith(b"%s acquired!")
    assert crew[20:].startswith(b"  %s joined!")
    assert _record("/COMMON/MESFILE.DK4", 10, 37).rstrip() == (
        b"Change supply ratio?"
    )
    cargo = _record("/COMMON/MESFILE.DK4", 10, 36)
    assert cargo[:65].strip() == b"Your sailors look tired. Rest at the inn?"
    assert cargo[65:93].strip() == b"You have no cargo."
    assert cargo[93:].strip() == (
        b"Not enough coins to fully resupply. Buy what you can?"
    )


def test_lil_runtime_repairs_are_present_and_printf_safe() -> None:
    assert _record("/data/SC2.DK4", 23, 18).rstrip() == b"Teach me more."
    contract = _record("/data/SC2.DK4", 24, 9)
    assert contract.startswith(b"\x09")
    assert b"small share" in contract
    assert b"%" not in contract
    refusal = _record("/data/SC2.DK4", 120, 12)
    assert refusal.startswith(b"\x02No thanks.")
    assert b"Not my thing." in refusal


def test_supply_ratio_heading_and_profile_are_unified() -> None:
    arm9 = NdsImage.open(CANDIDATE).read_file("/__arm9__.bin")
    assert arm9[0x14A44C : 0x14A458] == b"Supply Ratio"
    assert arm9[0x14A458] == 0

    profiles = json.loads(
        Path("translations/release_stack.json").read_text(encoding="utf-8")
    )["profiles"]
    unified = profiles["all-routes-unified-v1"]["batches"]
    assert "translations/common_mesfile_spacing_v4.json" in unified
    assert "translations/supply_ratio_label_arm9_v1.json" in unified
    assert "translations/lil_deep_route_v21.json" in unified
