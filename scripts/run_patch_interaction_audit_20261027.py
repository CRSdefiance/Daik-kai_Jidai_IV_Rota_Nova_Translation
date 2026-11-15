"""Replay retained ordinary inputs on the exact audit target in isolated processes."""

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import time

from dk4tool.patch.grand_race_menu_release import sha

ROOT = Path('work/patch_interaction_audit_20261027')
ROM = Path('out/font_v2_square_scratch_fix_20261027_test.nds')
DIGEST = '89860905d61e348ae053d40836159bc86bff5d85d3206ce3a0961a6d60142077'
CASES = {
    'guild': ('guild_transactions_actual_v2237_V2171', 'Guild item transactions; inherited Maria Seoul battery'),
    'inn': ('inn_actual_v2253_V2171', 'Inn one/three-night stays; inherited Istanbul test battery'),
    'palace': ('palace_v799_contract_success', 'Palace contract interaction; inherited Istanbul test battery'),
    'port': ('port_services_v762_sell_762', 'Port ship sale workflow; inherited Istanbul test battery'),
    'square': ('square_context_live_v2122_V2097', 'Square shops and dialogue; inherited Istanbul battery'),
    'shipyard': ('town_yard_live_v2156b_V2143', 'Shipyard services; inherited Istanbul battery'),
    'refit': ('refit_actual_v2276_V2171', 'Refit and fleet menus; inherited prepared five-ship Copenhagen battery'),
    'town_market_tavern': ('town_services_font_actual_v2098_V2097', 'Town Market/Tavern/service exchanges; retained system-unlock battery'),
    'recruitment': ('recruitment_actual_v2202_V2171', 'Tavern recruitment workflow; inherited battery'),
    'church': ('ceremony_v803_church_prayer_control', 'Church prayer; inherited battery'),
    'help': ('help_footer_v455', 'Help pages and return paths from fresh start'),
    'save_load': ('save_load_plaques_v612_current', 'Save/Load menus on an isolated copied battery'),
    'gallery': ('characters_gallery_v525', 'Gallery character pages; inherited explicitly prepared unlock battery'),
    'race': ('race_roster_v661_controlled', 'Grand Race roster; inherited explicitly prepared unlock battery'),
    'hodram_opening': ('hodram_opening_revised_v2025_RESEARCH', 'Ordinary Hodram route opening from fresh start'),
    'lil_opening': ('lil_opening_trace_v1706_RESEARCH_ONLY', 'Ordinary Lil opening from fresh start'),
    'maria_opening': ('maria_opening_revised_v2042_RESEARCH', 'Maria opening; inherited system-unlock battery'),
    'rafael_guided': ('rafael_opening_guided_v2008_RESEARCH_ONLY', 'Ordinary Rafael opening and guided tutorial choice from fresh start'),
}


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def save(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def prepare():
    assert sha(ROM.read_bytes()) == DIGEST
    plans = {}
    for case, (folder, scope) in CASES.items():
        source = Path('work/emulation_v193') / folder / 'capture_report.json'
        old = read(source)
        fixtures = {k: v for k, v in old.items() if k.startswith('synthetic_') and v}
        # These are only declarations of already prepared cartridge-save unlocks.
        # Other runtime fixture types require a separately inspected adapter.
        if set(fixtures) - {'synthetic_gallery_fixtures'}:
            plans[case] = dict(status='requires_fixture_review', source=str(source), fixtures=fixtures, scope=scope)
            continue
        case_root = ROOT / 'cases' / case
        case_root.mkdir(parents=True, exist_ok=True)
        battery = old.get('battery_save_preloaded')
        if battery:
            donor = Path(battery['source'])
            assert sha(donor.read_bytes()) == battery['source_sha256'], donor
        frames = old['frames']
        reference_frames = sorted({row['frame'] for row in old['frames_captured'] if row['frame'] >= 2000})
        # Retain all pixel captures. Native snapshots sample transitions and the
        # end; actual instruction/data ownership is evaluated separately.
        native_frames = sorted({reference_frames[0], frames,
            *[reference_frames[(len(reference_frames)-1) * n // 5] for n in range(1, 6)]}) if reference_frames else [frames]
        inputs = case_root / 'inputs.json'
        save(inputs, old['scripted_input_schedule'])
        plan = dict(case=case, scope=scope, source_report=str(source), source_report_sha256=sha(source.read_bytes()),
            target_ROM=str(ROM), target_ROM_sha256=DIGEST, frames=frames,
            inputs=str(inputs), inputs_sha256=sha(inputs.read_bytes()), captures=reference_frames,
            native_frames=native_frames, inherited_battery=battery,
            inherited_prepared_save_declarations=fixtures, new_runtime_gameplay_fixture=False,
            no_savestate=True, status='ready')
        save(case_root / 'plan.json', plan)
        plans[case] = plan
    save(ROOT / 'matrix_plan.json', plans)
    print('Prepared', sum(p['status'] == 'ready' for p in plans.values()), 'cases; reviewed-fixture cases:', [k for k,p in plans.items() if p['status'] != 'ready'])


def run_case(case):
    from scripts import headless_desmume_v193 as harness

    plan = read(ROOT / 'cases' / case / 'plan.json')
    assert plan['status'] == 'ready' and sha(ROM.read_bytes()) == DIGEST
    assert sha(Path(plan['inputs']).read_bytes()) == plan['inputs_sha256']
    output = ROOT / 'cases' / case / 'capture'
    assert not output.exists()
    battery = plan['inherited_battery']
    battery_args = []
    if battery:
        assert sha(Path(battery['source']).read_bytes()) == battery['source_sha256']
        battery_args = ['--battery-save', battery['source']]
    sys.argv = ['headless_desmume_v193.py', '--rom', str(ROM), '--out', str(output),
        '--frames', str(plan['frames']), '--inputs-json', plan['inputs'], '--capture-every', '999999',
        '--capture-at', *map(str, plan['captures']), '--capture-native-state-at', *map(str, plan['native_frames']),
        '--dump-capture-ram', '--touchscreen', *battery_args]
    harness.main()
    report = read(output / 'capture_report.json')
    assert report['ROM_sha256'] == DIGEST and report['cold_boot'] and not report['savestate_loaded']
    assert not report['callback_errors'] and report['frames'] == plan['frames']
    if battery:
        assert sha(Path(battery['source']).read_bytes()) == battery['source_sha256']
    save(ROOT / 'cases' / case / 'terminal.json', dict(
        status='executed_pending_visual_and_memory_review', target_ROM_sha256=DIGEST,
        frames=report['frames'], report_sha256=sha((output / 'capture_report.json').read_bytes()),
        original_donor_preserved=True, scope=plan['scope'], hardware_or_full_route_verification=False))


def run_group(cases, workers):
    plans = read(ROOT / 'matrix_plan.json')
    queue = [case for case in cases if plans[case]['status'] == 'ready']
    running = {}
    done = {}
    while queue or running:
        while queue and len(running) < workers:
            case = queue.pop(0)
            log_path = ROOT / 'cases' / case / 'run.log'
            log = log_path.open('w', encoding='utf-8')
            proc = subprocess.Popen([sys.executable, '-m', 'scripts.run_patch_interaction_audit_20261027', '--case', case],
                stdout=log, stderr=subprocess.STDOUT, env=dict(os.environ, PYTHONUTF8='1'),
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0)
            running[case] = (proc, log, time.monotonic())
            print('Started', case, flush=True)
        for case, (proc, log, start) in list(running.items()):
            code = proc.poll()
            if code is not None:
                log.close()
                done[case] = dict(exit_code=code, seconds=round(time.monotonic()-start, 2))
                del running[case]
                print('Completed', case, 'exit', code, flush=True)
        save(ROOT / 'matrix_progress.json', dict(done=done, running=list(running), queued=queue))
        if running:
            time.sleep(1)
    save(ROOT / 'matrix_execution_receipt.json', done)
    if any(row['exit_code'] for row in done.values()):
        raise SystemExit('Some replays require investigation; see run.log and matrix progress.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--prepare', action='store_true')
    parser.add_argument('--case', choices=list(CASES))
    parser.add_argument('--group', nargs='+', choices=list(CASES))
    parser.add_argument('--workers', type=int, default=3, choices=[1, 2, 3])
    args = parser.parse_args()
    if args.prepare:
        prepare()
    elif args.case:
        run_case(args.case)
    elif args.group:
        run_group(args.group, args.workers)
