"""Complete label masks and actual-screen preservation for the lazy canvas."""

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
from scripts.verify_commodity_layout_v346 import mask

ROOT = Path('work/analysis/commodity_lazy_canvas_v349')


def main():
    arm = (ROOT / 'research_arm9.bin').read_bytes()
    plan = json.loads((ROOT / 'plan.json').read_text())
    assert sha(arm) == plan['target_arm9_sha256']
    u = machine(arm)
    manuscript = json.loads(Path('translations/commodity_name_manuscript_v343.json').read_text(encoding='utf-8'))
    native = []
    for row in manuscript['records']:
        call(u, 0xCD1AC, (row['index'],))
        address = u.reg_read(UC_ARM_REG_R0)
        ptr = struct.unpack('<I', u.mem_read(address, 4))[0]
        assert bytes(u.mem_read(ptr, 64)).split(b'\0', 1)[0].decode('ascii') == row['English']
        if row['change_required']:
            for mode in (4, 16):
                r = execute(arm, row['English'], x=0, y=72, mode=mode, tracking=0,
                            buffered_context=True, text_entry_offset=0x15BB40)
                assert r['pixels'] == expected_pixels(arm, row['English'], 0, 72, mode, advance=5)
                assert r['context_tracking_after_return'] == 0
                assert r['final_x'] == len(row['English']) * 5 <= 95
                native.append({'id': row['index'], 'mode': mode, 'complete_pixels_exact': True})
    assert len(native) == 98
    font = GameAsciiFont.from_arm9(arm)
    parent = Path('work/emulation_v193/commodity_source_repack_v344')
    old = Image.open(parent / 'frame_016400_final.png').convert('RGB')
    live = []
    for variant, texts in [('normal', ['China', 'Silk Cloth', 'Jade']),
                           ('long', ['Black Glacier Sword', 'North Sea Ambergris', 'Fire and Ice Rubies'])]:
        folder = Path('work/emulation_v193/commodity_lazy_canvas_v349_' + variant)
        report = json.loads((folder / 'capture_report.json').read_text())
        fixture = ROOT / ('research_only_' + variant + '_Maria.nds')
        assert report['ROM_sha256'] == sha(fixture.read_bytes())
        assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
        image = Image.open(folder / 'frame_016400_final.png').convert('RGB')
        changed = [(x, y) for y in range(384) for x in range(256) if image.getpixel((x, y)) != old.getpixel((x, y))]
        assert all(160 <= x < 256 and 88 <= y < 164 for x, y in changed)
        masks = [mask(image, font, text, 88 + i * 16) for i, text in enumerate(texts)]
        stable, column_changes, transition_matches = 0, [], []
        for p in folder.glob('frame_*_cold_boot.png'):
            previous = parent / p.name
            if int(p.name.split('_')[1]) < 16400 and previous.exists():
                current_pixels = Image.open(p).convert('RGB')
                old_pixels = Image.open(previous).convert('RGB')
                if current_pixels.tobytes() == old_pixels.tobytes():
                    stable += 1
                    continue
                frame = int(p.name.split('_')[1])
                delta = [(x, y) for y in range(384) for x in range(256)
                         if current_pixels.getpixel((x, y)) != old_pixels.getpixel((x, y))]
                if all(160 <= x < 256 and 88 <= y < 164 for x, y in delta):
                    column_changes.append({'frame': frame, 'changed_pixels': len(delta)})
                    continue
                assert frame == 11400
                phase = Path('work/emulation_v193/commodity_v349_fade_parent/frame_011402_cold_boot.png')
                assert current_pixels.tobytes() == Image.open(phase).convert('RGB').tobytes()
                transition_matches.append({'target_frame': frame, 'exact_parent_phase_frame': 11402})
        ram = (folder / 'final_arm9_ram.bin').read_bytes()
        header = struct.unpack_from('<5I', ram, 0x2BD774)
        pixels = (0x022BD774 + header[4]) & 0xFFFFFFFF
        assert header[:3] == (4, 57, 132)
        assert (0x022BD774 + header[3]) & 0xFFFFFFFF == 0x02125A20
        assert 0x023A5AA0 <= pixels < pixels + 0x3B00 <= 0x023E0000
        assert any(ram[pixels - 0x02000000 + 8208:pixels - 0x02000000 + 15048])
        live.append({'fixture': str(fixture), 'ROM_sha256': report['ROM_sha256'],
                     'capture_report': str(folder / 'capture_report.json'),
                     'capture_report_sha256': sha((folder / 'capture_report.json').read_bytes()),
                     'labels': masks, 'earlier_frames_exact': stable,
                     'earlier_specialty_column_changes': column_changes,
                     'opening_wipe_phase_matches': transition_matches,
                     'all_other_screen_pixels_exact_including_percentages_and_date': True,
                     'actual_private_pixels_pointer': pixels})
    proof = {'all124_full_native_names': True, 'native_rasters': native, 'actual_captures': live,
             'ordinary_input_Maria_visibility_fixture_not_legitimate_unlock': True,
             'three_long_labels_supplied_not_normal_stock': True,
             'market_cargo_price_contexts_and_registered_integration_pending': True,
             'dense_transition_intermediate_frame11399_review_pending': True,
             'all18_plaques_remain_incomplete': True, 'full_goal_complete': False}
    (ROOT / 'proof.json').write_text(json.dumps(proof, indent=2) + '\n')
    print('124 getters,98 native rasters,6 actual full masks and all other screen pixels pass.')


if __name__ == '__main__':
    main()
