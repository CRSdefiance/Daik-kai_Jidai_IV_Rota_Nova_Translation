"""Follow the independently observed rename selector into native name entry."""

import sys
from pathlib import Path
from shutil import copy2

from dk4tool.patch.grand_race_menu_release import sha
from scripts import headless_desmume_v193 as harness
from scripts.context_refit_dialogue_v832 import ROOT, ROM
from scripts.verify_village_wrap_v608 import read, save

FOLDER = Path('work/emulation_v193/refit_dialogue_v832_name_entry')


def main():
    assert not FOLDER.exists()
    pre = read(ROOT / 'rename_run_plan.json')
    source = Path(pre['disposable_source'])
    assert sha(source.read_bytes()) == pre['donor_sha256']
    donor = ROOT / 'disposable_name_entry_source.dsv'
    assert not donor.exists()
    copy2(source, donor)
    inputs = [r for r in read(ROOT / 'rename_inputs.json') if r['start'] <= 12801]
    inputs += [{'start': f, 'duration': 8, 'buttons': [b]} for f, b in
               ((13101, 'A'), (13401, 'A'), (13701, 'B'), (14001, 'B'), (14301, 'B'))]
    path = ROOT / 'name_entry_inputs.json'
    save(path, inputs)
    captures = [3200, 11900, 12200, 12500, 12800, 13100, 13400, 13700, 14000, 14300, 14600]
    save(ROOT / 'name_entry_run_plan.json', {'candidate': str(ROM), 'candidate_sha256': sha(ROM.read_bytes()),
                                             'disposable_source': str(donor), 'donor_sha256': sha(donor.read_bytes()),
                                             'frames': 14600, 'captures': captures,
                                             'input_schedule': str(path), 'input_sha256': sha(path.read_bytes()),
                                             'no_new_code_RAM_or_gameplay_fixture': True,
                                             'observed_prefix_control': str(ROOT / 'rename_run_plan.json')})
    sys.argv = ['headless_desmume_v193.py', '--rom', str(ROM), '--out', str(FOLDER),
                '--frames', '14600', '--inputs-json', str(path), '--touchscreen',
                '--battery-save', str(donor), '--capture-every', '999999',
                '--capture-at', *map(str, captures), '--dump-capture-ram', '--dump-ram']
    harness.main()
    assert sha(donor.read_bytes()) == pre['donor_sha256']
    assert sha(source.read_bytes()) == pre['donor_sha256']


if __name__ == '__main__':
    main()
