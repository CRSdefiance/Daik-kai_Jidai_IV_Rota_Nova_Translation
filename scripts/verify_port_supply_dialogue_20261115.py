"""Verify the changed Port panels, disposal, and return to sailing."""

from pathlib import Path
from struct import unpack

from PIL import Image, ImageChops, ImageDraw
from unicorn.arm_const import UC_ARM_REG_R0

from scripts import replay_port_supply_dialogue_20261115 as replay
from scripts import stage_port_supply_dialogue_20261115 as stage
from scripts.preflight_shared_dynamic_notice_wrap_v1 import font_tools
from scripts.probe_button_prompt_native import BASE, call, machine
from scripts.stage_mutiny_review_v1 import render_portrait
from scripts.verify_captain_biographies_v1 import captured, shots
from scripts.verify_london_stockholm_dialogue_20261115 import BODY, native_hold


base, ROOT = stage.base, stage.ROOT
OUTPUT, SHEET = ROOT / 'gameplay_verification.json', ROOT / 'gameplay_comparison.png'
HELD = {'water': {3400: 813, 3800: 806}, 'riga': {4121: 814, 4251: 814}}


def totals(arm, snapshot, fleet):
    raw = Path(snapshot['path']).read_bytes()
    assert snapshot['read_only_export'] and stage.digest(raw) == snapshot['sha256']
    cpu = machine(arm)
    cpu.mem_write(BASE, raw)
    out = 0x02450000
    call(cpu, 0x34EB0, (fleet, out))
    call(cpu, 0xCB160, ())
    root = cpu.reg_read(UC_ARM_REG_R0)
    call(cpu, 0x397D8, (root,))
    company = cpu.reg_read(UC_ARM_REG_R0)
    call(cpu, 0x3CCC8, (root + 4 + company * 0x4C,))
    return list(unpack('<2I', cpu.mem_read(out, 8))), cpu.reg_read(UC_ARM_REG_R0)


def reports(folder, sha, fixtures):
    path = folder / 'capture/capture_report.json'
    r = base.load(path)
    assert r['ROM_sha256'] == sha and r['cold_boot'] and not r['savestate_loaded'] and not r['callback_errors']
    assert r['battery_save_preloaded']['copied_byte_exact_before_cold_boot']
    assert base.digest(r['battery_save_preloaded']['source']) == r['battery_save_preloaded']['source_sha256']
    assert {k for k, v in r.items() if k.startswith('synthetic_') and v} == fixtures
    return path, r


def main():
    assert not OUTPUT.exists() and not SHEET.exists()
    info = base.load(stage.STORED)
    assert base.digest(stage.ROM) == info['candidate_sha256']
    image = base.NdsImage.open(stage.ROM)
    arm, kanji = [image.read_file(p) for p in (stage.ARM, '/GRP/KANJI.FNT')]
    cases = {row['n']: row for row in info['native_cases']}
    raster, _, _ = font_tools(image)
    evidence, records, gallery = {}, [], []
    water_state = []
    for case, expected in HELD.items():
        if case == 'water':
            pair = (ROOT / 'water_before', ROOT / 'water_after')
            fixtures = {'synthetic_condition_fixtures'}
        else:
            pair = (stage.parent.stage.ROOT / 'riga', ROOT / 'riga')
            fixtures = set()
        (old_path, old), (new_path, new) = [
            reports(folder, sha, fixtures)
            for folder, sha in zip(pair, (info['previous_sha256'], info['candidate_sha256']), strict=True)
        ]
        assert old['core_DLL_sha256'] == new['core_DLL_sha256'] and old['core_options'] == new['core_options']
        assert old['battery_save_preloaded']['source_sha256'] == new['battery_save_preloaded']['source_sha256']
        evidence.update({str(p): base.digest(p) for p in (old_path, new_path)})
        if case == 'water':
            assert old['scripted_input_schedule'] == new['scripted_input_schedule']
            assert old['frames'] == new['frames'] == 7200
            for report in (old, new):
                fixture, = report['synthetic_condition_fixtures']
                assert fixture['frame'] == 3200 and fixture['all_other4MiB_RAM_exact']
                assert len(fixture['changes']) == 11
                assert fixture['after_water_food'] == [0, 700]
                assert fixture['before_water_food'] == [350, 350]
                snapshots = {row['frame']: row for row in report['read_only_pause_RAM_snapshots']}
                state = {frame: totals(arm, snapshots[frame], fixture['native_fleet']) for frame in (3200, 5200, 7200)}
                assert all(value == ([350, 350], 25975) for value in state.values()), state
                water_state.append({'ROM_sha256': report['ROM_sha256'], 'fleet_water_food_and_gold': state,
                                    'fixture': fixture, 'snapshots': snapshots})
                evidence.update({row['path']: row['sha256'] for row in snapshots.values()})
        else:
            assert new['scripted_input_schedule'] == [row for row in old['scripted_input_schedule']
                                                       if row['start'] < new['frames']]
            traces = [folder / 'requests.json' for folder in pair]
            a, b = map(base.load, traces)
            assert all(r['all_host_slots_restored_and_core_file_exact'] and not r['mismatches'] and not r['errors']
                       for r in (a, b))
            assert b['source_requests'] == [row for row in a['source_requests'] if row['frame'] < new['frames']]
            assert sum(row['message_ID'] == 814 for row in b['source_requests']) == 2
            evidence.update({str(path): base.digest(path) for path in traces})
        before, after = shots(old), shots(new)
        exact = []
        changed = []
        assert set(expected) <= before.keys() & after.keys()
        for frame in sorted(before.keys() & after.keys()):
            a, b = captured(before[frame]), captured(after[frame])
            evidence.update({row['path']: row['PNG_sha256'] for row in (before[frame], after[frame])})
            diff = ImageChops.difference(a, b).getbbox()
            if frame not in expected:
                assert diff is None, (case, frame, diff)
                exact.append(frame)
                continue
            assert diff and BODY[0] <= diff[0] < diff[2] <= BODY[2] and BODY[1] <= diff[1] < diff[3] <= BODY[3]
            n = expected[frame]
            contract = cases[n]
            plane, _ = render_portrait(raster, arm, kanji, bytes.fromhex(contract['native_output_hex']))
            assert stage.digest(plane) == contract['native_plane_sha256']
            ink = native_hold(b, plane)
            changed.append({'record': n, 'frame': frame, 'complete_ink_pixels': ink, 'before': before[frame],
                            'after': after[frame], 'changed_bounds': diff})
            if n not in {row[0] for row in gallery}:
                gallery.append((n, a, b))
        records.append({'case': case, 'complete_changed_message_holds': changed, 'exact_control_frames': exact})
    sheet = Image.new('RGB', (1024, 228 * len(gallery)), '#263238')
    draw = ImageDraw.Draw(sheet)
    for row, (n, before, after) in enumerate(gallery):
        for column, screen in enumerate((before, after)):
            x, y = column * 512, row * 228
            draw.text((x + 4, y + 4), f"{n} {'before' if column == 0 else 'after'}", fill='white')
            sheet.paste(screen.crop((0, 280, 256, 384)).resize((512, 208), Image.Resampling.NEAREST), (x, y + 18))
    sheet.save(SHEET)
    base.save(OUTPUT, {'candidate_sha256': info['candidate_sha256'], 'cases': records, 'water_service_state': water_state,
                       'ordinary_Riga_departure': True, 'Copenhagen_preconditions_fixture_only': True,
                       'native_only_changed_records': [816, 817], 'sheet_sha256': base.digest(SHEET),
                       'hardware': False, 'evidence': evidence})
    print('Four complete changed panel holds, matching controls and supply totals verified.')


if __name__ == '__main__':
    main()
