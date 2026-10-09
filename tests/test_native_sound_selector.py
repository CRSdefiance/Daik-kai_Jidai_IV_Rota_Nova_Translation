import json
import struct
from pathlib import Path

import pytest

from dk4tool.patch.bgm_title_tracking import apply_probe
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import TABLE_OFFSET, common_message_entries
from scripts.verify_native_sound_selector import BGM_IDS, verify_components


@pytest.fixture(scope='module')
def sound():
    base = NdsImage.open('out/raphael_natural_v2_accepted_base.nds')
    current = NdsImage.open('out/all_routes_combined_v128_candidate.nds')
    baseline_arm9 = base.read_file('/__arm9__.bin')
    entries = common_message_entries(base.read_file('/COMMON/MESFILE.DK4'),
                                     baseline_arm9, clean=False)
    expected = {i: entries[i].text.rstrip(b' ') for i in BGM_IDS}
    batch = json.loads(Path('translations/sound_selector_arm9.json').read_text(encoding='utf-8'))
    slots = [(r['id'], r['offset'], r['english'].encode('ascii').ljust(
        len(bytes.fromhex(r['source_hex'])), b'\0')) for r in batch['records'][1:]]
    return (current.read_file('/COMMON/MESFILE.DK4'), current.read_file('/__arm9__.bin'),
            expected, slots, baseline_arm9)


def test_relocated_titles_and_all_sound_slots_are_preserved(sound):
    result = verify_components(*sound)
    assert result['native_bgm_titles_checked'] == 38
    assert result['sfx_titles_checked'] == 57
    assert result['static_track_selection_bounds'] == [2, 39]
    assert result['static_native_title_id_bounds'] == [3251, 3288]
    assert not result['runtime_selection_and_playback_verified']


def test_valid_native_start_that_drops_the_first_title_character_is_rejected(sound):
    common, arm9, expected, slots, baseline = sound
    bad = bytearray(arm9)
    offset = TABLE_OFFSET + 3251 * 2
    start = struct.unpack_from('<H', bad, offset)[0]
    struct.pack_into('<H', bad, offset, start + 1)
    with pytest.raises(ValueError, match='Native BGM message 3251'):
        verify_components(common, bytes(bad), expected, slots, baseline)


def test_changed_selector_arithmetic_is_rejected(sound):
    common, arm9, expected, slots, baseline = sound
    bad = bytearray(arm9)
    bad[0x109270] ^= 1
    with pytest.raises(ValueError, match='Sound selector code differs'):
        verify_components(common, bytes(bad), expected, slots, baseline)


def test_changed_sfx_first_character_is_rejected(sound):
    common, arm9, expected, slots, baseline = sound
    bad = bytearray(arm9)
    bad[slots[0][1]] = ord('X')
    with pytest.raises(ValueError, match='SFX title'):
        verify_components(common, bytes(bad), expected, slots, baseline)


@pytest.mark.parametrize('offset', [0x108FC8, 0x108FD4, 0x10904C])
def test_changed_track_limit_or_playback_call_is_rejected(sound, offset):
    common, arm9, expected, slots, baseline = sound
    bad = bytearray(arm9)
    bad[offset] ^= 1
    with pytest.raises(ValueError, match='Sound selector code differs'):
        verify_components(common, bytes(bad), expected, slots, baseline)


def test_exact_tracking_renderer_requires_explicit_declaration(sound):
    common, arm9, expected, slots, baseline = sound
    tracked = apply_probe(arm9)
    with pytest.raises(ValueError, match='Sound selector code differs'):
        verify_components(common, tracked, expected, slots, baseline)
    result = verify_components(common, tracked, expected, slots, baseline, tracking_renderer=True)
    assert result['bgm_ascii_advance'] == 5
    assert result['sound_code_matches_exact_declared_renderer']
    assert not result['selector_code_unchanged']


@pytest.mark.parametrize('offset', [0xD57E8, 0x125A60])
def test_tracking_renderer_rejects_changed_context_or_font(sound, offset):
    common, arm9, expected, slots, baseline = sound
    bad = bytearray(apply_probe(arm9))
    bad[offset] ^= 1
    with pytest.raises(ValueError, match='Mapped BGM'):
        verify_components(common, bytes(bad), expected, slots, baseline, tracking_renderer=True)
