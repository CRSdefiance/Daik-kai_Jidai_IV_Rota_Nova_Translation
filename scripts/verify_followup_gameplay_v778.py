"""Verify bribe/follow-up,crowded refusal and Patron rumor on paired cold boots."""

import re
import struct
from pathlib import Path

from PIL import Image, ImageChops

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts import native_followup_expert_fixture_v778 as expert
from scripts import native_followup_crowd_fixture_v778 as crowd
from scripts import native_followup_shortage_fixture_v778 as shortage
from scripts.native_machine_scoped_v764 import machine
from scripts.native_call_abi_v764 import call
from scripts.probe_button_prompt_native import BASE
from scripts.verify_common_alignment_native_v257 import raster
from scripts.verify_followup_scoped_layout_v778 import formatter
from scripts.verify_market_gameplay_v753 import state
from scripts.verify_port_gameplay_v762 import cstring
from scripts.verify_shipyard_gameplay_v760 import models, independent_font
from scripts.verify_tavern_gameplay_v767 import persistent_objects
from scripts.verify_village_wrap_v608 import read, save
from unicorn.arm_const import UC_ARM_REG_R0

ROOT = Path('work/analysis/scheme_followup_integration_v778')
CAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193')
BODY, ADVANCE = (16, 294, 244, 366), (224, 360, 240, 376)
SCENES = {
    'bribe': {9600: 973, 10000: 973, 10800: 979, 11200: 979, 11600: 965, 12000: 965},
    'crowd': {6000: 984, 6400: 984}, 'shortage': {28800: 972, 29200: 972}}
TERMINAL = {'bribe': 13200, 'crowd': 7600, 'shortage': 30400}


def load(kind, suffix):
    path = CAP/f'followup_v778_{kind}_{suffix}'/'capture_report.json'
    r = read(path)
    assert r['cold_boot'] and not r['savestate_loaded'] and not r['callback_errors']
    assert not r['hardware_device_verification'] and not r['goal_complete']
    assert r['core_DLL_sha256'] == '42160dbfef89adfb3cfd975070a3047d8ad0979cead55607ebdfd3b931046c2b'
    assert sha(Path(r['ROM']).read_bytes()) == r['ROM_sha256']
    arm = NdsImage.open(r['ROM']).read_file('/__arm9__.bin')
    donor = r['battery_save_preloaded']
    assert donor['source'] != donor['destination'] and donor['copied_byte_exact_before_cold_boot']
    assert sha(Path(donor['source']).read_bytes()) == donor['source_sha256'] == '05fa512b078fd01a8f6bee605254e9f72bfe3453c0ea098d977c87d86b6b693e'
    ram = {}
    for row in r.get('read_only_capture_RAM_snapshots', []) + r['read_only_pause_RAM_snapshots']:
        raw = Path(row['path']).read_bytes()
        assert row['read_only_export'] and len(raw) == row['bytes'] == 0x400000
        assert sha(raw) == row['sha256']
        if row['frame'] in ram:
            assert ram[row['frame']] == raw
        ram[row['frame']] = raw
    if kind == 'shortage':
        key = 'synthetic_town_condition_fixtures'
        _, expected = shortage.set_condition(arm, ram[3200], {'town': 2, 'status': 5, 'days': 30})
        adapter = r['controlled_town_condition_adapter']
        fixture_file = Path(shortage.__file__)
        adapter_file = Path('scripts/run_followup_shortage_capture_v778.py')
        assert adapter['original_harness_file_unchanged']
        assert adapter['source_adapter_sha256'] == sha(Path('scripts/run_town_condition_capture_v774.py').read_bytes())
    else:
        key = 'synthetic_strategist_room_assignment_fixtures'
        module = expert if kind == 'bribe' else crowd
        _, expected = module.assign_expert(arm, ram[3200], True)
        adapter = r['controlled_strategist_adapter']
        fixture_file = Path(module.__file__)
        adapter_file = Path(f'scripts/run_followup_{"expert" if kind == "bribe" else "crowd"}_capture_v778.py')
        assert adapter['original_harness_unchanged'] and adapter['single_import_replacement']
        assert adapter['original_fixture_module_sha256'] == sha(Path('scripts/native_strategist_fixture_v624.py').read_bytes())
        assert adapter['original_experience_calendar_producer_sha256'] == sha(Path('scripts/native_scheme_expert_fixture_v776_v2.py').read_bytes())
        if kind == 'crowd':
            assert adapter['source_adapter_sha256'] == sha(Path('scripts/run_followup_expert_capture_v778.py').read_bytes())
    fixture, = r[key]
    assert fixture == {**expected, 'frame': 3200}
    assert not any(v for k, v in r.items() if k.startswith('synthetic_') and k != key)
    assert adapter['original_harness_sha256'] == sha(Path('scripts/headless_desmume_v193.py').read_bytes())
    assert adapter['adapter_sha256'] == sha(adapter_file.read_bytes())
    assert adapter['fixture_producer_sha256'] == sha(fixture_file.read_bytes())
    frames = {}
    for row in r['frames_captured']:
        assert sha(Path(row['path']).read_bytes()) == row['PNG_sha256']
        frames[row['frame']] = row
    return path, r, arm, frames, ram


def tasks(arm, raw):
    u = machine(arm)
    u.mem_write(BASE, raw)
    call(u, 0xCB130, ())
    root = u.reg_read(UC_ARM_REG_R0)
    return bytes(u.mem_read(root+4, 24*16))


def main():
    rows = {r['message_id']: r for r in read('translations/scheme_followup_editorial_manuscript_v2.json')['records']}
    run, _ = formatter()
    all_results = []
    for kind in SCENES:
        pa, old, oa, before, old_ram = load(kind, 'baseline')
        pb, new, arm, after, new_ram = load(kind, 'live')
        assert old['frames'] == new['frames'] == TERMINAL[kind]
        assert old['scripted_input_schedule'] == new['scripted_input_schedule']
        assert old['core_options'] == new['core_options']
        assert after.keys() <= before.keys() and old_ram.keys() == new_ram.keys()
        rom = NdsImage.open(new['ROM'])
        common = rom.read_file('/COMMON/MESFILE.DK4')
        entries = common_message_entries(common, arm, clean=False)
        blocks = IlnkContainer.parse(common).blocks
        p, w, owner = [struct.unpack_from('<I', arm, off)[0] for off in (0x5444C, 0x54450, 0x552A0)]
        phases = {f: Image.open(before[f]['path']).convert('RGB').crop(ADVANCE).tobytes()
                  for f, n in SCENES[kind].items() if n != 979}
        holds, controls, states, menu_phases = [], [], [], []
        for f in sorted(after):
            a, b = [Image.open(fs[f]['path']).convert('RGB') for fs in (before, after)]
            diff = ImageChops.difference(a, b)
            if f not in SCENES[kind]:
                assert diff.getbbox() is None, (kind, f, 'unselected full screen', diff.getbbox())
                controls.append(f)
                continue
            n, raw = SCENES[kind][f], new_ram[f]
            assert cstring(raw, owner+0x2030) == entries[n].text, (kind, f, n)
            assert raw.count(blocks[entries[n].block]) == 1
            pattern = b'(.*?)'.join(re.escape(part) for part in entries[n].text.split(b'%s'))
            match = re.fullmatch(pattern, cstring(raw, p))
            assert match is not None
            args = match.groups()
            assert args == ((b'London', b'Clifford') if n == 979 else ())
            u = machine(arm)
            u.mem_write(BASE, raw)
            native = run(u, rows[n], args)
            assert not native['findings']
            formatted = bytes.fromhex(native['formatted_hex'])
            assert formatted == cstring(raw, w), (kind, f, native['lines'])
            plane = raster(arm, formatted, 0x01FFCE40-BASE, size=(228, 64), instruction_limit=1000000)
            assert plane == independent_font(arm, rom.read_file('/GRP/KANJI.FNT'), native['lines'])
            expected = {(16+i%228, 296+i//228) for i, v in enumerate(plane) if v == 1}
            actual = {(x, y) for y in range(BODY[1], BODY[3]) for x in range(BODY[0], BODY[2]) if b.getpixel((x, y)) == (0, 8, 0)}
            assert expected == actual, (kind, f, len(expected-actual), len(actual-expected))
            previous = {(x, y) for y in range(BODY[1], BODY[3]) for x in range(BODY[0], BODY[2]) if a.getpixel((x, y)) == (0, 8, 0)}
            glyphs = expected | previous
            shadows = {(x+1, y+1) for x, y in glyphs}
            unexpected = [(x, y) for y in range(BODY[1], BODY[3]) for x in range(BODY[0], BODY[2])
                          if not (n != 979 and ADVANCE[0] <= x < ADVANCE[2] and ADVANCE[1] <= y < ADVANCE[3])
                          and (x, y) not in glyphs | shadows and a.getpixel((x, y)) != b.getpixel((x, y))]
            assert not unexpected, (kind, f, unexpected[:10])
            matches = []
            if n != 979:
                matches = [k for k, v in phases.items() if v == b.crop(ADVANCE).tobytes()]
                assert matches, (kind, f, 'unknown original advance phase')
                diff.paste((0, 0, 0), ADVANCE)
            diff.paste((0, 0, 0), BODY)
            assert diff.getbbox() is None, (kind, f, 'outside text', diff.getbbox())
            holds.append({'frame': f, 'message_id': n, 'lines': native['lines'],
                          'arguments': [v.decode() for v in args], 'capture': after[f],
                          'complete_independent_font_and_blank_paper_exact': True,
                          'all_other_pixels_exact': True, 'original_advance_phase_matches': matches,
                          'observed_speaker': 'Patron' if n == 972 else 'Gerhard (Strategist)'})
        for f in new_ram:
            assert state(oa, old_ram[f]) == state(arm, new_ram[f]), (kind, f, 'state')
            assert models(oa, old_ram[f]) == models(arm, new_ram[f]), (kind, f, 'models')
            assert persistent_objects(oa, old_ram[f]) == persistent_objects(arm, new_ram[f]), (kind, f, 'objects')
            assert tasks(oa, old_ram[f]) == tasks(arm, new_ram[f]), (kind, f, 'task records')
            states.append(f)
        cash_before = state(arm, new_ram[3200])['cash']
        cash_after = state(arm, new_ram[TERMINAL[kind]])['cash']
        assert cash_before == 40659
        assert cash_after == {'bribe': 39659, 'crowd': 40659, 'shortage': 39402}[kind]
        all_results.append({'kind': kind, 'capture_reports': [str(pa), str(pb)], 'holds': holds,
                            'whole_screen_controls': controls, 'paired_state_model_object_task_frames': states,
                            'unpaired_baseline_phase_window_captures': sorted(before.keys()-after.keys()),
                            'menu_phase_controls': menu_phases, 'cash_before': cash_before, 'cash_after': cash_after,
                            'normal_town_return_frame': TERMINAL[kind], 'declared_fixture_reproduced_exactly': True})
        print(kind, len(holds), 'holds;', len(controls), 'whole controls;', len(states), 'state/model/task pairs.', flush=True)
    boot_paths = [CAP/folder/'capture_report.json' for folder in ('schemes_v776_newgame', 'followup_v778_newgame')]
    boot = [read(p) for p in boot_paths]
    assert all(r['cold_boot'] and not r['savestate_loaded'] and not r['callback_errors'] and not r.get('battery_save_preloaded') for r in boot)
    assert all(not any(v for k, v in r.items() if k.startswith('synthetic_')) for r in boot)
    assert boot[0]['scripted_input_schedule'] == boot[1]['scripted_input_schedule']
    frame_sets = [{r['frame']: r for r in report['frames_captured']} for report in boot]
    assert frame_sets[0].keys() == frame_sets[1].keys() and len(frame_sets[0]) == 7
    for f in frame_sets[0]:
        images = []
        for fs in frame_sets:
            r = fs[f]
            assert sha(Path(r['path']).read_bytes()) == r['PNG_sha256']
            images.append(Image.open(r['path']).convert('RGB'))
        assert ImageChops.difference(*images).getbbox() is None
    patch = read(ROOT/'patch_proof.json')
    assert all(read(r['capture_reports'][1])['ROM_sha256'] == patch['candidate_sha256'] for r in all_results)
    save(ROOT/'gameplay_verification.json', {
        'candidate_sha256': patch['candidate_sha256'], 'scenarios': all_results,
        'newgame_reports': [str(p) for p in boot_paths], 'newgame_complete_frames_exact': sorted(frame_sets[0]),
        'actual_IDs': sorted({h['message_id'] for r in all_results for h in r['holds']}),
        'actual_original_scheme_scheduled_and1000_gold_charged': True,
        'future_scheme_outcome_or_earned_qualifications_not_claimed': True,
        'crowded_capacity_fixture_not_earned_Tavern_state': True,
        'two_byte_shortage_fixture_not_earned_condition_or_historical_shipwreck': True,
        'original_donor_save_unchanged': True,
        'context_amendment_972_speaker': 'Actual unmodified portrait/name label is Patron;earlier barmaid/NPC research wording is superseded. Native selected-town NPC getter and ID972 caller are unchanged.',
        'producer_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print('All five consumer types,normal returns,paired task/state models and seven ordinary New Game screens pass.', flush=True)


if __name__ == '__main__':
    main()
