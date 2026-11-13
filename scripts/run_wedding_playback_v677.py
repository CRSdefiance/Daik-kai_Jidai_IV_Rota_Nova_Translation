"""Isolated original Lil chapter70 playback, with a separately disclosed CPU argument fixture."""

import argparse
import ctypes as ct
import sys
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts import headless_desmume_v193 as harness
from scripts import inspect_desmume_gpu_v630 as gpu
from scripts import observe_graphic_paints_v669 as paints
from scripts.inspect_committed_gpu_v646 import export
from scripts.native_wedding_fixture_v677 import ROOT, Fixture
from scripts.observe_wedding_runtime_v676 import Observer
from scripts.run_village_visits_v664 import CAP
from scripts.verify_village_wrap_v608 import read, save


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', choices=('pilot', 'observed', 'fixture_baseline', 'disabled'), default='pilot')
    parser.add_argument('--tag', default='')
    args = parser.parse_args()
    pre = read(ROOT / 'preflight.json')
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    assert len(read(ROOT / 'fixture_controls.json')['native_prefix_cases']) == 5
    assert not args.tag or args.tag.replace('_', '').isalnum()
    folder = CAP / ('wedding_playback_v677_' + args.mode + ('_' + args.tag if args.tag else ''))
    assert not folder.exists()
    folder.mkdir(parents=True)
    observed, enabled = args.mode in ('pilot', 'observed'), args.mode != 'disabled'
    if args.mode == 'pilot':
        tail = ['--frames', '60000', '--inputs-json', str(ROOT / 'pilot_inputs.json'),
                '--capture-every', '999999', '--pause-at', '2500', '--dump-pause-ram', '--dump-ram']
    elif args.mode == 'disabled':
        config = read('work/analysis/wedding_movie_v676/runtime_contract.json')
        tail = ['--frames', '4000', '--inputs-json', str(ROOT / 'pilot_inputs.json'),
                '--capture-every', '999999', '--capture-at', *map(str, config['capture_frames']),
                '--dump-capture-ram', '--dump-ram']
    else:
        config = read(ROOT / 'playback_config.json')
        assert sha(Path(config['inputs']).read_bytes()) == config['inputs_sha256']
        tail = ['--frames', str(config['frames']), '--inputs-json', config['inputs'],
                '--capture-every', '999999', '--capture-at', *map(str, config['capture_frames']),
                '--dump-ram']
        if config.get('dump_capture_ram'):
            tail += ['--dump-capture-ram']
        if config.get('capture_window'):
            tail += ['--capture-window', *map(str, config['capture_window'])]
        if observed:
            tail += ['--capture-gpu-state-at', *map(str, config['gpu_frames'])]
    save(folder / 'run_contract.json', {'mode': args.mode, 'fixture_enabled': enabled,
        'original_image_entry_observation_enabled': observed,
        'preflight_sha256': sha((ROOT / 'preflight.json').read_bytes()),
        'runner_sha256': sha(Path(__file__).read_bytes()),
        'fixture_sha256': sha(Path('scripts/native_wedding_fixture_v677.py').read_bytes()),
        'observer_sha256': sha(Path('scripts/observe_wedding_runtime_v676.py').read_bytes()),
        'source_contract_sha256': sha((ROOT / 'source_contract.json').read_bytes()),
        'no_ROM_script_or_movie_file_substitution': True,
        'isolated_original_chapter_loader_argument_not_earned_story_completion': True})
    loader, old_root, old_export, installations = ct.CDLL, paints.ROOT, gpu.export, []
    paints.ROOT = ROOT

    def combined(core, directory, expected_ram):
        value = old_export(core, directory, expected_ram)
        committed = export(core, directory, expected_ram)
        data = {k: v for k, v in value.items() if k not in ('path', 'sha256')}
        data['read_only_committed_geometry'] = committed
        path = Path(value['path'])
        save(path, data)
        return {'path': str(path), 'sha256': sha(path.read_bytes()), **data}

    def loaded(path, *extra, **kwargs):
        core = loader(path, *extra, **kwargs)
        if str(path).lower().endswith('desmume_libretro.dll'):
            observer = Observer(core, folder / 'observer', capacity=1000000) if observed else None
            if observer:
                observer.install()
            fixture = Fixture(core, folder / 'chapter_fixture', pre['candidate'], enabled=enabled)
            if observer:
                assert fixture.original == observer.code_address
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

    ct.CDLL = loaded
    if args.mode == 'observed':
        gpu.export = combined
    sys.argv = ['headless_desmume_v193.py', '--rom', pre['candidate'], '--out', str(folder), *tail]
    try:
        harness.main()
    finally:
        ct.CDLL, gpu.export = loader, old_export
        for fixture, observer in installations:
            fixture.close()
            if observer:
                observer.close()
    for fixture, observer in installations:
        fixture.save()
        if observer:
            observer.save()
    paints.ROOT = old_root
    assert len(installations) == 1
    fixture = installations[0][0]
    assert fixture.applied == enabled
    rp = folder / 'capture_report.json'
    report = read(rp)
    report['isolated_chapter_loader_fixture'] = {'enabled': enabled, 'applied': fixture.applied,
        'receipt': str(folder / 'chapter_fixture/fixture.json'),
        'receipt_sha256': sha((folder / 'chapter_fixture/fixture.json').read_bytes()),
        'original_captain2_request22_to70_only_ARM9_R1_at_original_loader': enabled,
        'earned_wedding_or_route_completion_verified': False}
    if enabled:
        report['synthetic_original_chapter_loader_fixture'] = True
        report['earned_completion_verified'] = False
    save(rp, report)
    print('V677 terminal:', args.mode, 'chapter fixture applied:', fixture.applied, flush=True)


if __name__ == '__main__':
    main()
