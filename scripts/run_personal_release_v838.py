"""Cold-boot V838 startup or inspect the ordinary Deck path on a disposable save."""

import argparse
import sys
from pathlib import Path
from shutil import copy2

from dk4tool.patch.grand_race_menu_release import sha
from scripts import headless_desmume_v193 as harness
from scripts.prepare_personal_release_v838 import ROOT
from scripts.verify_village_wrap_v608 import read, save

CAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193')
ROM = Path('out/all_routes_combined_v838_candidate.nds')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--case', choices=('newgame', 'deck'), required=True)
    parser.add_argument('--run-label', default='')
    args = parser.parse_args()
    assert all(c.isalnum() or c == '_' for c in args.run_label)
    suffix = '_' + args.run_label if args.run_label else ''
    assert sha(ROM.read_bytes()) == read(ROM.with_suffix('.manifest.json'))['candidate_sha256']
    folder = CAP / f'personal_chatter_v838_{args.case}{suffix}'
    assert not folder.exists()
    donor_args, more, donor = [], [], None
    if args.case == 'newgame':
        events = read('work/analysis/cliff_editorial_v829/ordinary_newgame_inputs.json')
        frames, captures = 4000, [1, 60, 180, 1600, 2000, 3200, 4000]
    else:
        source = Path('E:/Rota Nova translations/Saves/rafael-twisted-horn-map2-v440.dsv')
        donor = ROOT / f'disposable_deck{suffix}_source.dsv'
        assert not donor.exists()
        digest = sha(source.read_bytes())
        copy2(source, donor)
        assert sha(donor.read_bytes()) == digest
        donor_args = ['--battery-save', str(donor)]
        prior = read(CAP / 'personal_chatter_v835_Rafael_context/capture_report.json')
        events = [e for e in prior['scripted_input_schedule'] if e['start'] <= 10001]
        frames, captures = 40000, [1, 60, 180, 3200, 7600, 9200, 9600, 10000, 10400]
        more = ['--pause-at', '10400', '--dump-pause-ram']
        save(ROOT / f'deck{suffix}_donor.json', {'source': str(source), 'source_sha256': digest,
             'disposable_source': str(donor), 'disposable_source_sha256': digest,
             'original_donor_never_passed_to_emulator': True,
             'no_new_RAM_code_text_or_eligibility_fixtures': True})
    inputs = ROOT / f'{args.case}{suffix}_inputs.json'
    save(inputs, events)
    save(ROOT / f'{args.case}{suffix}_run_plan.json', {
        'candidate': str(ROM), 'candidate_sha256': sha(ROM.read_bytes()), 'folder': str(folder),
        'frames_budget': frames, 'capture_at': captures, 'inputs': str(inputs),
        'input_sha256': sha(inputs.read_bytes()), 'no_savestate': True,
        'actual_revised_activity_display_not_assumed': True})
    sys.argv = ['headless_desmume_v193.py', '--rom', str(ROM), '--out', str(folder),
                '--frames', str(frames), '--inputs-json', str(inputs), '--touchscreen',
                '--capture-every', '999999', '--capture-at', *map(str, captures),
                '--dump-capture-ram', '--dump-ram', *donor_args, *more]
    harness.main()
    if donor:
        assert sha(donor.read_bytes()) == sha(source.read_bytes()) == digest


if __name__ == '__main__':
    main()
