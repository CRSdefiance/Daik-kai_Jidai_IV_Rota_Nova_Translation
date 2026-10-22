"""Exact complete actual fleet and compact roster popup glyph masks."""

import json
from collections import Counter
from pathlib import Path

from PIL import Image

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_plaque_release_v247 import find_mask

ROOT = Path('work/analysis/fleet_detail_v374')


def compact(font, text, shot, region):
    pixels = {}
    for index, char in enumerate(text):
        glyph = font.decode(char)
        for y in range(11):
            for x in range(6):
                pixels[index * 5 + x, y] = bool(glyph.getpixel((x, y)))
    width = len(text) * 5 + 1
    colors = [c for c, _ in Counter(shot.crop(region).get_flattened_data()).most_common() if min(c) > 180][:4]
    for color in colors:
        for y in range(region[1], region[3] - 10):
            for x in range(region[0], region[2] - width + 1):
                if all((shot.getpixel((x + dx, y + dy)) == color) == ink for (dx, dy), ink in pixels.items()):
                    return {'text': text, 'bounds': [x, y, x + width, y + 11], 'ink_pixels': sum(pixels.values()),
                            'complete_original_glyphs_and_blank_cells_exact': True}
    raise ValueError('No complete compact mask: ' + text)


def main():
    rom_path = ROOT / 'research_only_fleet_detail.nds'
    rom = NdsImage.open(rom_path)
    digest = sha(rom_path.read_bytes())
    font = GameAsciiFont.from_arm9(rom.read_file('/__arm9__.bin'))
    fleet_root = Path('work/emulation_v193/fleet_detail_v374')
    sort_root = Path('work/emulation_v193/fleet_sort_v374')
    for root in (fleet_root, sort_root):
        report = json.loads((root / 'capture_report.json').read_text())
        assert report['ROM_sha256'] == digest and report['cold_boot'] and not report['savestate_loaded']
        assert not report['callback_errors']
        source = report['battery_save_preloaded']['source']
        assert sha(Path(source).read_bytes()) == report['battery_save_preloaded']['source_sha256']
    shot = Image.open(fleet_root / 'frame_017200_final.png').convert('RGB')
    fleet = []
    for text, region in [('Bergstrom Fleet', (0, 0, 256, 16)),
                         ('Leader (Soldier)', (76, 20, 256, 42)),
                         ('Hodram Joakim Bergstrom', (76, 36, 256, 59)),
                         ('Hodram Joakim Bergstrom', (76, 228, 256, 251)),
                         ('Level   19', (76, 78, 256, 103)),
                         ('Level   19', (76, 270, 256, 295))]:
        fleet.append(find_mask(font, text, shot, region))
    popup = Image.open(sort_root / 'frame_012400_final.png').convert('RGB')
    labels = ['Role', 'Level', 'Vigor', 'Command', 'Sailing', 'Survey',
              'Finance', 'Swords', 'Aim', 'Speech', 'Guile', 'Observe']
    sort = [compact(font, text, popup, (40, 258, 220, 320)) for text in labels]
    assert len({tuple(row['bounds'][:2]) for row in sort}) == 12
    before = Image.open('work/emulation_v193/equipment_search_v367/frame_017200_final.png').convert('RGB')
    changed = [(x, y) for y in range(384) for x in range(256) if before.getpixel((x, y)) != shot.getpixel((x, y))]
    assert all(76 <= x < 256 and (20 <= y < 103 or 212 <= y < 295) for x, y in changed)
    proof = {'ROM_sha256': digest, 'actual_fleet_masks': fleet, 'actual_sort_masks': sort,
             'faction_name_complete_in_original_title_bar': True,
             'approved_middle_Joakim_complete_in_both_actual_fleet_views': True,
             'all12_source_original_sort_glyphs_complete_in_original_popup': True,
             'actual_fleet_changed_pixels': len(changed), 'all_other_fleet_frame_pixels_unchanged': True,
             'actual_sorted_roles_conditions_and_names_broader_contexts_remain_open': True,
             'weapon_armor_acquired': False, 'older_donor_history_unknown': True,
             'all18_plaques_incomplete': True, 'full_goal_complete': False}
    (ROOT / 'live_proof.json').write_text(json.dumps(proof, indent=2) + '\n')
    print('Six complete fleet masks and all12 full sort labels verified in actual cold-boot gameplay.')


if __name__ == '__main__':
    main()
