"""Verify matched steering evidence and a complete current-ROM Info Mode panel."""

import json
from pathlib import Path

from PIL import Image

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.sailing_panel_graphics import encode_panels
from dk4tool.rom.nds import NdsImage
from scripts.record_navigation_v327 import dark_text

ROOT = Path('work/analysis/navigation_touch_v386')
ROM = Path('out/all_routes_combined_v383_candidate.nds')


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def captures(name, digest):
    path = Path('work/emulation_v193') / name / 'capture_report.json'
    report = read(path)
    assert report['ROM_sha256'] == digest and report['frames'] == 8800
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    source = Path(report['battery_save_preloaded']['source'])
    assert sha(source.read_bytes()) == report['battery_save_preloaded']['source_sha256']
    for row in report['frames_captured']:
        assert sha(Path(row['path']).read_bytes()) == row['PNG_sha256']
    return path, report, {r['frame']: r for r in report['frames_captured']}


def main():
    digest = sha(ROM.read_bytes())
    assert read(ROM.with_suffix('.manifest.json'))['candidate_sha256'] == digest
    touch_path, touch, a = captures('navigation_touch_v386', digest)
    control_path, control, b = captures('navigation_no_steering_v386', digest)
    assert touch['battery_save_preloaded']['source_sha256'] == control['battery_save_preloaded']['source_sha256']
    expected = [e for e in touch['scripted_input_schedule'] if e['start'] <= 5601 or 'touch' not in e]
    assert control['scripted_input_schedule'] == expected
    exact, changed = [], []
    for frame, row in b.items():
        before = Image.open(row['path']).convert('RGB')
        after = Image.open(a[frame]['path']).convert('RGB')
        assert before.size == after.size == (256, 384)
        if before.tobytes() == after.tobytes():
            exact.append(frame)
        else:
            assert frame > 6000
            changed.append(frame)
    assert 6000 in exact and all(f in changed for f in (6400, 6800, 7200))
    assert Image.open(a[6800]['path']).crop((0, 192, 40, 222)).tobytes() != (
        Image.open(b[6800]['path']).crop((0, 192, 40, 222)).tobytes())
    arm = NdsImage.open(ROM).read_file('/__arm9__.bin')
    font = GameAsciiFont.from_arm9(arm)
    panel = encode_panels(arm, read('translations/sailing_mode_panels_manuscript_v1.json'))[0]
    shot = Image.open(b[8800]['path']).convert('RGB')
    expected_ink = set()
    for glyph in panel['glyphs']:
        mask = font.decode(glyph['character'])
        x0, y0 = glyph['origin']
        for y in range(11):
            for x in range(6):
                if mask.getpixel((x, y)):
                    expected_ink.add((x0 + x, y0 + y))
    observed_ink = {(x, y) for y in range(176) for x in range(256)
                    if tuple(c >> 3 for c in shot.getpixel((x, y))) == (31, 31, 31)}
    assert expected_ink == observed_ink
    assert all(tuple(c >> 3 for c in shot.getpixel((x, y))) ==
               ((31, 31, 31) if (x, y) in expected_ink else (0, 0, 0))
               for y in range(176) for x in range(256))
    tooltip = [dark_text(font, text, shot, region) for text, region in [
        ('Bergstrom Fleet', (105, 237, 230, 260)),
        ('Brigantine class', (105, 251, 240, 277)),
    ]]
    proof = {'candidate': str(ROM), 'candidate_sha256': digest,
             'capture_reports': {str(p): sha(p.read_bytes()) for p in (touch_path, control_path)},
             'identical_whole_frames_before_steering': exact,
             'changed_whole_frames_after_steering': changed,
             'touch_changed_movement_against_no_steering_control': True,
             'observed_coordinates_visually_read_not_native_position_getter': {
                 'initial6000': [57, 16], 'touch6800': [57, 24], 'control6800': [57, 19],
                 'touch8800': [58, 23]},
             'absolute_touch_compass_heading_mapping_not_proven': True,
             'complete_Info_Mode_panel': {'heading': panel['heading'], 'lines': panel['lines'],
                                          'ink_pixels': len(expected_ink), 'all_45056_ink_and_blank_pixels_exact': True},
             'complete_actual_ship_tooltip_masks': tooltip,
             'port_arrival': False, 'treasure_or_weapon_armor_acquisition': False,
             'all18_plaques_incomplete': True, 'ROM_changed': False, 'full_goal_complete': False}
    (ROOT / 'display_control_proof.json').write_text(json.dumps(proof, indent=2) + '\n', encoding='utf-8')
    print(f'Matched steering changes movement; complete Info Mode ({len(expected_ink)} ink pixels) and both tooltip lines pass.')


if __name__ == '__main__':
    main()
