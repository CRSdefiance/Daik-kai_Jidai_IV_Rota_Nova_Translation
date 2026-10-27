"""Actual stock offers, removed blank page, preserved state/return and New Game."""

import struct
from pathlib import Path

from ndspy.code import MainCodeFile
from PIL import Image, ImageChops
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import (
    UC_ARM_REG_PC,
    UC_ARM_REG_R0,
    UC_ARM_REG_R1,
    UC_ARM_REG_R2,
    UC_ARM_REG_R3,
    UC_ARM_REG_R7,
    UC_ARM_REG_R8,
    UC_ARM_REG_SP,
)

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.native_market_stock_edge_fixture_v756 import assign as assign_edge
from scripts.native_market_stock_fixture_v756 import assign
from scripts.native_market_stock_seed_fixture_v756 import assign as assign_seed
from scripts.prepare_market_stock_v756 import ROOT
from scripts.prepare_product_pitches_v747 import native_layout
from scripts.probe_button_prompt_native import BASE, STACK, call, machine
from scripts.verify_market_gameplay_v753 import SAVE_SHA, snapshot, state
from scripts.verify_village_wrap_v608 import read, save

CAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193')
ROM = Path('out/all_routes_combined_v756_candidate.nds')
BODY = (16, 294, 244, 366)


def captures(folder, frames, mode=None, reference=None, seeded=False):
    report = read(CAP / folder / 'capture_report.json')
    assert report['frames'] == frames and report['cold_boot'] and not report['savestate_loaded']
    assert not report['callback_errors'] and not report['hardware_device_verification']
    assert report['core_DLL_sha256'] == '42160dbfef89adfb3cfd975070a3047d8ad0979cead55607ebdfd3b931046c2b'
    assert sha(Path(report['ROM']).read_bytes()) == report['ROM_sha256']
    fixtures = report.get('synthetic_market_display_fixtures', [])
    assert len(fixtures) == int(mode is not None) + int(seeded)
    assert not any(v for k, v in report.items() if k.startswith('synthetic_') and k != 'synthetic_market_display_fixtures')
    if mode:
        donor = report['battery_save_preloaded']
        assert donor['source'] != donor['destination'] and donor['copied_byte_exact_before_cold_boot']
        assert sha(Path(donor['source']).read_bytes()) == donor['source_sha256'] == SAVE_SHA
        arm = NdsImage.open(report['ROM']).read_file('/__arm9__.bin')
        _, receipt = (assign_edge if mode == 'edge' else assign)(arm, snapshot(reference or report, 3200), {'mode': mode})
        assert fixtures[0]['frame'] == 3200 and receipt == {k: v for k, v in fixtures[0].items() if k != 'frame'}
        adapter = report['controlled_market_harness_adapter']
        if seeded:
            late = fixtures[1]
            _, seed_receipt = assign_seed(arm, snapshot(report, late['frame']), {'mode': 'rng', 'seed': 3})
            assert seed_receipt == {k: v for k, v in late.items() if k != 'frame'}
            assert late['frame'] == (7600 if 'v754_' in str(report['ROM']) else 7200)
        script = Path('scripts/run_market_stock_seed_capture_v756.py' if seeded else 'scripts/run_market_stock_edge_capture_v756.py' if mode == 'edge' else 'scripts/run_market_stock_capture_v756.py')
        assert adapter['original_harness_file_unchanged'] and adapter['adapter_sha256'] == sha(script.read_bytes())
        assert adapter['unchanged_original_harness_sha256'] == sha(Path('scripts/headless_desmume_v193.py').read_bytes())
    else:
        assert not report.get('battery_save_preloaded')
    rows = {}
    for row in report['frames_captured']:
        assert sha(Path(row['path']).read_bytes()) == row['PNG_sha256']
        rows[row['frame']] = row
    return report, rows


def runtime_arguments(arm, raw, count):
    u = machine(arm)
    u.mem_write(BASE, raw)
    def get(f, args=()):
        call(u, f, args)
        return u.reg_read(UC_ARM_REG_R0)
    town = get(0xB6618)
    pairs = [bytes(u.mem_read(get(0xB30EC, (town, i)), 2)) for i in (0, 1)]
    # Original BB874..BB89C assigns pair0 to sb, pair1 to stack+1C;
    # BB91C..BB958 assigns pair1's matching sale to r7, pair0's to r8.
    first, second = pairs[1][0], pairs[0][0]
    assert sum(p[0] != 125 for p in pairs) == count
    only = next(p[0] for p in pairs if p[0] != 125)
    u.mem_write(STACK + 0x10, bytes(4))
    u.mem_write(STACK + 0x28, struct.pack('<I', only))
    u.reg_write(UC_ARM_REG_SP, STACK)
    u.reg_write(UC_ARM_REG_R7, first)
    u.reg_write(UC_ARM_REG_R8, second)
    events = []
    def stop(cpu, address, size, unused):
        if address == BASE + 0x53FE4:
            n = cpu.reg_read(UC_ARM_REG_R1)
            values = []
            for reg in (UC_ARM_REG_R2, UC_ARM_REG_R3)[:count]:
                p = cpu.reg_read(reg)
                values.append(bytes(cpu.mem_read(p, 80)).split(b'\0')[0].decode('ascii'))
            events.append((n, values))
            cpu.emu_stop()
    handle = u.hook_add(UC_HOOK_CODE, stop)
    try:
        u.emu_start(BASE + (0xBBB10 if count == 2 else 0xBBBB4), 0x027E0000, count=10000)
    finally:
        u.hook_del(handle)
    assert u.reg_read(UC_ARM_REG_PC) == BASE + 0x53FE4 and len(events) == 1
    assert events[0][0] == (767 if count == 2 else 768)
    return events[0][1], {'actual_runtime_town_pairs': [p.hex() for p in pairs],
        'original_source_argument_prefix_with_real_product_root_and_virtual_getters': events[0],
        'supplied_trade_flag0_and_original_town_pair_order_no_portrait_execution_claim': True}


def persistent_models(arm, raw):
    u = machine(arm)
    u.mem_write(BASE, raw)
    def get(f, args=()):
        call(u, f, args)
        return u.reg_read(UC_ARM_REG_R0)
    company = get(0xCB160) + 4 + 2 * 0x4C
    fleet = get(0xCB1A8) + 0x88
    ship = get(0x36C94, (fleet + 12,))
    return {k: bytes(u.mem_read(p, n)) for k, p, n in (
        ('company', company, 76), ('fleet', fleet, 132), ('ship', ship, 140))}


def main():
    rom = NdsImage.open(ROM)
    arm, common = rom.read_file('/__arm9__.bin'), rom.read_file('/COMMON/MESFILE.DK4')
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    assert all(arm[a:b] == clean[a:b] for a, b in ((0xBB874, 0xBB89C), (0xBB91C, 0xBB95C)))
    entries = common_message_entries(common, arm, clean=False)
    blocks, font = IlnkContainer.parse(common).blocks, GameAsciiFont.from_arm9(arm)
    cpu = machine(arm)
    cpu.mem_write(0x02387A20, bytes(MainCodeFile(arm, BASE).sections[3].data[:-48]))
    checks, controls, timing, states, reports, randomized_hud = [], {}, [], [], [], []
    for mode in ('one', 'two', 'edge'):
        old, before = captures(f'market_v756_{mode}_754', 7801, mode)
        new, after = captures(f'market_v756_{mode}_756', 7801, mode)
        assert old['scripted_input_schedule'] == new['scripted_input_schedule'] and old['core_options'] == new['core_options']
        assert set(before) == set(after)
        number = 768 if mode == 'one' else 767
        values, arguments = runtime_arguments(arm, snapshot(new, 5200), 1 if mode == 'one' else 2)
        formatted, lines = native_layout(cpu, entries[number].text, number, values)
        expected = set()
        for row, line in enumerate(lines):
            for col, char in enumerate(line):
                glyph = font.decode(char)
                for y in range(11):
                    for x in range(6):
                        if glyph.getpixel((x, y)):
                            expected.add((22 + col * 6 + x, 296 + row * 16 + y))
        controls[mode] = []
        phase_report, phase_rows = (None, {})
        if mode == 'one':
            phase_report, phase_rows = captures('market_v756_one_754_phase_controls', 8481, mode, old)
            assert phase_report['scripted_input_schedule'][:len(old['scripted_input_schedule'])] == old['scripted_input_schedule']
            assert phase_report['core_options'] == old['core_options']
            for f in (3200, 5600, 6000, 6400, 6800, 7000, 7200):
                assert Path(phase_rows[f]['path']).read_bytes() == Path(before[f]['path']).read_bytes()
        for frame in sorted(after):
            a, b = (Image.open(rows[frame]['path']).convert('RGB') for rows in (before, after))
            diff = ImageChops.difference(a, b)
            if frame in (5800, 6000):
                ink = {(x, y) for y in range(BODY[1], BODY[3]) for x in range(BODY[0], BODY[2]) if b.getpixel((x, y)) == (0, 8, 0)}
                assert ink == expected, (mode, frame, len(ink - expected), len(expected - ink))
                old_ink = {(x, y) for y in range(BODY[1], BODY[3]) for x in range(BODY[0], BODY[2]) if a.getpixel((x, y)) == (0, 8, 0)}
                assert all(a.getpixel((x, y)) == b.getpixel((x, y))
                    for y in range(BODY[1], BODY[3]) for x in range(BODY[0], BODY[2]) if (x, y) not in expected | old_ink)
                diff.paste((0, 0, 0), BODY)
                assert diff.getbbox() is None, (mode, frame, diff.getbbox())
                if frame == 6000:
                    raw = snapshot(new, frame)
                    assert raw.count(blocks[entries[number].block]) == 1
                    owner = struct.unpack_from('<I', arm, 0x552A0)[0]
                    assert raw[owner + 0x2030 - BASE:owner + 0x2030 - BASE + len(entries[number].text) + 1] == entries[number].text + b'\0'
                checks.append({'scenario': mode, 'frame': frame, 'message_id': number,
                    'values': values, 'lines': lines, 'formatted_hex': formatted.hex(), 'arguments': arguments,
                    'capture': after[frame], 'every_glyph_blank_paper_cell_and_outside_pixel_exact': True})
            elif mode != 'one' or frame <= 5600:
                assert diff.getbbox() is None, (mode, frame, diff.getbbox())
                controls[mode].append(frame)
            else:
                # The old768 requires an extra A on a blank page. Match whole
                # later frames at their actual scene/blink phase, never mask UI.
                choices = [(f, row, 'original') for f, row in before.items() if f >= 6000]
                choices += [(f, row, 'phase-control') for f, row in phase_rows.items() if f >= 6000]
                matches = [(f, tag, row) for f, row, tag in choices if Path(row['path']).read_bytes() == Path(after[frame]['path']).read_bytes()]
                if matches:
                    f, tag, row = matches[0]
                    timing.append({'current_frame': frame, 'baseline_frame': f, 'baseline_capture': tag,
                        'whole_two_screen_image_exact_at_same_scene_and_indicator_phase': True})
                else:
                    # A different random result is real model data, not an
                    # indicator animation. Do not call this a whole-image match.
                    # Original return code subtracts2+rand(5) from fleet+3D;
                    # the separate same-seed pair below proves identical rules.
                    candidates = []
                    for f, row, tag in choices:
                        if f < 7800:
                            continue
                        d = ImageChops.difference(Image.open(row['path']).convert('RGB'), b).getbbox()
                        if d and 170 <= d[0] < d[2] <= 182 and 352 <= d[1] < d[3] <= 363:
                            candidates.append((f, tag, d))
                    assert candidates, (mode, frame, diff.getbbox())
                    f, tag, d = candidates[0]
                    randomized_hud.append({'current_frame': frame, 'baseline_frame': f, 'baseline_capture': tag,
                        'all_other_pixels_at_the_same_scene_exact': True, 'changed_numeral_bounds': d,
                        'whole_image_equality_not_claimed': True, 'original_random_fleet_field3D': {'baseline': 18, 'candidate': 22}})
        observed = []
        for report in (old, new):
            observations = {}
            for f in (3200, 5200, 5600, 6000, 6400, 6800, 7400, 7800):
                raw = snapshot(report, f)
                value = state(arm, raw)
                u = machine(arm)
                u.mem_write(BASE, raw)
                call(u, 0xCB1A8, ())
                root = u.reg_read(UC_ARM_REG_R0)
                call(u, 0x36180, (root + 0x88, 0x02440000))
                value['cargo_holds'] = u.reg_read(UC_ARM_REG_R0)
                observations[str(f)] = value
            observed.append(observations)
        assert observed[0] == observed[1]
        assert observed[1]['5200']['cash'] == 8371 and observed[1]['5200']['cargo_holds'] == 2
        assert observed[1]['5200']['share'] == 1 and observed[1]['7800']['share'] == 2
        assert observed[1]['6000']['cargo_holds'] == observed[1]['7800']['cargo_holds'] == 0
        assert observed[1]['7800']['cash'] == {'one': 30187, 'two': 30679, 'edge': 12390}[mode]
        states.append({'scenario': mode, 'all_eight_state_samples_equal_baseline': observed[1]})
        if mode == 'one':
            empty = Image.open(before[6400]['path']).convert('RGB')
            assert not any(empty.getpixel((x, y)) == (0, 8, 0) for y in range(294, 358) for x in range(16, 244))
            old_arm = NdsImage.open(old['ROM']).read_file('/__arm9__.bin')
            old_rom = NdsImage.open(old['ROM'])
            old_entry = common_message_entries(old_rom.read_file('/COMMON/MESFILE.DK4'), old_arm, clean=False)[768]
            owner = struct.unpack_from('<I', old_arm, 0x552A0)[0]
            raw = snapshot(old, 6400)
            assert raw[owner + 0x2030 - BASE:owner + 0x2030 - BASE + len(old_entry.text)] == old_entry.text
            assert b'\n \n \n' in old_entry.text
        reports.extend([str(CAP / f'market_v756_{mode}_{v}' / 'capture_report.json') for v in (754, 756)])
    game, game_rows = captures('market_v756_newgame', 4000)
    baseline, baseline_rows = captures('category_v754_newgame', 4000)
    assert game['scripted_input_schedule'] == baseline['scripted_input_schedule'] and set(game_rows) == set(baseline_rows)
    assert all(Path(game_rows[f]['path']).read_bytes() == Path(baseline_rows[f]['path']).read_bytes() for f in game_rows)
    seeded_old, seed_old_rows = captures('market_v756_one_seed3_754', 8481, 'one', seeded=True)
    seeded_new, seed_new_rows = captures('market_v756_one_seed3_756', 8481, 'one', seeded=True)
    old_models = persistent_models(arm, snapshot(seeded_old, 8400))
    new_models = persistent_models(arm, snapshot(seeded_new, 8400))
    assert old_models == new_models and new_models['fleet'][0x3D] == 20
    assert seeded_old['synthetic_market_display_fixtures'][1]['SDK_seed3_first_native_rand5'] == 2
    assert seeded_new['synthetic_market_display_fixtures'][1]['SDK_seed3_first_native_rand5'] == 2
    natural_old = read(CAP / 'market_v756_one_754_extra_page_control/capture_report.json')
    natural_new = read(CAP / 'market_v756_one_756/capture_report.json')
    a, b = persistent_models(arm, snapshot(natural_old, 8400)), persistent_models(arm, snapshot(natural_new, 7800))
    assert a['company'] == b['company'] and a['ship'] == b['ship']
    assert [(i, x, y) for i, (x, y) in enumerate(zip(a['fleet'], b['fleet'], strict=True)) if x != y] == [(0x3D, 18, 22)]
    seed_controls = []
    for frame in (7400, 7600, 7800, 8000, 8200, 8400, 8481):
        matches = [f for f, row in seed_old_rows.items() if f >= 7800 and Path(row['path']).read_bytes() == Path(seed_new_rows[frame]['path']).read_bytes()]
        assert matches, frame
        seed_controls.append({'candidate_frame': frame, 'baseline_frame': matches[0], 'whole_image_exact': True})
    for lo, hi in ((0x2FDA0, 0x2FDC4), (0x34540, 0x34564), (0x519D4, 0x51A28), (0xD9824, 0xD9870)):
        assert arm[lo:hi] == clean[lo:hi]
    assert sha(Path('E:/Rota Nova translations/Saves/hodram-istanbul-golden-cutlass-blue-oak-v474.dsv').read_bytes()) == SAVE_SHA
    assert sha(Path('E:/Rota Nova translations/Saves/Test fixtures/V751 disposable Istanbul donor.dsv').read_bytes()) == SAVE_SHA
    save(ROOT / 'gameplay_verification.json', {'candidate': str(ROM), 'candidate_sha256': game['ROM_sha256'],
        'six_terminal7801_frame_paired_original_trade_runs': True, 'bounded6_or8_byte_cargo_share_and_demand_fixtures': True,
        'actual_complete_stock_holds': checks, 'same_frame_whole_screen_controls': controls,
        'intentional_old768_blank_page_removed_and_later_whole_scene_phase_controls': timing,
        'natural_one_product_return_only_original_randomized_HUD_numeral_differs': randomized_hud,
        'same_seed3_original_return_cost_and_complete_models_match': {
            'whole_company76_fleet132_ship140_bytes_equal': True, 'full_scene_controls': seed_controls,
            'source_cost_and_RNG_code_exact_to_clean': True,
            'natural_old18_new22_are_original_rand5_results4_and0_not_blink_phase': True,
            'reports': [str(CAP / f'market_v756_one_seed3_{v}/capture_report.json') for v in (754, 756)]},
        'original_money_cargo_share_state_samples': states, 'ordinary_New_Game7_unique_whole_frame_pairs': sorted(game_rows),
        'capture_reports': reports, 'phase_control_report': str(CAP / 'market_v756_one_754_phase_controls/capture_report.json'),
        'source_saves_unchanged_sha256': SAVE_SHA,
        'other15_entries_native_source_font_coverage_not_all_actual_reward_activations': True,
        'no_hardware_full_route_or_earned_fixture_state_claim': True,
        'producer_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print('Six complete stock holds,original sale state/return,blank-page repair and New Game pass.', flush=True)


if __name__ == '__main__':
    main()
