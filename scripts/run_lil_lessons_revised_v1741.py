"""Cold-boot revised lesson, ordinary prior wind-branch inputs, read-only tracing."""
import ctypes as ct
import struct
import sys
from pathlib import Path
from types import FunctionType
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts import headless_desmume_v193 as harness
from scripts import observe_script_sources_v733 as original
from scripts.prepare_lil_lessons_research_v1739 import ROM
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/lil_lessons_revised_v1741')
CAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193/lil_lessons_revised_v1741_RESEARCH_ONLY')

if __name__ == '__main__':
    assert not ROOT.exists() and not CAP.exists()
    receipt = read('work/analysis/lil_lessons_research_v1739/research_image_receipt.json')
    digest = sha(ROM.read_bytes())
    assert digest == receipt['research_ROM_sha256']
    loader = read('work/analysis/lil_lessons_loader_v1740/whole_SC2_and_lesson_initial_entry_proof.json')
    assert loader['versions'][1]['ROM_sha256'] == digest
    previous = Path('E:/Rota Nova translations/Generated/work/emulation_v193/lil_lesson_context_v1723_1711/capture_report.json')
    report = read(previous)
    assert report['ROM_sha256'] == receipt['parent_sha256'] and report['frames'] == 29930
    arm = NdsImage.open(ROM).read_file('/__arm9__.bin')
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    assert arm[0x24048:0x24118] == clean[0x24048:0x24118]
    contract = Path('work/analysis/script_sources_v733/source_contract.json')
    for target in read(contract)['targets']:
        assert struct.unpack_from('<I', arm, target['PC'] - 0x02000000)[0] == target['word']
    ROOT.mkdir(parents=True)
    (ROOT / 'source_contract.json').write_bytes(contract.read_bytes())
    inputs = ROOT / 'ordinary_wind_branch_inputs.json'
    save(inputs, report['scripted_input_schedule'])
    frames = sorted({r['frame'] for r in report['frames_captured'] if r['frame'] >= 22900})
    frames = sorted(set(frames) | {f - 30 for f in frames if f >= 23230})
    env = {**original.__dict__, 'ROM': ROM, 'ROOT': ROOT}
    class Observer(original.Observer):
        __init__ = FunctionType(original.Observer.__init__.__code__, env, argdefs=original.Observer.__init__.__defaults__)
        save = FunctionType(original.Observer.save.__code__, env, argdefs=original.Observer.save.__defaults__)
    observers = []
    class Proxy:
        def __getattr__(self, name):
            return getattr(ct, name)
        def CDLL(self, path, *args, **kwargs):
            core = ct.CDLL(path, *args, **kwargs)
            if str(path).lower().endswith('desmume_libretro.dll'):
                observer = Observer(core, CAP / 'observer')
                observer.install()
                observers.append(observer)
                old = core.retro_run
                old.restype = None
                def run():
                    observer.next_frame()
                    old()
                core.retro_run = run
            return core
    save(ROOT / 'run_plan.json', {'research_ROM': str(ROM), 'research_ROM_sha256': digest,
        'capture_folder': str(CAP), 'inputs': str(inputs), 'inputs_sha256': sha(inputs.read_bytes()),
        'original_current_report': str(previous), 'original_report_sha256': sha(previous.read_bytes()),
        'frames': 29930, 'capture_frames': frames,
        'no_preloaded_battery_save_savestate_cheat_or_gameplay_fixture': True,
        'observer_sha256': sha(Path(original.__file__).read_bytes()),
        'harness_sha256': sha(Path(harness.__file__).read_bytes()),
        'runner_sha256': sha(Path(__file__).read_bytes()), 'not_a_registered_candidate_or_user_handoff': True,
        'full_goal_complete': False})
    old_ct = harness.ct
    harness.ct = Proxy()
    sys.argv = ['headless_desmume_v193.py', '--rom', str(ROM), '--out', str(CAP), '--frames', '29930',
        '--inputs-json', str(inputs), '--capture-every', '999999', '--capture-at', *map(str, frames),
        '--dump-capture-ram', '--dump-ram']
    try:
        harness.main()
    finally:
        harness.ct = old_ct
        for observer in observers:
            observer.close()
    for observer in observers:
        observer.save()
    save(ROOT / 'terminal.json', {'terminal': True, 'research_ROM_sha256': digest, 'frames': 29930,
        'observer_instances': len(observers), 'observer_host_slots_restored': True,
        'no_gameplay_fixture_save_or_ROM_runtime_edit': True})
