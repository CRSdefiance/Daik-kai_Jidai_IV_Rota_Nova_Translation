"""Fresh later Rafael test-save cold boot with an explicit optional counter fixture."""

import argparse
import sys
from pathlib import Path
from shutil import copy2

from dk4tool.patch.grand_race_menu_release import sha
from scripts import run_deck_elapsed_adapter_v839 as adapter
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/personal_chatter_v839')
CAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--version', type=int, choices=(834,838), default=838)
    parser.add_argument('--label', required=True)
    args = parser.parse_args()
    assert args.label and all(c.isalnum() or c == '_' for c in args.label)
    ROOT.mkdir(parents=True, exist_ok=True)
    rom = Path(f'out/all_routes_combined_v{args.version}_candidate.nds')
    assert sha(rom.read_bytes()) == read(rom.with_suffix('.manifest.json'))['candidate_sha256']
    folder = CAP / f'personal_activity_v839_{args.version}_{args.label}'
    source = Path('E:/Rota Nova translations/Saves/Test fixtures/V827 Rafael Istanbul after introduction.dsv')
    donor = ROOT / f'disposable_{args.version}_{args.label}.dsv'
    assert not folder.exists() and not donor.exists()
    digest = sha(source.read_bytes())
    provenance = read('work/analysis/ceremony_istanbul_v827/Rafael_Lil_normal_saves_pending_reload.json')['rows'][0]
    assert digest == provenance['sha256'] and str(source) == str(Path(provenance['normal_save']))
    copy2(source, donor)
    assert sha(donor.read_bytes()) == digest
    inputs = Path('work/analysis/ceremony_heroes_v825/load_save_inputs.json')
    plan = ROOT / f'{args.version}_{args.label}_run_plan.json'
    save(plan, {'ROM': str(rom), 'ROM_sha256': sha(rom.read_bytes()), 'folder': str(folder),
        'source_donor': str(source), 'source_donor_sha256': digest, 'disposable_source': str(donor),
        'source_has_prior_disclosed_ceremony_location_calendar_fixtures_no_earned_progress_claim': True,
        'ordinary_in_game_saved_donor': provenance, 'inputs': str(inputs),
        'inputs_sha256': sha(inputs.read_bytes()), 'frames_budget': 30000, 'initial_pause': 3200,
        'no_savestate_or_text_selector_code_RNG_substitutions': True,
        'optional_Deck_counter_fixture_must_be_explicitly_requested_at_pause': True})
    sys.argv = ['headless_desmume_v193.py', '--rom', str(rom), '--out', str(folder),
        '--battery-save', str(donor), '--inputs-json', str(inputs), '--touchscreen',
        '--frames', '30000', '--capture-every', '999999', '--capture-at', '1', '60', '180', '3200',
        '--dump-capture-ram', '--dump-pause-ram', '--dump-ram', '--pause-at', '3200',
        '--allow-deck-elapsed-fixtures']
    adapter.main()
    assert sha(source.read_bytes()) == sha(donor.read_bytes()) == digest


if __name__ == '__main__':
    main()
