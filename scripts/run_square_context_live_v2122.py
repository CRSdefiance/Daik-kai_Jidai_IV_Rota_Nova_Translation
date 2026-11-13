"""Ordinary Square/town dialogue from an unchanged genuine Istanbul save copy."""
import ctypes as ct
import sys
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts import headless_desmume_v193 as harness
from scripts import observe_square_context_v2122 as observed
from scripts.verify_village_wrap_v608 import read,save
ROOT=observed.ROOT
ROM=observed.ROM
CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193/square_context_live_v2122_V2097')
PRIOR=Path('E:/Rota Nova translations/Generated/work/emulation_v193/shop_business_v745_new/capture_report.json')
if __name__=='__main__':
 assert not ROOT.exists()and not CAP.exists();observed.prepare_contract()
 report=read(PRIOR);battery=report['battery_save_preloaded'];donor=Path(battery['source']);assert sha(donor.read_bytes())==battery['source_sha256']=='d991cb3bcdf74eed7aeb58c9a75957766b7c820d002423fd2b55cc8493cf8132'
 assert not any(v for k,v in report.items()if k.startswith('synthetic_'))
 digest=sha(ROM.read_bytes());assert digest==read(ROM.with_suffix('.manifest.json'))['candidate_sha256']
 inputs=ROOT/'ordinary_context_inputs.json';save(inputs,report['scripted_input_schedule']);frames=[3200,3500,4000,4400,4800,4900,5200,5500,5600,5900,6100,6500]
 save(ROOT/'run_plan.json',dict(candidate=str(ROM),candidate_sha256=digest,inputs=str(inputs),inputs_sha256=sha(inputs.read_bytes()),configured_maximum_frames=25000,pause_at=6500,captures=frames,original_genuine_save=str(donor),donor_sha256=sha(donor.read_bytes()),no_savestate_or_any_synthetic_fixture=True,prior_report=str(PRIOR),prior_report_sha256=sha(PRIOR.read_bytes()),observer_sha256=sha(Path(observed.__file__).read_bytes()),producer_sha256=sha(Path(__file__).read_bytes()),harness_sha256=sha(Path(harness.__file__).read_bytes()),full_goal_complete=False))
 class Proxy:
  def __getattr__(self,name):return getattr(ct,name)
  def CDLL(self,path,*args,**kwargs):
   core=ct.CDLL(path,*args,**kwargs)
   if str(path).lower().endswith('desmume_libretro.dll'):
    observer=observed.Observer(core,CAP/'common_observer');observers.append(observer);observer.install();old_run=core.retro_run;old_run.restype=None
    def run():observer.next_frame();old_run()
    core.retro_run=run
   return core
 observers=[];previous=harness.ct;harness.ct=Proxy()
 sys.argv=['headless_desmume_v193.py','--rom',str(ROM),'--out',str(CAP),'--frames','25000','--inputs-json',str(inputs),'--battery-save',str(donor),'--touchscreen','--pause-at','6500','--dump-pause-ram','--capture-every','999999','--capture-at',*map(str,frames),'--dump-capture-ram','--dump-ram']
 try:harness.main()
 finally:
  harness.ct=previous
  for observer in observers:observer.close()
 for observer in observers:observer.save()
 assert sha(donor.read_bytes())==battery['source_sha256']
 save(ROOT/'terminal.json',dict(terminal=True,frames=read(CAP/'capture_report.json')['frames'],candidate_sha256=digest,all_observer_host_slots_restored=True,original_genuine_donor_unchanged=True,no_savestate_or_any_synthetic_fixture=True,full_goal_complete=False))
