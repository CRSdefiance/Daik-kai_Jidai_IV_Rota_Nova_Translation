"""Bind the ordinary failed/repaired cold boots and read-only user state evidence."""

import json
import struct
from pathlib import Path

from ndspy.code import MainCodeFile
from PIL import Image

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage

ROOT = Path('work/lisbon_square_freeze_20261027')
ROM = Path('out/font_v2_square_scratch_fix_20261027_test.nds')


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def main():
    report_path = ROOT / 'repaired_cold_boot/capture_report.json'
    report = read(report_path)
    old = read(ROOT / 'repro_extended/capture_report.json')
    assert report['ROM_sha256'] == sha(ROM.read_bytes()) == '89860905d61e348ae053d40836159bc86bff5d85d3206ce3a0961a6d60142077'
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    assert report['frames'] == 33100 and not report.get('battery_save_preloaded')
    assert not any(value for key, value in report.items() if key.startswith('synthetic_'))
    assert report['scripted_input_schedule'][:len(old['scripted_input_schedule'])] == old['scripted_input_schedule']
    frames = {row['frame']: Path(row['path']) for row in report['frames_captured']}
    for row in report['frames_captured']:
        assert sha(Path(row['path']).read_bytes()) == row['PNG_sha256']
    pairs = []
    for frame in (2600, 15000, 19600, 27600, 28800, 29200):
        directory = 'repro' if frame in (2600, 15000, 19600) else 'repro_extended'
        before = ROOT / directory / f'frame_{frame:06d}_navigation.png'
        assert Image.open(before).convert('RGB').tobytes() == Image.open(frames[frame]).convert('RGB').tobytes(), frame
        pairs.append(frame)

    arm = NdsImage.open(ROM).read_file('/__arm9__.bin')
    section = bytes(MainCodeFile(arm, 0x02000000).sections[4].data)
    snapshots = []
    cached_pointers = set()
    directory = ROOT / 'repaired_cold_boot'
    for state in sorted(directory.glob('*native_state_*')):
        native = read(state / 'native_state.json')
        assert native['state_loaded'] is False and native['read_only_export']
        itcm = (state / 'arm9_itcm.bin').read_bytes()
        helper = bytearray(itcm[0x4200:0x4300])
        pointer = struct.unpack_from('<I', helper, 0xD8)[0]
        assert 0x02000000 <= pointer < 0x02400000
        cached_pointers.add(pointer)
        # C2D8 is the original footer helper's owned mutable heap-cache word.
        # All instructions, literals, and unused bytes must otherwise be exact.
        helper[0xD8:0xDC] = section[0x2D8:0x2DC]
        assert bytes(helper) == section[0x200:0x300], state
        assert itcm[0x4388:0x4504] == section[0x388:0x504], state
        snapshots.append(dict(path=str(state), font_code_and_Square_code_exact=True,
            sole_font_helper_mutable_word='01FFC2D8', footer_heap_cache=pointer))
    assert len(snapshots) >= 8 and len(cached_pointers) == 1
    frozen = read(ROOT / 'frozen_state_diagnosis.json')
    assert sha(Path(frozen['state_path']).read_bytes()) == frozen['state_sha256']
    assert bytes.fromhex(frozen['font_helper_actual']) == bytes(256)
    assert frozen['font_helper_changed_bytes'] == 138
    proof = dict(candidate=str(ROM), candidate_sha256=sha(ROM.read_bytes()),
        report=str(report_path), report_sha256=sha(report_path.read_bytes()),
        ordinary_cold_boot_frames=33100, no_savestate_or_gameplay_fixtures=True,
        whole_frame_controls_exact=pairs, original_inputs_replayed_through_failure=True,
        native_code_snapshots=snapshots, same_owned_footer_heap_cache_after_Square=True,
        visually_reviewed_Square_dialogue_shop_labels_menus_and_two_returns_to_town=True,
        viewed_frames=[29600, 30000, 30800, 31900, 33100],
        user_frozen_state_preserved=True, exact_user60_percent_event_state_not_replayed=True,
        hardware_or_full_route_verification=False)
    (ROOT / 'actual_runtime_proof.json').write_text(json.dumps(proof, indent=2) + '\n', encoding='utf-8')
    print('33100 ordinary cold-boot frames; six whole-frame controls; two Square returns; font code survives all native snapshots.')


if __name__ == '__main__':
    main()
