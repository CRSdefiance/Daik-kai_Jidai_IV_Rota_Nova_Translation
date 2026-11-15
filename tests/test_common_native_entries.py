from __future__ import annotations

import json
import struct
from pathlib import Path

import pytest

from dk4tool.dialogue.font_audit import SJIS_GLYPH_COUNT, SJIS_MAP_OFFSET, decode_glyph
from dk4tool.dialogue.qa import audit_native_common_entry
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_entry_tables import (
    B32_TABLE_OFFSET,
    ITEM_TABLES,
    b32_item_entries,
    native_item_entries,
)
from scripts.build_integrated_release import validate_fixed_allocation_policy


def test_native_wrapper_checks_actual_paragraph_bytes_without_stored_breaks() -> None:
    text = "A Chinese invention, vital when finding your direction at sea."
    source = "あ".encode("cp932") * 34
    audit = audit_native_common_entry(source, text + "{PAD}")
    assert not [issue for issue in audit["issues"] if issue["severity"] in {"error", "warning"}]
    encoded = bytes.fromhex(audit["native_encoded_hex"])
    assert encoded.rstrip(b" ") == text.encode("ascii")
    assert b"\n" not in encoded
    assert len(encoded) == len(source)
    assert len(audit["visible_lines"]) == 2


def test_native_wrapper_rejects_overflow_and_executable_ascii_macros() -> None:
    overflow = audit_native_common_entry("あ".encode("cp932") * 10, "This paragraph exceeds twenty bytes.{PAD}")
    assert any(issue["code"] == "native-entry-encoding" for issue in overflow["issues"])
    macro = audit_native_common_entry("あ".encode("cp932") * 25, "Fine ships sail faster.{PAD}")
    assert any("unsafe-literal-macro" in issue["message"] for issue in macro["issues"])


@pytest.fixture
def clean_item_sources() -> tuple[bytes, bytes]:
    path = Path("work/clean.nds")
    if not path.exists():
        pytest.skip("local clean ROM required for source-locked entry evidence")
    image = NdsImage.open(path)
    return image.read_file("/COMMON/MESFILE.DK4"), image.read_file("/__arm9__.bin")


def test_native_table_matches_clean_packed_bible_entry(clean_item_sources: tuple[bytes, bytes]) -> None:
    common, arm9 = clean_item_sources
    entries = b32_item_entries(common, arm9)
    bible = next(entry for entry in entries if entry.item_index == 107)
    assert bible.record_index == 1
    assert bible.block_offset == 184
    assert bible.start == 89
    assert bible.source.decode("cp932").startswith("聖書の難解な部分に")
    damaged = bytearray(arm9)
    damaged[B32_TABLE_OFFSET + 4:B32_TABLE_OFFSET + 6] = (185).to_bytes(2, "little")
    with pytest.raises(ValueError):
        b32_item_entries(common, damaged)


def test_new_layouts_keep_first_character_at_native_pointers(clean_item_sources: tuple[bytes, bytes]) -> None:
    common, arm9 = clean_item_sources
    entries = b32_item_entries(common, arm9)
    clean_rows = IlnkContainer.parse(common).blocks[32].split(b"\0")
    checked = 0
    for filename in ("common_remaining_b32_layout_v2.json", "common_b32_packed_layout_v3.json"):
        batch = json.loads((Path("translations") / filename).read_text(encoding="utf-8"))
        for record in batch["records"]:
            index = int(record["id"].split("_R")[1])
            selected = [entry for entry in entries if entry.record_index == index]
            raw = bytes.fromhex(record["replacement_hex"])
            assert len(raw) == len(clean_rows[index])
            assert record["entry_offsets"] == [entry.start for entry in selected]
            for entry, text in zip(selected, record["display_entries"], strict=True):
                assert raw[entry.start:entry.end].rstrip(b" ") == text.encode("cp932")
                first = text[0].encode("cp932")
                assert raw[entry.start:entry.start + len(first)] == first
                assert b"\n" not in raw[entry.start:entry.end]
                checked += 1
            assert raw[:selected[0].start] == clean_rows[index][:selected[0].start]
    assert checked == 46


def test_safe_reserved_latin_requires_explicit_glyph_declaration() -> None:
    raw = "Ｉndian".encode("cp932")
    record = {"id": "test", "replacement_hex": raw.hex(), "translated_ranges": [[0, len(raw)]],
              "entry_offsets": [0], "entry_ends": [len(raw)], "entry_guard_bytes": 0,
              "linebreak_guard_bytes": 0, "safe_literal_latin_glyphs": ["Ｉ"]}
    header = {"fixed_allocation_policy": "screen-entry-layout-v1", "records": [record]}
    validate_fixed_allocation_policy(Path("test.json"), header)
    record["safe_literal_latin_glyphs"] = []
    with pytest.raises(ValueError, match="non-ASCII"):
        validate_fixed_allocation_policy(Path("test.json"), header)
    record["safe_literal_latin_glyphs"] = ["日"]
    with pytest.raises(ValueError, match="unsupported"):
        validate_fixed_allocation_policy(Path("test.json"), header)


def test_fullwidth_I_has_an_exact_native_font_glyph(clean_item_sources: tuple[bytes, bytes]) -> None:
    _, arm9 = clean_item_sources
    image = NdsImage.open(Path("work/clean.nds"))
    mapping = struct.unpack_from(f"<{SJIS_GLYPH_COUNT}H", arm9, SJIS_MAP_OFFSET)
    glyph_index = mapping.index(int.from_bytes("Ｉ".encode("cp932"), "big"))
    assert glyph_index == 82
    glyph = decode_glyph(image.read_file("/GRP/KANJI.FNT"), glyph_index)
    assert glyph.getbbox() is not None
    row = next(row for row in json.loads(Path("translations/common_b32_packed_manuscript_v2.json").read_text(encoding="utf-8"))["records"] if row["item_index"] == 140)
    entry = next(entry for entry in b32_item_entries(*clean_item_sources) if entry.item_index == 140)
    audit = audit_native_common_entry(entry.source, row["english"])
    assert not [issue for issue in audit["issues"] if issue["severity"] in {"error", "warning"}]
    assert b"\x82\x68" in bytes.fromhex(audit["native_encoded_hex"])


@pytest.mark.parametrize("block,count,first,last", [(29, 10, 0, 9), (30, 49, 10, 58), (31, 46, 59, 104)])
def test_adjacent_item_tables_have_complete_source_locked_mapping(
    clean_item_sources: tuple[bytes, bytes], block: int, count: int, first: int, last: int,
) -> None:
    common, arm9 = clean_item_sources
    entries = native_item_entries(common, arm9, block)
    assert [entry.item_index for entry in entries] == list(range(first, last + 1))
    assert len(entries) == count
    assert all(entry.block_offset % 2 == 0 for entry in entries)
    damaged = bytearray(arm9)
    damaged[ITEM_TABLES[block][0] + 2] ^= 1
    with pytest.raises(ValueError, match="exact clean"):
        native_item_entries(common, damaged, block)


def test_b29_item_tail_does_not_authorize_diplomacy_records(clean_item_sources: tuple[bytes, bytes]) -> None:
    entries = native_item_entries(*clean_item_sources, 29)
    assert entries[0].block_offset == 3136
    assert entries[0].source.decode("cp932").startswith("新大陸で栽培されている植物")
    assert {entry.record_index for entry in entries} == set(range(53, 61))
    batch = json.loads(Path("translations/common_b29_native_layout_v1.json").read_text(encoding="utf-8"))
    assert {record["id"] for record in batch["records"]} == {f"DK4_MES_B29_R{i:04d}" for i in range(53, 61)}
    for record in batch["records"]:
        index = int(record["id"].split("_R")[1])
        raw = bytes.fromhex(record["replacement_hex"])
        selected = [entry for entry in entries if entry.record_index == index]
        assert record["entry_offsets"] == [entry.start for entry in selected]
        for entry, text in zip(selected, record["display_entries"], strict=True):
            assert raw[entry.start:entry.end].rstrip(b" ") == text.encode("cp932")
            assert raw[entry.start:entry.end].startswith(text[0].encode("cp932"))


@pytest.mark.parametrize("block,first,last", [(30, 10, 58), (31, 59, 104)])
@pytest.mark.parametrize("version", [1, 2])
def test_adjacent_layout_preserves_all_native_entry_starts(
    clean_item_sources: tuple[bytes, bytes], block: int, first: int, last: int, version: int,
) -> None:
    common, arm9 = clean_item_sources
    entries = native_item_entries(common, arm9, block)
    clean_rows = IlnkContainer.parse(common).blocks[block].split(b"\0")
    batch = json.loads(Path(f"translations/common_b{block}_native_layout_v{version}.json").read_text(encoding="utf-8"))
    seen = []
    for record in batch["records"]:
        index = int(record["id"].split("_R")[1])
        selected = [entry for entry in entries if entry.record_index == index]
        raw = bytes.fromhex(record["replacement_hex"])
        assert len(raw) == len(clean_rows[index])
        assert record["entry_offsets"] == [entry.start for entry in selected]
        assert raw[:selected[0].start] == clean_rows[index][:selected[0].start]
        for entry, text in zip(selected, record["display_entries"], strict=True):
            assert raw[entry.start:entry.end].rstrip(b" ") == text.encode("cp932")
            assert raw[entry.start:entry.end].startswith(text[0].encode("cp932"))
            assert not b"\n" in raw[entry.start:entry.end]
            seen.append(entry.item_index)
    assert seen == list(range(first, last + 1))
