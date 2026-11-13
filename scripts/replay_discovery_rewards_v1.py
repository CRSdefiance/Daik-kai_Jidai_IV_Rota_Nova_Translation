"""Replay ordinary Auto Move cancellation and the original village approach."""

import argparse
import inspect
from pathlib import Path
from types import FunctionType

from scripts import observe_setup_save_common_v1 as observer
from scripts import run_diplomatic_outcome_startup_v2 as startup
from scripts import run_sea_approach_village_replay_v1 as village
from scripts.audit_story_glyph_consistency import load
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.register_shipyard_fleet_setup_v1 import RELEASE
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.stage_shipyard_fleet_setup_v2 import ROOT as SHIPYARD


ROOT = Path('out/discovery_rewards_baseline_20261111_v1')
AUTO = Path('work/emulation_v193/auto_move_stop_confirm_v402/capture_report.json')
FOCUS = {*range(287, 315), 340, 341}


def auto_plan():
    old = load(AUTO)
    assert old['cold_boot'] and not old['savestate_loaded'] and not old['callback_errors']
    assert not any(value for key, value in old.items() if key.startswith('synthetic_'))
    donor = old['battery_save_preloaded']
    assert digest(donor['source']) == donor['source_sha256']
    return old['scripted_input_schedule'], (6800, 7200, 7300, 7350, 7600, 8000), old['frames'], donor


def replay_auto(rom, root, sha):
    source = checked_text(inspect.getsource(observer.main), {
        '    release = load(RELEASE)\n    rom = Path(release[\'candidate\'])':
            "    release = dict(candidate_sha256=ROM_SHA)\n    rom = TARGET",
        "    inputs = [{'start': frame, 'duration': 8, 'buttons': [key]} for frame, key in SCHEDULE[case]]":
            '    inputs, frames, duration, donor = auto_plan()',
        "    frames = [event['start'] + 199 for event in inputs]\n": '',
        "str(frames[-1] + 10)": 'str(duration)',
        '    installed = []':
            "    argv.extend(['--battery-save', donor['source'], '--touchscreen', '--dump-ram'])\n    installed = []",
        '    trace.save()': "    trace.save()\n    assert digest(donor['source']) == donor['source_sha256']",
        'battery_save_preloaded=False': 'battery_save_preloaded=True',
        'original_controller_only=True': 'original_controller_and_stylus_only=True',
    })
    env = {**vars(observer), **globals(), 'ROOT': root, 'ROM_SHA': sha, 'TARGET': rom}
    exec(compile(source, __file__ + '::observed-auto-move-stop', 'exec'), env)
    env['main']('auto')


def replay_village(rom, root, sha):
    env = {**vars(village), 'ROOT': root, 'ROM': rom}
    env['relocate'] = FunctionType(village.relocate.__code__, env)
    source = checked_text(inspect.getsource(village.village_replay), {
        "assert digest(ROM) == load(PROOF)['research_ROM_sha256']": 'assert digest(ROM) == ROM_SHA',
    })
    env['ROM_SHA'] = sha
    root.mkdir(exist_ok=True)
    exec(compile(source, __file__ + '::same-exact-proximity-fixture', 'exec'), env)
    env['village_replay']()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('case', choices=('auto', 'village', 'startup'))
    parser.add_argument('--staged', action='store_true')
    args = parser.parse_args()
    registered = load(RELEASE)
    if args.staged:
        from scripts.stage_discovery_rewards_v1 import PROOF, ROM, ROOT as STAGED
        sha = load(PROOF)['research_ROM_sha256']
        root, rom = STAGED, ROM
    else:
        root, rom, sha = ROOT, Path(registered['candidate']), registered['candidate_sha256']
    assert digest(rom) == sha
    if args.case == 'startup':
        assert args.staged
        env = {**vars(startup), 'EVIDENCE': PROOF, 'ROM': rom, 'STARTUP': root / 'own_startup',
               'PRIOR': SHIPYARD / 'own_startup'}
        FunctionType(startup.main.__code__, env)()
    else:
        (replay_auto if args.case == 'auto' else replay_village)(rom, root, sha)


if __name__ == '__main__':
    main()
