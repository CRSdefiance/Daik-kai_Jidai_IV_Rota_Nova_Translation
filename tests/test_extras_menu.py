from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from dk4tool.graphics.pxl import PxlImage
from dk4tool.rom.nds import NdsImage
from scripts.build_integrated_release import (
    apply_arm9_fixed_batch,
    apply_pxl_label_batches,
    resolve_release_batches,
)
from scripts.materialize_extras_menu_v1 import encode_pair_phase_multiline

BASE = Path("out/raphael_natural_v2_pre_extras_common_v6_accepted_rollback.nds")
ARM9_BATCH = Path("translations/extras_menu_arm9_v1.json")
GRAPHICS = [
    Path(f"translations/extras_online{number:02d}_graphics_v1.json")
    for number in [0, *range(50, 63)]
]


def _load(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def test_extras_profile_contains_the_complete_feature_layer() -> None:
    with pytest.raises(ValueError, match="accepted-baked"):
        resolve_release_batches("extras-menu-v1", [])


def test_combined_test_profile_adds_the_coordinated_sound_layer() -> None:
    with pytest.raises(ValueError, match="accepted-baked"):
        resolve_release_batches("extras-options-sound-v1", [])


def test_extras_arm9_text_is_source_locked_terminated_and_complete() -> None:
    image = NdsImage.open(BASE)
    source = image.read_file("/__arm9__.bin")
    batch = _load(ARM9_BATCH)
    assert hashlib.sha256(source).hexdigest() == batch["source_file_sha256"]
    assert len(batch["records"]) == 37

    rebuilt, record_ids = apply_arm9_fixed_batch(ARM9_BATCH, source)
    assert len(record_ids) == 37
    for record in batch["records"]:
        offset = int(record["offset"])
        expected = bytes.fromhex(str(record["source_hex"]))
        english = str(record["english"]).encode(str(record.get("encoding", "ascii")))
        actual = rebuilt[offset : offset + len(expected)]
        assert actual == english.ljust(len(expected), b"\0")
        assert actual[len(english)] == 0
        if b"\n" in english and record.get("encoding", "ascii") == "ascii":
            assert b"\n " in english
            assert not english.endswith(b"\n")

    assert rebuilt[0x13796C : 0x13797C] == b"Options\0Map\0\0\0\0\0"
    assert rebuilt[0x1385CC : 0x1385E4] == b"On\0\0\0\0\0\0\x90\xDD\x92\xE8\0\0\0\0Off\0\0\0\0\0"
    sail_prompt = rebuilt[0x13880C : 0x138842]
    assert not sail_prompt.startswith("現在".encode("cp932"))
    assert "Ｃｈａｎｇｅ　ｔｏ".encode("cp932") in sail_prompt


def test_extras_multiline_text_repairs_progressive_ascii_pair_phase() -> None:
    assert encode_pair_phase_multiline("A\nBC\nD\n") == b"A\n BC \n D"
    assert encode_pair_phase_multiline(
        "Learn about this game's\n"
        "tie-in with the PC title\n"
        "Uncharted Waters Online.\n"
        "Playing both games opens\n"
        "new ways to enjoy this game.\n"
    ) == (
        b"Learn about this game's\n "
        b"tie-in with the PC title \n "
        b"Uncharted Waters Online. \n "
        b"Playing both games opens \n "
        b"new ways to enjoy this game."
    )

    encoded = encode_pair_phase_multiline("AA\nB\nCCCC\nD")
    for index, value in enumerate(encoded):
        if value == 0x0A:
            printable = sum(0x20 <= byte < 0x80 for byte in encoded[:index])
            assert printable % 2 == 1
            assert encoded[index + 1] == 0x20


def test_extras_graphics_are_source_locked_fixed_size_and_renderable() -> None:
    image = NdsImage.open(BASE)
    for batch_path in GRAPHICS:
        batch = _load(batch_path)
        file_path = str(batch["file_path"])
        source = image.read_file(file_path)
        assert hashlib.sha256(source).hexdigest() == batch["source_file_sha256"]
        rebuilt, record_ids = apply_pxl_label_batches([batch_path], source)
        assert len(rebuilt) == len(source)
        assert rebuilt != source
        assert record_ids == [str(record["id"]) for record in batch["records"]]
        rendered = PxlImage.from_bytes(rebuilt).render()
        assert rendered.size == (256, 192)


def test_online_text_cards_use_the_multiline_solid_redraw() -> None:
    for batch_path in GRAPHICS[1:]:
        batch = _load(batch_path)
        assert len(batch["records"]) == 1
        record = batch["records"][0]
        assert record["box"] == [0, 0, 256, 192]
        assert record["erase"] == "solid"
        assert "\n" in record["text"]
        assert record["outline_index"] == 1
