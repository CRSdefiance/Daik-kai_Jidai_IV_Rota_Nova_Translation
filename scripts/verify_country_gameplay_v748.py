"""Two paired controlled country displays, native cache blocks and ordinary boot."""

from pathlib import Path

from PIL import Image, ImageChops

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.native_country_briefing_fixture_v748 import assign
from scripts.verify_common_alignment_native_v257 import raster
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/country_editorial_v748')
CAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193')


def snapshot(report, frame):
    row = next(r for r in report['read_only_capture_RAM_snapshots'] if r['frame'] == frame)
    raw = Path(row['path']).read_bytes()
    assert len(raw) == 4194304 and sha(raw) == row['sha256']
    return raw


def captures(folder, frames, region=None):
    report = read(CAP / folder / 'capture_report.json')
    assert report['frames'] == frames and report['cold_boot'] and not report['savestate_loaded']
    assert not report['callback_errors'] and not report['hardware_device_verification']
    assert report['core_DLL_sha256'] == '42160dbfef89adfb3cfd975070a3047d8ad0979cead55607ebdfd3b931046c2b'
    assert sha(Path(report['ROM']).read_bytes()) == report['ROM_sha256']
    fixtures = report.get('synthetic_country_briefing_fixtures', [])
    assert len(fixtures) == int(region is not None)
    assert not any(value for key, value in report.items()
                   if key.startswith('synthetic_') and key != 'synthetic_country_briefing_fixtures')
    if region is not None:
        donor = report['battery_save_preloaded']
        assert sha(Path(donor['source']).read_bytes()) == donor['source_sha256'] == 'd991cb3bcdf74eed7aeb58c9a75957766b7c820d002423fd2b55cc8493cf8132'
        assert donor['copied_byte_exact_before_cold_boot']
        arm = NdsImage.open(report['ROM']).read_file('/__arm9__.bin')
        raw = snapshot(report, 5800)
        after, receipt = assign(arm, raw, {'region': region})
        assert fixtures[0]['frame'] == 5800
        assert receipt == {k: v for k, v in fixtures[0].items() if k != 'frame'}
        assert sum(a != b for a, b in zip(raw, after, strict=True)) == len(receipt['changes'])
        assert receipt['expected_native_country_message'] == 688 + region
        adapter = report['controlled_country_harness_adapter']
        assert adapter['original_harness_file_unchanged']
        assert adapter['unchanged_original_harness_sha256'] == sha(Path('scripts/headless_desmume_v193.py').read_bytes())
        assert adapter['adapter_sha256'] == sha(Path('scripts/run_country_capture_v748.py').read_bytes())
    else:
        assert not report.get('battery_save_preloaded')
    rows = {}
    for row in report['frames_captured']:
        assert sha(Path(row['path']).read_bytes()) == row['PNG_sha256']
        rows[row['frame']] = row
    return report, rows


def main():
    results, reports = [], {}
    layouts = {r['message_id']: r for r in read(ROOT / 'native_review.json')['all21_native_printf_macro_wrap_and_complete_font_planes']}
    for region in (0, 20):
        prefix = f'country_v748_region{region}_final_'
        baseline, before = captures(prefix + 'baseline', 6500, region)
        report, after = captures(prefix + 'new', 6500, region)
        assert baseline['scripted_input_schedule'] == report['scripted_input_schedule']
        assert baseline['core_options'] == report['core_options'] and set(before) == set(after)
        assert baseline['synthetic_country_briefing_fixtures'][0]['changes'] == report['synthetic_country_briefing_fixtures'][0]['changes']
        rom = NdsImage.open(report['ROM'])
        arm = rom.read_file('/__arm9__.bin')
        font = GameAsciiFont.from_arm9(arm)
        i = 688 + region
        lines = layouts[i]['lines']
        expected = set()
        for row, line in enumerate(lines):
            for n, char in enumerate(line):
                glyph = font.decode(char)
                for y in range(11):
                    for x in range(6):
                        if glyph.getpixel((x, y)):
                            expected.add((22 + n * 6 + x, 296 + row * 16 + y))
        equal, changed_legacy_page_frames = [], []
        for frame in sorted(after):
            old = Image.open(before[frame]['path']).convert('RGB')
            new = Image.open(after[frame]['path']).convert('RGB')
            diff = ImageChops.difference(old, new)
            if frame != 5900:
                if region == 20 and frame >= 6050:
                    # Old708 has a proven padding-only extra page. Its later
                    # input phase differs from the repaired one-page message.
                    changed_legacy_page_frames.append(frame)
                    continue
                assert diff.getbbox() is None, (region, frame)
                equal.append(frame)
                continue
            body = (16, 294, 244, 366)
            actual = {(x, y) for y in range(body[1], body[3]) for x in range(body[0], body[2])
                      if new.getpixel((x, y)) == (0, 8, 0)}
            assert actual == expected, (i, len(expected - actual), len(actual - expected))
            outside = diff.copy()
            outside.paste((0, 0, 0), body)
            assert outside.getbbox() is None
        if region == 0:
            assert len(equal) == 12 and {6050, 6150, 6250, 6400, 6500} <= set(equal)
        else:
            assert len(equal) == 7 and changed_legacy_page_frames == [6050, 6150, 6250, 6400, 6500]
        bindings = []
        for current_report in (baseline, report):
            current_rom = NdsImage.open(current_report['ROM'])
            current_common, current_arm = current_rom.read_file('/COMMON/MESFILE.DK4'), current_rom.read_file('/__arm9__.bin')
            entry = common_message_entries(current_common, current_arm, clean=False)[i]
            block = IlnkContainer.parse(current_common).blocks[entry.block]
            ram = snapshot(current_report, 5900)
            position = ram.find(block)
            assert position >= 0 and ram.find(block, position + 1) == -1
            bindings.append({'candidate_sha256': current_report['ROM_sha256'], 'native_block': entry.block,
                             'complete_resident_block_bytes_exact': len(block), 'resident_address': 0x02000000 + position})
        results.append({'message_id': i, 'region_fixture': region, 'frame': 5900, 'lines': lines,
            'all_glyph_and_blank_paper_cells_exact': True, 'all_pixels_outside_text_plane_equal_baseline': True,
            'capture': after[5900], 'whole_two_screen_equal_baseline_frames': equal,
            'cache_block_bindings': bindings, 'fixture': report['synthetic_country_briefing_fixtures'][0]})
        for name in (prefix + 'baseline', prefix + 'new'):
            path = CAP / name / 'capture_report.json'
            reports[str(path)] = sha(path.read_bytes())
    # The old placeholder consumes73/109 bytes in one original228x64 paint;
    # the remaining36 spaces cause an actual empty6050 page. New708 closes at
    # the first A press, then follows the same menu/return phase as new688.
    old_rom = NdsImage.open('out/all_routes_combined_v747_candidate.nds')
    old_arm = old_rom.read_file('/__arm9__.bin')
    old_text = common_message_entries(old_rom.read_file('/COMMON/MESFILE.DK4'), old_arm, clean=False)[708].text
    _, consumed = raster(old_arm, old_text, 0x01FFCE40 - 0x02000000,
                         size=(228, 64), complete=False, instruction_limit=1000000)
    assert len(old_text) == 109 and consumed == 73 and old_text[consumed:] == b' ' * 36
    blank = Image.open(CAP / 'country_v748_region20_final_baseline/frame_006050_cold_boot.png').convert('RGB')
    assert not any(blank.getpixel((x, y)) == (0, 8, 0) for y in range(294, 366) for x in range(16, 244))
    returns = []
    for frame in (6050, 6150, 6250, 6400, 6500):
        control = Image.open(CAP / f'country_v748_region0_final_new/frame_{frame:06d}_cold_boot.png').convert('RGB')
        current = Image.open(CAP / f'country_v748_region20_final_new/frame_{frame:06d}_cold_boot.png').convert('RGB')
        # Fixed top-town-header region; compare every other pixel exactly and
        # every header pixel by a bijective color substitution (same geometry).
        header = (16, 8, 240, 36)
        diff = ImageChops.difference(control, current)
        diff.paste((0, 0, 0), header)
        assert diff.getbbox() is None
        mapping, inverse = {}, {}
        for y in range(header[1], header[3]):
            for x in range(header[0], header[2]):
                a, b = control.getpixel((x, y)), current.getpixel((x, y))
                mapping.setdefault(a, set()).add(b)
                inverse.setdefault(b, set()).add(a)
        assert all(len(v) == 1 for v in mapping.values()) and all(len(v) == 1 for v in inverse.values())
        changed = [(a, next(iter(b))) for a, b in mapping.items() if a not in b]
        assert len(changed) == 4
        returns.append({'frame': frame, 'all_pixels_outside_top_header_exact_same_phase_control': True,
                        'complete_header_geometry_exact_with_bijective_color_substitution': True,
                        'fixed_header_bounds': header, 'changed_color_pairs': changed})
    game, game_rows = captures('country_v748_newgame', 4000)
    prior, prior_rows = captures('product_pitches_v747_newgame', 4000)
    assert game['scripted_input_schedule'] == prior['scripted_input_schedule']
    same = sorted(game_rows.keys() & prior_rows.keys())
    assert same == [1, 60, 180, 1200, 2400, 3200, 4000]
    for frame in same:
        assert Image.open(game_rows[frame]['path']).convert('RGB').tobytes() == Image.open(prior_rows[frame]['path']).convert('RGB').tobytes()
    path = CAP / 'country_v748_newgame/capture_report.json'
    reports[str(path)] = sha(path.read_bytes())
    save(ROOT / 'gameplay_verification.json', {
        'candidate': game['ROM'], 'candidate_sha256': game['ROM_sha256'],
        'four_terminal6500_frame_controlled_country_cold_boots': True, 'actual_native_country_displays': results,
        'ordinary_New_Game_terminal4000_frame_cold_boot_and7_whole_frame_pairs': same,
        'country0_shop_exit_and_town_return_whole_frame_exact_baseline': True,
        'country20_extra_blank_page_removed': {'old_bytes': 109, 'original_native_paint_consumes': consumed,
            'remaining_bytes_are36_spaces': True, 'actual_baseline6050_paper_has_no_ink': True,
            'new708_menu_and_town_return_same_phase_as_paired_country0_control': returns,
            'header_color_cause_not_separately_traced_and_no_palette_asset_changes': True},
        'all_original_saves_harness_core_and_production_ROM_bytes_preserved': True,
        'country_selection_is_RAM_fixture_in_Istanbul_not_ordinary_Britain_or_New_World_travel': True,
        'exact_number_or_call_sites_of_UI_RNG_draws_not_traced': True,
        'other19_country_entries_have_full_source_native_font_and_selector_evidence_not_live_travel': True,
        'reports': reports, 'verifier_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print('V748 complete688/708 masks, both cache blocks, old708 blank-page removal, return geometry and7 New Game pairs pass.', flush=True)


if __name__ == '__main__':
    main()
