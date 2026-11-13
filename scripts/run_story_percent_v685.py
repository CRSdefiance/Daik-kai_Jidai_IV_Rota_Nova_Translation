"""Current Maria complete scene and inherited ordinary New Game regression."""

import argparse
import sys
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts import headless_desmume_v193 as harness
from scripts.prepare_story_percent_v685 import ROOT
from scripts.run_village_visits_v664 import CAP
from scripts.verify_story_percent_v685 import ROM
from scripts.verify_village_wrap_v608 import read, save


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('case', choices=('maria', 'baseline', 'ordinary'))
    case = parser.parse_args().case
    static = read(ROOT / 'static_release_proof.json')
    assert sha(ROM.read_bytes()) == static['candidate_sha256']
    assert sha(Path('translations/release_stack.json').read_bytes()) == static['registry_sha256']
    maria = read('work/analysis/maria_intro_v684/preflight.json')
    if case == 'ordinary':
        old = read(CAP / 'wedding_dialogue_v678_ordinary/capture_report.json')
        inputs = ROOT / 'ordinary_inputs.json'
        save(inputs, old['scripted_input_schedule'])
        config = {'frames': old['frames'], 'inputs': str(inputs),
                  'capture_frames': sorted({r['frame'] for r in old['frames_captured']})}
    else:
        config = read('work/analysis/maria_intro_v684/run_config.json')
    folder = CAP / ('story_percent_v685_' + case)
    assert not folder.exists()
    folder.mkdir()
    save(folder / 'run_contract.json', {'case': case, 'config': config,
        'candidate_sha256': static['candidate_sha256'], 'inputs_sha256': sha(Path(config['inputs']).read_bytes()),
        'runner_sha256': sha(Path(__file__).read_bytes()),
        'existing_Maria_system_unlock_save_not_earned': case != 'ordinary'})
    sys.argv = ['headless_desmume_v193.py', '--rom', str(ROM), '--out', str(folder),
        '--frames', str(config['frames']), '--inputs-json', config['inputs'], '--touchscreen',
        '--capture-every', '999999', '--capture-at', *map(str, config['capture_frames']), '--dump-ram']
    if case != 'ordinary':
        assert sha(Path(maria['donor']).read_bytes()) == maria['donor_sha256']
        # The same byte-exact save fixture is rebound to the new candidate.
        manifest_path = ROOT / 'unlock_manifest_v685.json'
        manifest = read(maria['unlock_manifest'])
        manifest.update(production_ROM=str(ROM), production_ROM_sha256=static['candidate_sha256'])
        save(manifest_path, manifest)
        sys.argv += ['--battery-save', maria['donor'], '--allow-gallery-fixtures',
                     '--gallery-save-fixture-manifest', str(manifest_path)]
        if case == 'maria':
            sys.argv += ['--dump-capture-ram']
    harness.main()
    print('V685 terminal:', case, flush=True)


if __name__ == '__main__':
    main()
