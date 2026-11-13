"""Explicit bounded work-room fixtures on fresh disposable Copenhagen saves."""

import argparse
import sys
from pathlib import Path
from shutil import copy2

from dk4tool.patch.grand_race_menu_release import sha
from scripts import run_work_room_adapter_v846 as adapter
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/work_comments_v846')
CAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--version', type=int, choices=(838,845), default=845)
    parser.add_argument('--label', required=True)
    args = parser.parse_args()
    assert args.label and all(c.isalnum() or c == '_' for c in args.label)
    ROOT.mkdir(parents=True, exist_ok=True)
    rom = Path(f'out/all_routes_combined_v{args.version}_candidate.nds')
    assert sha(rom.read_bytes()) == read(rom.with_suffix('.manifest.json'))['candidate_sha256']
    folder = CAP / f'work_comments_v846_{args.version}_{args.label}_scheduled'
    provenance = read('work/analysis/refit_editorial_v831/donor_copy.json')
    source = Path(provenance['disposable_source'])
    donor = ROOT / f'disposable_{args.version}_{args.label}_scheduled.dsv'
    assert not folder.exists() and not donor.exists()
    digest = sha(source.read_bytes())
    assert digest == provenance['disposable_source_sha256']
    copy2(source, donor)
    assert sha(donor.read_bytes()) == digest
    inputs = Path('work/analysis/ceremony_heroes_v825/load_save_inputs.json')
    plan = ROOT / f'{args.version}_{args.label}_scheduled_run_plan.json'
    save(plan, {'ROM': str(rom), 'ROM_sha256': sha(rom.read_bytes()), 'folder': str(folder),
        'source_donor': str(source), 'source_donor_sha256': digest, 'disposable_source': str(donor),
        'existing_isolated_five_ship_Copenhagen_save_no_earned_fleet_or_progression_claim': True,
        'existing_donor_provenance': provenance, 'inputs': str(inputs),
        'inputs_sha256': sha(inputs.read_bytes()), 'frames_budget': 30000, 'initial_pause': 3200,
        'no_savestate_or_text_selector_code_RNG_substitutions': True,
        'only_declared_work_room_fixture_enabled_no_earned_refit_assignment_or_recruitment_claim': True})
    sys.argv = ['headless_desmume_v193.py', '--rom', str(rom), '--out', str(folder),
        '--battery-save', str(donor), '--inputs-json', str(inputs), '--touchscreen',
        '--frames', '30000', '--capture-every', '999999', '--capture-at', '1', '60', '180', '3200',
        '--dump-capture-ram', '--dump-pause-ram', '--dump-ram', '--pause-at', '3200', '--allow-work-room-fixtures']
    adapter.main()
    assert sha(source.read_bytes()) == sha(donor.read_bytes()) == digest


if __name__ == '__main__':
    main()
