"""Audit two normally terminated approaches which never entered combat."""
import inspect
import struct
from pathlib import Path
from scripts import verify_ship_loadout_pilot_v1381 as previous
from scripts.native_combat_approach_fixture_v1463 import apply_fixture as southwest
from scripts.native_close_approach_fixture_v1467 import apply_fixture as closer,ROM
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/approach_pilots_verified_v1470')

def main():
    assert not ROOT.exists()
    release=read('work/analysis/ship_loss_surrender_release_v1455/registered_release_verification.json')
    source=inspect.getsource(previous.audit)
    old="digest=='dbf86d020cb868f443f9c6a9f68706e8cda28e9268ce0318a63ef765f4f3281c'"
    assert source.count(old)==1
    source=source.replace(old,"digest=="+repr(release['candidate_sha256']))
    old="assert [r['after'] for r in fixture['cannon_equipment']]==[4,7,7,7,7]"
    assert source.count(old)==1
    source=source.replace(old,"assert [r['after'] for r in fixture['cannon_equipment']]==[5,7,7,7,7]")
    rows=[]
    for name,fixture in [('combat_approach_v1464',southwest),('close_combat_approach_v1468',closer)]:
        run=Path('work/analysis')/name
        cap=Path('E:/Rota Nova translations/Generated/work/emulation_v193')/(name+'_1456')
        env={**previous.__dict__,'ROM':ROM,'apply_fixture':fixture}
        exec(compile(source,__file__,'exec'),env)
        proof,snapshots,arm=env['audit'](run,cap,9500)
        runner=Path('scripts/run_'+name.replace('combat_approach_v1464','combat_approach_v1464')+'.py')
        if name=='close_combat_approach_v1468': runner=Path('scripts/run_close_combat_approach_v1468.py')
        assert sha(runner.read_bytes())==read(run/'run_plan.json')['runner_sha256']
        observations=[]
        for frame in [9000,9100,9400,9500]:
            raw=Path(snapshots[frame]['path']).read_bytes();cpu,get=get_machine(arm,raw)
            mode=list(struct.unpack('<3I',cpu.mem_read(get(0x3F0F8)+8,12)))
            assert mode==[0,0,0]
            root=get(0xCB1A8);ships=[]
            for slot in range(5):
                mobile=get(0x36C70,root+4+132+12+8*slot)
                hc=[get(0x5543C,mobile),get(0x55444,mobile)]
                assert hc==([60,49] if slot==0 else [25,19])
                point=[v//128 for v in struct.unpack('<2i',cpu.mem_read(mobile+16,8))]
                ships.append({'slot':slot,'Hull_Crew':hc,'map_point':point})
            observations.append({'frame':frame,'mode':mode,'own_ships':ships})
        proof.update(actual_observations=observations,
            actual9400_screen_visually_reviewed='Declare War Mode;There are no targets to attack.',
            no_original_combat_started_in_observed_approach=True,
            no_new_gunnery_sinking_capture_or_surrender_event_claim=True,
            no_editorial_completion_credit=True,full_goal_complete=False)
        rows.append(proof)
    ROOT.mkdir(parents=True)
    save(ROOT/'terminal_approach_audit.json',{'runs':rows,
        'next_action':'Use source-bound stronger original fleets and verify actual loaded coordinates before choosing an encounter approach.',
        'producer_sha256':sha(Path(__file__).read_bytes()),'completed_entries_added':0,'full_goal_complete':False})
    print('Both9500-frame terminal runs fully audited;mode000 and own Hull/Crew unchanged. No original new event credit.')

if __name__=='__main__':main()
