"""Check full actual Refit compositions and unchanged ordinary New Game scenes."""

from pathlib import Path

from PIL import Image, ImageDraw

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.inspect_committed_gpu_v646 import CORE_SHA
from scripts.run_refit_display_v712 import ROM
from scripts.run_room_gender_v694 import CAP
from scripts.verify_full_fleet_battle_v652 import fleet_models
from scripts.verify_full_fleet_victory_v654 import funds
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/refit_help_v712')
HINTS = dict(zip((13100, 13400, 13700, 14000, 14300, 14600, 14900, 15200,
    15500, 15800, 16100, 16400, 16700, 17000, 17300, 17600, 17900, 18200,
    18500, 18800, 19100, 19400, 19700),
    (1286, 1287, 1283, 1280, 1281, 1248, 1247, 1277, 1278, 1255, 1249, 1250,
    1284, 1281, 1280, 1283, 1277, 1247, 1248, 1278, 1278, 1278, 1278), strict=True))
WHITE, BOX = (230, 230, 230), (64, 80, 232, 164)


def load(folder, expected_rom, frames):
    path = folder / 'capture_report.json'
    report = read(path)
    assert report['frames'] == frames and report['ROM_sha256'] == expected_rom
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    assert report['core_DLL_sha256'] == CORE_SHA
    shots = {}
    for row in report['frames_captured']:
        p = Path(row['path'])
        assert sha(p.read_bytes()) == row['PNG_sha256']
        image = Image.open(p).convert('RGB')
        if row['frame'] in shots:
            assert shots[row['frame']].tobytes() == image.tobytes()
        shots[row['frame']] = image
    return report, shots, {'report': str(path), 'sha256': sha(path.read_bytes())}


def main():
    pre = read(ROOT / 'preflight.json')
    config = read(ROOT / 'display_run_config.json')
    release = read(ROOT / 'release_proof.json')
    assert release['candidate_sha256'] == sha(ROM.read_bytes()) == config['current_candidate_sha256']
    yard_folder = CAP / 'refit_help_v712_yard'
    yard, shots, yard_receipt = load(yard_folder, release['candidate_sha256'], 19700)
    old, old_shots, old_receipt = load(CAP / 'yard_selection_v705_baseline', pre['candidate_sha256'], 19700)
    assert yard['scripted_input_schedule'] == old['scripted_input_schedule']
    assert shots.keys() == old_shots.keys() and len(shots) == 59
    assert yard['battery_save_preloaded']['source_sha256'] == pre['donor_sha256']
    assert not any(v for k, v in yard.items() if k.startswith('synthetic_'))
    background = Image.new('RGB', (168, 84))
    witnesses = []
    for y in range(80, 164):
        for x in range(64, 232):
            candidates = [(f, old_shots[f].getpixel((x, y))) for f in HINTS
                if old_shots[f].getpixel((x, y)) != WHITE]
            colours = {c for _, c in candidates}
            assert len(colours) == 1 and candidates
            background.putpixel((x - 64, y - 80), next(iter(colours)))
            witnesses.append({'XY': [x, y], 'unoccluded_reference_frame': candidates[0][0],
                'all_unoccluded_reference_RGB_values_equal': True})
    bg_path = ROOT / 'prechange_native_background.png'
    background.save(bg_path)
    font = GameAsciiFont.from_arm9(NdsImage.open(ROM).read_file('/__arm9__.bin'))
    native = read(ROOT / 'native_layout_proof.json')
    layouts = {r['message_id']: r for r in native['31_complete168x108_native_fonts']}
    repaired, unchanged, controls = [], [], 0
    for frame, current in shots.items():
        expected = old_shots[frame].copy()
        if frame in HINTS:
            row = layouts[HINTS[frame]]
            expected.paste(background, (64, 80))
            ink = set()
            for line_index, line in enumerate(row['lines']):
                for i, char in enumerate(line):
                    for y in range(11):
                        for x in range(6):
                            if font.decode(char).getpixel((x, y)):
                                point = (64 + i * 6 + x, 80 + line_index * 12 + y)
                                assert BOX[0] <= point[0] < BOX[2] and BOX[1] <= point[1] < BOX[3]
                                expected.putpixel(point, WHITE)
                                ink.add(point)
            actual = {(x, y) for y in range(80, 164) for x in range(64, 232)
                if current.getpixel((x, y)) == WHITE}
            assert actual == ink, (frame, sorted(actual ^ ink)[:8])
            for line_index, line in enumerate(row['lines']):
                for ch_index in (0, len(line) - 1):
                    erased = current.copy()
                    changed = False
                    for y in range(11):
                        for x in range(6):
                            p = (64 + ch_index * 6 + x, 80 + line_index * 12 + y)
                            if p in ink:
                                erased.putpixel(p, background.getpixel((p[0] - 64, p[1] - 80)))
                                changed = True
                    assert changed and erased.tobytes() != expected.tobytes()
                    controls += 1
            repaired.append({'frame': frame, 'message_id': HINTS[frame], 'English': row['English'],
                'all_lines': row['lines'], 'glyph_ink_pixels': len(ink),
                'full98304_pixel_two_screen_RGB_model_exact': True,
                'all_words_complete_all_line_starts_x64_and_original_brown_background_restored': True})
        else:
            unchanged.append(frame)
        assert current.tobytes() == expected.tobytes(), frame
    assert len(repaired) == 23 and len(unchanged) == 36
    snapshots = {r['frame']: r for r in yard['read_only_capture_RAM_snapshots']}
    fleet = []
    arm = NdsImage.open(ROM).read_file('/__arm9__.bin')
    for frame in (3200, 9800, 13400, 19700):
        row = snapshots[frame]
        raw = Path(row['path']).read_bytes()
        assert row['read_only_export'] and sha(raw) == row['sha256']
        models, coins = fleet_models(arm, raw, 1), funds(arm, raw)
        assert len(models) == 5 and coins == 25975
        fleet.append({'frame': frame, 'ships': models, 'funds': coins})
    newgame, ng_shots, ng_receipt = load(CAP / 'refit_help_v712_newgame', release['candidate_sha256'], 31000)
    control, ng_control, control_receipt = load(CAP / 'refit_help_v706_newgame_control', pre['candidate_sha256'], 31000)
    assert newgame['scripted_input_schedule'] == control['scripted_input_schedule']
    assert newgame['battery_save_preloaded']['source_sha256'] == control['battery_save_preloaded']['source_sha256']
    assert ng_shots.keys() == ng_control.keys() and len(ng_shots) == 49
    assert all(ng_shots[f].tobytes() == ng_control[f].tobytes() for f in ng_shots)
    selection = (13100, 13400, 14600, 14900, 15800, 16100, 16400, 19700)
    sheet = Image.new('RGB', (4 * 512, 2 * 410), '#202b32')
    draw = ImageDraw.Draw(sheet)
    for index, frame in enumerate(selection):
        x, y = index % 4 * 512, index // 4 * 410
        sheet.paste(old_shots[frame], (x, y + 24))
        sheet.paste(shots[frame], (x + 256, y + 24))
        draw.text((x + 6, y + 6), f'{frame}: V692 | V712', fill='white')
    sheet_path = ROOT / 'actual_before_after_refit.png'
    sheet.save(sheet_path)
    save(ROOT / 'display_proof.json', {'candidate': str(ROM), 'candidate_sha256': release['candidate_sha256'],
        'receipts': [yard_receipt, old_receipt, ng_receipt, control_receipt],
        'current19700_Refit_and31000_New_Game_runs_terminal_no_savestate': True,
        'reused_current_V692_controls_are_complete_report_and_ROM_bound_not_retimed': True,
        'all59_Refit_whole_two_screen_RGB_models_exact': True,
        '23_actual_help_compositions': repaired, '36_whole_unchanged_Refit_prefix_screens': unchanged,
        'prechange_native_background_all14112_pixels_have_unoccluded_equal_RGB_witnesses': witnesses,
        'background_does_not_guess_or_edit_production_art': True,
        'complete_actual_line_first_final_glyph_erasure_controls': controls,
        'four_original_fleet_and_funds_states': fleet,
        'all49_New_Game_title_chooser_story_and_Hangzhou_RGB_pairs_exact': True,
        'New_Game_uses_existing_isolated_system_unlock_not_earned_unlock_or_full_route': True,
        'all31_controlled_native_fonts13_distinct_actual_messages_other_scene_contexts_not_inferred': True,
        'final_Refit_screen_is_unaccepted_cancel_confirmation_not_a_save': True,
        'review_sheet': str(sheet_path), 'review_sheet_sha256': sha(sheet_path.read_bytes()),
        'verifier_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print('V712 actual:59 full Refit models,23 repaired help displays,49 complete New Game pairs and all first/final line glyphs pass.', flush=True)


if __name__ == '__main__':
    main()
