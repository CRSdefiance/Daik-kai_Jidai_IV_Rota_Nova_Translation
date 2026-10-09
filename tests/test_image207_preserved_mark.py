"""Regression: unknown source pixels and complete English must both survive."""

import json
from pathlib import Path

import pytest

from dk4tool.graphics.pxl import PxlImage
from scripts.build_integrated_release import apply_pxl_native_label_batch
from scripts.preserve_image207_v178 import BATCH, OLD, PATH, preservation, sources


@pytest.fixture(scope="module")
def case():
    base, prior = sources()
    target, _ = apply_pxl_native_label_batch(BATCH, base.read_file(PATH), base.read_file("/__arm9__.bin"))
    return base, prior, target


def test_original_clipped_mark_exact_and_english_does_not_move(case):
    base, prior, target = case
    a, b, c = [PxlImage.from_bytes(raw) for raw in (base.read_file(PATH), prior.read_file(PATH), target)]
    assert c.indices[:5120] == a.indices[:5120]
    assert c.indices[5120:] == b.indices[5120:]
    assert target[:a.pixels_offset] == a.source[:a.pixels_offset]
    assert preservation(target)["preserved_nonwhite_indices"] > 0
    old, new = [json.loads(p.read_text(encoding="utf-8")) for p in (OLD, BATCH)]
    assert old["records"][0]["text"] == new["records"][0]["text"] == "New World Village (Developed)"
    assert old["records"][0]["id"] == new["records"][0]["id"]


@pytest.mark.parametrize("position", ["first", "last"])
def test_cannot_drop_any_preserved_source_stroke_pixel(case, position):
    _, _, target = case
    pxl = PxlImage.from_bytes(target)
    ink = [i for i, v in enumerate(pxl.indices[:5120]) if v != 255]
    pxl.indices[ink[0] if position == "first" else ink[-1]] = 255
    with pytest.raises(ValueError, match="Clipped mark"):
        preservation(pxl.to_bytes())


@pytest.mark.parametrize("position", ["first", "last"])
def test_cannot_drop_leading_or_trailing_english_pixel(case, position):
    _, _, target = case
    pxl = PxlImage.from_bytes(target)
    ink = [i for i, v in enumerate(pxl.indices) if i >= 5120 and v == 168]
    # Sort by column first so this covers the N and closing parenthesis.
    ink.sort(key=lambda i: (i % 256, i // 256))
    pxl.indices[ink[0] if position == "first" else ink[-1]] = 255
    with pytest.raises(ValueError, match="unchanged complete English"):
        preservation(pxl.to_bytes())


def test_palette_mutation_rejected(case):
    _, _, target = case
    raw = bytearray(target)
    raw[20] ^= 1
    with pytest.raises(ValueError, match="header/palette"):
        preservation(bytes(raw))


def test_wrong_canonical_source_rejected(case):
    base, _, _ = case
    raw = bytearray(base.read_file(PATH))
    raw[-1] ^= 1
    with pytest.raises(ValueError, match="source SHA-256"):
        apply_pxl_native_label_batch(BATCH, bytes(raw), base.read_file("/__arm9__.bin"))


def test_exact_declared_supersession_and_every_other_stage_unchanged():
    stack = json.loads(Path("translations/release_stack.json").read_text(encoding="utf-8"))
    old, new = [stack["profiles"][p] for p in ("all-routes-unified-v177", "all-routes-unified-v178")]
    assert old["batches"].count(OLD.as_posix()) == 1
    assert new["batches"] == [BATCH.as_posix() if p == OLD.as_posix() else p for p in old["batches"]]
    assert len(new["batches"]) == 462
    assert all(new[k] == v for k, v in old.items() if k not in ("batches", "description", "note"))
