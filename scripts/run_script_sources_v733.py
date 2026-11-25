"""Paired current ordinary New Game trace; no ROM, save or gameplay fixtures."""

import argparse
import ctypes as ct
import struct
import sys
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts import check_file_requests_v681 as checks
from scripts import headless_desmume_v193 as harness
from scripts.inspect_committed_gpu_v646 import CORE, CORE_SHA
from scripts.inspect_resource_dispatch_v668 import tables
from scripts.observe_script_sources_v733 import ROM, ROOT, Observer
from scripts.verify_village_wrap_v608 import read, save

CAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193')
FRAMES = [1, 60, 180, 900, 1200, 1500, 1600, 1800, 2000, 2100, 2400, 2800, 3200, 3600, 3900, 4000]


def prepare():
    ROOT.mkdir(parents=True, exist_ok=True)
    assert not (ROOT / 'preflight.json').exists()
    rom, clean = NdsImage.open(ROM), NdsImage.open('work/clean.nds')
    arm, original = (r.read_file('/__arm9__.bin') for r in (rom, clean))
    assert arm[0x24048:0x24118] == original[0x24048:0x24118]
    raw = CORE.read_bytes()
    assert sha(raw) == CORE_SHA
    native_base, table = tables(raw)
    targets = []
    for pc, name in ((0x02024070, 'before_command'), (0x02024074, 'after_command')):
        word = struct.unpack_from('<I', arm, pc - 0x02000000)[0]
        index = ((word >> 16) & 0xFF0) | ((word >> 4) & 15)
        targets.append({'PC': pc, 'name': name, 'word': word, 'instruction_index': index,
            'handler_RVA': struct.unpack_from('<Q', raw, table['file_offset'] + index * 8)[0] - native_base})
    save(ROOT / 'source_contract.json', {'targets': targets, 'interpreter_table': table,
        'core_sha256': CORE_SHA, 'original_loop_range': [0x24048, 0x24118],
        'original_filter_assembler': 'scripts/observe_file_requests_v681.py',
        'original_filter_assembler_sha256': sha(Path('scripts/observe_file_requests_v681.py').read_bytes()),
        'CPU_memory_read_helper': 'scripts/trace_file_ids_v683.py',
        'CPU_memory_read_helper_sha256': sha(Path('scripts/trace_file_ids_v683.py').read_bytes())})
    previous_root = checks.ROOT
    checks.ROOT = ROOT
    try:
        checks.main()
    finally:
        checks.ROOT = previous_root
    save(ROOT / 'inputs.json', read('work/analysis/file_requests_v681/ordinary_inputs.json'))
    save(ROOT / 'preflight.json', {'candidate': str(ROM), 'candidate_sha256': sha(ROM.read_bytes()),
        'release_hashes': {str(p): sha(p.read_bytes()) for p in (ROM, ROM.with_suffix('.manifest.json'),
            ROM.with_suffix('.xdelta'), Path('translations/release_stack.json'),
            Path('out/raphael_natural_v2_accepted_base.nds'))},
        'runner_sha256': sha(Path(__file__).read_bytes()),
        'observer_sha256': sha(Path('scripts/observe_script_sources_v733.py').read_bytes()),
        'shared_harness_sha256': sha(Path('scripts/headless_desmume_v193.py').read_bytes()),
        'inputs_sha256': sha((ROOT / 'inputs.json').read_bytes()), 'capture_frames': FRAMES,
        'frames': 4000, 'no_save_savestate_or_gameplay_fixture': True, 'full_goal_complete': False})


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=('prepare', 'baseline', 'observed'))
    args = parser.parse_args()
    if args.mode == 'prepare':
        prepare()
        return
    pre = read(ROOT / 'preflight.json')
    assert pre['runner_sha256'] == sha(Path(__file__).read_bytes())
    assert pre['observer_sha256'] == sha(Path('scripts/observe_script_sources_v733.py').read_bytes())
    for p, digest in pre['release_hashes'].items():
        assert sha(Path(p).read_bytes()) == digest
    folder = CAP / ('script_sources_v733_' + args.mode)
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

    previous_ct = harness.ct
    if args.mode == 'observed':
        harness.ct = CtypesProxy()
    sys.argv = ['headless_desmume_v193.py', '--rom', str(ROM), '--out', str(folder),
        '--frames', '4000', '--inputs-json', str(ROOT / 'inputs.json'), '--touchscreen',
        '--capture-every', '999999', '--capture-at', *map(str, FRAMES), '--dump-ram']
    try:
        harness.main()
    finally:
        harness.ct = previous_ct
        for observer in observers:
            observer.close()
    for observer in observers:
        observer.save()
    print('V733 terminal', args.mode, flush=True)


if __name__ == '__main__':
    main()
