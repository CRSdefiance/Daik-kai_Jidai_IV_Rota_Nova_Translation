"""Compare every stat plaque with the native font and the clean selection state."""

from pathlib import Path
from struct import unpack_from

from PIL import Image, ImageChops, ImageDraw

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.graphics.pxl import PxlImage
from scripts import stage_sailor_stat_labels_20261114 as stage
from scripts.verify_portrait_native_pixels_v202 import native5


base = stage.base
BEFORE = Path('out/deck_stat_highlights_20261114_v2')
WORK = Path('work/sailor_stat_labels_20261114_v1')
OUTPUT = WORK / 'live_verification.json'
FRAMES = (6200, 6599, 6999, 7399, 7799, 8199, 8599, 8999, 9399, 9799, 10199, 10599)
SKILLS = ('All', 'Command', 'Sailing', 'Survey', 'Finance', 'Observe', 'Vigor',
          'Aim', 'Swords', 'Speech', 'Guile', 'Restored')
SKILL_IDS = (1, 2, 3, 4, 9, 0, 6, 5, 7, 8)
INK = (230, 230, 230)


def capture(folder, sha):
    report = folder / 'capture/capture_report.json'
    data = base.load(report)
    assert data['ROM_sha256'] == sha and data['frames'] == 10601
    assert data['cold_boot'] and not data['savestate_loaded'] and not data['callback_errors']
    assert not any(value for key, value in data.items() if key.startswith('synthetic_'))
    donor = data['battery_save_preloaded']
    assert donor['copied_byte_exact_before_cold_boot']
    assert base.digest(donor['source']) == donor['source_sha256']
    rows = {entry['frame']: entry for entry in data['frames_captured'] if entry['frame'] in FRAMES}
    assert set(rows) == set(FRAMES)
    for row in rows.values():
        assert base.digest(row['path']) == row['PNG_sha256']
    return report, data, rows


def font_pixels(font, label, y):
    pixels = set()
    for index, character in enumerate(label):
        glyph = font.decode(character)
        pixels.update((126 + index * 6 + x, y + 3 + dy)
                      for x in range(6) for dy in range(11) if glyph.getpixel((x, dy)))
    return pixels


def visible_white(image, left, top, right, bottom):
    return {(x, y) for x in range(left, right) for y in range(top, bottom)
            if image.getpixel((x, y)) == INK}


def main():
    assert not OUTPUT.exists()
    release, staged = base.load(stage.parent.RELEASE), base.load(stage.ROOT / 'stage.json')
    reports = {
        side: capture(folder, digest)
        for side, folder, digest in (
            ('Japanese', BEFORE / 'clean', release['clean_input_sha256']),
            ('Before', BEFORE / 'current', release['candidate_sha256']),
            ('Fixed', stage.ROOT, staged['sha256']),
        )
    }
    assert all(reports['Japanese'][1][key] == data[key] for _, data, _ in reports.values()
               for key in ('scripted_input_schedule', 'core_DLL_sha256', 'core_options'))
    assert len({data['battery_save_preloaded']['source_sha256'] for _, data, _ in reports.values()}) == 1
    dependencies = {str(path): base.digest(path) for path, _, _ in reports.values()}
    image = base.NdsImage.open(stage.ROM)
    arm = image.read_file(stage.ARM)
    font = GameAsciiFont.from_arm9(arm)
    art = PxlImage.from_bytes(image.read_file(stage.ART)).render().convert('RGB')
    selected_by_skill = unpack_from('<20I', arm, 0x148448)
    expected_sets = [set(range(6)), *(set(selected_by_skill[2 * i:2 * i + 2]) for i in SKILL_IDS), set(range(6))]
    WORK.mkdir(exist_ok=True)
    sheet = Image.new('RGB', (840, 12 * 205), '#252830')
    draw = ImageDraw.Draw(sheet)
    cases = []
    for line, (frame, skill, selected) in enumerate(zip(FRAMES, SKILLS, expected_sets, strict=True)):
        screens = {}
        for column, (side, (_, _, rows)) in enumerate(reports.items()):
            row = rows[frame]
            dependencies[row['path']] = row['PNG_sha256']
            with Image.open(row['path']) as screen:
                assert screen.size == (256, 384)
                screens[side] = screen.convert('RGB')
            tile = screens[side].crop((122, 97, 256, 190))
            sheet.paste(tile.resize((268, 186), Image.Resampling.NEAREST), (8 + column * 280, 17 + 205 * line))
            draw.text((10 + column * 280, 205 * line), f'{skill}  {side}', fill='white')
        before, fixed, clean = screens['Before'], screens['Fixed'], screens['Japanese']
        diff = ImageChops.difference(before, fixed).getbbox()
        if diff:
            assert diff[0] >= 124 and diff[1] >= 99 and diff[2] <= 170 and diff[3] <= 189
        rows = []
        for index, label in enumerate(stage.LABELS):
            y = 99 + index * 15
            expected_ink = font_pixels(font, label, y) if index in selected else set()
            actual_ink = visible_white(fixed, 124, y, 170, y + 15)
            assert actual_ink == expected_ink, (frame, skill, label, len(actual_ink), len(expected_ink))
            assert bool(visible_white(clean, 124, y, 149, y + 15)) == (index in selected)
            assert all(native5(fixed.getpixel((x, dy))) == native5(art.getpixel((x, dy)))
                       for x in range(124, 170) for dy in range(y, y + 15) if (x, dy) not in expected_ink)
            rows.append(dict(label=label, selected=index in selected, ink_pixels=len(expected_ink)))
        cases.append(dict(frame=frame, selected_skill=skill, rows=rows, changed_bounds=diff))
    path = WORK / 'all_stat_selection_states.png'
    sheet.save(path)
    base.save(OUTPUT, dict(candidate_sha256=staged['sha256'], parent_sha256=staged['parent_sha256'],
        clean_sha256=release['clean_input_sha256'], cases=cases, complete_plaque_masks=6 * len(cases),
        all_non_plaque_frame_pixels_exact=True, all_original_skill_attribute_pairs_exact=True,
        ordinary_saved_game_inputs=True, hardware=False, sheet=str(path), sheet_sha256=base.digest(path),
        dependencies=dependencies | {__file__: base.digest(__file__)}))
    print('Verified 72 complete plaque masks, all ten skill states and the baseline and restored states.')


if __name__ == '__main__':
    main()
