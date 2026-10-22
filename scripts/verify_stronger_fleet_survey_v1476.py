"""Terminal source/input/RAM audit including one rejected no-effect touch command."""
import inspect,struct
from pathlib import Path
from scripts import verify_ship_loadout_pilot_v1381 as previous
from scripts.native_stronger_fleet_location_v1471 import apply_fixture,ROM
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/stronger_fleet_survey_verified_v1476')

def audit(run,cap,terminal_frame,allowed_rejected):
    release=read('work/analysis/ship_loss_surrender_release_v1455/registered_release_verification.json')
    source=inspect.getsource(previous.audit)
    replacements=[
        ("digest=='dbf86d020cb868f443f9c6a9f68706e8cda28e9268ce0318a63ef765f4f3281c'",'digest=='+repr(release['candidate_sha256'])),
        ("assert len(fixture['owned_bytes'])==45","assert len(fixture['owned_bytes'])==40"),
        ("    assert [r['after'] for r in fixture['cannon_equipment']]==[4,7,7,7,7]\n",''),
        ("        assert item['validation_passed']", "        if not item['validation_passed']:\n            assert item in allowed_rejected and item['rejected_before_any_input_or_fixture']\n            continue"),
        ('entire4MiB_sole_prebattle45_owned_byte_fixture_and_all_input_schedule_audited','entire4MiB_sole_prebattle40_owned_byte_fixture_and_all_validated_input_schedule_audited'),
        ('source_census_and_fixture_equipment_are_not_earned_acquisition','source_location_fixture_is_not_earned_travel')]
    for old,new in replacements:
        assert source.count(old)==1,old
        source=source.replace(old,new)
    env={**previous.__dict__,'ROM':ROM,'apply_fixture':apply_fixture,'allowed_rejected':allowed_rejected}
    exec(compile(source,__file__,'exec'),env)
    proof,snapshots,arm=env['audit'](run,cap,terminal_frame)
    journal=read(cap/'navigation_command_journal.json')['commands_received']
    assert [r for r in journal if not r['validation_passed']]==allowed_rejected
    proof['rejected_before_any_input_or_fixture_commands']=allowed_rejected
    return proof,snapshots,arm

def observe(arm,snapshot):
    raw=Path(snapshot['path']).read_bytes();cpu,get=get_machine(arm,raw);root=get(0xCB1A8)
    fleets=[]
    for identity in [1,4]:
        f=root+4+132*identity;ships=[]
        for slot in range(5):
            mobile,model=get(0x36C70,f+12+8*slot),get(0x36C94,f+12+8*slot)
            if not mobile:continue
            ships.append({'slot':slot,'mobile':mobile,'model':model,
                'map_point':[v//128 for v in struct.unpack('<2i',cpu.mem_read(mobile+16,8))],
                'Hull_Crew':[get(0x5543C,mobile),get(0x55444,mobile)],'cannon_type':get(0x1856C,model)})
        fleets.append({'fleet':identity,'company':get(0x35320,f),'ships':ships})
    return {'frame':snapshot['frame'],'mode':list(struct.unpack('<3I',cpu.mem_read(get(0x3F0F8)+8,12))),'fleets':fleets}

if __name__=='__main__':
    assert not ROOT.exists()
    run=Path('work/analysis/stronger_fleet_location_v1472')
    cap=Path('E:/Rota Nova translations/Generated/work/emulation_v193/stronger_fleet_location_v1472_1456')
    rejected=[{'frame':5200,'command':{'until':5300,'touch':[163,273],'duration':8},'validation_passed':False,
        'rejected_before_any_input_or_fixture':'Invalid navigation coordinates or fields'}]
    proof,snapshots,arm=audit(run,cap,6100,rejected)
    assert sha(Path('scripts/run_stronger_fleet_location_v1472.py').read_bytes())==read(run/'run_plan.json')['runner_sha256']
    observations=[observe(arm,snapshots[n]) for n in [5100,6000,6100]]
    assert all(r['mode']==[0,0,0] for r in observations)
    assert all([s['cannon_type'] for s in r['fleets'][1]['ships']]==[3,3,2,2,2] for r in observations)
    proof.update(actual_loaded_fleet_observations=observations,
        actual_screens_visually_reviewed=[5100,5200,5300,5400,5600,5800,5900,6000],
        original_enemy_loaded_at5100=[20176,4311],separation_at6000=[316,-6],
        no_original_battle_or_new_report_event_observed=True,
        next_action='Fresh same40-byte location fixture;select original Y modes immediately at4810/4820/4830 before fleets separate.',
        producer_sha256=sha(Path(__file__).read_bytes()),completed_entries_added=0,full_goal_complete=False)
    ROOT.mkdir(parents=True);save(ROOT/'terminal_location_survey_audit.json',proof)
    print('6100-frame survey terminal;one40-byte own-location fixture and one rejected no-effect touch fully audited. Stronger fleet unchanged;no event credit.')
