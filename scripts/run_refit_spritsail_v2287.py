"""Registered V2284 ordinary equipment navigation or clean New Game cold boot."""
import argparse,ctypes as ct,sys
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts import headless_desmume_v193 as harness
from scripts import observe_refit_spritsail_v2286 as observed
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/refit_spritsail_runs_v2287');ROM=Path('out/all_routes_combined_v2284_candidate.nds')
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--case',choices=['refit','newgame'],required=True);args=parser.parse_args();case=args.case;ROOT.mkdir(parents=True,exist_ok=True);planpath=ROOT/(case+'_plan.json');assert not planpath.exists();cap=Path('E:/Rota Nova translations/Generated/work/emulation_v193')/f'refit_spritsail_v2287_{case}_V2284';assert not cap.exists();digest=sha(ROM.read_bytes());assert read(ROM.with_suffix('.manifest.json'))['candidate_sha256']==digest;observers=[]
 if case=='refit':
  observed.prepare_contract();schedule=[r for r in read('work/analysis/refit_actual_v2276/ordinary_refit_inputs.json')if r['start']<=13701]
  for f,button in[(14001,'A'),(14301,'DOWN'),(14601,'DOWN'),(14901,'DOWN'),(15201,'DOWN'),(15501,'UP'),(15801,'B'),(16101,'B'),(16401,'A'),(16701,'B'),(17001,'B')]:schedule.append(dict(start=f,duration=8,buttons=[button]))
  donor=Path('work/analysis/refit_editorial_v831/disposable_refit_source.dsv');assert sha(donor.read_bytes())=='febc859c5af2df6fa8023c349bb7f31b5fc15ea769fb2eea527b3a3f80521731';battery=['--battery-save',str(donor)];frames=17401;captures=[1,60,180,3200,11900,*range(12800,17401,300)]
 else:
  schedule=read('work/analysis/cliff_editorial_v829/ordinary_newgame_inputs.json');battery=[];frames=4001;captures=[1,60,180,1600,2000,3200,4000]
 inputs=ROOT/(case+'_inputs.json');save(inputs,schedule);save(planpath,dict(candidate=str(ROM),candidate_sha256=digest,profile='all-routes-unified-v2284',case=case,frames=frames,inputs=str(inputs),inputs_sha256=sha(inputs.read_bytes()),captures=captures,inherited_five_ship_test_battery_not_earned_progress=case=='refit',no_new_RAM_code_gameplay_fixture_or_savestate=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
 class Proxy:
  def __getattr__(self,name):return getattr(ct,name)
  def CDLL(self,path,*a,**kw):
   core=ct.CDLL(path,*a,**kw)
   if case=='refit'and str(path).lower().endswith('desmume_libretro.dll'):
    observer=observed.Observer(core,cap/'refit_observer');observers.append(observer);observer.install();old_run=core.retro_run;old_run.restype=None
    def run():observer.next_frame();old_run()
    core.retro_run=run
   return core
 previous=harness.ct;harness.ct=Proxy();sys.argv=['headless_desmume_v193.py','--rom',str(ROM),'--out',str(cap),'--frames',str(frames),'--inputs-json',str(inputs),*battery,'--touchscreen','--capture-every','999999','--capture-at',*map(str,captures),'--dump-capture-ram','--dump-ram']
 try:harness.main()
 finally:
  harness.ct=previous
  for observer in observers:observer.close()
 for observer in observers:observer.save()
 if case=='refit':assert sha(donor.read_bytes())=='febc859c5af2df6fa8023c349bb7f31b5fc15ea769fb2eea527b3a3f80521731'
 save(ROOT/(case+'_terminal.json'),dict(terminal=True,frames=read(cap/'capture_report.json')['frames'],all_host_slots_restored=True,no_new_RAM_or_gameplay_fixture=True,full_goal_complete=False))
