"""Verify two explicitly synthetic Grand Race UI conditions without multiplayer credit."""

import struct
from pathlib import Path

from PIL import Image, ImageChops

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.research_race_roster_v661 import main as native_main
from scripts.verify_confirmed_name_widget_pixels_v198 import complete_mask
from scripts.verify_movie_transition_bitmaps_v648 import rgb
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/race_roster_v661')
CAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193')
NAMES = [('Maria', 202), ('Chun', 216), ('Rafael', 240), ('Test Ship 2', 254),
         ('Hodram', 280), ('Test Ship 3', 294), ('Lil', 318), ('Test Ship 4', 332)]


def report(name, frames):
    path = CAP / ('race_roster_v661_' + name) / 'capture_report.json'
    data = read(path)
    assert data['ROM_sha256'] == read(ROOT / 'preflight.json')['candidate_sha256']
    assert data['frames'] == frames and data['cold_boot'] and not data['savestate_loaded']
    assert not data['callback_errors']
    assert data['battery_save_preloaded']['source_sha256'] == read(ROOT / 'preflight.json')['donor_sha256']
    images, ram = {}, {}
    for item in data['frames_captured']:
        p = Path(item['path'])
        assert sha(p.read_bytes()) == item['PNG_sha256']
        images[item['frame']] = Image.open(p).convert('RGB')
    for item in data.get('read_only_capture_RAM_snapshots', []):
        p = Path(item['path'])
        assert item['read_only_export'] and sha(p.read_bytes()) == item['sha256']
        ram[item['frame']] = p.read_bytes()
    for item in data.get('read_only_capture_native_states', []):
        p = Path(item['path'])
        assert sha(p.read_bytes()) == item['sha256']
        assert item['read_only_export'] and not item['state_loaded']
        assert item['main_RAM_unchanged_by_export'] and item['serialized_RAM_matches_same_frame_direct_export']
        for region in item['regions'].values():
            assert sha(Path(region['path']).read_bytes()) == region['sha256']
    return data, images, ram, {'path': str(path), 'sha256': sha(path.read_bytes())}


def main():
    pre = read(ROOT / 'preflight.json')
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    assert sha(Path(pre['donor']).read_bytes()) == pre['donor_sha256']
    arm = NdsImage.open(pre['candidate']).read_file('/__arm9__.bin')
    clean_arm = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    # Original host/SDK control flow and the two descriptors establish that this
    # Select is a text footer. This does not classify any other Confirm parent.
    spans = [(0xF98FC, 0xFA0CC), (0xFA5B0, 0xFA650), (0xFB528, 0xFB5B8),
             (0xFB6A0, 0xFB6D0), (0x10C4E8, 0x10C590), (0x10CB74, 0x10CD74),
             (0xCA890, 0xCA9E8), (0x11B620, 0x11B668)]
    for lo, hi in spans:
        assert arm[lo:hi] == clean_arm[lo:hi], (hex(lo), hex(hi))
    footer_edits = {0xCA7A8: 'f0c8fceb', 0xCA7B0: '0140a0e1',
                    0xCA808: 'e2c8fceb', 0xCA864: 'd4c8fceb'}
    assert {off: arm[off:off + 4].hex() for off in range(0xCA780, 0xCA890, 4)
            if arm[off:off + 4] != clean_arm[off:off + 4]} == footer_edits
    back = struct.unpack_from('<6I', arm, 0x11B620)
    ready = struct.unpack_from('<6I', arm, 0x11B650)
    assert back[:4] == ready[:4] == (0, 0, 0, 0)
    assert back[4:] == (0x0211B50C, 0)
    assert ready[4:] == (0x0211B50C, 0x0211B51C)
    assert arm[0x11B50C:0x11B511] == b'Back\0'
    assert arm[0x11B51C:0x11B523] == b'Select\0'
    _base, bi, _br, bb = report('host_baseline', 4400)
    _control, ci, cr, cb = report('controlled', 5000)
    _ring, ri, rr, rb = report('controlled_ring', 5000)
    before_pairs = []
    for frame in (1, 60, 180, 4400):
        assert bi[frame].tobytes() == ci[frame].tobytes() == ri[frame].tobytes()
        before_pairs.append(frame)
    for images in (ci, ri):
        assert images[4400].tobytes() == images[4690].tobytes()
    assert ci[4400].tobytes() == ci[4490].tobytes()
    assert ci[4550].tobytes() == ci[4590].tobytes()
    diff = ImageChops.difference(ci[4490], ci[4590])
    assert diff.getbbox() == (154, 368, 251, 384)
    footer_changes = sum(p != (0, 0, 0) for p in diff.get_flattened_data())
    assert footer_changes == 1228
    for frame, value in ((4490, 0), (4590, 2)):
        assert struct.unpack_from('<H', cr[frame], 0x1929B4 + 0xAC)[0] == value
        assert struct.unpack_from('<4I', cr[frame], 0x1929B4 + 0x88) == (0x0237B644, 0, 0, 0)
    font = GameAsciiFont.from_arm9(arm)
    masks, rejected = [], 0
    for frame in (4450, 4490, 4550, 4590):
        assert ri[frame].tobytes() == ri[4490].tobytes()
        raw, image = rr[frame], ri[frame].point(lambda n: n >> 3)
        assert struct.unpack_from('<4I', raw, 0x1929B4 + 0x88) == tuple(0x0237B644 + i * 52 for i in range(4))
        assert struct.unpack_from('<4I', raw, 0x1929B4 + 0xB0) == (3, 0, 1, 2)
        for text, y in NAMES:
            count, bounds = complete_mask(font, text, image, 74, y, (28, 28, 28))
            assert 0 <= bounds[0] < bounds[2] <= 256 and bounds[3] <= 384
            for index in (0, len(text) - 1):
                altered = image.copy()
                x0 = 74 + index * 6
                point = next((x0 + x, y + dy) for dy in range(11) for x in range(6)
                             if font.decode(text[index]).getpixel((x, dy)))
                altered.putpixel(point, (0, 0, 0))
                try:
                    complete_mask(font, text, altered, 74, y, (28, 28, 28))
                except ValueError:
                    rejected += 1
                else:
                    raise AssertionError('Lost leading/trailing letter was not detected')
            masks.append({'frame': frame, 'text': text, 'bounds': bounds, 'ink_points': count})
    fixture_reports = []
    for suffix, allowed in [('', {(0x0237B642, 2), (0x0237B678, 156), (0x0237D9F0, 2)}),
                            ('_ring', {(0x0237BBC0 + i * 512, 212) for i in range(4)} | {(0x0237D9F0, 2)})]:
        p = ROOT / ('roster_fixture_events' + suffix + '.json')
        events = read(p)
        assert events['final_frame'] == 5000 and len(events['events']) == 201
        assert not events['wireless_peer_verified'] and not events['ROM_changed']
        assert [e['before_frame'] for e in events['events']] == list(range(4401, 4602))
        assert all({(w['address'], w['bytes']) for w in e['writes']} == allowed for e in events['events'])
        fixture_reports.append({'path': str(p), 'sha256': sha(p.read_bytes())})
    native_main()
    native_path = ROOT / 'native_roster_research.json'
    native = read(native_path)
    assert len(native['completed_cards']) == 4
    assert native['all34208_card_pixels_assigned_over_poison'] and native['no_card_output_read_before_write']
    lower = (ROOT / 'native_four_cards_lower.bin').read_bytes()
    assert sha(lower) == native['lower_sha256']
    image = Image.new('RGB', (256, 192))
    image.putdata(rgb([v for v, in struct.iter_unpack('<H', lower)]))
    assert image.tobytes() == ri[4590].crop((0, 192, 256, 384)).tobytes()
    image.save(ROOT / 'native_four_cards_lower.png')
    proof = {'candidate': pre['candidate'], 'candidate_sha256': pre['candidate_sha256'],
        'previous_status_only_turn_classification': 'no progress; current continuation revalidated live files and advanced V661',
        'reports': {'baseline': bb, 'ready_only_fixture': cb, 'receive_ring_fixture': rb},
        'all_three_runs_terminal': True, 'baseline_frames': 4400, 'two_fixture_runs_frames': 5000,
        'pre_fixture_whole_frames_exact_across_three_cold_boots': before_pairs,
        'both_restored_waiting_screens_whole_frame_exact': True,
        'ready_only_1228_changed_pixels_confined_to_Back_Select_footer': footer_changes,
        'four_cards_do_not_prove_simultaneous_ready_footer_or_wireless': True,
        'source_descriptors': {'Back': list(back), 'Back_Select': list(ready)},
        'host_original_ready_branch': [0x020F9E94, 0x020F9EBC],
        'original_source_spans_exact_clean': [{'start': lo, 'end': hi, 'sha256': sha(arm[lo:hi])} for lo, hi in spans],
        'existing_registered_footer_English_measure_draw_gap_adaptation': {
            'four_words_different_from_clean': footer_edits,
            'module': 'dk4tool/patch/help_footer_release_v3.py',
            'module_sha256': sha(Path('dk4tool/patch/help_footer_release_v3.py').read_bytes()),
            'configuration': 'translations/help_footer_release_v3.json',
            'configuration_sha256': sha(Path('translations/help_footer_release_v3.json').read_bytes())},
        'complete_card_name_masks': masks, 'first_final_deletion_controls_rejected': rejected,
        'native_card_proof': {'path': str(native_path), 'sha256': sha(native_path.read_bytes())},
        'all34208_card_pixels_repainted_over_poison_and_all49152_lower_RGB_pixels_exact': True,
        'native_portrait_cache_is_actual_captured_source_not_new_independent_ROM_art_transcript': True,
        'fixture_reports': fixture_reports,
        'first_output_fixture_packet_loss_and_unloaded_portrait_replay_failure_retained': True,
        'six_small_control_parents_and_full_goal_remain_open': True,
        'no_ROM_patch_manifest_registry_or_release_pointer_change': True,
        'no_wireless_completed_race_physical_hardware_or_guide_approval_claim': True,
        'full_goal_complete': False,
        'scripts': {p: sha(Path(p).read_bytes()) for p in ('scripts/run_race_roster_v661.py',
            'scripts/research_race_roster_v661.py', 'scripts/verify_race_roster_v661.py')}}
    save(ROOT / 'proof.json', proof)
    print(f'V661: {len(masks)} complete fields; {rejected} boundary controls; 34208 card pixels; separate ready-only footer; full goal open.')


if __name__ == '__main__':
    main()
