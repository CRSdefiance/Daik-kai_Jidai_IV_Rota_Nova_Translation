from pathlib import Path

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from scripts.audit_release_translation_integrity import build_report


CANDIDATE = Path("out/all_routes_unified_v5_candidate.nds")
CLEAN = Path("work/clean.nds")


def record(rom: NdsImage, file_path: str, block: int, index: int) -> bytes:
    return IlnkContainer.parse(rom.read_file(file_path)).blocks[block].split(b"\0")[index]


def test_full_release_integrity_audit_has_no_blocking_issue() -> None:
    report = build_report(CANDIDATE, CLEAN, "all-routes-unified-v1")
    assert report["status"] == "pass"
    assert report["blocking_issue_count"] == 0
    assert report["audited_entry_count"] >= 890
    assert report["unsafe_percent_record_count"] == 0
    assert report["runtime_name_count"] == 10


def test_cargo_setup_preserves_all_three_independent_entries() -> None:
    raw = record(NdsImage.open(CANDIDATE), "/COMMON/MESFILE.DK4", 10, 36)
    entries = [raw[0:65], raw[65:93], raw[93:152]]
    assert b"Your sailors look tired" in entries[0]
    assert b"You have no cargo." in entries[1]
    assert b"Not enough coins to fully resupply" in entries[2]
    assert all(entry.strip(b" ") for entry in entries)


def test_literal_percent_text_is_runtime_safe() -> None:
    rom = NdsImage.open(CANDIDATE)
    help_text = record(rom, "/COMMON/HELP.DK4", 38, 0)
    tutorial = record(rom, "/data/SC0.DK4", 45, 52)
    assert b"percent" in help_text and b"%" not in help_text
    assert b"20 percent market share" in tutorial
    assert b"20%" not in tutorial
