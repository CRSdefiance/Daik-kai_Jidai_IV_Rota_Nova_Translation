"""Verify ordinary long equipment confirmation against full native glyph cells."""

import json
from pathlib import Path

from PIL import Image

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.execute_modal_v362 import execute

ROOT = Path('work/analysis/equipment_release_v364')
CAPTURE = Path('work/emulation_v193/equipment_long_v364')


def verify_letters(image, events, font, origin):
    matched = []
    for event in events:
        glyph = font.decode(chr(event['code']))
        for y in range(11):
            for x in range(6):
                point = (origin[0] + event['x'] + x, origin[1] + event['y'] + y)
                actual = max(image.getpixel(point)[:3]) < 70
                assert actual == bool(glyph.getpixel((x, y))), (point, event)
                if actual:
                    matched.append(point)
    return len(set(matched))


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    report = json.loads((CAPTURE / 'capture_report.json').read_text(encoding='utf-8'))
    assert report['cold_boot'] and not report['savestate_loaded']
    assert report['battery_save_preloaded']['source_sha256'] == '3b538b99ebef7f230424c0172c69889c9a6cf8b5fdb442d4a1ae5a13e631bf0b'
    image = NdsImage.open(report['ROM'])
    assert sha(Path(report['ROM']).read_bytes()) == report['ROM_sha256']
    arm, kanji = image.read_file('/__arm9__.bin'), image.read_file('/GRP/KANJI.FNT')
    geometry = json.loads(Path('work/analysis/equipment_confirmation_v362/actual_geometry.json').read_text())
    text = '  Rafael Castor equipped Travels of\n  Marco Polo.'
    native = execute(arm, text, modal=True, mode=4, kanji_font=kanji,
                     modal_guarded=True, confirmation_contract=geometry)
    screenshot = CAPTURE / 'frame_010800_final.png'
    captured = Image.open(screenshot).convert('RGB')
    # The native text surface is inset into the original bottom-screen paper.
    count = verify_letters(captured, native['glyph_events'], GameAsciiFont.from_arm9(arm), (14, 298))
    short_before = Path('work/emulation_v193/equipment_saved_v362')
    short_after = Path('work/emulation_v193/equipment_wrap_v363')
    old = {r['frame']: r for r in json.loads((short_before / 'capture_report.json').read_text())['frames_captured']}
    new = {r['frame']: r for r in json.loads((short_after / 'capture_report.json').read_text())['frames_captured']}
    assert old.keys() == new.keys()
    assert all(Image.open(old[f]['path']).tobytes() == Image.open(new[f]['path']).tobytes() for f in new)
    proof = {'ordinary_long_item_confirmation_verified': True,
             'actual_full_confirmation': 'Rafael Castor equipped Travels of Marco Polo.',
             'layout': text, 'complete_native_glyph_ink_pixels': count,
             'all_glyph_cells_including_blank_cells_exact': True,
             'short_confirmation_replay_full_frames_unchanged': len(new),
             'report': str(CAPTURE / 'capture_report.json'),
             'report_sha256': sha((CAPTURE / 'capture_report.json').read_bytes()),
             'screenshot': str(screenshot), 'screenshot_sha256': sha(screenshot.read_bytes()),
             'ROM_sha256': report['ROM_sha256'],
             'normal_purchase_and_equip_no_memory_or_unlock_fixture': True,
             'all18_plaques_incomplete': True, 'full_goal_complete': False}
    (ROOT / 'research_live_proof.json').write_text(json.dumps(proof, indent=2) + '\n')
    inputs = report['scripted_input_schedule']
    (ROOT / 'long_inputs.json').write_text(json.dumps(inputs, indent=2) + '\n')
    print(f'Actual complete Marco Polo confirmation: {count} ink pixels and blank cells exact; {len(new)} short replay frames unchanged.')


if __name__ == '__main__':
    main()
