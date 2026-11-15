import struct

import pytest

from dk4tool.patch.bgm_title_tracking import (
    PATCH_OFFSET,
    REPLACEMENT,
    SOURCE,
    apply_probe,
)
from dk4tool.rom.nds import NdsImage
from scripts.audit_common_bgm_titles import title_geometry


@pytest.fixture(scope='module')
def baseline_arm9():
    return NdsImage.open('out/raphael_natural_v2_accepted_base.nds').read_file('/__arm9__.bin')


def test_only_four_title_instructions_change_and_no_cave_is_used(baseline_arm9):
    patched = apply_probe(baseline_arm9)
    assert patched[:PATCH_OFFSET] == baseline_arm9[:PATCH_OFFSET]
    assert patched[PATCH_OFFSET + 16:] == baseline_arm9[PATCH_OFFSET + 16:]
    assert len(patched) == len(baseline_arm9)
    assert baseline_arm9[PATCH_OFFSET:PATCH_OFFSET + 16] == SOURCE
    assert patched[PATCH_OFFSET:PATCH_OFFSET + 16] == REPLACEMENT


@pytest.mark.parametrize('offset', [0x109290, 0xD57E8, 0xD5AE0, 0x125A60])
def test_changed_title_cursor_tracking_or_font_is_rejected(baseline_arm9, offset):
    bad = bytearray(baseline_arm9)
    bad[offset] ^= 1
    with pytest.raises(ValueError, match='differs'):
        apply_probe(bytes(bad))


def test_complete_village_title_fits_the_mapped_five_pixel_probe():
    result = title_geometry('Southeast Asian Village', advance=5)
    assert result['width_pixels'] == 115
    assert result['left'] == 7 and result['right'] == 122
    assert result['fits_panel']


def test_probe_centering_matches_native_arithmetic_for_every_title(baseline_arm9):
    # Independently decode the four replacement opcodes, then reproduce
    # positive-length ADD/ASR and the following unchanged RSB immediate.
    assert struct.unpack('<4I', REPLACEMENT) == (
        0xE3E02000, 0xE58D201C, 0xE0801100, 0xE1A000C1)
    assert struct.unpack_from('<I', baseline_arm9, 0x109290)[0] == 0xE2603040
    for length in range(1, 26):
        r1 = length + (length << 2)
        r0 = r1 >> 1
        r3 = 64 - r0
        assert r3 == title_geometry('A' * length, advance=5)['left']
