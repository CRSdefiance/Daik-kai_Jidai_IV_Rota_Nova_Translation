import struct

import pytest

from dk4tool.rom.nds import NdsImage
from scripts.execute_scene_caption_raster import execute
from scripts.probe_deck_explanation_layout import format_paragraph, geometry
from scripts.probe_deck_explanation_sources import ROWS


def source():
    return NdsImage.open('out/all_routes_combined_v145_candidate.nds').read_file('/__arm9__.bin')


def test_native_deck_bitmap_width_mutation_is_detected():
    original = source()
    assert geometry(original)['dimensions'] == [168, 84]
    changed = bytearray(original)
    assert struct.unpack_from('<I', changed, 0x19FAC)[0] == 0xE3A0E02A
    struct.pack_into('<I', changed, 0x19FAC, 0xE3A0E029)
    with pytest.raises(ValueError, match='bitmap initialization differs'):
        geometry(bytes(changed))


def test_deck_continuation_without_native_guard_is_rejected():
    text = format_paragraph(ROWS[0][4]).replace('\n  ', '\n')
    with pytest.raises(ValueError, match='two-space guards'):
        execute(source(), text, tracking=0, x=0, y=0, surface_size=(168, 84), deck=True)


def test_unmapped_deck_origin_or_tracking_is_rejected():
    for tracking, x in ((-1, 0), (0, 1)):
        with pytest.raises(ValueError, match='native zero origin/tracking'):
            execute(source(), ROWS[1][4], tracking=tracking, x=x, y=0,
                    surface_size=(168, 84), deck=True)
