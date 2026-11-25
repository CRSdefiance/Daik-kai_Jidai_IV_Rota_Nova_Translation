"""Cold-boot an explicit candidate with reproducible, isolated UI inputs.

No ROM is built or edited. Interactive mode accepts the existing harness's JSON
navigation commands; it enables no gameplay fixtures. Screens reached must be
reviewed separately: an input schedule is not proof of the resulting screen.
"""
import argparse
import hashlib
import json
import sys
import time
from pathlib import Path

# Load Pillow from the interpreter before optional local dependency directories.
from PIL import Image  # noqa: F401

REPO = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(REPO), str(REPO / '.deps'), str(REPO / '.runtime_deps')]

from scripts import headless_desmume_v193 as harness


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--rom', type=Path, required=True)
    p.add_argument('--expect-sha256', required=True)
    p.add_argument('--out', type=Path, required=True)
    p.add_argument('--flow', choices=['sailing', 'startup', 'town-refit', 'interactive', 'schedule', 'results'], required=True)
    p.add_argument('--inputs', type=Path)
    p.add_argument('--battery', type=Path)
    p.add_argument('--frames', type=int)
    p.add_argument('--pause-at', type=int, default=3200)
    p.add_argument('--commands-file', type=Path, help='Interactive JSON command array; may be appended while paused')
    p.add_argument('--capture-at', type=int, nargs='*', default=[])
    args = p.parse_args()
    if args.out.exists():
        p.error('Use a new output folder; existing evidence and battery saves are preserved')
    assert sha(args.rom) == args.expect_sha256, 'Candidate hash differs'
    flow = args.flow
    defaults = {
        'sailing': (32800, 'work/font_offset_one_20261027/sailing_inputs.json', None,
                    [2000, 4000, 24000, 28000, 30800, 32800]),
        'startup': (7001, 'work/font_offset_one_20261027/hodram_inputs.json', None,
                    [1100, 1600, 2000, 2400, 3200, 4000, 5000, 6000, 7000]),
        'town-refit': (17401, 'work/analysis/lil_B179_runs_v4751/town_inputs.json',
                       'work/analysis/refit_editorial_v831/disposable_refit_source.dsv',
                       [11900, 12800, 13100, 13400, 13700, 14000, 14300, 14600,
                        14900, 15200, 15500, 15800, 16100, 16400, 16700, 17000, 17300]),
        'interactive': (200000, '../tmp/lisbon_guild_hover_v8865_run2/inputs.json',
                        'work/analysis/weapon_clues_v470/lisbon_test_copy.dsv', []),
        'schedule': (0, None, None, []),
        'results': (100000, None, None, [4800]),
    }
    frames, inputs, battery, captures = defaults[flow]
    results_preflight = None
    if flow == 'results':
        results_preflight = json.loads(Path('work/analysis/full_fleet_victory_v654/replay_preflight.json').read_text(encoding='utf-8'))
        for field in ['donor', 'inputs', 'commands', 'fixture_source']:
            assert sha(results_preflight[field]) == results_preflight[field + '_sha256']
        inputs, battery = Path(results_preflight['inputs']), Path(results_preflight['donor'])
    frames = args.frames or frames
    inputs = args.inputs or (Path(inputs) if inputs else None)
    battery = args.battery or (Path(battery) if battery else None)
    if not frames or inputs is None:
        p.error('A schedule needs --inputs and --frames')
    captures = sorted(set(captures + args.capture_at))
    schedule = json.loads(inputs.read_text(encoding='utf-8'))
    args.out.mkdir(parents=True)
    plan = dict(format='dk4-ui-text-smoke-v1', ROM=str(args.rom.resolve()),
                ROM_sha256=sha(args.rom), flow=flow, frames=frames,
                runner_file_sha256_at_start=sha(Path(__file__)),
                inputs=str(inputs.resolve()), inputs_sha256=sha(inputs),
                input_events=schedule, captures=captures,
                battery_source=str(battery.resolve()) if battery else None,
                battery_sha256=sha(battery) if battery else None,
                inherited_save_progression_not_reverified=bool(battery),
                savestate_loaded=False, new_gameplay_fixtures_enabled=False,
                screen_reachability_requires_review=True)
    if results_preflight:
        plan.update(new_gameplay_fixtures_enabled=True,
                    fixture='Two original bounded approach-coordinate fixtures; no recovery or result writes',
                    fixture_source=results_preflight['fixture_source'],
                    fixture_source_sha256=results_preflight['fixture_source_sha256'],
                    commands_source=results_preflight['commands'],
                    commands_source_sha256=results_preflight['commands_sha256'],
                    earned_travel_and_original_donor_progression_not_verified=True)
    (args.out / 'run_plan.json').write_text(json.dumps(plan, indent=2) + '\n')
    command = ['headless_desmume_v193.py', '--rom', str(args.rom), '--out', str(args.out),
               '--frames', str(frames), '--inputs-json', str(inputs), '--touchscreen',
               '--capture-every', '1000', '--dump-ram', '--dump-native-state']
    if battery:
        command += ['--battery-save', str(battery)]
    if captures:
        command += ['--capture-at', *map(str, captures)]
    if flow in ['interactive', 'results']:
        command += ['--pause-at', str(4800 if flow == 'results' else args.pause_at), '--dump-pause-ram']
        if results_preflight:
            import builtins
            from dk4tool.rom.nds import NdsImage
            from scripts import native_battle_fixture_v620 as dispatch
            from scripts import native_full_fleet_proximity_v653 as original_fixture
            from scripts import native_village_contexts_v618 as terrain_source
            from ndspy.code import loadOverlayTable
            candidate_image = NdsImage.open(args.rom)
            candidate_arm = candidate_image.read_file('/__arm9__.bin')
            arm_hash = hashlib.sha256(candidate_arm).hexdigest()
            # Requalification is explicit for this tested runtime. The original
            # fixture still checks every native getter/setter/terrain span
            # against clean code and permits writes to eight coordinate bytes.
            assert arm_hash == 'be6c9ff56915146a8ddb49a365dd48ec2851cf2d813660aa5f110d0653285d21'
            original_fixture.ARM = arm_hash
            # The historical V604 ROM has been retired. Requalify the entire
            # decoder overlay and map assets, and the original collision routine,
            # against clean source before supplying this candidate as reference.
            clean_image = NdsImage.open('work/clean.nds')
            clean_arm = clean_image.read_file('/__arm9__.bin')
            assert candidate_arm[0x69B5C:0x69E00] == clean_arm[0x69B5C:0x69E00]
            assert candidate_image.read_file('/data/WORLDMAP.DK4') == clean_image.read_file('/data/WORLDMAP.DK4')
            def terrain_overlay(image):
                return loadOverlayTable(image.rom.arm9OverlayTable, lambda _, f: image.rom.files[f])[0]
            current_overlay, clean_overlay = terrain_overlay(candidate_image), terrain_overlay(clean_image)
            assert current_overlay.ramAddress == clean_overlay.ramAddress == 0x01FFA000
            assert current_overlay.data == clean_overlay.data
            original_fixture.REFERENCE = args.rom

            class QualifiedTerrainReference:
                @staticmethod
                def open(path):
                    if Path(path).as_posix() == 'out/all_routes_combined_v604_candidate.nds':
                        return candidate_image
                    return NdsImage.open(path)

            terrain_source.NdsImage = QualifiedTerrainReference
            plan['terrain_requalification'] = dict(
                collision_code_exact_clean=True, complete_overlay0_exact_clean=True,
                WORLDMAP_exact_clean=True, current_reference_ROM_sha256=args.expect_sha256,
                terrain_source_sha256=sha(Path('scripts/native_village_contexts_v618.py')))
            (args.out / 'run_plan.json').write_text(json.dumps(plan, indent=2) + '\n')

            def approach_only(arm, raw, action):
                assert action == 'approach'
                after, proof = original_fixture.apply_fixture(arm, raw, action)
                assert len(proof['owned_bytes']) == 8
                assert proof['no_enemy_stats_war_outcome_reward_inventory_or_resource_flags_changed']
                proof['requalified_candidate_ARM9_sha256'] = arm_hash
                return after, proof

            dispatch.apply_fixture = approach_only
            commands = iter(json.loads(Path(results_preflight['commands']).read_text(encoding='utf-8')))
            builtins.input = lambda: json.dumps(next(commands))
            command += ['--allow-battle-fixtures']
        if args.commands_file:
            # File-fed ordinary controller commands work with noninteractive
            # terminal launchers too. The emulator remains paused while waiting.
            import builtins
            next_command = 0

            def navigation_input():
                nonlocal next_command
                while True:
                    try:
                        commands = json.loads(args.commands_file.read_text(encoding='utf-8'))
                        if len(commands) > next_command:
                            value = commands[next_command]
                            next_command += 1
                            return json.dumps(value)
                    except (FileNotFoundError, json.JSONDecodeError):
                        pass
                    time.sleep(0.2)

            builtins.input = navigation_input
    sys.argv = command
    harness.main()
    report = json.loads((args.out / 'capture_report.json').read_text(encoding='utf-8'))
    assert report['ROM_sha256'] == args.expect_sha256
    assert report['cold_boot'] and not report['savestate_loaded']
    assert not report['callback_errors']
    if flow == 'results':
        fixtures = report.get('synthetic_battle_recovery_proximity_fixtures', [])
        assert len(fixtures) == 2 and all(f['action'] == 'approach' for f in fixtures)
        assert not any(value for key, value in report.items()
                       if key.startswith('synthetic_') and key != 'synthetic_battle_recovery_proximity_fixtures')
    else:
        assert not any(value for key, value in report.items() if key.startswith('synthetic_'))
    if battery:
        assert sha(battery) == plan['battery_sha256'], 'Source battery was changed'
    print('Verified run identity, cold boot, callback health and unchanged source battery.', flush=True)


if __name__ == '__main__':
    main()
