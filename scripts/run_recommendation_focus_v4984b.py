"""Paired cold boots through the original reward branch with disclosed input fixtures."""
import argparse,ctypes as ct,sys
from pathlib import Path
from scripts import headless_desmume_v193 as harness
from scripts import observe_recommendation_v4984 as observed
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--case',choices=['current','reviewed'],required=True);case=p.parse_args().case
    prepared=Path('work/analysis/recommendation_focus_tools_v4983/prepared_reference_and_fixture_tools.json');refs=read(prepared)
    rom=Path(refs['parent' if case=='current' else 'research_ROM']);digest=sha(rom.read_bytes());assert digest==refs['parent_sha256' if case=='current' else 'research_ROM_sha256']
    observed.configure(case,rom);root=observed.ROOT;cap=Path('E:/Rota Nova translations/Generated/work/emulation_v193/recommendation775_v4984_'+case)
    assert not root.exists() and not cap.exists();observed.prepare_contract()
    priorpath=Path('E:/Rota Nova translations/Generated/work/emulation_v193/market_v756_edge_756/capture_report.json');prior=read(priorpath)
    donor=Path(prior['battery_save_preloaded']['source']);donor_hash=sha(donor.read_bytes());assert donor_hash=='d991cb3bcdf74eed7aeb58c9a75957766b7c820d002423fd2b55cc8493cf8132'
    schedule=[r for r in prior['scripted_input_schedule'] if r['start']<7201]
    schedule.extend(dict(start=f,duration=8,buttons=['A']) for f in range(7201,10002,400))
    schedule.extend(dict(start=f,duration=8,buttons=['B']) for f in [10801,11201,11601])
    assert any(r.get('market_fixture')=={'mode':'edge'} and r['start']==3200 for r in schedule)
    inputs=root/'inputs.json';save(inputs,schedule);captures=[3200,4900,*range(5300,12001,100),12001]
    save(root/'run_plan.json',dict(case=case,ROM=str(rom),ROM_sha256=digest,frames=12001,inputs=str(inputs),inputs_sha256=sha(inputs.read_bytes()),captures=captures,
        donor=str(donor),donor_sha256=donor_hash,prepared=str(prepared),prepared_sha256=sha(prepared.read_bytes()),
        synthetic_cargo_IDs_and_town_demand_share80_fixture_at3200=True,synthetic_qualification2_reward_quantity16_and_bonus1_inputs_at_original_BBCA4=True,
        no_code_PC_RNG_cash_or_actual_cargo_quantity_fixture=True,not_earned_inventory_share_large_sale_qualification_or_reward=True,
        not_registered_candidate_or_user_handoff=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    class Proxy:
        def __getattr__(self,name):return getattr(ct,name)
        def CDLL(self,path,*args,**kwargs):
            core=ct.CDLL(path,*args,**kwargs)
            if str(path).lower().endswith('desmume_libretro.dll'):
                observer=observed.Observer(core,cap/'common_observer');observers.append(observer);observer.install();old_run=core.retro_run;old_run.restype=None
                def run():observer.next_frame();old_run()
                core.retro_run=run
            return core
    observers=[];previous=harness.ct;harness.ct=Proxy()
    sys.argv=['headless_desmume_v193.py','--rom',str(rom),'--out',str(cap),'--frames','12001','--inputs-json',str(inputs),
        '--battery-save',str(donor),'--allow-market-fixtures','--touchscreen','--capture-every','999999','--capture-at',*map(str,captures),'--dump-ram']
    try:
        from scripts import recommendation_harness_v4984b as adapter
        adapter.PROXY=Proxy()
        adapter.main()
    finally:
        harness.ct=previous
        for observer in observers:observer.close()
    for observer in observers:observer.save()
    assert len(observers)==1 and len(observers[0].fixtures)==1
    reportpath=cap/'capture_report.json';report=read(reportpath)
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors'] and report['frames']==12001
    report['synthetic_recommendation_reward_input_fixtures']=observers[0].fixtures;save(reportpath,report)
    assert sha(donor.read_bytes())==donor_hash
    save(root/'terminal.json',dict(terminal=True,case=case,frames=12001,ROM_sha256=digest,report=str(reportpath),report_sha256=sha(reportpath.read_bytes()),
        observer=str(cap/'common_observer/requests.json'),donor_unchanged=True,all_observer_slots_restored=True,fixture_reward_not_earned=True,full_goal_complete=False))
    print(case+'12001-frame focused reward-input cold boot terminal;not an earned recommendation.',flush=True)
