"""Full actual panel/transition pixels and independent native font models."""

from pathlib import Path

from PIL import Image, ImageDraw

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.finish_refit_display_v712 import HINTS, WHITE, load
from scripts.prepare_refit_release_v831 import ROOT
from scripts.run_refit_release_v831 import CAP
from scripts.verify_full_fleet_battle_v652 import fleet_models
from scripts.verify_full_fleet_victory_v654 import funds
from scripts.verify_refit_release_v831 import OLD, ROM
from scripts.verify_village_wrap_v608 import read, save


def main():
    reports, shots, receipts = {}, {}, {}
    for case, rom, frames in (('before', OLD, 20600), ('after', ROM, 20600),
                              ('newgame_before', OLD, 4000), ('newgame_after', ROM, 4000)):
        reports[case], shots[case], receipts[case] = load(CAP / f'refit_editorial_v831_{case}', sha(rom.read_bytes()), frames)
        assert not any(value for key, value in reports[case].items() if key.startswith('synthetic_'))
    assert reports['before']['scripted_input_schedule'] == reports['after']['scripted_input_schedule']
    assert reports['newgame_before']['scripted_input_schedule'] == reports['newgame_after']['scripted_input_schedule']
    assert shots['before'].keys() == shots['after'].keys() and len(shots['after']) == 62
    assert shots['newgame_before'].keys() == shots['newgame_after'].keys() and len(shots['newgame_after']) == 7
    donor = read(ROOT / 'donor_copy.json')
    for key in ('before', 'after'):
        assert reports[key]['battery_save_preloaded']['source_sha256'] == donor['disposable_source_sha256']
    for key in ('newgame_before', 'newgame_after'):
        assert not reports[key].get('battery_save_preloaded')
    assert sha(Path(donor['protected_source']).read_bytes()) == donor['protected_source_sha256']
    assert sha(Path(donor['disposable_source']).read_bytes()) == donor['disposable_source_sha256']
    background = Image.new('RGB', (168, 84))
    for y in range(80, 164):
        for x in range(64, 232):
            colours = {shots['before'][f].getpixel((x, y)) for f in HINTS if shots['before'][f].getpixel((x, y)) != WHITE}
            assert len(colours) == 1
            background.putpixel((x - 64, y - 80), next(iter(colours)))
    background.save(ROOT / 'current_before_native_background.png')
    font = GameAsciiFont.from_arm9(NdsImage.open(ROM).read_file('/__arm9__.bin'))
    layouts = {r['message_id']: r for r in read('work/analysis/refit_editorial_v830/native_font_verification.json')['records']}
    actual, unchanged = [], []
    controls = 0
    for frame, current in shots['after'].items():
        expected = shots['before'][frame].copy()
        if frame in HINTS:
            row = layouts[HINTS[frame]]
            expected.paste(background, (64, 80))
            ink = set()
            for line_index, line in enumerate(row['lines']):
                for index, char in enumerate(line):
                    glyph = font.decode(char)
                    for y in range(11):
                        for x in range(6):
                            if glyph.getpixel((x, y)):
                                point = (64 + index * 6 + x, 80 + line_index * 12 + y)
                                assert 64 <= point[0] < 232 and 80 <= point[1] < 140
                                expected.putpixel(point, WHITE)
                                ink.add(point)
            visible = {(x, y) for y in range(80, 164) for x in range(64, 232) if current.getpixel((x, y)) == WHITE}
            assert visible == ink, (frame, 'actual font ink mismatch', sorted(visible ^ ink)[:10])
            for line_index, line in enumerate(row['lines']):
                for index in (0, len(line) - 1):
                    glyph_pixels = {p for p in ink if 64 + index * 6 <= p[0] < 70 + index * 6
                                    and 80 + line_index * 12 <= p[1] < 91 + line_index * 12}
                    assert glyph_pixels
                    damaged = current.copy()
                    for p in glyph_pixels:
                        damaged.putpixel(p, background.getpixel((p[0] - 64, p[1] - 80)))
                    assert damaged.tobytes() != expected.tobytes()
                    controls += 1
            actual.append({'frame': frame, 'message_id': HINTS[frame], 'English': row['English'],
                           'lines': row['lines'], 'actual_ink_pixels': len(ink),
                           'full_two_screen_RGB_model_exact': True,
                           'complete_first_final_glyphs_and_blank_cells': True,
                           'all_line_starts_x64_no_clipping': True})
        else:
            unchanged.append(frame)
        assert current.tobytes() == expected.tobytes(), (frame, 'outside body/whole-screen model mismatch')
    assert all(shots['newgame_before'][f].tobytes() == im.tobytes() for f, im in shots['newgame_after'].items())
    states = []
    arms = [NdsImage.open(p).read_file('/__arm9__.bin') for p in (OLD, ROM)]
    for frame in (3200, 11900, 19700, 20000, 20300, 20600):
        raw = []
        for case in ('before', 'after'):
            folder = CAP / f'refit_editorial_v831_{case}'
            snapshot = next(r for r in reports[case]['read_only_capture_RAM_snapshots'] if r['frame'] == frame)
            data = Path(snapshot['path']).read_bytes()
            assert snapshot['read_only_export'] and sha(data) == snapshot['sha256']
            raw.append(data)
        a, b = [fleet_models(arm, v, 1) for arm, v in zip(arms, raw, strict=True)]
        assert a == b and len(a) == 5
        money = [funds(arm, v) for arm, v in zip(arms, raw, strict=True)]
        assert money[0] == money[1] == 25975
        states.append({'frame': frame, 'five_ship_fleet_models_equal': True, 'funds_equal': money[1]})
    selected = [3200, 11900, 13100, 13400, 14000, 14300, 14900, 15200, 16100, 16400, 20000, 20600]
    sheet = Image.new('RGB', (4 * 256, 3 * 412), '#263238')
    draw = ImageDraw.Draw(sheet)
    for index, frame in enumerate(selected):
        x, y = (index % 4) * 256, (index // 4) * 412
        draw.text((x + 6, y + 5), f'V831 frame {frame} / {HINTS.get(frame, "entry-exit")}', fill='white')
        sheet.paste(shots['after'][frame], (x, y + 28))
    sheet_path = ROOT / 'actual_refit_review_sheet.png'
    sheet.save(sheet_path)
    save(ROOT / 'actual_gameplay_verification.json', {
        'candidate': str(ROM), 'candidate_sha256': sha(ROM.read_bytes()), 'receipts': receipts,
        'two20600_frame_ordinary_navigation_cold_boots_with_disposable_fixture_save': True,
        'no_new_gameplay_RAM_or_code_fixture_or_savestate': True,
        'actual23_help_holds_cover13_distinct_messages': actual,
        'whole_two_screen_models_match_all62_observed_frames': True,
        'unchanged_entry_menu_and_cancel_exit_frames': unchanged,
        'native_background_all14112_unoccluded_colour_witnesses_agree': True,
        'first_final_glyph_erasure_negative_controls': controls,
        'five_ship_and_funds_state_checks': states,
        'ordinary_New_Game_without_save_or_fixture_all7_frames_exact': True,
        'review_sheet': str(sheet_path), 'review_sheet_sha256': sha(sheet_path.read_bytes()),
        'visual_review_pending': True,
        'scope': 'Actual13 distinct Refit help selections including9 revised messages, entry/exit and ordinary startup. All31 have independent controlled native coverage. Not31 ordinary visits, full-route playthrough or hardware verification.',
        'verifier_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print('Actual23 holds/13 help selections,all62 whole-screen models,normal exit and7 New Game pairs pass;visual sheet pending.', flush=True)


if __name__ == '__main__':
    main()
