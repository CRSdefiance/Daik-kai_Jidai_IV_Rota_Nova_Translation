"""Cold-load the verified original encounter with read-only shot boundary tracing."""
import ctypes as ct
import json
import os
import sys
from pathlib import Path
from shutil import copy2
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts import headless_desmume_v193 as harness
from scripts import native_battle_fixture_v620 as dispatch
from scripts.native_lookout_contact_v1798b import apply_fixture, ROM
from scripts.observe_shot_branch_v1797 import Observer, CONTRACT
from scripts.run_activity_special_live_v988 import GrowingCommands
from scripts.verify_village_wrap_v608 import read, save

ROOT=Path('work/analysis/observed_lookout_v1799')
CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193/observed_lookout_v1799_1775')

if __name__=='__main__':
    assert not ROOT.exists()and not CAP.exists()
    assert read('work/analysis/shot_observer_contract_v1796/preflight.json')['all30_grouped_prefix_ABI_controls_pass']
    digest=sha(ROM.read_bytes());assert digest==read(ROM.with_suffix('.manifest.json'))['candidate_sha256']
    assert digest==read(CONTRACT)['candidate_sha256']
    arm=NdsImage.open(ROM).read_file('/__arm9__.bin')
    for target in read(CONTRACT)['targets']:
        assert int.from_bytes(arm[target['PC']-0x02000000:target['PC']-0x02000000+4],'little')==target['word']
    assert sha(Path(harness.__file__).read_bytes())=='d5bcc9a11b5602bfb44d54e75b02a7a7a0165c9ee819a07cd0cbdac2130b8c6e'
    prior=read('work/analysis/two_stage_sighting_v1787_twoStageReady8/run_plan.json')
    source=Path(prior['source_donor']);source_sha=sha(source.read_bytes());assert source_sha==prior['source_donor_sha256']
    ROOT.mkdir(parents=True);donor=ROOT/'disposable_regional.dsv';copy2(source,donor)
    inputs=ROOT/'original_load_inputs.json';inputs.write_bytes(Path(prior['inputs']).read_bytes())
    commands=[json.loads(s)for s in Path(prior['append_only_navigation']).read_text().splitlines()if s]
    commands=[r for r in commands if 'stop'not in r];assert commands[-1]['until']==5503
    journal=ROOT/'navigation.jsonl';journal.write_text(''.join(json.dumps(r)+'\n'for r in commands),encoding='utf-8')
    observers=[]
    class Commands(GrowingCommands):
        def readline(self,*args):
            for observer in observers:save(ROOT/'live_observer_progress.json',observer.progress())
            return super().readline(*args)
    class Proxy:
        def __getattr__(self,name):return getattr(ct,name)
        def CDLL(self,path,*args,**kwargs):
            core=ct.CDLL(path,*args,**kwargs)
            if str(path).lower().endswith('desmume_libretro.dll'):
                observer=Observer(core,CAP/'observer');observer.install();observers.append(observer)
                old=core.retro_run;old.restype=None
                def run():observer.next_frame();old()
                core.retro_run=run
            return core
    save(ROOT/'run_plan.json',{'candidate':str(ROM),'candidate_sha256':digest,'source_donor':str(source),
        'source_donor_sha256':source_sha,'disposable_donor':str(donor),'inputs':str(inputs),'inputs_sha256':sha(inputs.read_bytes()),
        'append_only_navigation':str(journal),'capture_folder':str(CAP),'PID':os.getpid(),
        'fixture_module':'scripts/native_lookout_contact_v1798b.py','fixture_module_sha256':sha(Path('scripts/native_lookout_contact_v1798b.py').read_bytes()),
        'observer_module_sha256':sha(Path('scripts/observe_shot_branch_v1797.py').read_bytes()),'observer_contract_sha256':sha(CONTRACT.read_bytes()),
        'runner_sha256':sha(Path(__file__).read_bytes()),'no_ROM_message_RNG_or_outcome_patch':True,
        'replay_to5503_uses_verified13_location_fixtures_and_ordinary_dismissal':True,'full_goal_complete':False})
    stream=Commands(journal);old_stdin=sys.stdin;old_ct=harness.ct;old_fixture=dispatch.apply_fixture
    sys.stdin=stream;harness.ct=Proxy();dispatch.apply_fixture=apply_fixture
    sys.argv=['headless_desmume_v193.py','--rom',str(ROM),'--out',str(CAP),'--frames','50000',
        '--inputs-json',str(inputs),'--touchscreen','--capture-every','999999','--capture-at','3400',
        '--battery-save',str(donor),'--pause-at','3400','--dump-capture-ram','--dump-pause-ram','--dump-ram','--allow-battle-fixtures']
    try:harness.main()
    finally:
        sys.stdin=old_stdin;harness.ct=old_ct;dispatch.apply_fixture=old_fixture;stream.close()
        for observer in observers:observer.close()
    for observer in observers:observer.save()
    assert sha(source.read_bytes())==sha(donor.read_bytes())==source_sha
    save(ROOT/'terminal.json',{'terminal':True,'frame':read(CAP/'capture_report.json')['frames'],'candidate_sha256':digest,
        'source_and_disposable_donors_unchanged':True,'all_observer_slots_restored':True,
        'navigation_sha256':sha(journal.read_bytes()),'no_target_or_editorial_completion_credit_without_separate_proof':True})
    print('Observed Lookout run terminal;native host slots restored andboth battery saves exact.',flush=True)
