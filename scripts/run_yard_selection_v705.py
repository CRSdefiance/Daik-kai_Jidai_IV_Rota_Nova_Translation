"""Replay ordinary five-ship Sell/Refit navigation with a read-only observer."""

import argparse
import ctypes as ct
import sys
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts import headless_desmume_v193 as harness
from scripts import observe_graphic_paints_v669 as paints
from scripts.run_room_gender_v694 import CAP, ROM
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/yard_selection_v705')


def prepare():
    pre = read(ROOT / 'preflight.json')
    pilot = CAP / 'yard_selection_v705_pilot_console/capture_report.json'
    report = read(pilot)
    assert report['frames'] == 19700 and report['ROM_sha256'] == pre['candidate_sha256']
    assert report['cold_boot'] and not report['callback_errors'] and not report['savestate_loaded']
    assert report['scripted_input_schedule'] == read(ROOT / 'full_inputs.json')
    assert not any(v for k, v in report.items() if k.startswith('synthetic_'))
    source = read(paints.ROOT / 'source_contract.json')
    current = NdsImage.open(ROM)
    old = NdsImage.open(paints.ROM)
    assert all(current.read_file(r['path']) == old.read_file(r['path']) for r in source['source_assets'])
    arm, original = current.read_file('/__arm9__.bin'), NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    assert all(arm[t['PC'] - 0x02000000:t['PC'] - 0x02000000 + 4]
        == original[t['PC'] - 0x02000000:t['PC'] - 0x02000000 + 4]
        for t in source['targets'] if t['PC'] >= 0x02000000)
    save(ROOT / 'host_controls.json', paints.controls())
    paths = ('scripts/run_yard_selection_v705.py', 'scripts/observe_graphic_paints_v669.py',
        str(paints.ROOT / 'source_contract.json'), str(ROOT / 'full_inputs.json'), str(ROOT / 'capture_frames.json'))
    save(ROOT / 'run_config.json', {'frames': 19700, 'inputs': str(ROOT / 'full_inputs.json'),
        'captures': read(ROOT / 'capture_frames.json'), 'pilot_report': str(pilot),
        'pilot_report_sha256': sha(pilot.read_bytes()), 'frozen_files': {p: sha(Path(p).read_bytes()) for p in paths},
        'whole_target_assets_exact_current_to_observer_version': True,
        'original_resource_source_and_crop_not_injected': True,
        'no_inventory_location_funds_health_story_or_outcome_fixture': True})
    print('V705 ordinary pilot terminal; 59 inputs, original observer source and native host controls frozen.', flush=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--prepare', action='store_true')
    parser.add_argument('--baseline', action='store_true')
    args = parser.parse_args()
    if args.prepare:
        prepare()
        return
    pre, config = read(ROOT / 'preflight.json'), read(ROOT / 'run_config.json')
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    for path, digest in config['frozen_files'].items():
        assert sha(Path(path).read_bytes()) == digest
    assert sha(Path(pre['donor']).read_bytes()) == pre['donor_sha256']
    suffix = 'baseline' if args.baseline else 'observed'
    folder = CAP / f'yard_selection_v705_{suffix}'
    assert not folder.exists()
    folder.mkdir()
    save(folder / 'run_contract.json', {'config': config, 'baseline': args.baseline,
        'runner_sha256': sha(Path(__file__).read_bytes()), 'ordinary_gameplay_inputs_only': True})
    loader, observers, frame = ct.CDLL, [], 0

    def loaded(path, *extra, **kwargs):
        core = loader(path, *extra, **kwargs)
        if not str(path).lower().endswith('desmume_libretro.dll'):
            return core
        observer = None if args.baseline else paints.Observer(core, folder / 'observer')
        if observer:
            observer.install()
            observers.append(observer)
        original_run = core.retro_run
        original_run.restype = None

        def run():
            nonlocal frame
            frame += 1
            if observer:
                observer.next_frame()
            original_run()
        core.retro_run = run
        return core

    ct.CDLL = loaded
    sys.argv = ['headless_desmume_v193.py', '--rom', pre['candidate'], '--out', str(folder),
        '--frames', str(config['frames']), '--inputs-json', config['inputs'], '--touchscreen',
        '--battery-save', pre['donor'], '--capture-every', '999999',
        '--capture-at', *map(str, config['captures']), '--dump-capture-ram', '--dump-pause-ram']
    try:
        harness.main()
    finally:
        ct.CDLL = loader
        for observer in observers:
            observer.close()
    for observer in observers:
        observer.save()
    assert frame == config['frames']
    print('V705 terminal', suffix, frame, flush=True)


if __name__ == '__main__':
    main()
