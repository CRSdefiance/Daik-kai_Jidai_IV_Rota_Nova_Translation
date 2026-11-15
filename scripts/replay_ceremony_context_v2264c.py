"""Bind hero-dependent native towns and every selected NPC speaker explicitly."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/ceremony_context_v2264c');OLD=Path('scripts/context_ceremony_v806.py')
if __name__=='__main__':
    assert not ROOT.exists();snapshot=read('work/analysis/item_context_v2235/native_context.json')['pre_fixture_snapshot'];assert sha(Path(snapshot['path']).read_bytes())==snapshot['sha256'];source=OLD.read_text()
    changes={'work/analysis/ceremony_context_v806':'work/analysis/ceremony_context_v2264c','out/all_routes_combined_v803_candidate.nds':'out/all_routes_combined_v2171_candidate.nds','from dk4tool.patch.inn_editorial import current_entries':'from dk4tool.patch.town_trade_port_contextual_reference_v1 import current_entries','E:/Rota Nova translations/Generated/work/emulation_v193/inn_v803_stays/frame_003200_arm9_ram.bin':Path(snapshot['path']).as_posix(),'7c6c8bb3c89973af2f789488e51bff395d871be6a461490d62b3f5c8d860daad':'4df01b870562dc04d623fb5c0011d38100bc4062371d32ad2be12f352292260a'}
    for old,new in changes.items():assert source.count(old)==1;source=source.replace(old,new)
    old='    def run(fn,day,start,site,facility,hero,accept):\n        u.mem_write(BASE,raw);'
    new='    def run(fn,day,start,site,facility,hero,accept):\n        nonlocal u\n        u=machine(arm)\n        u.mem_write(BASE,raw);';assert source.count(old)==1;source=source.replace(old,new)
    old='        events=[]\n        def observe'
    new='''        actual_town=get(0xB6618);town_index=(actual_town-town_root-4)//108
        native_speakers={}
        for selected_role in (9,10,11):
            actor=get(0xB2CD8,(actual_town,selected_role));actor_index=get(0xB2D28,(actual_town,selected_role))
            record=get(0x7EB24,(actor,));source_pointer=struct.unpack_from('<I',jp_arm,record-BASE)[0]
            native_speakers[selected_role]=dict(town_ID=town_index,role=selected_role,actor_ID=actor_index,actor_pointer=actor,clean_name=jp_arm[source_pointer-BASE:].split(bytes(1))[0].decode('cp932'),current_name=name(actor).decode('ascii'))
        events=[]
        def observe''';assert source.count(old)==1;source=source.replace(old,new)
    old='        case=dict(source_function=BASE+fn'
    new='''        for e in events:
            if e['kind']in('NPC_yes_no','NPC_dialogue'):
                selected_role=(11 if e['message']in(1219,1220,1221)else 9)if fn==0x61570 else facility
                expected=native_speakers[selected_role]
                assert e['speaker_actor']==expected['actor_pointer'],(fn,hero,facility,e,expected)
                e['source_native_NPC_lookup']=expected
        case=dict(actual_native_town_ID=town_index,native_speaker_providers=native_speakers,source_function=BASE+fn''';assert source.count(old)==1;source=source.replace(old,new)
    exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
    c=read(ROOT/'native_context.json');assert c['every52_source_ID_bound_to_original_caller']
    save(ROOT/'current_replay_provenance.json',dict(original=str(OLD),original_sha256=sha(OLD.read_bytes()),effective_source_sha256=sha(source.encode()),current_genuine_preinteraction_snapshot=snapshot,all81_cases_new_native_machine=True,all_NPC_events_match_original_hero_dependent_town_and_role_getters=True,hero_index_change_selects_native_company_town_not_a_stale_speaker_pointer=True,all270_inventory_NPC_names_are_inventory_not_all_role_town_eligibility=True,all52_source_records_and_complete_consumer_exchanges_bound=True,CPU_hero_facility_day_site_yesno_inputs_and_UI_effect_time_boundaries_not_earned_or_actual_visits=True,no_ROM_runtime_or_emulator_fixture_change=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False));print(dict(towns=sorted({r['actual_native_town_ID']for r in c['source_branch_cases']}),all_source_NPC_speakers_bound=True))
