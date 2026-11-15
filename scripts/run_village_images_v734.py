"""Current Ezo arrival/story/password/port replay with a complete request trace."""

import argparse
import ctypes as ct
import io
import json
import struct
import sys
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts import check_file_requests_v681 as checks
from scripts import headless_desmume_v193 as harness
from scripts import native_location_fixture_v519 as location
from scripts import native_village_visits_v664 as old_location
from scripts.inspect_committed_gpu_v646 import CORE, CORE_SHA
from scripts.inspect_resource_dispatch_v668 import tables
from scripts.observe_file_requests_v681 import assemble
from scripts.observe_village_images_v734 import ROM, ROOT, Observer
from scripts.record_memory_streams_v682 import copy
from scripts.verify_village_wrap_v608 import read, save

CAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193')
ARM_SHA = 'af4ce98637f6febb4e3e0dab7ce63f5984050deb267713b1c741f5005eb98e41'


def relocate(arm, raw, village):
    assert sha(arm) == ARM_SHA and village == 18
    reference = NdsImage.open('out/all_routes_combined_v653_candidate.nds').read_file('/__arm9__.bin')
    assert sha(reference) == old_location.ARM
    assert all(arm[a:b] == reference[a:b] for a, b in old_location.SPANS)
    after, receipt = old_location.relocate(reference, raw, village)
    receipt.update(actual_current_ARM9_sha256=sha(arm),
        V734_current_guard='pinned-V712-original-coordinate-functions-exact-V653',
        unchanged_V664_helper_sha256=sha(Path('scripts/native_village_visits_v664.py').read_bytes()))
    return after, receipt


def prepare():
    ROOT.mkdir(parents=True, exist_ok=True)
    assert not (ROOT / 'preflight.json').exists()
    rom, clean = NdsImage.open(ROM), NdsImage.open('work/clean.nds')
    arm, original = (r.read_file('/__arm9__.bin') for r in (rom, clean))
    assert sha(arm) == ARM_SHA
    reference = NdsImage.open('out/all_routes_combined_v653_candidate.nds')
    refarm = reference.read_file('/__arm9__.bin')
    assert all(arm[a:b] == refarm[a:b] for a, b in old_location.SPANS)
    assert rom.read_file('/data/WORLDMAP.DK4') == reference.read_file('/data/WORLDMAP.DK4') == clean.read_file('/data/WORLDMAP.DK4')
    oldproof = Path('work/analysis/village_development_v665/proof.json')
    row = next(r for r in read(oldproof)['all24_development_cases'] if r['index'] == 18)
    report_path, controller_path = Path(row['report']['path']), Path(row['controller']['path'])
    assert sha(report_path.read_bytes()) == row['report']['sha256']
    assert sha(controller_path.read_bytes()) == row['controller']['sha256']
    report, controller = read(report_path), read(controller_path)
    assert report['frames'] == 16700 and controller['error'] is None
    source = report['battery_save_preloaded']
    donor = Path(source['source'])
    assert sha(donor.read_bytes()) == source['source_sha256'] == '958d6e36f521e4f8b0940e0c60a4de08df8fcae71f9e6f6e3271156cf25beadb'
    copied = ROOT / 'Ezo_source_TEST_ONLY.dsv'
    copy(donor, copied)
    save(ROOT / 'inputs.json', report['scripted_input_schedule'])
    commands = [{k: v for k, v in r['command'].items() if k in ('until', 'location_town', 'stop')}
        for r in controller['commands']]
    assert commands[-1] == {'stop': True}
    assert all(c.get('location_town', 18) == 18 for c in commands)
    save(ROOT / 'commands.json', commands)
    raw = CORE.read_bytes()
    assert sha(raw) == CORE_SHA
    base, table = tables(raw)
    targets = []
    declarations = ((0x020DED50, 'filename'), (0x020DEDA0, 'numeric_ID'), (0x020DEE1C, 'direct_range'),
        (0x0204704C, 'raw_SLACK_entry'), (0x0209EDEC, 'raw_SLACK_known_return'),
        (0x02028B74, 'event_still_formatter'))
    ranges = [(0xDED50, 0xDEEE0), (0x4704C, 0x470B4), (0x9ED3C, 0x9EE94), (0x28B74, 0x28BAC)]
    assert all(arm[a:b] == original[a:b] for a, b in ranges)
    for pc, name in declarations:
        word = struct.unpack_from('<I', arm, pc - 0x02000000)[0]
        index = ((word >> 16) & 0xFF0) | ((word >> 4) & 15)
        targets.append({'PC': pc, 'name': name, 'word': word, 'instruction_index': index,
            'handler_RVA': struct.unpack_from('<Q', raw, table['file_offset'] + index * 8)[0] - base})
    save(ROOT / 'source_contract.json', {'targets': targets, 'interpreter_table': table,
        'core_sha256': CORE_SHA, 'exact_clean_native_ranges': ranges,
        'assembler_sha256': sha(Path('scripts/observe_file_requests_v681.py').read_bytes()),
        'mapped_read_helper_sha256': sha(Path('scripts/trace_file_ids_v683.py').read_bytes()),
        'file_IDs': {str(i): p for p, i in rom.path_map().items()}})
    previous_root, previous_assemble = checks.ROOT, checks.assemble

    def grouped(cpu, header, callback, original_handler, selected, address):
        group = [t for t in targets if t['instruction_index'] == selected[0]['instruction_index']]
        return assemble(cpu, header, callback, original_handler, group, address)

    checks.ROOT, checks.assemble = ROOT, grouped
    try:
        checks.main()
    finally:
        checks.ROOT, checks.assemble = previous_root, previous_assemble
    assert len(read(ROOT / 'native_prefix_controls.json')['native_host_cases']) == 30
    save(ROOT / 'preflight.json', {'candidate': str(ROM), 'candidate_sha256': sha(ROM.read_bytes()),
        'release_hashes': {str(p): sha(p.read_bytes()) for p in (ROM, ROM.with_suffix('.manifest.json'),
            ROM.with_suffix('.xdelta'), Path('translations/release_stack.json'),
            Path('out/raphael_natural_v2_accepted_base.nds'))},
        'historical_proof': str(oldproof), 'historical_proof_sha256': sha(oldproof.read_bytes()),
        'historical_report': str(report_path), 'historical_report_sha256': sha(report_path.read_bytes()),
        'historical_controller': str(controller_path), 'historical_controller_sha256': sha(controller_path.read_bytes()),
        'original_donor': str(donor), 'original_donor_sha256': sha(donor.read_bytes()),
        'test_copy': str(copied), 'test_copy_sha256': sha(copied.read_bytes()),
        'historical_successful_phases': row['phases'], 'frames': 16700,
        'runner_sha256': sha(Path(__file__).read_bytes()),
        'observer_sha256': sha(Path('scripts/observe_village_images_v734.py').read_bytes()),
        'shared_harness_sha256': sha(Path('scripts/headless_desmume_v193.py').read_bytes()),
        'location_helper_sha256': sha(Path('scripts/native_village_visits_v664.py').read_bytes()),
        'inputs_sha256': sha((ROOT / 'inputs.json').read_bytes()),
        'commands_sha256': sha((ROOT / 'commands.json').read_bytes()),
        'only_coordinate_fixtures_no_password_development_or_scene_flag_writes': True,
        'full_goal_complete': False})
    print('V734 exact Ezo schedule,protected source copy,six observation targets and30 grouped native controls ready.')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=('prepare', 'baseline', 'observed'))
    args = parser.parse_args()
    if args.mode == 'prepare':
        prepare()
        return
    pre = read(ROOT / 'preflight.json')
    assert pre['runner_sha256'] == sha(Path(__file__).read_bytes())
    assert pre['observer_sha256'] == sha(Path('scripts/observe_village_images_v734.py').read_bytes())
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    folder = CAP / ('village_images_v734_Ezo_' + args.mode)
    assert not folder.exists()
    observers = []

    class CtypesProxy:
        def __getattr__(self, name):
            return getattr(ct, name)

        def CDLL(self, path, *extra, **kwargs):
            core = ct.CDLL(path, *extra, **kwargs)
            if str(path).lower().endswith('desmume_libretro.dll'):
                observer = Observer(core, folder / 'observer')
                observer.install()
                observers.append(observer)
                original_run = core.retro_run
                original_run.restype = None

                def run():
                    observer.next_frame()
                    original_run()
                core.retro_run = run
            return core

    old_ct, old_stdin, old_relocate = harness.ct, sys.stdin, location.relocate
    if args.mode == 'observed':
        harness.ct = CtypesProxy()
    location.relocate = relocate
    sys.stdin = io.StringIO(''.join(json.dumps(c) + '\n' for c in read(ROOT / 'commands.json')))
    sys.argv = ['headless_desmume_v193.py', '--rom', str(ROM), '--out', str(folder),
        '--frames', '16700', '--inputs-json', str(ROOT / 'inputs.json'), '--battery-save', pre['test_copy'],
        '--pause-at', '5200', '--allow-location-fixtures', '--touchscreen', '--capture-every', '999999',
        '--dump-pause-ram', '--dump-ram', '--dump-native-state']
    try:
        harness.main()
    finally:
        harness.ct, sys.stdin, location.relocate = old_ct, old_stdin, old_relocate
        for observer in observers:
            observer.close()
    for observer in observers:
        observer.save()
    for key in ('original_donor', 'test_copy'):
        assert sha(Path(pre[key]).read_bytes()) == pre[key + '_sha256']
    print('V734 Ezo terminal', args.mode, flush=True)


if __name__ == '__main__':
    main()
