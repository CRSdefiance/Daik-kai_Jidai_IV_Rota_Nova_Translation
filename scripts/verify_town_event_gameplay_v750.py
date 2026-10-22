"""Verify actual question, both responses, arrival, native cache and flag transitions."""

import struct
from pathlib import Path

from PIL import Image, ImageChops
from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.native_promoter_travel_fixture_v750 import assign
from scripts.probe_button_prompt_native import BASE, call, machine
from scripts.verify_country_gameplay_v748 import snapshot
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/town_events_v750')
CAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193')


def captures(folder, frames, mode=None):
    path = CAP / folder / 'capture_report.json'
    report = read(path)
    assert report['frames'] == frames and report['cold_boot'] and not report['savestate_loaded']
    assert not report['callback_errors'] and not report['hardware_device_verification']
    assert report['core_DLL_sha256'] == '42160dbfef89adfb3cfd975070a3047d8ad0979cead55607ebdfd3b931046c2b'
    assert sha(Path(report['ROM']).read_bytes()) == report['ROM_sha256']
    fixtures = report.get('synthetic_promoter_travel_fixtures', [])
    assert len(fixtures) == int(mode is not None)
    assert not any(v for k, v in report.items() if k.startswith('synthetic_') and k != 'synthetic_promoter_travel_fixtures')
    if mode:
        donor = report['battery_save_preloaded']
        assert sha(Path(donor['source']).read_bytes()) == donor['source_sha256'] == 'd991cb3bcdf74eed7aeb58c9a75957766b7c820d002423fd2b55cc8493cf8132'
        assert donor['copied_byte_exact_before_cold_boot']
        arm = NdsImage.open(report['ROM']).read_file('/__arm9__.bin')
        raw = snapshot(report, 3200)
        request = {'arrival': True} if mode == 'arrival' else {'product': 14, 'level': 25}
        after, receipt = assign(arm, raw, request)
        assert fixtures[0]['frame'] == 3200 and receipt == {k: v for k, v in fixtures[0].items() if k != 'frame'}
        assert sum(a != b for a, b in zip(raw, after, strict=True)) == (1 if mode == 'arrival' else 4)
        adapter = report['controlled_promoter_travel_harness_adapter']
        assert adapter['original_harness_file_unchanged']
        assert adapter['unchanged_original_harness_sha256'] == sha(Path('scripts/headless_desmume_v193.py').read_bytes())
        assert adapter['adapter_sha256'] == sha(Path('scripts/run_promoter_travel_capture_v750.py').read_bytes())
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


def state_fields(arm, raw):
    cpu = machine(arm)
    cpu.mem_write(BASE, raw)
    call(cpu, 0xCB184, ())
    player = cpu.reg_read(UC_ARM_REG_R0)
    call(cpu, 0xCB178, ())
    state = cpu.reg_read(UC_ARM_REG_R0)
    return {'travel_flag': struct.unpack_from('<I', raw, player + 0x1A4C - BASE)[0] & 4,
        'tracked_city': raw[state + 0x3020 - BASE], 'player_address': player, 'state_address': state}


def main():
    native = read(ROOT / 'native_review.json')
    layouts = {r['message_id']: r['lines'] for r in native['all257_complete_printf_wrap_and_native_font_cases'] if not r['substitutions']}
    observations, reports, control_frames, transitions = [], {}, {}, []
    for mode in ('accept', 'decline', 'arrival'):
        prefix = f'town_v750_{mode}_'
        baseline, before = captures(prefix + 'baseline', 6501, mode)
        report, after = captures(prefix + 'new', 6501, mode)
        assert baseline['scripted_input_schedule'] == report['scripted_input_schedule']
        assert baseline['core_options'] == report['core_options'] and set(before) == set(after)
        assert baseline['synthetic_promoter_travel_fixtures'][0]['changes'] == report['synthetic_promoter_travel_fixtures'][0]['changes']
        selected = {3800: 738, 4000: 738} if mode == 'arrival' else {
            4600: 739, 4800: 739, 5000: 740 if mode == 'accept' else 741, 5200: 740 if mode == 'accept' else 741}
        rom = NdsImage.open(report['ROM'])
        arm, common = rom.read_file('/__arm9__.bin'), rom.read_file('/COMMON/MESFILE.DK4')
        font = GameAsciiFont.from_arm9(arm)
        entries = common_message_entries(common, arm, clean=False)
        blocks = IlnkContainer.parse(common).blocks
        equal = []
        for frame in sorted(after):
            old, new = (Image.open(p).convert('RGB') for p in (before[frame]['path'], after[frame]['path']))
            diff = ImageChops.difference(old, new)
            if frame not in selected:
                assert diff.getbbox() is None, (mode, frame)
                equal.append(frame)
                continue
            i = selected[frame]
            expected = set()
            for row, line in enumerate(layouts[i]):
                for n, char in enumerate(line):
                    glyph = font.decode(char)
                    for y in range(11):
                        for x in range(6):
                            if glyph.getpixel((x, y)):
                                expected.add((22 + n * 6 + x, 296 + row * 16 + y))
            # Entire original228x64 font plane at y296, plus two clear rows above.
            # Question buttons begin below this plane and are compared unchanged.
            body = (16, 294, 244, 360)
            actual = {(x, y) for y in range(body[1], body[3]) for x in range(body[0], body[2]) if new.getpixel((x, y)) == (0, 8, 0)}
            assert actual == expected, (mode, i, frame, len(expected - actual), len(actual - expected))
            diff.paste((0, 0, 0), body)
            assert diff.getbbox() is None, (mode, i, frame)
            block = blocks[entries[i].block]
            raw = snapshot(report, frame)
            at = raw.find(block)
            assert at >= 0 and raw.find(block, at + 1) == -1
            fields = state_fields(arm, raw)
            # Original event setters run after the blocking dialogue returns.
            assert fields['travel_flag'] == (4 if mode == 'arrival' else 0), (mode, frame, fields)
            if mode == 'arrival':
                assert fields['tracked_city'] == 74
            observations.append({'mode': mode, 'message_id': i, 'frame': frame, 'lines': layouts[i],
                'all_glyph_and_blank_plane_pixels_exact': True, 'every_other_pixel_including_question_buttons_exact_baseline': True,
                'native_cache_block': entries[i].block, 'whole_resident_block_bytes_exact': len(block),
                'resident_address': BASE + at, 'actual_original_state_fields': fields, 'capture': after[frame]})
        assert len(equal) == (18 if mode == 'arrival' else 16)
        assert {5400, 5800, 6200, 6400, 6500, 6501} <= set(equal)
        settled_frame = 4200 if mode == 'arrival' else 5400
        fields = state_fields(arm, snapshot(report, settled_frame))
        assert fields['travel_flag'] == (4 if mode == 'accept' else 0), (mode, settled_frame, fields)
        assert fields['tracked_city'] == 22
        transitions.append({'mode': mode, 'frame_after_dialogue_close': settled_frame, 'original_state': fields})
        control_frames[mode] = equal
        for suffix in ('baseline', 'new'):
            path = CAP / (prefix + suffix) / 'capture_report.json'
            reports[str(path)] = sha(path.read_bytes())
    assert len(observations) == 10 and sum(map(len, control_frames.values())) == 50
    game, game_rows = captures('town_v750_newgame', 4000)
    prior, prior_rows = captures('rumors_v749_newgame', 4000)
    assert game['scripted_input_schedule'] == prior['scripted_input_schedule']
    same = sorted(game_rows.keys() & prior_rows.keys())
    assert same == [1, 60, 180, 1200, 2400, 3200, 4000]
    for frame in same:
        assert Image.open(game_rows[frame]['path']).convert('RGB').tobytes() == Image.open(prior_rows[frame]['path']).convert('RGB').tobytes()
    path = CAP / 'town_v750_newgame/capture_report.json'
    reports[str(path)] = sha(path.read_bytes())
    save(ROOT / 'gameplay_verification.json', {'candidate': game['ROM'], 'candidate_sha256': game['ROM_sha256'],
        'six_terminal6501_frame_cold_boots_with_declared_event_fixtures': True,
        'actual_dialogue_observations': observations, 'whole_two_screen_equal_baseline_controls': control_frames,
        'ordinary_New_Game_terminal4000_frame_and7_whole_frame_pairs': same,
        '739_Yes_No_buttons_and_all_non_text_pixels_preserved': True,
        'original_acceptance_sets_flag_refusal_does_not_arrival_clears_flag_and_updates_city': True,
        'actual_state_transitions_after_original_blocking_dialogue_returns': transitions,
        'only1_or4_declared_RAM_data_bytes_changed_by_fixture': True,
        'other7_entries_have_full_source_context_and_native_font_evidence_not_earned_relief_or_live_trend_claim': True,
        'actual_inherited675_676_displays_unchanged': True,
        'no_hardware_whole_route_or_earned_transport_claim': True,
        'reports': reports, 'script_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print('V750:10 complete dialogue holds,50 unchanged controls, original question/flag transitions and7 New Game pairs pass.', flush=True)


if __name__ == '__main__':
    main()
