"""Actual full glyphs, runtime nouns, unchanged controls/models and caption use."""

import struct
from pathlib import Path

from ndspy.code import MainCodeFile
from PIL import Image, ImageChops
from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.native_market_contract_fixture_v758 import assign
from scripts.prepare_product_pitches_v747 import native_layout
from scripts.probe_button_prompt_native import BASE, STACK, call, machine
from scripts.review_market_contract_v758 import ROOT
from scripts.verify_market_gameplay_v753 import SAVE_SHA, snapshot, state
from scripts.verify_market_stock_gameplay_v756 import persistent_models
from scripts.verify_village_wrap_v608 import read, save

CAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193')
ROM = Path('out/all_routes_combined_v758_candidate.nds')
BODY = (16, 294, 244, 366)


def captures(mode, version):
    path = CAP / f'market_contract_v758_{mode}_{version}' / 'capture_report.json'
    d = read(path)
    assert d['cold_boot'] and not d['savestate_loaded'] and not d['callback_errors']
    assert not d['hardware_device_verification'] and not d['goal_complete']
    assert d['core_DLL_sha256'] == '42160dbfef89adfb3cfd975070a3047d8ad0979cead55607ebdfd3b931046c2b'
    assert sha(Path(d['ROM']).read_bytes()) == d['ROM_sha256']
    arm = NdsImage.open(d['ROM']).read_file('/__arm9__.bin')
    if mode != 'newgame':
        donor = d['battery_save_preloaded']
        assert donor['source'] != donor['destination'] and donor['source_sha256'] == SAVE_SHA
        assert donor['copied_byte_exact_before_cold_boot'] and sha(Path(donor['source']).read_bytes()) == SAVE_SHA
    else:
        assert not d.get('battery_save_preloaded')
    fixtures = d.get('synthetic_market_display_fixtures', [])
    assert len(fixtures) == int(mode in ('governor', 'advice'))
    if fixtures:
        _, receipt = assign(arm, snapshot(d, 3200), {'mode': mode})
        assert fixtures[0]['frame'] == 3200 and receipt == {k: v for k, v in fixtures[0].items() if k != 'frame'}
        adapter = d['controlled_market_harness_adapter']
        assert adapter['original_harness_file_unchanged']
        assert adapter['adapter_sha256'] == sha(Path('scripts/run_market_contract_capture_v758.py').read_bytes())
        assert adapter['unchanged_original_harness_sha256'] == sha(Path('scripts/headless_desmume_v193.py').read_bytes())
    rows = {}
    for r in d['frames_captured']:
        assert sha(Path(r['path']).read_bytes()) == r['PNG_sha256']
        rows[r['frame']] = r
    return path, d, rows


def main():
    rom = NdsImage.open(ROM)
    common, arm = rom.read_file('/COMMON/MESFILE.DK4'), rom.read_file('/__arm9__.bin')
    entries = common_message_entries(common, arm, clean=False)
    blocks, font = IlnkContainer.parse(common).blocks, GameAsciiFont.from_arm9(arm)
    cpu = machine(arm)
    cpu.mem_write(0x02387A20, bytes(MainCodeFile(arm, BASE).sections[3].data[:-48]))
    scenes, control, models, reports = [], {}, [], []
    for mode in ('palace', 'governor', 'advice', 'investment'):
        pa, a, before = captures(mode, 757)
        pb, b, after = captures(mode, 758)
        assert a['frames'] == b['frames'] == (6001 if mode == 'advice' else 5600 if mode == 'investment' else 5601)
        assert a['scripted_input_schedule'] == b['scripted_input_schedule'] and a['core_options'] == b['core_options']
        assert set(before) == set(after)
        values, arguments = (), {}
        if mode in ('palace', 'governor'):
            u = machine(arm)
            u.mem_write(BASE, snapshot(b, 4400))
            call(u, 0xB6618, ())
            town = u.reg_read(UC_ARM_REG_R0)
            call(u, 0xB507C, (town, 6))
            flag = u.reg_read(UC_ARM_REG_R0)
            pointer = struct.unpack_from('<I', arm, 0xBA480 if flag else 0xBA47C)[0]
            name = bytes(u.mem_read(pointer, 64)).split(b'\0')[0].decode('ascii')
            assert name == ('Palace' if mode == 'palace' else "Governor's Office")
            number, values = 761, (name,)
            arguments = {'native_town_facility_flag': flag, 'actual_source_literal_pointer': pointer, 'complete_name': name}
        elif mode == 'advice':
            receipt = b['synthetic_market_display_fixtures'][0]
            assert receipt['original_extra_stock_predicate_after'] == 1 and receipt['native_role3_actor'] == 16
            number = receipt['expected_message']
            assert number == 754 and receipt['native_voice_index'] == 1
            arguments = {'native_voice_index': 1, 'native_missing_index_fallback_used': True, 'original_extra_stock_predicate': 1, 'original_ability4_20': 226}
        else:
            number = None
        if number is not None:
            parent = 0x02053DB8 if mode == 'advice' else 0x02054014
            cpu.mem_write(STACK + 0x27C, struct.pack('<I', 0x02118480))
            formatted, lines = native_layout(cpu, entries[number].text, number, values, parent)
            expected = set()
            for row, line in enumerate(lines):
                for col, char in enumerate(line):
                    glyph = font.decode(char)
                    for y in range(11):
                        for x in range(6):
                            if glyph.getpixel((x, y)):
                                expected.add((22 + col * 6 + x, 296 + row * 16 + y))
        control[mode] = []
        for frame, item in after.items():
            x, y = [Image.open(rows[frame]['path']).convert('RGB') for rows in (before, after)]
            difference = ImageChops.difference(x, y)
            if number is not None and frame in (4600, 4800):
                ink = {(i, j) for j in range(BODY[1], BODY[3]) for i in range(BODY[0], BODY[2]) if y.getpixel((i, j)) == (0, 8, 0)}
                assert ink == expected, (mode, frame, len(ink - expected), len(expected - ink))
                prior = {(i, j) for j in range(BODY[1], BODY[3]) for i in range(BODY[0], BODY[2]) if x.getpixel((i, j)) == (0, 8, 0)}
                assert all(x.getpixel((i, j)) == y.getpixel((i, j)) for j in range(BODY[1], BODY[3]) for i in range(BODY[0], BODY[2]) if (i, j) not in expected | prior)
                difference.paste((0, 0, 0), BODY)
                assert difference.getbbox() is None, (mode, frame, difference.getbbox())
                if frame == 4800:
                    raw = snapshot(b, frame)
                    assert raw.count(blocks[entries[number].block]) == 1
                    owner = struct.unpack_from('<I', arm, 0x552A0)[0]
                    assert raw[owner + 0x2030 - BASE:owner + 0x2030 - BASE + len(entries[number].text) + 1] == entries[number].text + b'\0'
                scenes.append({'mode': mode, 'message_id': number, 'arguments': arguments, 'values': values, 'lines': lines,
                    'frame': frame, 'capture': item, 'all_glyphs_blank_cells_and_outside_pixels_exact': True})
            else:
                assert difference.getbbox() is None, (mode, frame, difference.getbbox())
                control[mode].append(frame)
        sampled = []
        for frame in b['exact_requested_capture_frames']:
            ar, br = snapshot(a, frame), snapshot(b, frame)
            assert persistent_models(arm, ar) == persistent_models(arm, br), (mode, frame, 'persistent models')
            assert state(arm, ar) == state(arm, br), (mode, frame, 'town/company state')
            sampled.append({'frame': frame, 'state': state(arm, br), 'whole_company_fleet_ship_models_exact': True})
        models.append({'mode': mode, 'all_sampled_states': sampled})
        reports += [str(pa), str(pb)]
    baseline_path = CAP / 'market_v757_newgame/capture_report.json'
    old = read(baseline_path)
    _, new, rows = captures('newgame', 758)
    before = {r['frame']: r for r in old['frames_captured']}
    assert old['scripted_input_schedule'] == new['scripted_input_schedule'] and set(before) == set(rows)
    assert all(Path(before[f]['path']).read_bytes() == Path(rows[f]['path']).read_bytes() for f in rows)
    for p in ('E:/Rota Nova translations/Saves/hodram-istanbul-golden-cutlass-blue-oak-v474.dsv',
              'E:/Rota Nova translations/Saves/Test fixtures/V751 disposable Istanbul donor.dsv'):
        assert sha(Path(p).read_bytes()) == SAVE_SHA
    save(ROOT / 'gameplay_verification.json', {'candidate': str(ROM), 'candidate_sha256': sha(ROM.read_bytes()),
        'six_actual_full_dialogue_holds': scenes, 'all_other_whole_frame_controls': control,
        'all_sampled_complete_persistent_models_and_town_company_states_equal': models,
        'normal_investment_caption_used_and_all_whole_screens_equal': True,
        'New_Game7_unique_whole_frame_pairs': sorted(rows), 'capture_reports': reports,
        'three_paired_Market_cases_plus_one_investment_pair_and_one_New_Game_cold_boot': True,
        'six_other_advice_variants_source_native_font_not_all_actual_role_activations': True,
        'no_hardware_full_route_earned_fixtures_or_double_stock_purchase_claim': True,
        'source_saves_unchanged_sha256': SAVE_SHA, 'producer_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print('Six full native dialogue holds,all controls/models,Investment caption and New Game pass.', flush=True)


if __name__ == '__main__':
    main()
