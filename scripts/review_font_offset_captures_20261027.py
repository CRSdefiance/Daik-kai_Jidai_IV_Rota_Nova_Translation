"""Check actual button masks and compare the repaired baseline with the high-font test."""

import json
from pathlib import Path

from PIL import Image, ImageDraw

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_plaque_release_v247 import find_mask

ROOT = Path('work/font_offset_test_20261027_v2')
PRIOR = Path('work/font_test_20261027')
ROM = Path('out/font_v2_draw_down_two_v2_20261027_test.nds')


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def pictures(report):
    rows = {r['frame']: r for r in report['frames_captured']}
    for r in rows.values():
        assert sha(Path(r['path']).read_bytes()) == r['PNG_sha256']
    return rows


if __name__ == '__main__':
    digest = sha(ROM.read_bytes())
    font = GameAsciiFont.from_arm9(NdsImage.open(ROM).read_file('/__arm9__.bin'))
    runs, masks, selected = [], [], []
    for case in ['newgame', 'town']:
        terminal, old_terminal = read(ROOT / (case + '_terminal.json')), read(PRIOR / (case + '_terminal.json'))
        assert terminal['terminal'] and terminal['candidate_sha256'] == digest
        report, old = read(terminal['report']), read(old_terminal['report'])
        assert sha(Path(terminal['report']).read_bytes()) == terminal['report_sha256']
        assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
        for key in ['frames', 'core_DLL_sha256', 'core_options', 'scripted_input_schedule']:
            assert report[key] == old[key]
        now, then = pictures(report), pictures(old)
        if case == 'newgame':
            a = Image.open(now[4000]['path']).convert('RGB')
            b = Image.open(then[4000]['path']).convert('RGB')
            for box in [(0, 0, 256, 192), (0, 192, 72, 272)]:
                assert a.crop(box).tobytes() == b.crop(box).tobytes()
        checks = [(1600, ['Back', 'Select'])] if case == 'newgame' else [(11900, ['Back', 'Select']), (13700, ['Finish', 'Undo', 'Back', 'Edit'])]
        for frame, labels in checks:
            image, original = Image.open(now[frame]['path']).convert('RGB'), Image.open(then[frame]['path']).convert('RGB')
            for label in labels:
                current = find_mask(font, label, image, (0, 366, 256, 384))
                previous = find_mask(font, label, original, (0, 366, 256, 384))
                assert current['bounds'][0] == previous['bounds'][0]
                assert current['bounds'][1] == previous['bounds'][1] + 2
                masks.append(dict(case=case, frame=frame, current=current, previous=previous,
                    exactly_two_pixels_lower=True, complete_ink_and_blank_pixels=True))
        wanted = [1100, 2000, 4000] if case == 'newgame' else [11900, 13700, 17401]
        for frame in wanted:
            selected.append(dict(case=case, frame=frame, current=now[frame]['path'],
                previous=then[frame]['path'] if frame in then else None))
        runs.append(dict(case=case, frames=report['frames'], report=terminal['report'],
            report_sha256=terminal['report_sha256'], callback_errors=[], cold_boot=True,
            town_uses_inherited_test_battery=case == 'town'))
    # Explicitly reject a white/black startup even when the emulator produced
    # valid callbacks and a complete report, as happened in the revoked probe.
    for row in selected:
        assert len(Image.open(row['current']).convert('RGB').getcolors(256 * 384) or []) > 20
    sheets = []
    for case in ['newgame', 'town']:
        rows = [r for r in selected if r['case'] == case]
        sheet = Image.new('RGB', (768, 414), '#17252b')
        draw = ImageDraw.Draw(sheet)
        for i, r in enumerate(rows):
            draw.text((i * 256 + 4, 6), f'{case} frame{r["frame"]}', fill='white')
            sheet.paste(Image.open(r['current']).convert('RGB'), (i * 256, 26))
        path = ROOT / (case + '_review.png')
        sheet.save(path)
        sheets.append(str(path))
    before = Image.open(next(r['previous'] for r in selected if r['case'] == 'town' and r['frame'] == 13700)).convert('RGB')
    after = Image.open(next(r['current'] for r in selected if r['case'] == 'town' and r['frame'] == 13700)).convert('RGB')
    crop = Image.new('RGB', (768, 160), '#17252b')
    draw = ImageDraw.Draw(crop)
    for i, (image, label) in enumerate([(before, 'Previous font test'), (after, 'Drawing lowered 2 pixels')]):
        draw.text((8, i * 80 + 4), label, fill='white')
        crop.paste(image.crop((0, 366, 256, 384)).resize((768, 54), Image.Resampling.NEAREST), (0, i * 80 + 22))
    crop.save(ROOT / 'button_before_after.png')
    result = dict(candidate_sha256=digest, runs=runs, actual_complete_button_masks=masks,
        paired_button_mask_count=len(masks), all_tested_buttons_exactly_two_pixels_lower=True,
        reviewed_sheets=sheets, visual_review_pending=True,
        original_opening_background_and_portrait_preserved=True,
        targeted_emulator_checks_not_full_route_or_hardware_verification=True)
    (ROOT / 'capture_verification.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print('Actual startup/town button masks complete and exactly2pixels lower:', len(masks))
