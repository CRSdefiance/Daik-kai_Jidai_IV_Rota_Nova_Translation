"""Read-only source rows for actual inherited equipment-border transition frames."""

import ctypes as ct
import sys
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts import headless_desmume_v193 as harness
from scripts.observe_transition_scanlines_v659 import Observer
from scripts.verify_village_wrap_v608 import read

ROOT = Path('work/analysis/equipment_cursor_v663')
OUT = Path('E:/Rota Nova translations/Generated/work/emulation_v193/equipment_cursor_v663_scanlines')


def main():
    pre = read(ROOT / 'preflight.json')
    phases = read(ROOT / 'phase_candidates.json')
    frames = phases['mixed_frames']
    assert frames
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    loader, installed = ct.CDLL, []

    def loaded(path, *args, **kwargs):
        core = loader(path, *args, **kwargs)
        if str(path).lower().endswith('desmume_libretro.dll'):
            observer = Observer(core, OUT / 'scanlines', frames)
            run_original = core.retro_run
            run_original.restype = None

            def run():
                observer.frame += 1
                if observer.frame == min(frames):
                    observer.install()
                run_original()
                if observer.frame == max(frames):
                    observer.close()
            core.retro_run = run
            installed.append(observer)
        return core

    ct.CDLL = loaded
    selected = [4300, 6300] + [f for s in (6400, 6800, 7200, 7600, 8000) for f in range(s, s + 64)]
    sys.argv = ['headless_desmume_v193.py', '--rom', pre['candidate'], '--out', str(OUT),
        '--frames', '8063', '--inputs-json', str(ROOT / 'inputs.json'), '--battery-save', pre['donor'],
        '--touchscreen', '--capture-every', '999999', '--capture-at', *map(str, selected)]
    try:
        harness.main()
    finally:
        ct.CDLL = loader
        for observer in installed:
            observer.close()
    for observer in installed:
        observer.save()
    print('V663 terminal diagnostic source-row run; all original rendering retained.', flush=True)


if __name__ == '__main__':
    main()
