"""Revised Stockholm research after native loader approval;three coordinate-only fixtures andoriginal discovery."""
import ctypes as ct
import sys
import struct
from pathlib import Path
from types import FunctionType
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts import headless_desmume_v193 as harness
from scripts import observe_script_sources_v733 as original
from scripts.prepare_lil_Stockholm_research_v1862 import ROM
from scripts.run_activity_special_live_v988 import GrowingCommands
from scripts import native_battle_fixture_v620 as fixture_dispatch
from scripts.native_lil_Stockholm_location_v1850 import apply_fixture, REQUEST
import json
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/lil_Stockholm_revised_run_v1864')
CAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193/lil_Stockholm_revised_run_v1864_RESEARCH_ONLY')

if __name__ == '__main__':
    assert read('work/analysis/lil_Stockholm_loader_v1863/whole_SC2_and_B27_initial_entry_proof.json')['all336_whole_blocks_and672_modes_each_pass']
    assert not ROOT.exists() and not CAP.exists()
    previous = read('work/analysis/lil_lessons_revised_v1741/run_plan.json')
    digest = sha(ROM.read_bytes())
    assert digest == read('work/analysis/lil_Stockholm_research_v1862/research_image_receipt.json')['research_ROM_sha256']
    assert read('work/analysis/lil_crew_lesson_v1756/terminal.json')['terminal']
    arm = NdsImage.open(ROM).read_file('/__arm9__.bin')
    contract = Path('work/analysis/script_sources_v733/source_contract.json')
    for target in read(contract)['targets']:
        assert struct.unpack_from('<I', arm, target['PC'] - 0x02000000)[0] == target['word']
    ROOT.mkdir(parents=True)
    (ROOT/'source_contract.json').write_bytes(contract.read_bytes())
    inputs = ROOT/'ordinary_replay_inputs.json'
    save(inputs, read(previous['inputs']))
    journal = ROOT/'navigation.jsonl'
    source_journal=Path('work/analysis/lil_Stockholm_context_run_v1851/navigation.jsonl')
    assert read('work/analysis/lil_Stockholm_context_run_v1851/terminal.json')['frame']==62850
    assert read('work/analysis/lil_Stockholm_location_v1850/coordinate_only_preflight.json')['original_town7_known_flag0_preserved_native_discovery_and_docking_required']
    commands=[json.loads(line)for line in source_journal.read_text().splitlines()if line]
    commands=[r for r in commands if not r.get('stop')and r.get('until',999999)<=50640]
    assert commands[-1]['until']==50640
    journal.write_text(''.join(json.dumps(r)+'\n'for r in commands),encoding='utf-8')
    env = {**original.__dict__, 'ROM': ROM, 'ROOT': ROOT}
    class Observer(original.Observer):
        __init__ = FunctionType(original.Observer.__init__.__code__, env, argdefs=original.Observer.__init__.__defaults__)
        save = FunctionType(original.Observer.save.__code__, env, argdefs=original.Observer.save.__defaults__)
    observers = []
    class Commands(GrowingCommands):
        def readline(self, *args):
            for observer in observers:
                save(ROOT/'live_observer_progress.json', {'rows': observer.rows, 'errors': observer.errors,
                    'callbacks': observer.header[2], 'mismatches': observer.header[3],
                    'pending': {str(k):v for k,v in observer.pending.items()}, 'live_not_terminal_proof': True})
            return super().readline(*args)
    class Proxy:
        def __getattr__(self,name): return getattr(ct,name)
        def CDLL(self,path,*args,**kwargs):
            core=ct.CDLL(path,*args,**kwargs)
            if str(path).lower().endswith('desmume_libretro.dll'):
                observer=Observer(core,CAP/'observer'); observer.install(); observers.append(observer)
                old=core.retro_run; old.restype=None
                def run(): observer.next_frame(); old()
                core.retro_run=run
            return core
    save(ROOT/'run_plan.json', {'research_ROM': str(ROM), 'research_ROM_sha256': digest,
        'inputs': str(inputs), 'inputs_sha256': sha(inputs.read_bytes()), 'append_only_navigation': str(journal),
        'initial_pause_frame': 29930, 'no_preloaded_save_or_savestate': True,
        'declared_each16_byte_location_only_fixtures': ['scripts/native_lil_Bruges_location_v1754.py','scripts/native_lil_Amsterdam_location_v1833c.py','scripts/native_lil_Stockholm_location_v1850.py'],
        'normal_docking_and_event_eligibility_not_overridden': True,
        'replayed_source_journal':str(source_journal),'replayed_source_journal_sha256':sha(source_journal.read_bytes()),
        'only_SC2B27_resized_relative_to_registered_V1841':True,
        'source_V1756_plan_fixture_path_metadata_erratum':'Actual import and fixture hash are1754;its slash-path metadata named1752c.',
        'observer_sha256': sha(Path(original.__file__).read_bytes()),
        'harness_sha256': sha(Path(harness.__file__).read_bytes()), 'runner_sha256': sha(Path(__file__).read_bytes()),
        'full_goal_complete': False})
    stream=Commands(journal); old_stdin=sys.stdin; sys.stdin=stream; old_ct=harness.ct; harness.ct=Proxy()
    old_fixture=fixture_dispatch.apply_fixture; fixture_dispatch.apply_fixture=apply_fixture
    sys.argv=['headless_desmume_v193.py','--rom',str(ROM),'--out',str(CAP),'--frames','100000',
        '--inputs-json',str(inputs),'--capture-every','999999','--capture-at','29930','--pause-at','29930',
        '--dump-capture-ram','--dump-pause-ram','--dump-ram','--touchscreen','--allow-battle-fixtures']
    try: harness.main()
    finally:
        sys.stdin=old_stdin; harness.ct=old_ct; stream.close(); fixture_dispatch.apply_fixture=old_fixture
        for observer in observers: observer.close()
    for observer in observers: observer.save()
    save(ROOT/'terminal.json', {'terminal': True, 'research_ROM_sha256': digest,
        'frame': read(CAP/'capture_report.json')['frames'], 'observer_host_slots_restored': True,
        'location_only_fixture_declared_no_event_outcome_or_ROM_runtime_edit': True})
