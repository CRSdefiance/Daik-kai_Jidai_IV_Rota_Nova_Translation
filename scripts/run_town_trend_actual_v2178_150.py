"""Actual revised trend display from an isolated save copy with declared bounded trend/RNG fixture."""
import ctypes as ct
import sys
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts import headless_desmume_v193 as harness
from scripts import observe_promoter_context_v2144 as observed
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/town_trend_actual_v2178_150')
ROM=Path('out/all_routes_combined_v2171_candidate.nds')
observed.ROOT=ROOT;observed.ROM=ROM
CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193/town_trend_actual_v2178_150_V2171')
PRIOR=Path('E:/Rota Nova translations/Generated/work/emulation_v193/responses_v751_50_2_final_new/capture_report.json')
if __name__=='__main__':
 assert not ROOT.exists()and not CAP.exists();observed.prepare_contract()
 report=read(PRIOR);battery=report['battery_save_preloaded'];donor=Path('E:/Rota Nova translations/Saves/hodram-istanbul-golden-cutlass-blue-oak-v474.dsv');assert sha(donor.read_bytes())==battery['source_sha256']=='d991cb3bcdf74eed7aeb58c9a75957766b7c820d002423fd2b55cc8493cf8132'
 assert len(report['synthetic_town_trend_fixtures'])==1
 digest=sha(ROM.read_bytes());assert digest==read(ROM.with_suffix('.manifest.json'))['candidate_sha256']
 inputs=ROOT/'ordinary_context_inputs.json';save(inputs,report['scripted_input_schedule']);frames=[3200,3500,3800,4200,4400,4600,4800,5000,5200,5600,6000,6500]
 save(ROOT/'run_plan.json',dict(candidate=str(ROM),candidate_sha256=digest,inputs=str(inputs),inputs_sha256=sha(inputs.read_bytes()),configured_maximum_frames=6501,pause_at=3200,captures=frames,original_genuine_save=str(donor),donor_sha256=sha(donor.read_bytes()),declared_trend_and_original_SDK_RNG_fixture=True,source_trend_level=150,source_RNG_seed=2,prior_report=str(PRIOR),prior_report_sha256=sha(PRIOR.read_bytes()),observer_sha256=sha(Path(observed.__file__).read_bytes()),producer_sha256=sha(Path(__file__).read_bytes()),harness_sha256=sha(Path(harness.__file__).read_bytes()),full_goal_complete=False))
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
 sys.argv=['headless_desmume_v193.py','--rom',str(ROM),'--out',str(CAP),'--frames','6501','--inputs-json',str(inputs),'--battery-save',str(donor),'--touchscreen','--allow-town-trend-fixtures','--pause-at','3200','--dump-pause-ram','--capture-every','999999','--capture-at',*map(str,frames),'--dump-capture-ram','--dump-ram']
 original=Path(harness.__file__).read_text();assert sha(Path(harness.__file__).read_bytes())=='d5bcc9a11b5602bfb44d54e75b02a7a7a0165c9ee819a07cd0cbdac2130b8c6e'
 replacements={'from scripts.native_missionary_fixture_v623 import assign as assign_missionary':'from scripts.native_town_trend_fixture_v2177 import assign as assign_missionary',"'missionary_fixture'":"'town_trend_fixture'",'args.allow_missionary_fixtures':'args.allow_town_trend_fixtures','--allow-missionary-fixtures':'--allow-town-trend-fixtures',"'synthetic_missionary_Chapel_assignment_fixtures'":"'synthetic_town_trend_fixtures'",'Isolated Chapel/Manuel fixture applied; no earned refit, qualification or assignment credit.':'Declared bounded trend and SDK RNG fixture applied; ordinary trend creation not claimed.','Allow the bounded three-byte Chapel/Manuel role fixture for Square display testing.':'Allow the bounded trend and original SDK RNG fixture.','Missionary display fixture requires':'Promoter display fixture requires'}
 effective=original;counts={}
 for old,new in replacements.items():
  counts[old]=effective.count(old);assert counts[old]in(1,2);effective=effective.replace(old,new)
 import types
 module=types.ModuleType('_promoter_host_v2144');module.__file__=str(Path(harness.__file__).resolve());sys.modules[module.__name__]=module;exec(compile(effective,module.__file__,'exec'),module.__dict__);module.ct=harness.ct
 save(ROOT/'effective_harness_adapter.json',dict(original_harness_sha256=sha(original.encode()),effective_harness_sha256=sha(effective.encode()),exact_replacement_counts=counts,fixture_module='scripts/native_town_trend_fixture_v2177.py',fixture_module_sha256=sha(Path('scripts/native_town_trend_fixture_v2177.py').read_bytes()),source_harness_file_unchanged=True,full_goal_complete=False))
 import io,json
 old_stdin=sys.stdin;sys.stdin=io.StringIO(json.dumps(dict(until=6501,town_trend_fixture=dict(level=150,seed=2),duration=8))+"\n"+json.dumps(dict(stop=True))+"\n")
 try:module.main()
 finally:
  sys.stdin=old_stdin
  harness.ct=previous
  for observer in observers:observer.close()
 for observer in observers:observer.save()
 assert sha(donor.read_bytes())==battery['source_sha256']
 save(ROOT/'terminal.json',dict(terminal=True,frames=read(CAP/'capture_report.json')['frames'],candidate_sha256=digest,all_observer_host_slots_restored=True,original_genuine_donor_unchanged=True,declared_trend_and_original_SDK_RNG_fixture=True,source_trend_level=150,source_RNG_seed=2,full_goal_complete=False))
