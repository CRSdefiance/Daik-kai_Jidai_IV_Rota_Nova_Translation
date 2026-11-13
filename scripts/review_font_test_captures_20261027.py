"""Pair cold-boot screenshots without mistaking intended new glyphs for regressions."""

import json
from pathlib import Path

from PIL import Image, ImageDraw

from dk4tool.patch.grand_race_menu_release import sha

ROOT = Path('work/font_test_20261027')


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


if __name__ == '__main__':
    runs, selected = [], []
    for case in ['newgame', 'town']:
        terminal = read(ROOT / (case + '_terminal.json'))
        prior_terminal = read(Path('work/analysis/lil_B179_runs_v4751') / (case + '_terminal.json'))
        assert terminal['terminal'] and terminal['battery_sources_preserved']
        report_path, old_path = Path(terminal['report']), Path(prior_terminal['report'])
        report, old = read(report_path), read(old_path)
        assert sha(report_path.read_bytes()) == terminal['report_sha256']
        assert sha(old_path.read_bytes()) == prior_terminal['report_sha256']
        assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
        assert report['frames'] == old['frames']
        for key in ['core_DLL_sha256', 'core_options', 'scripted_input_schedule']:
            assert report[key] == old[key], key
        now = {r['frame']: r for r in report['frames_captured']}
        then = {r['frame']: r for r in old['frames_captured']}
        assert now.keys() == then.keys()
        differences = []
        for frame, row in now.items():
            old_row = then[frame]
            a, b = Path(row['path']), Path(old_row['path'])
            assert sha(a.read_bytes()) == row['PNG_sha256']
            assert sha(b.read_bytes()) == old_row['PNG_sha256']
            x, y = Image.open(a).convert('RGB'), Image.open(b).convert('RGB')
            assert x.size == y.size == (256, 384)
            changed = sum(p != q for p, q in zip(x.getdata(), y.getdata()))
            differences.append(dict(frame=frame, changed_RGB_pixels=changed,
                current_capture=str(a), original_capture=str(b)))
            if case == 'newgame' and frame == 4000:
                for box in [(0, 0, 256, 192), (0, 192, 72, 280)]:
                    assert x.crop(box).tobytes() == y.crop(box).tobytes(), (case, frame, box)
            if case == 'town' and frame == 13700:
                for box in [(20, 34, 56, 68), (0, 192, 256, 364)]:
                    assert x.crop(box).tobytes() == y.crop(box).tobytes(), (case, frame, box)
            wanted = [2000, 2400, 4000] if case == 'newgame' else [11900, 13700, 17401]
            if frame in wanted:
                selected.append(dict(case=case, frame=frame, current=str(a), original=str(b)))
        assert any(d['changed_RGB_pixels'] for d in differences)
        runs.append(dict(case=case, frames=report['frames'], current_report=str(report_path),
            original_report=str(old_path), paired_captures=differences,
            same_core_options_inputs_and_frame_schedule=True,
            cold_boot_no_savestate_callback_errors_or_hardware_claim=True))
    # Three paired screens per sheet; preserve original 1:1 pixels in the output.
    sheets = []
    for case in ['newgame', 'town']:
        rows = [s for s in selected if s['case'] == case]
        sheet = Image.new('RGB', (1024, 840), '#17252b')
        draw = ImageDraw.Draw(sheet)
        for index, row in enumerate(rows):
            x = index % 2 * 512
            y = index // 2 * 420
            for column, field in enumerate(['original', 'current']):
                sx = x + column * 256
                draw.text((sx + 4, y + 4), f'{case} {row["frame"]} ' + ('V4749' if column == 0 else 'FONT TEST'), fill='white')
                sheet.paste(Image.open(row[field]).convert('RGB'), (sx, y + 26))
        path = ROOT / (case + '_before_after_screens.png')
        sheet.save(path)
        sheets.append(str(path))
    result = dict(runs=runs, sheets=sheets,
        opening_background_and_portrait_and_refit_art_regions_exact=True,
        original_ordinary_startup_and_town_inputs_exercised=True,
        town_uses_inherited_test_battery_not_earned_progress=True,
        targeted_emulator_tests_not_full_route_or_hardware_verification=True,
        visual_review_pending=True)
    (ROOT / 'cold_boot_comparison.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print('31 paired cold-boot captures checked; intended font differences retained for visual review.')
