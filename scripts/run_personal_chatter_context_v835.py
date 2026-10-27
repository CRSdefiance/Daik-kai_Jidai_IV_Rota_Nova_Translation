"""Ordinary current-ROM Deck navigation with a protected Rafael test-save copy."""

import sys
from pathlib import Path
from shutil import copy2

from dk4tool.patch.grand_race_menu_release import sha
from scripts import headless_desmume_v193 as harness
from scripts.prepare_personal_chatter_v835 import ROOT, ROM
from scripts.verify_village_wrap_v608 import read, save


def main():
    source = Path('E:/Rota Nova translations/Saves/rafael-twisted-horn-map2-v440.dsv')
    donor = ROOT / 'disposable_Rafael_source.dsv'
    folder = Path('E:/Rota Nova translations/Generated/work/emulation_v193/personal_chatter_v835_Rafael_context')
    assert not donor.exists() and not folder.exists()
    source_hash = sha(source.read_bytes())
    copy2(source, donor)
    assert sha(donor.read_bytes()) == source_hash
    prior = read('E:/Rota Nova translations/Generated/work/emulation_v193/deck_gender_v692_hodram_pilot2/capture_report.json')
    inputs = [r for r in prior['scripted_input_schedule'] if r['start'] <= 6801]
    path = ROOT / 'Rafael_context_inputs.json'
    save(path, inputs)
    save(ROOT / 'Rafael_context_run_plan.json', {
        'ROM': str(ROM), 'ROM_sha256': sha(ROM.read_bytes()), 'source_donor': str(source),
        'source_donor_sha256': source_hash, 'disposable_source': str(donor), 'folder': str(folder),
        'inputs': str(path), 'inputs_sha256': sha(path.read_bytes()), 'pause_at': 7200,
        'no_new_gameplay_fixtures': True, 'original_donor_never_passed_to_emulator': True,
        'provenance': 'Retained Rafael test donor from V440;earned progression or unlocks are not inferred. No savestate or new RAM/code fixture.'})
    sys.argv = ['headless_desmume_v193.py', '--rom', str(ROM), '--out', str(folder),
                '--battery-save', str(donor), '--inputs-json', str(path), '--touchscreen', '--frames', '20000',
                '--capture-every', '999999', '--capture-at', '3200', '5200', '5600', '6000', '6400', '6800', '7200',
                '--dump-capture-ram', '--dump-pause-ram', '--dump-ram', '--pause-at', '7200']
    harness.main()
    assert sha(source.read_bytes()) == sha(donor.read_bytes()) == source_hash


if __name__ == '__main__':
    main()
