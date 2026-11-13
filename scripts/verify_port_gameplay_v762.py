"""Actual service-dialogue glyphs, original state/returns and New Game controls."""

import re
import runpy
import struct
from pathlib import Path

from PIL import Image, ImageChops

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.prepare_port_release_v762 import MANUSCRIPT, ROOT
from scripts.probe_button_prompt_native import BASE, machine
import scripts.probe_shipyard_runtime_v759 as formatter
from scripts.verify_common_alignment_native_v257 import raster
from scripts.verify_market_gameplay_v753 import SAVE_SHA, snapshot, state
from scripts.verify_shipyard_gameplay_v760 import FULL_SAVE_SHA, independent_font, models
from scripts.verify_village_wrap_v608 import read, save

CAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193')
ROM = Path('out/all_routes_combined_v762_candidate.nds')
BODY = (16, 294, 244, 366)


def cstring(raw, at):
    assert BASE <= at < BASE + len(raw) - 256
    return raw[at - BASE:at - BASE + 256].split(b'\0')[0]


def capture(folder, fixture=None):
    path = CAP / folder / 'capture_report.json'; d = read(path)
    assert d['cold_boot'] and not d['savestate_loaded'] and not d['callback_errors']
    assert not d['hardware_device_verification'] and not d['goal_complete']
    assert d['core_DLL_sha256'] == '42160dbfef89adfb3cfd975070a3047d8ad0979cead55607ebdfd3b931046c2b'
    assert d['ROM_sha256'] == sha(Path(d['ROM']).read_bytes())
    arm = NdsImage.open(d['ROM']).read_file('/__arm9__.bin')
    donor = d.get('battery_save_preloaded')
    if donor:
        assert donor['source'] != donor['destination'] and donor['copied_byte_exact_before_cold_boot']
        assert sha(Path(donor['source']).read_bytes()) == donor['source_sha256']
        assert donor['source_sha256'] in (SAVE_SHA, FULL_SAVE_SHA)
    fixtures = d.get('synthetic_port_service_fixtures', [])
    assert len(fixtures) == int(fixture is not None)
    assert not any(v for k, v in d.items() if k.startswith('synthetic_') and k != 'synthetic_port_service_fixtures')
    if fixture:
        originals = [Path('scripts/native_port_fixture_v762.py'), ROOT / 'no_money_fixture_producer_RESEARCH.py']
        producer = next(p for p in originals if sha(p.read_bytes()) == fixtures[0]['fixture_source_sha256'])
        _, receipt = runpy.run_path(str(producer))['assign'](arm, snapshot(d, 3200), {'mode': fixture})
        assert fixtures[0]['frame'] == 3200 and receipt == {k: v for k, v in fixtures[0].items() if k != 'frame'}
        adapter = d['controlled_port_service_harness_adapter']
        assert adapter['original_harness_file_unchanged']
        assert adapter['unchanged_original_harness_sha256'] == sha(Path('scripts/headless_desmume_v193.py').read_bytes())
        assert adapter['adapter_sha256'] in [sha(p.read_bytes()) for p in (Path('scripts/run_port_capture_v762.py'), ROOT / 'no_money_capture_adapter_RESEARCH.py')]
    rows = {}
    for r in d['frames_captured']:
        assert sha(Path(r['path']).read_bytes()) == r['PNG_sha256']; rows[r['frame']] = r
    return path, d, arm, rows


def main():
    rom = NdsImage.open(ROM); arm, common = rom.read_file('/__arm9__.bin'), rom.read_file('/COMMON/MESFILE.DK4')
    entries = common_message_entries(common, arm, clean=False); blocks = IlnkContainer.parse(common).blocks
    kanji = rom.read_file('/GRP/KANJI.FNT'); font = GameAsciiFont.from_arm9(arm)
    formatter.YESNO = (*formatter.YESNO, 806, 812, 813, 816, 817, 1246)
    raw_pointer, wrapped_pointer, owner = [struct.unpack_from('<I', arm, off)[0] for off in (0x5444C, 0x54450, 0x552A0)]
    patches = read(ROOT / 'runtime_plan.json')['patches']
    scenes, controls, states, reports = [], {}, [], []
    cases = [
        ('sell', 'shipyard_v760_sell_760', None, {4600: 267}),
        ('copy_no_funds', 'port_services_v762_copy_no_funds_760', None, {6200: 1245, 6400: 1245}),
        ('tavern_no_money', 'port_services_v762_tavern_no_money_760', 'no_money', {4600: 819, 5800: 819}),
        ('tavern_round_no_money', 'port_services_v762_tavern_round_no_money_760', 'no_money', {6200: 819}),
        ('water_only', 'port_services_v762_water_only_760', 'water_only', {3400: 813, 3800: 806}),
    ]
    for mode, before_folder, fixture, selected in cases:
        pa, a, old_arm, before = capture(before_folder, fixture)
        pb, b, _, after = capture(f'port_services_v762_{mode}_762', fixture)
        assert a['scripted_input_schedule'] == b['scripted_input_schedule'] and a['core_options'] == b['core_options']
        assert a['frames'] == b['frames'] and set(before) == set(after)
        controls[mode] = []
        for frame, row in after.items():
            x, y = [Image.open(rows[frame]['path']).convert('RGB') for rows in (before, after)]
            difference = ImageChops.difference(x, y)
            if frame in selected:
                n = selected[frame]; template = entries[n].text; raw = snapshot(b, frame)
                assert cstring(raw, owner + 0x2030) == template and raw.count(blocks[entries[n].block]) == 1
                if n == 267:
                    wrapped, lines, values = template, [template.decode('ascii')], ()
                    plane = raster(arm, wrapped, 0xD5404, size=(240, 64))
                    expected_plane = bytearray(240 * 64)
                    for col, char in enumerate(lines[0]):
                        glyph = font.decode(char)
                        for gy in range(11):
                            for gx in range(6):
                                if glyph.getpixel((gx, gy)): expected_plane[gy * 240 + col * 6 + gx] = 1
                    assert plane == bytes(expected_plane); width = 240
                else:
                    printf = cstring(raw, raw_pointer)
                    match = re.fullmatch(b'(.*?)'.join(re.escape(p) for p in template.split(b'%s')), printf)
                    assert match, (mode, frame, n, printf)
                    values = match.groups(); cpu = machine(arm); cpu.mem_write(BASE, raw)
                    native = formatter.layout(cpu, template, n, values)
                    assert not native['findings']
                    wrapped, lines = bytes.fromhex(native['formatted_hex']), native['lines']
                    assert cstring(raw, wrapped_pointer) == wrapped
                    plane = raster(arm, wrapped, 0x01FFCE40 - BASE, size=(228, 64), instruction_limit=1000000)
                    assert plane == independent_font(arm, kanji, lines); width = 228
                expected = {(16 + i % width, 296 + i // width) for i, value in enumerate(plane) if value == 1}
                actual = {(i, j) for j in range(BODY[1], BODY[3]) for i in range(BODY[0], BODY[2]) if y.getpixel((i, j)) == (0, 8, 0)}
                assert actual == expected, (mode, frame, n, len(actual - expected), len(expected - actual))
                prior = {(i, j) for j in range(BODY[1], BODY[3]) for i in range(BODY[0], BODY[2]) if x.getpixel((i, j)) == (0, 8, 0)}
                shadows = {(i + 1, j + 1) for i, j in actual | prior}
                assert all(x.getpixel((i, j)) == y.getpixel((i, j)) for j in range(BODY[1], BODY[3]) for i in range(BODY[0], BODY[2]) if (i, j) not in actual | prior | shadows)
                difference.paste((0, 0, 0), BODY)
                assert difference.getbbox() is None, (mode, frame, difference.getbbox())
                scenes.append({'mode': mode, 'frame': frame, 'message_id': n, 'arguments': [v.decode('cp932') for v in values],
                    'lines': lines, 'capture': row, 'full_independent_font_plane_and_every_actual_foreground_glyph_equal': True,
                    'full_resident_COMMON_copy_and_outside_body_pixels_exact': True})
            else:
                assert difference.getbbox() is None, (mode, frame, difference.getbbox())
                controls[mode].append(frame)
        sampled = []
        for frame in b['exact_requested_capture_frames']:
            if frame < 3200: continue
            ar, br = snapshot(a, frame), snapshot(b, frame)
            assert models(old_arm, ar) == models(arm, br), (mode, frame, 'models')
            assert state(old_arm, ar) == state(arm, br), (mode, frame, 'state')
            for p in patches:
                at, data = p['address'], bytes.fromhex(p['target_hex'])
                assert br[at - BASE:at - BASE + len(data)] == data
            values = state(arm, br)
            expected_cash = 8371 if mode == 'copy_no_funds' or mode == 'sell' else 25975 if mode == 'water_only' or frame == 3200 else 0
            assert values['cash'] == expected_cash, (mode, frame, values['cash'])
            sampled.append({'frame': frame, 'state': values, 'whole_active_company_fleet_member_ship_models': models(arm, br)})
        states.append({'mode': mode, 'all_sampled_source_target_models_and_native_states_equal': sampled})
        reports += [str(pa), str(pb)]
    pa, a, _, before = capture('shipyard_v760_newgame_exact_760')
    pb, b, _, after = capture('port_services_v762_newgame_762')
    assert a['scripted_input_schedule'] == b['scripted_input_schedule'] and not b.get('battery_save_preloaded')
    assert set(before) == set(after) == {1, 60, 180, 1600, 2000, 3200, 4000}
    assert all(Path(before[f]['path']).read_bytes() == Path(after[f]['path']).read_bytes() for f in after)
    reports += [str(pa), str(pb)]
    assert len(scenes) == 8 and {r['message_id'] for r in scenes} == {267, 806, 813, 819, 1245}
    assert all(r['arguments'] == ['２１４００'] for r in scenes if r['message_id'] == 1245)
    save(ROOT / 'gameplay_verification.json', {'candidate': str(ROM), 'candidate_sha256': sha(ROM.read_bytes()),
        'eight_complete_actual_dialogue_holds': scenes, 'all_other_whole_frame_controls': controls,
        'all_sampled_native_models_money_and_state_pairs': states, 'New_Game7_unique_frames_identical': sorted(after),
        'capture_reports': reports, 'no_hardware_full_playthrough_or_all_companion_activations_claim': True,
        '13_other_IDs_source_native_font_with_family_gameplay_samples': True,
        'source_native_methods_supply_financial_prerequisites_not_earned_state': True,
        'producer_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print(f'Eight actual full glyph holds,five message IDs,{sum(map(len, controls.values()))} whole-screen controls,native states and seven New Game frames pass.', flush=True)


if __name__ == '__main__': main()
