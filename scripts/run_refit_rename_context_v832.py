"""Observe original rename prompts with ordinary input and a disposable save."""

import sys
from pathlib import Path
from shutil import copy2

from dk4tool.patch.grand_race_menu_release import sha
from scripts import headless_desmume_v193 as harness
from scripts.context_refit_dialogue_v832 import ROOT, ROM
from scripts.verify_village_wrap_v608 import read, save

FOLDER = Path('work/emulation_v193/refit_dialogue_v832_rename_context')


def main():
    assert not FOLDER.exists()
    old = read('work/analysis/refit_editorial_v831/donor_copy.json')
    source = Path(old['disposable_source'])
    assert sha(source.read_bytes()) == old['disposable_source_sha256']
    donor = ROOT / 'disposable_rename_source.dsv'
    assert not donor.exists()
    copy2(source, donor)
    inputs = [r for r in read('work/analysis/yard_selection_v705/full_inputs.json') if r['start'] <= 11901]
    inputs += [{'start': f, 'duration': 8, 'buttons': [b]} for f, b in
               ((12201, 'DOWN'), (12501, 'A'), (12801, 'A'), (13101, 'B'), (13401, 'B'), (13701, 'B'))]
    path = ROOT / 'rename_inputs.json'
    save(path, inputs)
    captures = [1, 3200, 11900, 12200, 12500, 12800, 13100, 13400, 13700, 14000]
    save(ROOT / 'rename_run_plan.json', {'candidate': str(ROM), 'candidate_sha256': sha(ROM.read_bytes()),
                                         'disposable_source': str(donor), 'donor_sha256': sha(donor.read_bytes()),
                                         'frames': 14000, 'captures': captures,
                                         'input_schedule': str(path), 'input_sha256': sha(path.read_bytes()),
                                         'no_new_code_RAM_or_gameplay_fixture': True,
                                         'source_save_provenance': old})
    sys.argv = ['headless_desmume_v193.py', '--rom', str(ROM), '--out', str(FOLDER),
                '--frames', '14000', '--inputs-json', str(path), '--touchscreen',
                '--battery-save', str(donor), '--capture-every', '999999',
                '--capture-at', *map(str, captures), '--dump-capture-ram', '--dump-ram']
    harness.main()
    assert sha(donor.read_bytes()) == old['disposable_source_sha256']
    assert sha(source.read_bytes()) == old['disposable_source_sha256']


if __name__ == '__main__':
    main()
