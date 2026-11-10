"""Cold-boot the separate font candidate using retained ordinary startup inputs."""

import argparse
import json
import sys
from pathlib import Path
from shutil import copy2

from dk4tool.patch.grand_race_menu_release import sha
from scripts import headless_desmume_v193 as harness

ROOT = Path('work/font_punctuation_20261027')
ROM = Path('out/font_v2_punctuation_one_pixel_20261027_test.nds')


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--case', choices=['newgame', 'town'], required=True)
    case = parser.parse_args().case
    source_plan = Path('work/analysis/lil_B179_runs_v4751') / (case + '_plan.json')
    prior = read(source_plan)
    if case == 'newgame':
        prior['captures'] = sorted(set(prior['captures'] + [1100]))
    inputs = Path(prior['inputs'])
    assert sha(inputs.read_bytes()) == prior['inputs_sha256']
    manifest = read(ROM.with_suffix('.manifest.json'))
    digest = sha(ROM.read_bytes())
    assert manifest['candidate_sha256'] == digest
    output = ROOT / ('cold_boot_' + case)
    assert not output.exists()
    battery, source, donor = [], None, None
    if case == 'town':
        source = Path(prior['source_donor'])
        assert sha(source.read_bytes()) == prior['source_donor_sha256']
        donor = ROOT / 'town_disposable.dsv'
        assert not donor.exists()
        copy2(source, donor)
        battery = ['--battery-save', str(donor)]
    save(ROOT / (case + '_plan.json'), dict(candidate=str(ROM), candidate_sha256=digest,
        frames=prior['frames'], captures=prior['captures'], inputs=str(inputs),
        inputs_sha256=sha(inputs.read_bytes()), source_plan=str(source_plan),
        source_plan_sha256=sha(source_plan.read_bytes()),
        battery_source=str(source) if source else None,
        inherited_town_fixture_not_earned_gameplay=case == 'town',
        no_savestate_or_new_RAM_code_gameplay_fixture=True))
    sys.argv = ['headless_desmume_v193.py', '--rom', str(ROM), '--out', str(output),
        '--frames', str(prior['frames']), '--inputs-json', str(inputs), *battery,
        '--touchscreen', '--capture-every', '999999', '--capture-at', *map(str, prior['captures'])]
    harness.main()
    report = read(output / 'capture_report.json')
    assert report['ROM_sha256'] == digest and report['cold_boot'] and not report['savestate_loaded']
    assert not report['callback_errors'] and report['frames'] == prior['frames']
    if source:
        assert sha(source.read_bytes()) == sha(donor.read_bytes()) == prior['source_donor_sha256']
    save(ROOT / (case + '_terminal.json'), dict(terminal=True, frames=report['frames'],
        candidate_sha256=digest, report=str(output / 'capture_report.json'),
        report_sha256=sha((output / 'capture_report.json').read_bytes()),
        battery_sources_preserved=True, hardware_or_full_route_verification=False))
    print(case, 'cold boot complete', flush=True)
