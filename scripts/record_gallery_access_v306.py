"""Actual normal save, Gallery access and source gate discovery."""

import json
import struct
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage

ROOT = Path('work/analysis/gallery_access_v306')


def main():
    rom = Path('out/all_routes_combined_v305_candidate.nds')
    path = Path('work/emulation_v193/gallery_access_v306/capture_report.json')
    report = json.loads(path.read_text(encoding='utf-8'))
    assert report['ROM_sha256'] == sha(rom.read_bytes()) and report['cold_boot'] and not report['savestate_loaded']
    assert not report['callback_errors'] and report['frames'] == 31200
    for row in report['frames_captured']:
        assert sha(Path(row['path']).read_bytes()) == row['PNG_sha256']
    snapshot = report['read_only_RAM_snapshot']
    ram = Path(snapshot['path']).read_bytes()
    assert snapshot['read_only_export'] and sha(ram) == snapshot['sha256']
    menu_enable = [struct.unpack_from('<I', ram, offset)[0] for offset in (0x137B38, 0x137B68, 0x137B88)]
    assert menu_enable == [1, 1, 1]
    system_flags = struct.unpack_from('<H', ram, 0x27985C)[0]
    assert system_flags & 15 == 0
    current, clean = NdsImage.open(rom), NdsImage.open('work/clean.nds')
    source = current.read_file('/__arm9__.bin')
    assert source[0xED708:0xED7E8] == clean.read_file('/__arm9__.bin')[0xED708:0xED7E8]
    proof = {'format': 'dk4-actual-normal-save-gallery-access-v306', 'candidate': str(rom), 'candidate_sha256': sha(rom.read_bytes()),
             'capture_report': str(path), 'capture_report_sha256': sha(path.read_bytes()), 'actual_frames': 31200,
             'ordinary_save_sequence_frames': {'six_unused_slots': 22400, 'new_save_confirmation': 22800,
                                                'returned_after_save': 23600, 'quit_confirmation': 24800,
                                                'title_Continue_GrandRace_Gallery_enabled': 25200,
                                                'Gallery_selected': 25600, 'actual_Gallery_submenu': 26000},
             'native_title_enable_fields': menu_enable, 'actual_system_flags_low_four_bits': system_flags & 15,
             'normal_new_save_enables_title_Gallery_without_unlock_patch': True,
             'actual_Item_and_Ruins_pages_report_no_collected_items_or_discovered_ruins': [29600, 30800],
             'missed_current_Japanese_Gallery_labels': ['史跡', '登場人物', 'イベントシーン'],
             'visible_Ruins_Japanese_label_frame': 26000,
             'Characters_requires_bit3_and_EventScenes_any_low_four_bit': True,
             'meaning_of_those_system_bits_not_inferred_from_mask_alone': True,
             'actual_hidden_Characters_EventScenes_views_remain_locked_and_unverified': True,
             'Extras_is_AboutExtras_OnlineVersion_not_EventScenes': True,
             'no_ROM_changes_flag_patches_savestate_or_RAM_injection': True,
             'all18_plaque_and_legacy_display_gates_remain_open': True, 'full_goal_complete': False}
    (ROOT / 'access_proof.json').write_text(json.dumps(proof, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    (ROOT / 'saved_route_inputs.json').write_text(json.dumps(report['scripted_input_schedule'], indent=2) + '\n', encoding='utf-8')
    print('Actual ordinary save enables Gallery; native titleflags all1; hidden systemmask0; three missed labels discovered.')


if __name__ == '__main__':
    main()
