"""Bind two actual regional-rumor displays, their cache and exit-page behavior."""

from pathlib import Path

from PIL import Image, ImageChops

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.native_regional_rumor_fixture_v749 import assign
from scripts.verify_common_alignment_native_v257 import raster
from scripts.verify_country_gameplay_v748 import snapshot
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/regional_rumors_v749')
CAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193')


def captures(folder, frames, region=None):
    path = CAP / folder / 'capture_report.json'
    report = read(path)
    assert report['frames'] == frames and report['cold_boot'] and not report['savestate_loaded']
    assert not report['callback_errors'] and not report['hardware_device_verification']
    assert report['core_DLL_sha256'] == '42160dbfef89adfb3cfd975070a3047d8ad0979cead55607ebdfd3b931046c2b'
    assert sha(Path(report['ROM']).read_bytes()) == report['ROM_sha256']
    fixtures = report.get('synthetic_regional_rumor_fixtures', [])
    assert len(fixtures) == int(region is not None)
    assert not any(v for k, v in report.items() if k.startswith('synthetic_') and k != 'synthetic_regional_rumor_fixtures')
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
        assert receipt['expected_native_rumor_message'] == 709 + region
        adapter = report['controlled_rumor_harness_adapter']
        assert adapter['original_harness_file_unchanged']
        assert adapter['unchanged_original_harness_sha256'] == sha(Path('scripts/headless_desmume_v193.py').read_bytes())
        assert adapter['adapter_sha256'] == sha(Path('scripts/run_regional_rumor_capture_v749.py').read_bytes())
        journal = read(CAP / folder / 'navigation_command_journal.json')
        assert [x['frame'] for x in journal['commands_received']] == [5800, 6500]
        assert journal['commands_received'][-1]['command'] == {'stop': True}
        assert all(x['validation_passed'] for x in journal['commands_received'])
    else:
        assert not report.get('battery_save_preloaded')
    rows = {}
    for row in report['frames_captured']:
        assert sha(Path(row['path']).read_bytes()) == row['PNG_sha256']
        rows[row['frame']] = row
    return report, rows


def main():
    layouts = {r['message_id']: r for r in read(ROOT / 'native_review.json')['all21_native_printf_macro_wrap_and_complete_font_planes']}
    results, reports = [], {}
    for region in (0, 20):
        prefix = f'rumors_v749_region{region}_final_'
        baseline, before = captures(prefix + 'baseline', 6500, region)
        report, after = captures(prefix + 'new', 6500, region)
        assert baseline['scripted_input_schedule'] == report['scripted_input_schedule']
        assert baseline['core_options'] == report['core_options'] and set(before) == set(after)
        assert baseline['synthetic_regional_rumor_fixtures'][0]['changes'] == report['synthetic_regional_rumor_fixtures'][0]['changes']
        rom = NdsImage.open(report['ROM'])
        arm = rom.read_file('/__arm9__.bin')
        font = GameAsciiFont.from_arm9(arm)
        i, expected = 709 + region, set()
        for row, line in enumerate(layouts[i]['lines']):
            for n, char in enumerate(line):
                glyph = font.decode(char)
                for y in range(11):
                    for x in range(6):
                        if glyph.getpixel((x, y)):
                            expected.add((22 + n * 6 + x, 296 + row * 16 + y))
        equal, different_page_phase = [], []
        for frame in sorted(after):
            old, new = (Image.open(p).convert('RGB') for p in (before[frame]['path'], after[frame]['path']))
            diff = ImageChops.difference(old, new)
            if frame == 5900:
                body = (16, 294, 244, 366)
                actual = {(x, y) for y in range(body[1], body[3]) for x in range(body[0], body[2]) if new.getpixel((x, y)) == (0, 8, 0)}
                assert actual == expected, (i, len(expected - actual), len(actual - expected))
                diff.paste((0, 0, 0), body)
                assert diff.getbbox() is None
            elif region == 0 and frame >= 6050:
                different_page_phase.append(frame)
            else:
                assert diff.getbbox() is None, (region, frame)
                equal.append(frame)
        assert len(equal) == (7 if region == 0 else 12)
        assert different_page_phase == ([6050, 6150, 6250, 6400, 6500] if region == 0 else [])
        bindings = []
        for current_report in (baseline, report):
            current_rom = NdsImage.open(current_report['ROM'])
            common, current_arm = current_rom.read_file('/COMMON/MESFILE.DK4'), current_rom.read_file('/__arm9__.bin')
            entry = common_message_entries(common, current_arm, clean=False)[i]
            block = IlnkContainer.parse(common).blocks[entry.block]
            ram = snapshot(current_report, 5900)
            position = ram.find(block)
            assert position >= 0 and ram.find(block, position + 1) == -1
            bindings.append({'ROM_sha256': current_report['ROM_sha256'], 'block': entry.block,
                'whole_block_bytes_exact': len(block), 'resident_address': 0x02000000 + position})
        results.append({'message_id': i, 'frame': 5900, 'lines': layouts[i]['lines'],
            'all_glyph_and_blank_paper_cells_exact': True, 'every_pixel_outside_text_plane_exact_baseline': True,
            'capture': after[5900], 'whole_two_screen_equal_baseline_frames': equal,
            'cache_block_bindings': bindings, 'fixture': report['synthetic_regional_rumor_fixtures'][0]})
        for name in (prefix + 'baseline', prefix + 'new'):
            path = CAP / name / 'capture_report.json'
            reports[str(path)] = sha(path.read_bytes())
    old_rom = NdsImage.open('out/all_routes_combined_v748_candidate.nds')
    old_arm = old_rom.read_file('/__arm9__.bin')
    old_text = common_message_entries(old_rom.read_file('/COMMON/MESFILE.DK4'), old_arm, clean=False)[709].text
    _, consumed = raster(old_arm, old_text, 0x01FFCE40 - 0x02000000, size=(228, 64), complete=False, instruction_limit=1000000)
    assert len(old_text) == 107 and consumed == 73 and old_text[consumed:] == b' ' * 34
    blank = Image.open(CAP / 'rumors_v749_region0_final_baseline/frame_006050_cold_boot.png').convert('RGB')
    assert not any(blank.getpixel((x, y)) == (0, 8, 0) for y in range(294, 366) for x in range(16, 244))
    returns = []
    for frame in (6050, 6150, 6250, 6400, 6500):
        control = Image.open(CAP / f'rumors_v749_region20_final_new/frame_{frame:06d}_cold_boot.png').convert('RGB')
        current = Image.open(CAP / f'rumors_v749_region0_final_new/frame_{frame:06d}_cold_boot.png').convert('RGB')
        header = (16, 8, 240, 36)
        diff = ImageChops.difference(control, current)
        diff.paste((0, 0, 0), header)
        assert diff.getbbox() is None
        forward, inverse = {}, {}
        for y in range(header[1], header[3]):
            for x in range(header[0], header[2]):
                a, b = control.getpixel((x, y)), current.getpixel((x, y))
                forward.setdefault(a, set()).add(b)
                inverse.setdefault(b, set()).add(a)
        assert all(len(v) == 1 for v in forward.values()) and all(len(v) == 1 for v in inverse.values())
        changed = [(a, next(iter(b))) for a, b in forward.items() if a not in b]
        assert len(changed) == 4
        returns.append({'frame': frame, 'every_pixel_outside_header_exact_control': True,
            'complete_header_geometry_exact_under_bijective_color_substitution': True, 'header_bounds': header, 'changed_color_pairs': changed})
    game, game_rows = captures('rumors_v749_newgame', 4000)
    prior, prior_rows = captures('country_v748_newgame', 4000)
    assert game['scripted_input_schedule'] == prior['scripted_input_schedule']
    same = sorted(game_rows.keys() & prior_rows.keys())
    assert same == [1, 60, 180, 1200, 2400, 3200, 4000]
    for frame in same:
        assert Image.open(game_rows[frame]['path']).convert('RGB').tobytes() == Image.open(prior_rows[frame]['path']).convert('RGB').tobytes()
    path = CAP / 'rumors_v749_newgame/capture_report.json'
    reports[str(path)] = sha(path.read_bytes())
    save(ROOT / 'gameplay_verification.json', {'candidate': game['ROM'], 'candidate_sha256': game['ROM_sha256'],
        'four_terminal6500_frame_controlled_cold_boots': True, 'actual_native_rumor_displays': results,
        'ordinary_New_Game_terminal4000_frame_and7_whole_frame_pairs': same,
        'old709_padding_only_extra_page_removed': {'old_bytes': 107, 'first_paint_bytes': consumed,
            'remaining34_spaces_and_actual_blank6050_verified': True, 'new_return_same_phase_control': returns},
        'other19_rumors_source_native_font_and_selector_verified_not_live_regional_travel': True,
        'explicit_RAM_region_and_RNG_fixture_in_Istanbul_original_zero_share_preserved': True,
        'header_color_selection_cause_and_actual_UI_RNG_call_sequence_not_traced': True,
        'no_hardware_whole_route_or_earned_travel_claim': True,
        'reports': reports, 'verifier_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print('V749 actual709/729 complete text masks, resident block, blank-page removal, returns and7 New Game pairs pass.', flush=True)


if __name__ == '__main__':
    main()
