"""Cold boot changed wedding chapter or ordinary title/story/town regression."""

import argparse
import ctypes as ct
import sys
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts import headless_desmume_v193 as harness
from scripts import observe_graphic_paints_v669 as paints
from scripts.native_wedding_fixture_v677 import Fixture
from scripts.observe_wedding_runtime_v676 import Observer
from scripts.prepare_wedding_dialogue_v678 import ROOT
from scripts.run_village_visits_v664 import CAP
from scripts.verify_village_wrap_v608 import read, save
from scripts.verify_wedding_dialogue_v678 import ROM


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=('wedding', 'baseline', 'ordinary'))
    mode = parser.parse_args().mode
    proof = read(ROOT / 'static_release_proof.json')
    assert sha(ROM.read_bytes()) == proof['candidate_sha256']
    folder = CAP / ('wedding_dialogue_v678_' + mode)
    assert not folder.exists()
    folder.mkdir()
    original = read('work/analysis/wedding_playback_v677/playback_config.json')
    if mode == 'ordinary':
        prior = CAP / 'village_consistency_v666_newgame/capture_report.json'
        config = read(prior)
        inputs = ROOT / 'ordinary_inputs.json'
        save(inputs, config['scripted_input_schedule'])
        frames, captures = config['frames'], sorted({s['frame'] for s in config['frames_captured']})
    else:
        inputs = Path(original['inputs'])
        assert sha(inputs.read_bytes()) == original['inputs_sha256']
        frames = original['frames']
        captures = sorted(set(original['capture_frames']) | {11300, 11500, 11700, 14100, 14300, 14500})
    source_contract = ROOT / 'source_contract.json'
    source = Path('work/analysis/wedding_playback_v677/source_contract.json')
    if not source_contract.exists():
        source_contract.write_bytes(source.read_bytes())
    assert source_contract.read_bytes() == source.read_bytes()
    controls = Path('work/analysis/wedding_playback_v677/fixture_controls.json')
    assert len(read(controls)['native_prefix_cases']) == 5
    save(folder / 'run_contract.json', {
        'mode': mode, 'candidate': str(ROM), 'candidate_sha256': proof['candidate_sha256'],
        'runner_sha256': sha(Path(__file__).read_bytes()), 'inputs': str(inputs),
        'inputs_sha256': sha(inputs.read_bytes()), 'frames': frames, 'capture_frames': captures,
        'fixture_sha256': sha(Path('scripts/native_wedding_fixture_v677.py').read_bytes()),
        'observer_sha256': sha(Path('scripts/observe_wedding_runtime_v676.py').read_bytes()),
        'source_contract_sha256': sha(source_contract.read_bytes()),
        'isolated_chapter_argument_not_earned_wedding': mode != 'ordinary',
        'no_save_or_savestate': True, 'read_only_image_observer': mode == 'wedding'})
    loader, old_root, installations = ct.CDLL, paints.ROOT, []
    paints.ROOT = ROOT

    def loaded(path, *args, **kwargs):
        core = loader(path, *args, **kwargs)
        if str(path).lower().endswith('desmume_libretro.dll'):
            observer = Observer(core, folder / 'observer', capacity=1000000) if mode == 'wedding' else None
            if observer:
                observer.install()
            fixture = Fixture(core, folder / 'chapter_fixture', ROM)
            fixture.install()
            original_run = core.retro_run
            original_run.restype = None

            def run():
                if observer:
                    observer.next_frame()
                fixture.next_frame()
                original_run()
            core.retro_run = run
            installations.append((fixture, observer))
        return core

    if mode != 'ordinary':
        ct.CDLL = loaded
    sys.argv = ['headless_desmume_v193.py', '--rom', str(ROM), '--out', str(folder),
        '--frames', str(frames), '--inputs-json', str(inputs), '--touchscreen',
        '--capture-every', '999999', '--capture-at', *map(str, captures), '--dump-ram']
    if mode == 'wedding':
        sys.argv += ['--dump-capture-ram']
    try:
        harness.main()
    finally:
        ct.CDLL = loader
        for fixture, observer in installations:
            fixture.close()
            if observer:
                observer.close()
    for fixture, observer in installations:
        fixture.save()
        assert fixture.applied
        if observer:
            observer.save()
    paints.ROOT = old_root
    if mode != 'ordinary':
        rp = folder / 'capture_report.json'
        report = read(rp)
        report['synthetic_original_chapter_loader_fixture'] = True
        report['earned_completion_verified'] = False
        report['fixture_receipt'] = str(folder / 'chapter_fixture/fixture.json')
        save(rp, report)
    print('V678 terminal:', mode, flush=True)


if __name__ == '__main__':
    main()
