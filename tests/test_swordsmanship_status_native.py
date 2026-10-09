"""Protect the stats variadic stack argument and actual numeric/bitmap bounds."""

import struct
from pathlib import Path

import pytest
from unicorn import UcError

from dk4tool.patch.swordsmanship_status_release import (
    BASE,
    BITMAP_WIDTH,
    DESCRIPTOR,
    INHERITED_TRACKING_WRAPPER,
    formatted,
)
from dk4tool.rom.nds import NdsImage
from scripts.execute_scene_caption_raster import execute
from scripts.probe_common_display_name_hook import branch_link
from scripts.probe_duel_parent_composition import composition
from scripts.probe_map_tooltip_cp932_pixels import expected_pixels
from scripts.verify_swordsmanship_status_research import clamp, compose, geometry


@pytest.fixture(scope='module')
def source_font():
    return (Path('work/analysis/swordsmanship_status_research_arm9.bin').read_bytes(),
            NdsImage.open('work/clean.nds').read_file('/GRP/KANJI.FNT'))


@pytest.mark.parametrize('mode,index', [(4, 0), (16, 1)])
def test_third_variadic_stack_argument_survives_full_native_caller(source_font, mode, index):
    source, font = source_font
    value = formatted(500, 65535, 'Wounded')
    native = execute(source, value, sword_stats=(500, 65535, 2), duel_actor_index=index,
                     surface_size=(BITMAP_WIDTH, 12), kanji_font=font, mode=mode)
    assert [g['code'] for g in native['glyph_events']] == list(value.encode('ascii'))
    assert all(g['x'] + 6 <= BITMAP_WIDTH and g['y'] == 0 for g in native['glyph_events'])
    assert native['pixels'] == expected_pixels(source, font, native['glyph_events'], mode, background=0)


def test_reusing_push_wrapper_reproduces_invalid_suffix_pointer(source_font):
    source, font = source_font
    changed = bytearray(source)
    struct.pack_into('<I', changed, 0xE2FC, branch_link(BASE + 0xE2FC, INHERITED_TRACKING_WRAPPER))
    with pytest.raises(UcError):
        execute(bytes(changed), formatted(500, 65535, 'Wounded'), sword_stats=(500, 65535, 2),
                surface_size=(BITMAP_WIDTH, 12), kanji_font=font)


def test_native_skill_clamp_and_exact_bitmap_are_required(source_font):
    source, font = source_font
    assert [r['native_clamped_skill'] for r in clamp(source)] == [0, 0, 0, 1, 499, 500, 500, 500, 500]
    assert [geometry(source, i)['actual_constructor_stack_arguments'] for i in (0, 1)] == [[BITMAP_WIDTH, 12, 0, 0]] * 2
    with pytest.raises(ValueError, match='mapped skill'):
        execute(source, formatted(501, 65535, 'Healthy'), sword_stats=(501, 65535, 0), surface_size=(BITMAP_WIDTH, 12), kanji_font=font)


def test_original_short_crop_is_rejected_and_complete_state_fits_native_panels(source_font):
    source, font = source_font
    panels = composition(source)
    native = execute(source, formatted(500, 65535, 'Wounded'), sword_stats=(500, 65535, 2),
                     surface_size=(BITMAP_WIDTH, 12), kanji_font=font)
    for slot in panels['actor_slots']:
        compose(native, slot, 16)
    panels['actor_slots'][0]['draw_requests'][2]['size'][0] = 24
    with pytest.raises(ValueError, match='split or drop'):
        compose(native, panels['actor_slots'][0], 16)
    changed = bytearray(source)
    struct.pack_into('<I', changed, DESCRIPTOR + 76, 24)
    with pytest.raises(ValueError, match='crop clips'):
        composition(bytes(changed))
