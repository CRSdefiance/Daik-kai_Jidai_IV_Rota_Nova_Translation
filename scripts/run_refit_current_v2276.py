"""Current ordinary Refit navigation; inherited five-ship save, no new RAM fixture."""
import ctypes as ct
import sys
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts import headless_desmume_v193 as harness
from scripts import observe_refit_current_v2275 as observed
from scripts.verify_village_wrap_v608 import read,save
ROOT=observed.ROOT;ROM=observed.ROM
CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193/refit_actual_v2276_V2171')
PRIOR=Path('work/emulation_v193/refit_editorial_v831_after/capture_report.json')
if __name__=='__main__':
    assert not ROOT.exists()and not CAP.exists();observed.prepare_contract();prior=read(PRIOR);battery=prior['battery_save_preloaded'];donor=Path(battery['source']);assert sha(donor.read_bytes())==battery['source_sha256']=='febc859c5af2df6fa8023c349bb7f31b5fc15ea769fb2eea527b3a3f80521731'
    digest=sha(ROM.read_bytes());assert read(ROM.with_suffix('.manifest.json'))['candidate_sha256']==digest;inputs=ROOT/'ordinary_refit_inputs.json';save(inputs,prior['scripted_input_schedule']);frames=sorted({r['frame']for r in prior['frames_captured']})
    save(ROOT/'run_plan.json',dict(candidate=str(ROM),candidate_sha256=digest,inputs=str(inputs),inputs_sha256=sha(inputs.read_bytes()),frames=20601,captures=frames,source_battery=str(donor),source_battery_sha256=sha(donor.read_bytes()),inherited_five_ship_Copenhagen_test_save_not_earned_progress=True,no_new_RAM_code_or_gameplay_fixture=True,prior_report=str(PRIOR),prior_report_sha256=sha(PRIOR.read_bytes()),observer_sha256=sha(Path(observed.__file__).read_bytes()),harness_sha256=sha(Path(harness.__file__).read_bytes()),producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    observers=[]
    class Proxy:
        def __getattr__(self,name):return getattr(ct,name)
        def CDLL(self,path,*args,**kwargs):
            core=ct.CDLL(path,*args,**kwargs)
            if str(path).lower().endswith('desmume_libretro.dll'):
                observer=observed.Observer(core,CAP/'refit_observer');observers.append(observer);observer.install();old_run=core.retro_run;old_run.restype=None
                def run():observer.next_frame();old_run()
                core.retro_run=run
            return core
    previous=harness.ct;harness.ct=Proxy();sys.argv=['headless_desmume_v193.py','--rom',str(ROM),'--out',str(CAP),'--frames','20601','--inputs-json',str(inputs),'--battery-save',str(donor),'--touchscreen','--capture-every','999999','--capture-at',*map(str,frames),'--dump-capture-ram','--dump-ram']
    try:harness.main()
    finally:
        harness.ct=previous
        for observer in observers:observer.close()
    for observer in observers:observer.save()
    assert sha(donor.read_bytes())==battery['source_sha256'];save(ROOT/'terminal.json',dict(terminal=True,frames=read(CAP/'capture_report.json')['frames'],all_host_slots_restored=True,original_battery_unchanged=True,no_new_emulator_fixture=True,full_goal_complete=False))
