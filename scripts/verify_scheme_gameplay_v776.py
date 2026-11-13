"""Verify actual scheme prompts through ordinary menus after a bounded fixture."""

import re
import struct
from pathlib import Path

from PIL import Image, ImageChops

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.native_machine_scoped_v764 import machine
from scripts.native_scheme_expert_fixture_v776_v2 import assign_expert
from scripts.probe_button_prompt_native import BASE
from scripts.verify_common_alignment_native_v257 import raster
from scripts.verify_market_gameplay_v753 import state
from scripts.verify_port_gameplay_v762 import cstring
from scripts.verify_scheme_scoped_layout_v776 import formatter
from scripts.verify_shipyard_gameplay_v760 import models, independent_font
from scripts.verify_tavern_gameplay_v767 import persistent_objects
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/tavern_schemes_integration_v776')
CAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193')
BODY = (16, 294, 244, 366)
ADVANCE = (224, 360, 240, 376)
SCENES = {
    6000: 909, 6400: 909, 7200: 915, 7600: 915,
    14400: 909, 15200: 915, 16400: 921, 17200: 941, 17600: 941,
    19600: 909, 20800: 915, 21200: 915, 22000: 933, 22400: 933,
    23200: 949, 23600: 949, 25600: 909, 27200: 915,
    28400: 927, 28800: 927, 29600: 957, 30000: 957,
}
EXPECTED_ARGS = {909: (), 915: (), 921: (), 927: (), 933: (),
                 941: (b'Clifford', b'London'),
                 949: (b'Argot Co.', b'Clifford'),
                 957: (b'London', b'Clifford')}


def load(folder):
    path = CAP / folder / 'capture_report.json'
    report = read(path)
    assert report['cold_boot'] and not report['savestate_loaded']
    assert not report['callback_errors'] and not report['hardware_device_verification']
    assert not report['goal_complete']
    assert report['core_DLL_sha256'] == '42160dbfef89adfb3cfd975070a3047d8ad0979cead55607ebdfd3b931046c2b'
    assert report['ROM_sha256'] == sha(Path(report['ROM']).read_bytes())
    arm = NdsImage.open(report['ROM']).read_file('/__arm9__.bin')
    donor, pin = report['battery_save_preloaded'], read('work/analysis/condition_rumor_v774/source_donor.json')
    assert Path(donor['source']).resolve() == Path(pin['path']).resolve()
    assert donor['source'] != donor['destination'] and donor['copied_byte_exact_before_cold_boot']
    assert sha(Path(donor['source']).read_bytes()) == donor['source_sha256'] == pin['sha256']
    assert not any(v for k, v in report.items() if k.startswith('synthetic_') and k != 'synthetic_strategist_room_assignment_fixtures')
    ram = {}
    for row in report.get('read_only_capture_RAM_snapshots', []) + report['read_only_pause_RAM_snapshots']:
        raw = Path(row['path']).read_bytes()
        assert row['read_only_export'] and row['bytes'] == len(raw) == 0x400000
        assert sha(raw) == row['sha256']
        if row['frame'] in ram:
            assert ram[row['frame']] == raw
        ram[row['frame']] = raw
    fixture, = report['synthetic_strategist_room_assignment_fixtures']
    _, expected = assign_expert(arm, ram[3200], True)
    assert fixture == {**expected, 'frame': 3200}
    adapter = report['controlled_strategist_adapter']
    assert adapter['original_harness_unchanged'] and adapter['single_import_replacement']
    for key, file in (
        ('original_harness_sha256', 'scripts/headless_desmume_v193.py'),
        ('adapter_sha256', 'scripts/run_scheme_expert_capture_v776_v2.py'),
        ('fixture_producer_sha256', 'scripts/native_scheme_expert_fixture_v776_v2.py'),
        ('original_fixture_module_sha256', 'scripts/native_strategist_fixture_v624.py'),
    ):
        assert adapter[key] == sha(Path(file).read_bytes())
    frames = {}
    for row in report['frames_captured']:
        assert sha(Path(row['path']).read_bytes()) == row['PNG_sha256']
        frames[row['frame']] = row
    return path, report, arm, frames, ram


def main():
    pa, old, old_arm, before, old_ram = load('schemes_v776_qualified_baseline')
    pb, new, arm, after, new_ram = load('schemes_v776_qualified_live')
    pp, phase_report, phase_arm, phase_frames, phase_ram = load('schemes_v776_baseline_menu_phases')
    assert old['frames'] == new['frames'] == 31200
    assert old['scripted_input_schedule'] == new['scripted_input_schedule']
    assert old['core_options'] == new['core_options']
    assert phase_report['ROM_sha256'] == old['ROM_sha256']
    assert phase_report['scripted_input_schedule'] == old['scripted_input_schedule']
    assert phase_report['core_options'] == old['core_options']
    assert phase_ram == old_ram
    assert after.keys() <= before.keys() and old_ram.keys() == new_ram.keys()
    baseline_only = sorted(before.keys() - after.keys())
    assert baseline_only == [400, 800, 1200, 1600, 2000, 2400, 2800]
    rom = NdsImage.open(new['ROM'])
    common = rom.read_file('/COMMON/MESFILE.DK4')
    entries = common_message_entries(common, arm, clean=False)
    blocks = IlnkContainer.parse(common).blocks
    manuscript = read('translations/tavern_schemes_editorial_manuscript_v4.json')
    rows = {r['message_id']: r for r in manuscript['records']}
    run, _ = formatter()
    p, w, owner = [struct.unpack_from('<I', arm, off)[0] for off in (0x5444C, 0x54450, 0x552A0)]
    scenes, controls, states, menu_phases = [], [], [], []
    # Only documented ordinary-dialogue holds supply stock advance animation phases.
    phases = {f: Image.open(before[f]['path']).convert('RGB').crop(ADVANCE).tobytes()
              for f, n in SCENES.items() if n < 940}
    for f in sorted(after):
        a, b = [Image.open(frames[f]['path']).convert('RGB') for frames in (before, after)]
        diff = ImageChops.difference(a, b)
        if f not in SCENES:
            if f in (15600, 16800, 21600, 30800):
                if f in (15600, 21600):
                    bounds, candidates, available = (72, 258, 184, 274), [8000], before
                elif f == 16800:
                    bounds, candidates, available = (74, 268, 182, 296), range(16770, 16831), phase_frames
                else:
                    bounds, candidates, available = (60, 240, 105, 260), range(30800, 30861), phase_frames
                matches = [k for k in candidates if k in available and
                           Image.open(available[k]['path']).convert('RGB').crop(bounds).tobytes() == b.crop(bounds).tobytes()]
                assert matches, (f, 'menu phase absent from original baseline')
                diff.paste((0, 0, 0), bounds)
                assert diff.getbbox() is None, (f, 'outside original blinking menu')
                menu_phases.append({'frame': f, 'bounds': bounds, 'exact_original_phase_matches': matches,
                                    'all_menu_glyphs_and_pixels_exact_to_original_phase': True,
                                    'every_pixel_outside_menu_phase_exact_to_same_frame': True})
                continue
            assert diff.getbbox() is None, (f, 'unselected full screen', diff.getbbox())
            controls.append(f)
            continue
        n, raw = SCENES[f], new_ram[f]
        assert cstring(raw, owner + 0x2030) == entries[n].text, (f, n)
        assert raw.count(blocks[entries[n].block]) == 1
        pattern = b'(.*?)'.join(re.escape(part) for part in entries[n].text.split(b'%s'))
        match = re.fullmatch(pattern, cstring(raw, p))
        assert match is not None, (f, cstring(raw, p))
        args = match.groups()
        expected_args = EXPECTED_ARGS[n]
        if n == 915:
            expected_args = (b'Lure Fleet' if f < 20000 else b'Forge Papers' if f < 25600 else b'Bad Rumors',)
        assert args == expected_args, (f, args)
        u = machine(arm)
        u.mem_write(BASE, raw)
        native = run(u, rows[n], args)
        assert not native['findings'], (f, native['findings'])
        formatted = bytes.fromhex(native['formatted_hex'])
        assert formatted == cstring(raw, w), (f, native['lines'])
        plane = raster(arm, formatted, 0x01FFCE40 - BASE, size=(228, 64), instruction_limit=1000000)
        assert plane == independent_font(arm, rom.read_file('/GRP/KANJI.FNT'), native['lines'])
        expected = {(16 + i % 228, 296 + i // 228) for i, v in enumerate(plane) if v == 1}
        actual = {(x, y) for y in range(BODY[1], BODY[3]) for x in range(BODY[0], BODY[2])
                  if b.getpixel((x, y)) == (0, 8, 0)}
        assert expected == actual, (f, len(expected - actual), len(actual - expected))
        previous = {(x, y) for y in range(BODY[1], BODY[3]) for x in range(BODY[0], BODY[2])
                    if a.getpixel((x, y)) == (0, 8, 0)}
        glyphs = expected | previous
        shadows = {(x + 1, y + 1) for x, y in glyphs}
        unexpected = [(x, y) for y in range(BODY[1], BODY[3]) for x in range(BODY[0], BODY[2])
                      if not (n < 940 and ADVANCE[0] <= x < ADVANCE[2] and ADVANCE[1] <= y < ADVANCE[3])
                      and (x, y) not in glyphs | shadows and a.getpixel((x, y)) != b.getpixel((x, y))]
        assert not unexpected, (f, unexpected[:10])
        matches = []
        if n < 940:
            matches = [k for k, v in phases.items() if v == b.crop(ADVANCE).tobytes()]
            assert matches, (f, 'unknown original advance phase')
            diff.paste((0, 0, 0), ADVANCE)
        diff.paste((0, 0, 0), BODY)
        assert diff.getbbox() is None, (f, 'outside dialogue', diff.getbbox())
        scenes.append({'frame': f, 'message_ID': n, 'arguments': [v.decode('ascii') for v in args],
                       'lines': native['lines'], 'capture': after[f],
                       'complete_independent_font_and_blank_paper_exact': True,
                       'all_other_pixels_exact': True, 'original_advance_phase_matches': matches})
    for f in sorted(new_ram):
        assert state(old_arm, old_ram[f]) == state(arm, new_ram[f]), (f, 'state')
        assert models(old_arm, old_ram[f]) == models(arm, new_ram[f]), (f, 'models')
        assert persistent_objects(old_arm, old_ram[f]) == persistent_objects(arm, new_ram[f]), (f, 'objects')
        states.append(f)
    assert state(arm, new_ram[3200])['cash'] == 40659
    assert all(state(arm, new_ram[f])['cash'] == 40644 for f in (12800, 18000, 24000, 30400, 31200))
    games = [read(CAP / folder / 'capture_report.json') for folder in
             ('recruitment_v773_newgame_v773', 'schemes_v776_newgame')]
    assert all(r['cold_boot'] and not r['savestate_loaded'] and not r['callback_errors'] for r in games)
    assert all(not r.get('battery_save_preloaded') and not any(v for k, v in r.items() if k.startswith('synthetic_')) for r in games)
    assert games[0]['scripted_input_schedule'] == games[1]['scripted_input_schedule']
    boot = [{r['frame']: r for r in g['frames_captured']} for g in games]
    assert boot[0].keys() == boot[1].keys() and len(boot[0]) == 7
    for f in boot[0]:
        images = []
        for i in (0, 1):
            row = boot[i][f]
            assert sha(Path(row['path']).read_bytes()) == row['PNG_sha256']
            images.append(Image.open(row['path']).convert('RGB'))
        assert ImageChops.difference(*images).getbbox() is None
    assert read(ROOT / 'patch_proof.json')['candidate_sha256'] == new['ROM_sha256']
    save(ROOT / 'gameplay_verification.json', {
        'candidate': new['ROM'], 'candidate_sha256': new['ROM_sha256'],
        'capture_reports': [str(pa), str(pb), str(pp)], 'actual_scheme_holds': scenes,
        'actual_IDs': sorted({r['message_ID'] for r in scenes}),
        'whole_screen_controls': controls, 'paired_state_model_object_frames': states,
        'original_menu_animation_phase_controls': menu_phases,
        'baseline_only_boot_captures_without_paired_credit': baseline_only,
        'newgame_whole_screen_frames': sorted(boot[0]),
        'same_bounded_fixture_receipt_reproduced_on_both_ROMs': True,
        'original_save_unchanged': True, 'three_schemes_cancelled_without_payment': True,
        'ordinary_town_return_frame': 31200, 'normal_scheme_success_outcome_verified': False,
        'earned_experience_assignment_calendar_progress_verified': False,
        'all56_records_native_verified_actual_family_samples8_IDs': True,
        'cash_before': 40659, 'cash_after_drinks_and_three_scheme_cancels': 40644,
        'producer_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print(f'{len(scenes)} actual holds/eight families, {len(controls)} full-screen controls, {len(states)} paired states and seven New Game frames pass.', flush=True)


if __name__ == '__main__':
    main()
