"""Actual compact city specialties and unchanged neighboring widgets."""

import json
import struct
from pathlib import Path

from PIL import Image
from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from scripts.execute_sailing_footer_v317 import execute
from scripts.probe_button_prompt_native import call, machine
from scripts.probe_scene_caption_raster import expected_pixels

ROOT = Path('work/analysis/commodity_layout_v346')


def mask(image, font, text, y):
    expected = {(160 + n * 5 + x, y + yy) for n, c in enumerate(text)
                for yy in range(11) for x in range(6) if font.decode(c).getpixel((x, yy))}
    actual = {(x, yy) for yy in range(y, y + 11) for x in range(160, 256)
              if image.getpixel((x, yy)) == (230, 230, 230)}
    assert actual == expected, (text, len(expected - actual), len(actual - expected))
    return {'text': text, 'origin': [160, y], 'advance': 5, 'exact_ink_pixels': len(expected),
            'first_internal_final_letters_and_blank_cells_exact': True}


def main():
    arm = (ROOT / 'research_arm9.bin').read_bytes()
    manuscript = json.loads(Path('translations/commodity_name_manuscript_v343.json').read_text(encoding='utf-8'))
    u = machine(arm)
    native = []
    for row in manuscript['records']:
        call(u, 0xCD1AC, (row['index'],))
        address = u.reg_read(UC_ARM_REG_R0)
        pointer = struct.unpack('<I', u.mem_read(address, 4))[0]
        assert bytes(u.mem_read(pointer, 64)).split(b'\0', 1)[0].decode('ascii') == row['English']
        if row['change_required']:
            for mode in (4, 16):
                text = row['English']
                r = execute(arm, text, x=108, y=0, tracking=0, mode=mode,
                            buffered_context=True, text_entry_offset=0x15BB40)
                # Original packed renderer clears the shared nibble for odd lengths.
                reference = text
                assert r['pixels'] == expected_pixels(arm, reference, 108, 0, mode, advance=5)
                assert r['context_tracking_after_return'] == 0 and r['final_x'] == 108 + len(text) * 5 <= 203
                native.append({'id': row['index'], 'mode': mode, 'complete_bitmap_exact': True})
    assert len(native) == 98
    font = GameAsciiFont.from_arm9(arm)
    live = []
    for variant, labels in [('normal', ['China', 'Silk Cloth', 'Jade']),
                            ('long', ['Black Glacier Sword', 'North Sea Ambergris', 'Fire and Ice Rubies'])]:
        folder = Path('work/emulation_v193/commodity_' + variant + '_labels_v346_repacked')
        report = json.loads((folder / 'capture_report.json').read_text())
        fixture = ROOT / ('research_only_' + ('normal_names' if variant == 'normal' else 'long_names') + '_Maria.nds')
        assert report['ROM_sha256'] == sha(fixture.read_bytes())
        assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
        current = Image.open(folder / 'frame_016400_final.png').convert('RGB')
        parent = Image.open('work/emulation_v193/commodity_source_repack_v344/frame_016400_final.png').convert('RGB')
        changed = [(x, y) for y in range(384) for x in range(256)
                   if current.getpixel((x, y)) != parent.getpixel((x, y))]
        assert all(160 <= x < 256 and 88 <= y < 164 for x, y in changed)
        matches = [mask(current, font, text, 88 + i * 16) for i, text in enumerate(labels)]
        stable = 0
        for p in folder.glob('frame_*_cold_boot.png'):
            old = Path('work/emulation_v193/commodity_source_repack_v344') / p.name
            if old.exists() and int(p.name.split('_')[1]) < 16400:
                assert Image.open(p).tobytes() == Image.open(old).tobytes(), p
                stable += 1
        live.append({'fixture': str(fixture), 'ROM_sha256': report['ROM_sha256'],
                     'capture_report': str(folder / 'capture_report.json'),
                     'capture_report_sha256': sha((folder / 'capture_report.json').read_bytes()),
                     'labels': matches, 'changed_pixels': len(changed), 'earlier_complete_frames_exact': stable,
                     'all_other_final_pixels_including_market_share_exact': True})
    for p in ['translations/graphics_completion_campaign_v1.json', 'translations/graphics_visual_audit_v150.json']:
        inventory = json.loads(Path(p).read_text())['plaque_style_v247']['ongoing_plaque_inventory']
        assert len(inventory) == 18 and all(not r['fully_completed'] for r in inventory)
    proof = {'all124_native_names_full': True, 'native_compact_rasters': native, 'actual_captures': live,
             'research_Maria_visibility_not_legitimate_unlock': True,
             'long_fixture_supplies_three_labels_not_normal_stock': True,
             'all_other_commodity_UI_parents_pending': True, 'not_registered_or_for_handoff': True,
             'all18_plaques_incomplete': True, 'full_goal_complete': False}
    (ROOT / 'proof.json').write_text(json.dumps(proof, indent=2) + '\n')
    print('124 names,98 compact rasters,6 actual labels and neighboring widgets verified; other commodity parents remain open.')


if __name__ == '__main__':
    main()
