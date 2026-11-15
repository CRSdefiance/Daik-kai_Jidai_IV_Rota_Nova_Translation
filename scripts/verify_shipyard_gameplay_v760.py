"""Bound actual Yard framebuffer glyphs, arguments, states and cold-boot controls."""

import re
import runpy
import struct
from pathlib import Path

from PIL import Image, ImageChops
from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.dialogue.font_audit import GameAsciiFont, SJIS_GLYPH_COUNT, SJIS_MAP_OFFSET, decode_glyph
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.probe_button_prompt_native import BASE, call, machine
from scripts.probe_shipyard_runtime_v759 import layout
from scripts.verify_common_alignment_native_v257 import raster
from scripts.verify_market_gameplay_v753 import SAVE_SHA, snapshot, state
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/shipyard_storage_v760')
CAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193')
ROM = Path('out/all_routes_combined_v760_candidate.nds')
FULL_SAVE_SHA = 'febc859c5af2df6fa8023c349bb7f31b5fc15ea769fb2eea527b3a3f80521731'
BODY = (16, 294, 244, 366)


def cstring(raw, address):
    assert BASE <= address < BASE + len(raw) - 256
    return raw[address - BASE:address - BASE + 256].split(b'\0')[0]


def capture(folder, request=None):
    path = CAP / folder / 'capture_report.json'
    d = read(path)
    assert d['cold_boot'] and not d['savestate_loaded'] and not d['callback_errors']
    assert not d['hardware_device_verification'] and not d['goal_complete']
    assert d['core_DLL_sha256'] == '42160dbfef89adfb3cfd975070a3047d8ad0979cead55607ebdfd3b931046c2b'
    assert sha(Path(d['ROM']).read_bytes()) == d['ROM_sha256']
    arm = NdsImage.open(d['ROM']).read_file('/__arm9__.bin')
    donor = d.get('battery_save_preloaded')
    if donor:
        assert donor['source'] != donor['destination'] and donor['copied_byte_exact_before_cold_boot']
        assert sha(Path(donor['source']).read_bytes()) == donor['source_sha256']
        assert donor['source_sha256'] in (SAVE_SHA, FULL_SAVE_SHA)
    fixtures = d.get('synthetic_shipyard_repair_fixtures', [])
    assert len(fixtures) == int(request is not None)
    assert not any(v for k, v in d.items() if k.startswith('synthetic_') and k != 'synthetic_shipyard_repair_fixtures')
    if fixtures:
        producers = [Path('scripts/native_shipyard_fixture_v760.py'), *ROOT.glob('*fixture*RESEARCH.py')]
        producer = next(p for p in producers if sha(p.read_bytes()) == fixtures[0]['fixture_source_sha256'])
        _, receipt = runpy.run_path(str(producer))['assign'](arm, snapshot(d, 3200), request)
        assert fixtures[0]['frame'] == 3200 and receipt == {k: v for k, v in fixtures[0].items() if k != 'frame'}
        adapter = d['controlled_shipyard_harness_adapter']
        assert adapter['original_harness_file_unchanged']
        assert adapter['adapter_sha256'] == sha(Path('scripts/run_shipyard_capture_v760.py').read_bytes())
        assert adapter['unchanged_original_harness_sha256'] == sha(Path('scripts/headless_desmume_v193.py').read_bytes())
    rows = {}
    for row in d['frames_captured']:
        assert sha(Path(row['path']).read_bytes()) == row['PNG_sha256']
        rows[row['frame']] = row
    return path, d, arm, rows


def models(arm, raw):
    u = machine(arm)
    u.mem_write(BASE, raw)
    def get(fn, args=()):
        call(u, fn, args)
        return u.reg_read(UC_ARM_REG_R0)
    root = get(0xCB160)
    company = root + 4 + get(0x397D8, (root,)) * 0x4C
    fleet = get(0xCB1A8) + 4 + get(0x2E58C) * 0x84
    ship_root = get(0xCB148)
    ids = [u.mem_read(fleet + 0x10 + i * 8, 1)[0] for i in range(5)]
    result = {'company': sha(bytes(u.mem_read(company, 0x4C))), 'fleet': sha(bytes(u.mem_read(fleet, 0x84)))}
    for index in ids:
        if index != 155:
            result[f'ship_{index}'] = sha(bytes(u.mem_read(ship_root + 4 + index * 0x8C, 0x8C)))
    return result


def independent_font(arm, kanji, lines):
    font = GameAsciiFont.from_arm9(arm)
    mapping = struct.unpack_from(f'<{SJIS_GLYPH_COUNT}H', arm, SJIS_MAP_OFFSET)
    expected = bytearray(228 * 64)
    for row, line in enumerate(lines):
        x = 6
        for char in line:
            code = char.encode('cp932')
            glyph = font.decode(char) if len(code) == 1 else decode_glyph(kanji, mapping.index(int.from_bytes(code, 'big')))
            if len(code) == 2:
                for y in range(11):
                    for dx in range(glyph.width):
                        if glyph.getpixel((dx, y)):
                            expected[(row * 16 + y + 1) * 228 + x + dx + 1] = 15
            for y in range(11):
                for dx in range(glyph.width):
                    if glyph.getpixel((dx, y)):
                        expected[(row * 16 + y) * 228 + x + dx] = 1
            x += 6 * len(code)
        assert x <= 228 and row < 4
    return bytes(expected)


def main():
    rom = NdsImage.open(ROM)
    arm, common = rom.read_file('/__arm9__.bin'), rom.read_file('/COMMON/MESFILE.DK4')
    entries = common_message_entries(common, arm, clean=False)
    blocks = IlnkContainer.parse(common).blocks
    kanji = rom.read_file('/GRP/KANJI.FNT')
    assert kanji == NdsImage.open('out/all_routes_combined_v255_candidate.nds').read_file('/GRP/KANJI.FNT')
    raw_pointer, wrapped_pointer, owner = [struct.unpack_from('<I', arm, off)[0] for off in (0x5444C, 0x54450, 0x552A0)]
    patches = read(ROOT / 'registered_verification.json')['proof']['owned_runtime']['patches']
    scenes, controls, sampled_models, reports = [], {}, [], []
    cases = [
        ('sell_quote', None, {4600: 788, 4800: 788, 5400: 789, 5600: 789, 5800: 788, 6000: 788}),
        ('repair_applied', {'mode': 'repair_helper'}, {3800: 802, 4200: 802, 4600: 791, 4800: 791, 5000: 798, 5200: 798, 5400: 801, 5600: 801}),
        ('copy_funded_FALCON', {'mode': 'copy_name', 'name': 'FALCON'}, {5400: 785, 6200: 803, 6400: 803}),
        ('copy_preparation_0', {'mode': 'copy_name', 'name': 'FALCON', 'preparation': 0}, {5400: 785, 6200: 804, 6400: 804}),
        ('copy_preparation_1', {'mode': 'copy_name', 'name': 'ICARUS', 'preparation': 1}, {5400: 785, 6200: 803, 6400: 803}),
        ('repair_pair', {'mode': 'repair_pair'}, {3800: 802, 4600: 801, 4800: 801}),
        ('repair_pair_no_funds', {'mode': 'repair_pair_no_funds'}, {5000: 799, 5200: 799}),
        ('repair_menu_quote', {'mode': 'repair_pair'}, {3800: 802, 5400: 800, 5600: 800}),
    ]
    for mode, request, selected in cases:
        pa, a, old_arm, before = capture(f'shipyard_v760_{mode}_758', request)
        pb, b, _, after = capture(f'shipyard_v760_{mode}_760', request)
        assert a['frames'] == b['frames'] and set(before) == set(after)
        assert a['scripted_input_schedule'] == b['scripted_input_schedule'] and a['core_options'] == b['core_options']
        controls[mode] = []
        for frame, row in after.items():
            x, y = [Image.open(rows[frame]['path']).convert('RGB') for rows in (before, after)]
            difference = ImageChops.difference(x, y)
            if frame in selected:
                n = selected[frame]
                raw = snapshot(b, frame)
                template = entries[n].text
                assert cstring(raw, owner + 0x2030) == template
                assert raw.count(blocks[entries[n].block]) == 1
                printf = cstring(raw, raw_pointer)
                match = re.fullmatch(b'(.*?)'.join(re.escape(p) for p in template.split(b'%s')), printf)
                assert match, (mode, frame, n, printf)
                args = match.groups()
                cpu = machine(arm)
                cpu.mem_write(BASE, raw)
                native = layout(cpu, template, n, args)
                formatted = bytes.fromhex(native['formatted_hex'])
                assert formatted == cstring(raw, wrapped_pointer)
                assert not native['findings'], (mode, frame, native)
                plane = raster(arm, formatted, 0x01FFCE40 - BASE, size=(228, 64), instruction_limit=1000000)
                assert plane == independent_font(arm, kanji, native['lines'])
                expected = {(16 + i % 228, 296 + i // 228) for i, value in enumerate(plane) if value == 1}
                actual = {(i, j) for j in range(BODY[1], BODY[3]) for i in range(BODY[0], BODY[2]) if y.getpixel((i, j)) == (0, 8, 0)}
                assert actual == expected, (mode, frame, n, len(actual - expected), len(expected - actual))
                prior = {(i, j) for j in range(BODY[1], BODY[3]) for i in range(BODY[0], BODY[2]) if x.getpixel((i, j)) == (0, 8, 0)}
                shadow = {(i + 1, j + 1) for i, j in actual | prior}
                assert all(x.getpixel((i, j)) == y.getpixel((i, j)) for j in range(BODY[1], BODY[3]) for i in range(BODY[0], BODY[2]) if (i, j) not in actual | prior | shadow)
                difference.paste((0, 0, 0), BODY)
                assert difference.getbbox() is None, (mode, frame, difference.getbbox())
                scenes.append({'mode': mode, 'frame': frame, 'message_id': n, 'arguments': [v.decode('cp932') for v in args],
                    'lines': native['lines'], 'capture': row, 'printf_copy_block_and_native_wrapped_bytes_exact': True,
                    'independent_full_ASCII_KANJI_font_plane_and_all_visible_foreground_pixels_exact': True,
                    'all_outside_body_pixels_and_untouched_paper_cells_exact': True})
            else:
                assert difference.getbbox() is None, (mode, frame, difference.getbbox())
                controls[mode].append(frame)
        states = []
        for frame in b['exact_requested_capture_frames']:
            ar, br = snapshot(a, frame), snapshot(b, frame)
            assert models(old_arm, ar) == models(arm, br), (mode, frame, 'models')
            assert state(old_arm, ar) == state(arm, br), (mode, frame, 'state')
            for patch in patches:
                at, data = patch['address'], bytes.fromhex(patch['target_hex'])
                if BASE <= at < BASE + 0x400000:
                    assert br[at - BASE:at - BASE + len(data)] == data, (mode, frame, hex(at))
            states.append({'frame': frame, 'state': state(arm, br), 'active_company_fleet_and_all_member_ship_models': models(arm, br)})
        sampled_models.append({'mode': mode, 'paired_native_models_and_town_company_states_exact': states})
        reports += [str(pa), str(pb)]
    # V758 actual New Game is the immediate-parent checkpoint. Keep its original
    # schedule and exact capture frames, rather than retiming the new ROM.
    old_path = CAP / 'market_contract_v758_newgame_758/capture_report.json'
    a = read(old_path); before = {r['frame']: r for r in a['frames_captured']}
    assert a['ROM_sha256'] == '40acbf6bd11d40a99186d078c4671470e4ef1129515a854f67e6c4c09115c302'
    pb, b, _, after = capture('shipyard_v760_newgame_exact_760')
    assert not b.get('battery_save_preloaded') and a['scripted_input_schedule'] == b['scripted_input_schedule']
    assert set(before) == set(after) == {1, 60, 180, 1600, 2000, 3200, 4000}
    assert all(Path(before[f]['path']).read_bytes() == Path(after[f]['path']).read_bytes() for f in after)
    reports += [str(old_path), str(pb)]
    assert {r['message_id'] for r in scenes} == {785, 788, 789, 791, 798, 799, 800, 801, 802, 803, 804}
    assert any(r['message_id'] == 803 and r['arguments'][-1] == '１ day' and r['arguments'][0] == 'ICARUS' for r in scenes)
    assert any(r['message_id'] == 804 and r['arguments'][0] == 'FALCON' for r in scenes)
    for p in ('E:/Rota Nova translations/Saves/hodram-istanbul-golden-cutlass-blue-oak-v474.dsv',
              'E:/Rota Nova translations/Saves/Test fixtures/V751 disposable Istanbul donor.dsv'):
        assert sha(Path(p).read_bytes()) == SAVE_SHA
    save(ROOT / 'gameplay_verification.json', {'candidate': str(ROM), 'candidate_sha256': sha(ROM.read_bytes()),
        'actual_complete_dialogue_holds': scenes, 'all_other_whole_frame_controls': controls,
        'sampled_native_models_states_and_loaded_main_RAM_patches': sampled_models,
        'New_Game7_unique_whole_frame_pairs': sorted(after), 'capture_reports': reports,
        'all_other_variants_source_native_font_not_all_actual_activations': True,
        'targeted_automated_cold_boot_emulator_tests_not_hardware_or_complete_playthrough': True,
        'no_earned_fixture_wealth_damage_design_qualification_or_purchase_claim': True,
        'donor_saves_rehashed_unchanged': True, 'producer_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print(f'{len(scenes)} actual full glyph holds, {sum(map(len, controls.values()))} whole-frame controls, all paired sampled models and seven New Game frames pass.', flush=True)


if __name__ == '__main__':
    main()
