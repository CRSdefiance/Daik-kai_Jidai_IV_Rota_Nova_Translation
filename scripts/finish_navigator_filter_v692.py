"""Verify full live filter rows, original gameplay choices and ordinary regression."""

from pathlib import Path

from PIL import Image, ImageDraw

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.inspect_committed_gpu_v646 import CORE_SHA
from scripts.run_navigator_filter_v692 import CAP, ROM, ROOT
from scripts.verify_regional_ui_v616 import full_cells, glyphs
from scripts.verify_village_wrap_v608 import read, save

POPUPS = (8800, 9200, 10800, 11200, 13200, 13600, 14000)


def pictures(report):
    result = {}
    for row in report['frames_captured']:
        path = Path(row['path'])
        assert sha(path.read_bytes()) == row['PNG_sha256']
        image = Image.open(path).convert('RGB')
        if row['frame'] in result:
            assert result[row['frame']].tobytes() == image.tobytes()
        result[row['frame']] = image
    return result


def unchanged_controls(font, image):
    # Locate only unchanged Unassigned/All controls. Their independent center
    # and two-row pitch determine Captain's origin, never the repaired letters.
    controls = []
    for text in ('Unassigned', 'All'):
        ink = glyphs(font, text)
        matches = [(x, y) for y in range(250, 313) for x in range(90, 169 - len(text) * 6)
                   if all(image.getpixel((x + dx, y + dy)) == (8, 8, 8) for dx, dy in ink)]
        assert len(matches) == 1, (text, matches)
        x, y = matches[0]
        full_cells(image, font, text, x, y, (8, 8, 8))
        controls.append((text, x, y))
    _, ux, uy = controls[0]
    _, ax, ay = controls[1]
    assert ux + 30 == ax + 9 and ay - uy == 40
    return ux + (60 - 42) // 2, uy + (ay - uy) // 2, controls


def main():
    static = read(ROOT / 'static_release_proof.json')
    assert sha(ROM.read_bytes()) == static['candidate_sha256']
    font = GameAsciiFont.from_arm9(NdsImage.open(ROM).read_file('/__arm9__.bin'))
    plans = read(ROOT / 'all_choices/run_cases.json')
    reports, images, receipts = {}, {}, []
    for name in ('source_full', 'hodram_full', 'maria_full', 'ordinary'):
        folder = CAP / ('navigator_filter_v692_' + name)
        path = folder / 'capture_report.json'
        report, contract = read(path), read(folder / 'run_contract.json')
        row = plans['cases'][name] if name != 'ordinary' else read(ROOT / 'run_cases.json')['cases']['ordinary']
        assert contract['config'] == row
        assert report['frames'] == row['frames'] and report['ROM_sha256'] == row['ROM_sha256']
        assert sha(Path(row['ROM']).read_bytes()) == row['ROM_sha256']
        assert report['core_DLL_sha256'] == CORE_SHA and report['cold_boot']
        assert not report['savestate_loaded'] and not report['callback_errors']
        assert report['scripted_input_schedule'] == read(row['inputs'])
        assert sha(Path(row['inputs']).read_bytes()) == row['inputs_sha256']
        assert not any(v for k, v in report.items() if k.startswith('synthetic_'))
        if row['donor']:
            assert report['battery_save_preloaded']['source_sha256'] == row['donor_sha256']
            assert sha(Path(row['donor_path']).read_bytes()) == row['donor_sha256']
        else:
            assert not report.get('battery_save_preloaded')
        reports[name], images[name] = report, pictures(report)
        receipts.append({'case': name, 'report': str(path), 'sha256': sha(path.read_bytes())})
    assert images['source_full'].keys() == images['hodram_full'].keys()
    changes = [f for f in images['source_full']
               if images['source_full'][f].tobytes() != images['hodram_full'][f].tobytes()]
    assert changes == sorted((*POPUPS, 9600)), changes
    # Retain, rather than silently mask, the separate selected-officer cursor
    # appearance. No caption pixels differ in this frame. The complete cell
    # repeats an unchanged source appearance, but same-frame timing is unproven.
    cursor_source, cursor_current = images['source_full'][9600], images['hodram_full'][9600]
    cursor_points = [(x, y) for y in range(384) for x in range(256)
                     if cursor_source.getpixel((x, y)) != cursor_current.getpixel((x, y))]
    assert len(cursor_points) == 87
    assert all(88 <= x < 104 and 247 <= y < 268 and
               cursor_source.getpixel((x, y)) == (0, 165, 172) and
               cursor_current.getpixel((x, y)) == (16, 16, 16) for x, y in cursor_points)
    cursor_box = (88, 244, 104, 276)
    assert cursor_current.crop(cursor_box).tobytes() == images['source_full'][11600].crop(cursor_box).tobytes()
    cursor_observation = {'frame': 9600, 'changed_pixels': 87, 'difference_bounds': [88, 247, 104, 268],
        'whole_selected_cell': list(cursor_box), 'original_same_appearance_reference_frame': 11600,
        'whole512_pixel_cell_exact_to_retained_source_appearance': True,
        'same_frame_cursor_phase_not_proven_no_retimed_frame_or_full_frame_equality_claim': True}
    second_source, second_current = images['source_full'][10800], images['hodram_full'][10800]
    second_points = [(x, y) for y in range(384) for x in range(256)
                     if not (96 <= x < 166 and 282 <= y < 293) and
                     second_source.getpixel((x, y)) != second_current.getpixel((x, y))]
    assert len(second_points) == 1446
    assert all(6 <= x < 158 and 208 <= y < 278 and
               second_current.getpixel((x, y)) == (0, 165, 172) for x, y in second_points)
    assert all(second_current.getpixel((x, y)) == images['source_full'][14000].getpixel((x, y))
               for y in range(384) for x in range(256) if not (96 <= x < 166 and 282 <= y < 293))
    second_cursor = {'frame': 10800, 'changed_non_caption_pixels': 1446,
        'difference_bounds': [6, 208, 158, 278], 'original_same_appearance_reference_frame': 14000,
        'whole98304_pixel_frame_except_caption_exact_to_retained_source_appearance': True,
        'same_frame_cursor_phase_not_proven_no_retimed_baseline_equality_claim': True}
    cells = []
    for case in ('hodram_full', 'maria_full'):
        for frame in POPUPS:
            im = images[case][frame]
            x, y, controls = unchanged_controls(font, im)
            assert (x, y) == (107, 282)
            result = full_cells(im, font, 'Captain', x, y, (8, 8, 8))
            # Include the complete row interior, including removed Japanese ink
            # and blank cells on both sides, rather than positive-letter samples.
            expected = {(x + dx, y + dy) for dx, dy in glyphs(font, 'Captain')}
            actual = {(xx, yy) for yy in range(y, y + 11) for xx in range(96, 166)
                      if im.getpixel((xx, yy)) == (8, 8, 8)}
            assert actual == expected
            if case == 'hodram_full' and frame != 10800:
                source = images['source_full'][frame]
                assert all(im.getpixel((xx, yy)) == source.getpixel((xx, yy))
                           for yy in range(384) for xx in range(256)
                           if not (96 <= xx < 166 and y <= yy < y + 11))
                assert any(source.getpixel(p) != im.getpixel(p) for p in expected)
            cells.append({'case': case, 'frame': frame, 'independent_unchanged_controls': controls,
                'complete_row_bounds': [96, y, 166, y + 11], 'caption': result,
                'complete_row_ink_and_blank_cells_no_Japanese_residue_exact': True})
    ordinary_old_path = CAP / 'story_percent_v685_ordinary/capture_report.json'
    ordinary_old = read(ordinary_old_path)
    assert ordinary_old['ROM_sha256'] == read(ROOT / 'build_preflight.json')['source_candidate_sha256']
    old_images = pictures(ordinary_old)
    assert ordinary_old['scripted_input_schedule'] == reports['ordinary']['scripted_input_schedule']
    assert old_images.keys() == images['ordinary'].keys() and len(old_images) == 89
    assert all(old_images[f].tobytes() == im.tobytes() for f, im in images['ordinary'].items())
    # Final RAM has only the declared original caption storage changed after
    # ordinary New Game; it has not opened the repaired filter popup.
    old_ram = bytearray((CAP / 'story_percent_v685_ordinary/final_arm9_ram.bin').read_bytes())
    new_ram = (CAP / 'navigator_filter_v692_ordinary/final_arm9_ram.bin').read_bytes()
    from dk4tool.patch.navigator_captain_filter import AFTER, OFFSET
    old_ram[OFFSET:OFFSET + 8] = AFTER
    assert bytes(old_ram) == new_ram
    # The failed original observer's game output is independently checked before
    # the later schedule differs. Its unmatched return is not gender evidence.
    pilot = read(CAP / 'deck_gender_v692_hodram_unassigned/capture_report.json')
    pilot_images = pictures(pilot)
    common = sorted(f for f in pilot_images if f <= 8800 and f in images['source_full'])
    assert all(pilot_images[f].tobytes() == images['source_full'][f].tobytes() for f in common)
    # Record complete terminal menu-run differences honestly; only ordinary
    # RAM receives an exact post-change claim above.
    ram_a = (CAP / 'navigator_filter_v692_source_full/final_arm9_ram.bin').read_bytes()
    ram_b = (CAP / 'navigator_filter_v692_hodram_full/final_arm9_ram.bin').read_bytes()
    diffs = [i for i, (a, b) in enumerate(zip(ram_a, ram_b, strict=True)) if a != b]
    save(ROOT / 'menu_terminal_RAM_diagnostic.json', {'different_bytes': len(diffs),
        'addresses': [0x02000000 + i for i in diffs], 'source_sha256': sha(ram_a), 'candidate_sha256': sha(ram_b),
        'not_an_unqualified_equal_RAM_claim': True})
    sheet = Image.new('RGB', (3 * 256, 2 * 408), '#263238')
    draw = ImageDraw.Draw(sheet)
    panels = [('source_full', 8800, 'V685 original Japanese filter'),
              ('hodram_full', 8800, 'V692 complete Captain'), ('maria_full', 8800, 'V692 Maria filter'),
              ('hodram_full', 9600, 'Captain filter applied'), ('hodram_full', 11600, 'All filter applied'),
              ('hodram_full', 14400, 'Unassigned filter restored')]
    for index, (name, frame, label) in enumerate(panels):
        x, y = index % 3 * 256, index // 3 * 408
        draw.text((x + 4, y + 4), label, fill='white')
        sheet.paste(images[name][frame], (x, y + 24))
    review = ROOT / 'actual_filter_review.png'
    sheet.save(review)
    save(ROOT / 'proof.json', {'candidate': str(ROM), 'candidate_sha256': static['candidate_sha256'],
        'capture_reports': receipts, 'all14_complete_Captain_rows_both_saved_routes': cells,
        'full_RGB_changed_frames': changes, 'separate_source_cursor_appearances': [cursor_observation, second_cursor],
        'whole_filter_frames_unchanged': len(images['source_full']) - len(changes),
        'ordinary_full_RGB_baseline_pairs': len(old_images), 'ordinary_full_RAM_only_declared_caption_slot_differs': True,
        'failed_observer_game_output_independently_matches_before_schedule_diverges': common,
        'normal_officer_duty_changes_and_original_Captain_All_Unassigned_inputs': True,
        'actual_filter_gameplay_outcomes_require_visual_review': str(review),
        'review_sheet': str(review), 'review_sheet_sha256': sha(review.read_bytes()),
        'initial_popup_reset_assumption_and_unmatched_original_return_observer_failure_retained': True,
        'no_actual_020157D8_gender_parent_display_or_global_nonuse_claim': True,
        'runner_sha256': sha(Path('scripts/run_navigator_filter_v692.py').read_bytes()),
        'launcher_sha256': sha(Path('scripts/run_filter_choices_v692.py').read_bytes()),
        'verifier_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print(f'V692 live:14 whole caption rows;{len(old_images)} ordinary pairs;two original cursor appearances retained.', flush=True)


if __name__ == '__main__':
    main()
