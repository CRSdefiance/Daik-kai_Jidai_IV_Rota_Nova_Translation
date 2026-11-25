import struct

import pytest

from dk4tool.rom.nds import NdsImage
from scripts.execute_map_entity_tooltip_copy import format_copy, select
from scripts.execute_scene_caption_raster import execute
from scripts.prepare_map_entity_tooltips import RANGES, ROWS, prepare
from scripts.probe_map_entity_tooltip_raster import verify_raster


@pytest.fixture(scope='module')
def images():
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    canonical = NdsImage.open('out/raphael_natural_v2_accepted_base.nds').read_file('/__arm9__.bin')
    current = NdsImage.open('out/all_routes_combined_v139_candidate.nds').read_file('/__arm9__.bin')
    return clean, canonical, current


@pytest.fixture(scope='module')
def compiled(images):
    return prepare(*images)


@pytest.mark.parametrize('case', ['pirates', 'monster', 'unknown', 'named'])
def test_actual_native_selection_preserves_full_labels(compiled, case):
    select(compiled[1], case)


@pytest.mark.parametrize('name,ship_class', [
    (b'Pirates', b'Carrack'), (b'Monster', b'Dhow'),
    (b'???', 'キャラック'.encode('cp932')),
])
def test_native_printf_retains_name_and_class_bytes(compiled, name, ship_class):
    format_copy(compiled[1], 0x705F0, [name, ship_class], name + b'\n  ' + ship_class + b' class')


def test_native_percentage_escape_and_minimum_field_width(compiled):
    # Field widths are minimum widths: long actual values must not be truncated.
    format_copy(compiled[1], 0x705F4, [b'Fleet', b'1234567', b'123456789'],
                b'Fleet  1234567%\n  Armament 123456789')


def test_selected_leading_character_mutation_rejects(compiled):
    changed = bytearray(compiled[1])
    offset = struct.unpack_from('<I', changed, 0x705EC)[0] - 0x02000000
    changed[offset] = ord('X')
    with pytest.raises(ValueError, match='full wording'):
        select(bytes(changed), 'pirates')


def test_changed_source_padding_rejects(images):
    clean, canonical, current = images
    changed = bytearray(clean)
    changed[0x1190F3] = 1
    with pytest.raises(ValueError, match='padding'):
        prepare(bytes(changed), canonical, current)


def test_extra_literal_consumer_rejects(images):
    clean, canonical, current = images
    changed = bytearray(clean)
    struct.pack_into('<I', changed, 0x100, 0x021190ED)
    with pytest.raises(ValueError, match='additional literal'):
        prepare(bytes(changed), canonical, current)


def test_complete_allocation_preserves_every_unrelated_byte(images, compiled):
    current, proposed = images[2], compiled[1]
    owned = {i for lo, hi in RANGES for i in range(lo, hi)}
    owned.update(i for _, _, _, field, *_ in ROWS for i in range(field, field + 4))
    assert all(i in owned for i, (a, b) in enumerate(zip(current, proposed, strict=True)) if a != b)
    assert compiled[2]['allocated_bytes'] == 51
    assert all(r['review']['formatting'] is False for r in compiled[0]['records'])


@pytest.mark.parametrize('name', ['Pirates', 'FleetX', '???', 'Nagarpur Co.'])
@pytest.mark.parametrize('mode', [4, 16])
def test_native_guarded_pixels_keep_every_character_on_correct_row(compiled, name, mode):
    verify_raster(compiled[1], name + '\n  Armed Retonda class', mode)


@pytest.mark.parametrize('name', ['Pirates', 'FleetX'])
def test_single_blank_is_insufficient_for_both_parities(compiled, name):
    result = execute(compiled[1], name + '\n Carrack class', tooltip=True)
    visible = [g for g in result['glyphs'] if g['y'] == 12 and g['code'] != 32]
    if name == 'Pirates':
        assert visible[0]['x'] == 0
    else:
        # Even preceding parity puts C and a at the same x: byte-copy success
        # alone cannot approve formatting. Two generated blanks fix this.
        assert visible[0]['x'] == visible[1]['x'] == 6


def test_no_guard_moves_leading_character_to_previous_row(compiled):
    result = execute(compiled[1], 'Pirates\nCarrack class', tooltip=True)
    leading = next(g for g in result['glyphs'] if g['code'] == ord('C'))
    assert leading['y'] == 0


def test_tooltip_width_overflow_is_not_approved(compiled):
    with pytest.raises(ValueError, match='physical screen width'):
        verify_raster(compiled[1], 'Fleet\n  ' + 'A' * 41, 16)
