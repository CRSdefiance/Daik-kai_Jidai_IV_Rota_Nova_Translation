"""Read-only original admiral/gun census;no live or CPU attribute changes."""
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/original_fleet_admirals_v1504')
ROM=Path('out/all_routes_combined_v1492_candidate.nds')

if __name__=='__main__':
    assert not ROOT.exists()
    release=read('work/analysis/battle_reaction_release_v1491/registered_release_verification.json')
    assert sha(ROM.read_bytes())==release['candidate_sha256']
    cap=Path('E:/Rota Nova translations/Generated/work/emulation_v193/battle_reaction_control_v1497_1492')
    report=read(cap/'capture_report.json');snapshot=next(s for s in report['read_only_pause_RAM_snapshots'] if s['frame']==4800)
    raw=Path(snapshot['path']).read_bytes();assert sha(raw)==snapshot['sha256']
    arm=NdsImage.open(ROM).read_file('/__arm9__.bin');clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    assert arm[0x7DCC8:0x7DE00]==clean[0x7DCC8:0x7DE00]
    cpu,get=get_machine(arm,raw);fleets=get(0xCB1A8)
    captain=get(0x3697C,fleets+4+132);assert get(0x7EE08,captain)==get(0x7F244)==1
    own_fencing=get(0x7DCC8,captain,5);assert own_fencing==120
    census_path=Path('work/analysis/original_fleet_guns_v1469/original_fleet_census.json');census=read(census_path)
    rows=[]
    for f in census['stronger_original_fleets_at_sea']:
        fleet=fleets+4+132*f['fleet'];assert get(0x35320,fleet)==f['company'] and get(0x34674,fleet)==115
        actor=get(0x3697C,fleet);identity=get(0x7EE08,actor);fencing=get(0x7DCC8,actor,5)
        for s in f['ships']:
            model=get(0x36C94,fleet+12+8*s['slot']);assert model==s['model']
            assert get(0x1856C,model)==s['original_cannon_type']
            assert [get(0x183A0,model),get(0x181BC,model)]==s['stored_Hull_Crew']
        rows.append({**f,'original_admiral_actor_ID':identity,'original_admiral_actor_object':actor,
            'native_fencing':fencing,'native_max_HP':get(0x7DF58,actor,0,0),
            'lower_native_fencing_than_player':fencing<own_fencing})
    candidates=[r for r in rows if r['lower_native_fencing_than_player'] and any(s['native_strength']>=3 for s in r['ships'])]
    ROOT.mkdir(parents=True)
    save(ROOT/'original_admiral_and_gun_census.json',{'candidate':str(ROM),'candidate_sha256':release['candidate_sha256'],
        'snapshot':snapshot,'source_cannon_census':str(census_path),'source_cannon_census_sha256':sha(census_path.read_bytes()),
        'own_original_fencing':own_fencing,'all27_original_at_sea_fleets':rows,
        'lower_fencing_stronger_gun_encounter_candidates':candidates,
        'candidate_ranking_is_a_test_lead_not_proof_of_AI_duel_preference':True,
        'no_live_or_CPU_actor_equipment_HP_fencing_RNG_eligibility_or_result_changes':True,
        'no_original_reaction_event_or_editorial_completion_credit':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('Own original fencing',own_fencing,';lower-fencing stronger-gun candidates:')
    for r in candidates:print('fleet',r['fleet'],'company',r['company'],'actor',r['original_admiral_actor_ID'],'fencing',r['native_fencing'],'point',r['cached_map_point'])
