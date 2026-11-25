"""Check the complete exit label, menu geometry and return to Narvik."""

from PIL import Image, ImageChops, ImageDraw

from dk4tool.dialogue.font_audit import GameAsciiFont
from scripts import replay_developed_port_menu_20261115 as replay
from scripts import stage_developed_port_menu_20261115 as stage
from scripts.checkpoint_market_shared_consumers_20261114 import font_mask
from scripts.verify_captain_biographies_v1 import captured, shots
from scripts.verify_personal_gameplay_v841 import get_machine


base = stage.base
OUTPUT = stage.ROOT / 'narvik_verification.json'
SHEET = stage.ROOT / 'narvik_port_menu.png'
BOX = (88, 291, 168, 304)
PORTRAIT = (0, 192, 256, 384)
FOCUS = (76, 252, 180, 320)


def verify():
    staged = base.load(stage.STORED)
    parent = replay.ROOT / 'narvik_original_v3/capture'
    revised = stage.ROOT / 'narvik_revised/capture'
    pre, post = [base.load(folder / 'capture_report.json') for folder in (parent, revised)]
    assert pre['ROM_sha256'] == staged['previous_sha256'] and post['ROM_sha256'] == staged['candidate_sha256']
    assert pre['scripted_input_schedule'] == post['scripted_input_schedule']
    assert pre['core_options'] == post['core_options']
    expected_events = base.load(replay.HISTORY)['scripted_input_schedule'] + [
        dict(start=at, duration=8, buttons=[key]) for at, key in replay.ACTIONS]
    assert pre['scripted_input_schedule'] == expected_events
    evidence = {str(path): base.digest(path) for path in (replay.HISTORY, stage.STORED,
        parent / 'capture_report.json', revised / 'capture_report.json')}
    for report in (pre, post):
        assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
        assert report['frames'] == 14800 and not any(
            value for key, value in report.items() if key.startswith('synthetic_')
            and key != 'synthetic_location_fixtures')
        fixture, = report['synthetic_location_fixtures']
        assert fixture['village_id'] == 15 and fixture['only_eight_ship_coordinate_bytes_owned']
        assert fixture['expected_selector_point_after_original_update'] == [22048, 2234]
        assert base.digest(report['battery_save_preloaded']['source']) == report['battery_save_preloaded']['source_sha256']
    arm = base.NdsImage.open(stage.ROM).read_file(stage.ARM)
    font = GameAsciiFont.from_arm9(arm)
    before, after = map(shots, (pre, post))
    controls, menu = [], []
    sheet = Image.new('RGB', (832, 250), '#283133')
    draw = ImageDraw.Draw(sheet)
    for frame in replay.CAPTURES:
        a, b = map(captured, (before[frame], after[frame]))
        evidence.update({row['path']: row['PNG_sha256'] for row in (before[frame], after[frame])})
        assert a.size == b.size == (256, 384)
        diff = ImageChops.difference(a, b)
        bounds = diff.getbbox()
        if frame not in (14100, 14400):
            assert bounds is None, (frame, bounds)
            controls.append(frame)
            continue
        x0, y0, x1, y1 = bounds
        assert BOX[0] <= x0 < x1 <= BOX[2] and BOX[1] <= y0 < y1 <= BOX[3]
        lines_color = (8, 8, 8)
        count = font_mask(b, font, stage.ENGLISH, 92, 293, BOX, lines_color)
        assert count == 136
        assert b.getpixel((93, 291)) == ((205, 198, 180) if frame == 14100 else (0, 165, 172))
        for report, rom in ((pre, stage.parent.ROM), (post, stage.ROM)):
            snap, = [row for row in report['read_only_pause_RAM_snapshots'] if row['frame'] == frame]
            assert snap['read_only_export'] and base.digest(snap['path']) == snap['sha256']
            evidence[snap['path']] = snap['sha256']
            with open(snap['path'], 'rb') as file:
                raw = file.read()
            _, get = get_machine(base.NdsImage.open(rom).read_file(stage.ARM), raw)
            assert get(0x7F244) == 1 and get(0xB65E4) == 105
        menu.append(dict(frame=frame, complete_english_ink_pixels=count, original_town_getter=105,
            selected=frame == 14400, difference_bounds=list(bounds), complete_blank_cells=True))
        row = (frame == 14400) * 125
        for column, (name, screen) in enumerate((('Previous', a), ('Revised', b))):
            x = 416 * column
            draw.text((x + 4, row + 2), f'{name}, frame {frame}', fill='white')
            sheet.paste(screen.crop(FOCUS).resize((312, 102), Image.Resampling.NEAREST), (x + 4, row + 20))
    final, town = captured(after[14800]), captured(after[12980])
    assert final.crop(PORTRAIT).tobytes() == captured(before[14800]).crop(PORTRAIT).tobytes()
    # Check the returned Port icon, its town label and the normal footer modes.
    for box in ((206, 195, 255, 268), (153, 367, 256, 383)):
        assert final.crop(box).tobytes() == town.crop(box).tobytes()
    assert final.crop(FOCUS).tobytes() != captured(after[14400]).crop(FOCUS).tobytes()
    sheet.save(SHEET)
    base.save(OUTPUT, dict(candidate_sha256=staged['candidate_sha256'], cases=menu, equal_control_frames=controls,
        actual_gameplay=True, port_return_frame=14800, natural_village_development=True,
        position_fixture_only=True, normal_long_distance_travel_verified=False, hardware=False,
        native_format=dict(nul_terminated=True, in_slot=True, macro_count=0, substitutions=0, native_pages=1),
        sheet=str(SHEET), sheet_sha256=base.digest(SHEET), evidence=evidence))
    print('Both selected states pass complete glyph masks and ordinary selection returns to town.')


if __name__ == '__main__':
    verify()
