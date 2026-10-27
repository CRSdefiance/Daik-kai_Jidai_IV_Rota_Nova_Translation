"""Cold-boot original regional UI, source-art controls, naming and ordinary regression."""

import argparse
import sys
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.regional_fleet_plaques import FILE
from dk4tool.rom.nds import NdsImage
from scripts import headless_desmume_v193 as harness
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/regional_fleet_v616')
CAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193')
ROM = Path('out/all_routes_combined_v616_candidate.nds')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('context', choices=('policy', 'source', 'names', 'names_final', 'market'))
    args = parser.parse_args()
    rom = ROM
    if args.context == 'source':
        control = NdsImage.open(ROM)
        before = {p: data for _, p, data in control.iter_files()} | dict(control.iter_components())
        original = NdsImage.open('work/clean.nds').read_file(FILE)
        control.replace_file(FILE, original)
        rom = ROOT / 'original_regional_art_CONTROL_ONLY.nds'
        control.save(rom)
        saved = NdsImage.open(rom)
        after = {p: data for _, p, data in saved.iter_files()} | dict(saved.iter_components())
        assert [p for p in before if before[p] != after[p]] == [FILE]
        save(ROOT / 'source_art_control.json', {'ROM': str(rom), 'ROM_sha256': sha(rom.read_bytes()),
             'parent_ROM': str(ROM), 'parent_sha256': sha(ROM.read_bytes()), 'sole_changed_file': FILE,
             'exact_clean_source_PXL_sha256': sha(original), 'same_code_dialogue_inputs_and_other_art': True,
             'research_control_only_not_a_clean_Japanese_playthrough_or_release': True})
    if args.context == 'market':
        baseline = read(CAP / 'golden_route_plaques_v613_market_current/capture_report.json')
        plan = ROOT / 'market_inputs.json'
        save(plan, baseline['scripted_input_schedule'])
        frames = baseline['frames']
        captures = sorted({row['frame'] for row in baseline['frames_captured']})
    elif args.context in ('names', 'names_final'):
        plan, frames = ROOT / 'names_replay_inputs.json', 20000
        captures = [3400, 6200, 9800]
        if args.context == 'names_final':
            inputs = read(plan)
            inputs.append({'start': 9801, 'duration': 8, 'buttons': ['A']})
            plan = ROOT / 'names_final_inputs.json'
            save(plan, inputs)
            captures.append(10200)
    else:
        plan, frames = ROOT / 'policy_replay_inputs.json', 15800
        captures = [3400, 6200, 6600, 7000, 7400, 9800, 10600, 13000, 13800, 14600, 15800]
    argv = ['headless_desmume_v193.py', '--rom', str(rom), '--out', str(CAP / ('regional_ui_v616_' + args.context)),
            '--frames', str(frames), '--inputs-json', str(plan), '--touchscreen', '--capture-every', '999999',
            '--capture-at', *map(str, captures)]
    if args.context != 'market':
        fixture = read('work/analysis/regional_fleet_v615/formed_fixture_manifest.json')
        donor = Path(fixture['fixture'])
        assert not fixture['cold_reload_verification_pending'] and sha(donor.read_bytes()) == fixture['fixture_sha256']
        argv += ['--battery-save', str(donor), '--dump-capture-ram']
    if args.context in ('names', 'names_final'):
        argv += ['--pause-at', '10200' if args.context == 'names_final' else '9800', '--dump-pause-ram']
    sys.argv = argv
    harness.main()


if __name__ == '__main__':
    main()
