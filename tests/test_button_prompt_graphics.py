"""Meaningful regression gates for both source-locked button prompt copies."""

import json
from pathlib import Path

import pytest

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.graphics.pxl import PxlImage
from dk4tool.rom.nds import NdsImage
from scripts.build_integrated_release import apply_ilnk_pxl_sync_batch, apply_pxl_native_label_batch
from scripts.materialize_button_prompt_v160 import LABEL, SYNC
from scripts.probe_button_prompt_native import dimensions, glyphs
from scripts.research_button_prompt import ARCHIVE, BLOCK, BOX, LOOSE, ROM, TEXT, design, make


@pytest.fixture(scope='module')
def case():
    rom = NdsImage.open(ROM)
    return rom, make(rom)


def test_complete_native_glyphs_and_first_character(case):
    rom, (loose, _, mask, origin) = case
    glyphs(rom.read_file('/__arm9__.bin'), loose, mask, origin)
    missing_first = mask.copy()
    missing_first.paste(0, (origin[0], origin[1], origin[0] + 6, origin[1] + 11))
    with pytest.raises(ValueError, match='first character'):
        glyphs(rom.read_file('/__arm9__.bin'), loose, missing_first, origin)


@pytest.mark.parametrize('index', [20, 21, 255])
def test_native_full_image_size_and_clamped_selectors(case, index):
    rom, (loose, _, _, _) = case
    dimensions(rom.read_file('/__arm9__.bin'), loose, index)


def test_paired_batches_equal_reviewed_artwork(case):
    rom, (loose, archive, _, _) = case
    base = NdsImage.open('out/raphael_natural_v2_accepted_base.nds')
    actual, _ = apply_pxl_native_label_batch(LABEL, base.read_file(LOOSE), base.read_file('/__arm9__.bin'))
    assert actual == loose
    actual, _ = apply_ilnk_pxl_sync_batch(SYNC, base.read_file(ARCHIVE), loose)
    assert actual == archive
    a, b = IlnkContainer.parse(rom.read_file(ARCHIVE)), IlnkContainer.parse(actual)
    assert len(a.blocks) == len(b.blocks)
    assert all(x == y for i, (x, y) in enumerate(zip(a.blocks, b.blocks)) if i != BLOCK)


def test_complete_source_pixels_and_metadata_locked(case):
    rom, _ = case
    original = rom.read_file(LOOSE)
    p = PxlImage.from_bytes(original)
    bad = NdsImage.open(ROM)
    changed = bytearray(original)
    changed[p.pixels_offset + 31] ^= 1
    bad.replace_file(LOOSE, bytes(changed))
    with pytest.raises(ValueError, match='Japanese prompt'):
        make(bad)


def test_owned_rectangle_and_complete_natural_instruction(case):
    rom, (loose, _, _, _) = case
    old, new = PxlImage.from_bytes(rom.read_file(LOOSE)), PxlImage.from_bytes(loose)
    assert old.source[:old.pixels_offset] == new.source[:new.pixels_offset]
    l, t, r, b = BOX
    assert all(old.indices[y * 156 + x] == new.indices[y * 156 + x]
               for y in range(24) for x in range(156) if not (l <= x < r and t <= y < b))
    with pytest.raises(ValueError, match='complete prompt'):
        design(old.indices, GameAsciiFont.from_arm9(rom.read_file('/__arm9__.bin')), TEXT[1:])


def test_all_previous_batches_and_terminal_stages_inherited():
    registry = json.loads(Path('translations/release_stack.json').read_text(encoding='utf-8'))
    old, new = registry['profiles']['all-routes-unified-v159'], registry['profiles']['all-routes-unified-v160']
    assert new['batches'] == old['batches'] + [LABEL.as_posix(), SYNC.as_posix()]
    assert len(new['batches']) == 437
    assert new['status'] == 'experimental'
    for key, value in old.items():
        if key not in ('batches', 'note', 'description'):
            assert new[key] == value
