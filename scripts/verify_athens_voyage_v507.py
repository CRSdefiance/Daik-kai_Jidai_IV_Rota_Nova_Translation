"""Verify normal Athens arrival and pin a shared portrait-dialogue defect."""

import json
from pathlib import Path

from PIL import Image

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.verify_commodity_layout_v346 import mask
from scripts.verify_confirmed_name_widget_pixels_v198 import complete_mask

OUT = Path('work/analysis/environment_voyage_v507')
CAPTURE = Path('work/emulation_v193/environment_voyage_v507')
ROM = Path('out/all_routes_combined_v502_candidate.nds')


def main():
    report_path = CAPTURE / 'capture_report.json'
    report = json.loads(report_path.read_text(encoding='utf-8'))
    assert report['ROM_sha256'] == sha(ROM.read_bytes())
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    assert not report.get('synthetic_inventory_fixtures')
    donor = report['battery_save_preloaded']
    assert sha(Path(donor['source']).read_bytes()) == donor['source_sha256']
    for row in report['frames_captured']:
        assert sha(Path(row['path']).read_bytes()) == row['PNG_sha256']
    rom = NdsImage.open(ROM)
    arm = rom.read_file('/__arm9__.bin')
    font = GameAsciiFont.from_arm9(arm)
    image = Image.open(CAPTURE / 'frame_020600_navigation.png').convert('RGB')
    labels = [mask(image, font, word, 88+i*16)
              for i, word in enumerate(('Olive Oil', 'Sultana', 'Artwork', 'Statues'))]
    entries = common_message_entries(rom.read_file('/COMMON/MESFILE.DK4'), arm, clean=False)
    clean = NdsImage.open('work/clean.nds')
    source = common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'), clean.read_file('/__arm9__.bin'), clean=True)[827]
    assert entries[827].text == b'Right...%s, right? A toast to our new friendship!'
    raw = (CAPTURE / 'frame_023300_arm9_ram.bin').read_bytes()
    expanded = b'Right...Hodram, right? A toast to our new friendship!'
    assert expanded+b'\0' in raw
    toast = Image.open(CAPTURE / 'frame_023300_navigation.png').convert('RGB')
    # Find the exact original painter's two visible row strings, without
    # inferring a word boundary from the screenshot thumbnail.
    matches = []
    for split in range(1,len(expanded)):
        for first_x in (16,22):
            for dropped in (0,1):
                try:
                    a = complete_mask(font, expanded[:split].decode(), toast, first_x, 296, (0,8,0))
                    b = complete_mask(font, expanded[split+dropped:].decode(), toast, 22, 312, (0,8,0))
                except (AssertionError, IndexError, ValueError):
                    continue
                matches.append({'first_row': expanded[:split].decode(), 'second_row': expanded[split+dropped:].decode(),
                                'first_x': first_x, 'second_x': 22, 'ink_pixels': a[0]+b[0],
                                'split_byte': split, 'dropped_character': expanded[split:split+dropped].decode(),
                                'word_split': chr(expanded[split-1]).isalnum() and chr(expanded[split]).isalnum()})
    assert len(matches) == 1 and matches[0]['word_split'] and matches[0]['dropped_character'] == 'r'
    saved = CAPTURE / 'saves/all_routes_combined_v502_candidate.dsv'
    proof = {
        'candidate_sha256': report['ROM_sha256'], 'capture_report': str(report_path),
        'capture_report_sha256': sha(report_path.read_bytes()), 'frames': report['frames'],
        'cold_boot_without_savestate_or_state_injection': True,
        'original_donor_unchanged': True, 'Athens_arrived_through_normal_steering': True,
        'complete_four_specialty_masks': labels,
        'normal_resupply_then_saved_slot6': True,
        'saved_battery': str(saved), 'saved_battery_sha256': sha(saved.read_bytes()),
        'rest_at_inn_not_completed': True,
        'new_layout_defect': {'native_message_id': 827, 'clean_Japanese': source.text.decode('cp932'),
                              'expanded_ASCII': expanded.decode(), 'observed_rows': matches,
                              'existing_word_wrap_scope_misses_this_message': True,
                              'fix_not_yet_integrated': True},
        'production_ROM_unchanged': True, 'full_goal_complete': False,
    }
    (OUT / 'voyage_proof.json').write_text(json.dumps(proof, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({'stock_labels': labels, 'confirmed_toast_rows': matches},indent=2))


if __name__ == '__main__':
    main()
