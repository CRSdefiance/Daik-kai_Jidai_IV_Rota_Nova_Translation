"""Compare the changed Refit holds, surroundings, and original menu return."""

from pathlib import Path

from PIL import Image, ImageChops, ImageDraw

from dk4tool.dialogue.font_audit import GameAsciiFont
from scripts import stage_refit_help_wraps_20261115 as stage
from scripts.finish_refit_display_v712 import WHITE


base = stage.base
OUTPUT = stage.ROOT / 'gameplay_verification.json'
INPUTS = Path('work/analysis/refit_actual_v2276/ordinary_refit_inputs.json')
DONOR = Path('work/analysis/refit_editorial_v831/disposable_refit_source.dsv')
REVISED = {13100: 1286, 15500: 1278, 18800: 1278, 19700: 1278}
CROP = (64, 80, 232, 164)


def foreground(image, font, lines):
    left, top, right, bottom = CROP
    expected = {(left + i * 6 + x, top + row * 12 + 1 + y)
                for row, line in enumerate(lines) for i, char in enumerate(line)
                for glyph in (font.decode(char),)
                for x in range(6) for y in range(11) if glyph.getpixel((x, y))}
    seen = {(x, y) for x in range(left, right) for y in range(top, bottom)
            if image.getpixel((x, y)) == WHITE}
    assert expected == seen
    return expected


def main():
    assert not OUTPUT.exists()
    staged = base.load(stage.STORED)
    assert base.digest(stage.ROM) == staged['candidate_sha256']
    assert base.digest(stage.parent.ROM) == staged['previous_sha256']
    paths = [stage.ROOT / folder / 'capture_report.json' for folder in ('replay_parent', 'replay')]
    old, new = reports = tuple(map(base.load, paths))
    assert [row['ROM_sha256'] for row in reports] == [staged['previous_sha256'], staged['candidate_sha256']]
    inputs = base.load(INPUTS)
    for report in reports:
        assert report['frames'] == 20601 and report['scripted_input_schedule'] == inputs
        assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
        assert not any(v for k, v in report.items() if k.startswith('synthetic_'))
        donor = report['battery_save_preloaded']
        assert donor['source_sha256'] == base.digest(DONOR) and donor['copied_byte_exact_before_cold_boot']
    assert all(old[key] == new[key] for key in ('core_DLL_sha256', 'core_options'))
    captures = [{row['frame']: row for row in report['frames_captured']} for report in reports]
    assert captures[0].keys() == captures[1].keys() and len(captures[0]) == 15
    font = GameAsciiFont.from_arm9(base.NdsImage.open(stage.ROM).read_file(stage.ARM))
    rows = {row['message_id']: row for row in base.load(stage.REVIEW)['records']}
    identical, revised = [], []
    evidence = {str(path): base.digest(path) for path in (*paths, INPUTS, DONOR, Path(__file__))}
    sheet = Image.new('RGB', (1024, 432), '#242a31')
    draw = ImageDraw.Draw(sheet)
    for frame in sorted(captures[0]):
        images = []
        for by_frame in captures:
            entry = by_frame[frame]
            path = entry['path']
            assert base.digest(path) == entry['PNG_sha256']
            evidence[path] = entry['PNG_sha256']
            with Image.open(path) as opened:
                images.append(opened.convert('RGB'))
        assert all(image.size == (256, 384) for image in images)
        diff = ImageChops.difference(*images).getbbox()
        if frame not in REVISED:
            assert diff is None
            identical.append(frame)
            continue
        n = REVISED[frame]
        row = rows[n]
        old_mask = foreground(images[0], font, [line.rstrip() for line in row['previous_English'].splitlines()])
        new_mask = foreground(images[1], font, row['generated_lines'])
        columns = (range(diff[0], diff[2]), range(diff[1], diff[3]))
        changed = {(x, y) for x in columns[0] for y in columns[1]
                   if images[0].getpixel((x, y)) != images[1].getpixel((x, y))}
        assert changed == old_mask ^ new_mask
        revised.append(dict(frame=frame, message_id=n, bounds=diff, full_glyph_pixels=len(new_mask)))
        if frame in (13100, 15500):
            y = 216 * (frame == 15500)
            for column, label in enumerate(('Previous', 'Revised')):
                draw.text((column * 512 + 10, y + 7), f'{label} / COMMON {n}', fill='white')
                cropped = images[column].crop((0, 77, 256, 173)).resize((512, 192), Image.Resampling.NEAREST)
                sheet.paste(cropped, (column * 512, y + 24))
    assert len(identical) == 11 and len(revised) == 4
    sheet_path = stage.ROOT / 'refit_before_after.png'
    sheet.save(sheet_path)
    base.save(OUTPUT, dict(candidate_sha256=staged['candidate_sha256'], revised_holds=revised,
        exact_transition_and_control_frames=identical, screenshot=str(sheet_path),
        screenshot_sha256=base.digest(sheet_path), evidence=evidence, hardware=False,
        scope='Ordinary Refit input with the existing copied Copenhagen five-ship test battery.'))
    print('Verified four changed holds and eleven pixel-identical surrounding two-screen frames.')


if __name__ == '__main__':
    main()
