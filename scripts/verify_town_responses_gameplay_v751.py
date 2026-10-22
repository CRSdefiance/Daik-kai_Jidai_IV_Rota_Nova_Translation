"""Actual original trend-selection displays, native cache and menu-return proof."""

from pathlib import Path

from PIL import Image, ImageChops
from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.native_town_trend_fixture_v751 import assign
from scripts.probe_button_prompt_native import BASE, call, machine
from scripts.verify_country_gameplay_v748 import snapshot
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/town_responses_v751')
CAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193')
SAVE_SHA = 'd991cb3bcdf74eed7aeb58c9a75957766b7c820d002423fd2b55cc8493cf8132'


def captures(folder, frames, request=None):
    path = CAP / folder / 'capture_report.json'
    report = read(path)
    assert report['frames'] == frames and report['cold_boot'] and not report['savestate_loaded']
    assert not report['callback_errors'] and not report['hardware_device_verification']
    assert report['core_DLL_sha256'] == '42160dbfef89adfb3cfd975070a3047d8ad0979cead55607ebdfd3b931046c2b'
    assert sha(Path(report['ROM']).read_bytes()) == report['ROM_sha256']
    fixtures = report.get('synthetic_town_trend_fixtures', [])
    assert len(fixtures) == int(request is not None)
    assert not any(v for k, v in report.items() if k.startswith('synthetic_') and k != 'synthetic_town_trend_fixtures')
    if request:
        donor = report['battery_save_preloaded']
        source = Path(read(ROOT / 'disposable_save_provenance.json')['disposable_source'])
        assert Path(donor['source']).resolve() == source.resolve()
        assert sha(source.read_bytes()) == donor['source_sha256'] == SAVE_SHA
        assert donor['copied_byte_exact_before_cold_boot'] and Path(donor['destination']).resolve() != source.resolve()
        arm = NdsImage.open(report['ROM']).read_file('/__arm9__.bin')
        raw = snapshot(report, 3200)
        after, receipt = assign(arm, raw, request)
        assert fixtures[0]['frame'] == 3200 and receipt == {k: v for k, v in fixtures[0].items() if k != 'frame'}
        assert sum(a != b for a, b in zip(raw, after, strict=True)) == 6
        adapter = report['controlled_town_trend_harness_adapter']
        assert adapter['original_harness_file_unchanged']
        assert adapter['unchanged_original_harness_sha256'] == sha(Path('scripts/headless_desmume_v193.py').read_bytes())
        assert adapter['adapter_sha256'] == sha(Path('scripts/run_town_trend_capture_v751.py').read_bytes())
        journal = read(CAP / folder / 'navigation_command_journal.json')
        assert [x['frame'] for x in journal['commands_received']] == [3200, 6501]
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
    native = read(ROOT / 'native_review.json')
    layouts = {r['message_id']: r['lines'] for r in native['all376_complete_native_font_cases'] if r['substitutions'] == ['Olive Oil']}
    checks, reports, controls = [], {}, {}
    for level, seed, message in ((50, 2, 655), (50, 3, 653), (150, 2, 654)):
        prefix = f'responses_v751_{level}_{seed}_final_'
        request = {'level': level, 'seed': seed}
        baseline, before = captures(prefix + 'baseline', 6501, request)
        report, after = captures(prefix + 'new', 6501, request)
        assert baseline['scripted_input_schedule'] == report['scripted_input_schedule']
        assert baseline['core_options'] == report['core_options'] and set(before) == set(after)
        assert baseline['synthetic_town_trend_fixtures'][0]['changes'] == report['synthetic_town_trend_fixtures'][0]['changes']
        rom = NdsImage.open(report['ROM'])
        arm, common = rom.read_file('/__arm9__.bin'), rom.read_file('/COMMON/MESFILE.DK4')
        font = GameAsciiFont.from_arm9(arm)
        entry = common_message_entries(common, arm, clean=False)[message]
        block = IlnkContainer.parse(common).blocks[entry.block]
        expected = set()
        for row, line in enumerate(layouts[message]):
            for n, char in enumerate(line):
                glyph = font.decode(char)
                for y in range(11):
                    for x in range(6):
                        if glyph.getpixel((x, y)):
                            expected.add((22 + n * 6 + x, 296 + row * 16 + y))
        equal = []
        for frame in sorted(after):
            old, new = (Image.open(p).convert('RGB') for p in (before[frame]['path'], after[frame]['path']))
            diff = ImageChops.difference(old, new)
            if frame not in (4600, 4800):
                assert diff.getbbox() is None, (level, seed, frame)
                equal.append(frame)
                continue
            body = (16, 294, 244, 366)
            actual = {(x, y) for y in range(body[1], body[3]) for x in range(body[0], body[2]) if new.getpixel((x, y)) == (0, 8, 0)}
            assert actual == expected, (message, frame, len(expected - actual), len(actual - expected))
            diff.paste((0, 0, 0), body)
            assert diff.getbbox() is None
            raw = snapshot(report, frame)
            at = raw.find(block)
            assert at >= 0 and raw.find(block, at + 1) == -1
            cpu = machine(arm)
            cpu.mem_write(BASE, raw)
            call(cpu, 0xB6618, ())
            town = cpu.reg_read(UC_ARM_REG_R0)
            call(cpu, 0xB31E0, (town, 14))
            assert cpu.reg_read(UC_ARM_REG_R0) == level
            checks.append({'message_id': message, 'frame': frame, 'level': level, 'seed': seed, 'lines': layouts[message],
                'all_glyph_and_blank_plane_pixels_exact': True, 'every_other_pixel_including_portrait_exact_baseline': True,
                'original_town_trend_getter_verified': True, 'whole_resident_native_cache_bytes_exact': len(block),
                'native_cache_block': entry.block, 'resident_address': BASE + at, 'capture': after[frame]})
        assert len(equal) == 17 and {5000, 5400, 5800, 6200, 6400, 6500, 6501} <= set(equal)
        controls[f'{level}_{seed}'] = equal
        for suffix in ('baseline', 'new'):
            path = CAP / (prefix + suffix) / 'capture_report.json'
            reports[str(path)] = sha(path.read_bytes())
    assert len(checks) == 6 and sum(map(len, controls.values())) == 51
    game, game_rows = captures('responses_v751_newgame', 4000)
    prior, prior_rows = captures('town_v750_newgame', 4000)
    assert game['scripted_input_schedule'] == prior['scripted_input_schedule']
    same = sorted(game_rows.keys() & prior_rows.keys())
    assert same == [1, 60, 180, 1200, 2400, 3200, 4000]
    for frame in same:
        assert Image.open(game_rows[frame]['path']).convert('RGB').tobytes() == Image.open(prior_rows[frame]['path']).convert('RGB').tobytes()
    path = CAP / 'responses_v751_newgame/capture_report.json'
    reports[str(path)] = sha(path.read_bytes())
    donor = read(ROOT / 'disposable_save_provenance.json')
    assert sha(Path(donor['protected_original']).read_bytes()) == donor['protected_original_sha256'] == SAVE_SHA
    assert sha(Path(donor['disposable_source']).read_bytes()) == donor['disposable_source_sha256'] == SAVE_SHA
    save(ROOT / 'gameplay_verification.json', {'candidate': game['ROM'], 'candidate_sha256': game['ROM_sha256'],
        'six_terminal6501_frame_cold_boots_with_declared_town_trend_and_seed_fixtures': True,
        'actual_dialogue_observations': checks, 'whole_two_screen_equal_baseline_controls': controls,
        'ordinary_New_Game_terminal4000_frame_and7_whole_frame_pairs': same,
        'all_other_RAM_bytes_original_save_and_disposable_donor_preserved': True,
        'original_UI_RNG_draw_count_not_traced_topics_bound_to_actual_complete_display': True,
        'other4_responses_have_complete_source_caller_and_native_font_evidence_not_earned_item_transfer_claim': True,
        'no_hardware_whole_route_or_ordinary_trend_creation_claim': True,
        'reports': reports, 'script_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print('V751:6 complete653-655 holds,51 unchanged menu/town controls, resident cache and7 New Game pairs pass.', flush=True)


if __name__ == '__main__':
    main()
