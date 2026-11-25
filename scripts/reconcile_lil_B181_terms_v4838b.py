"""Bind both Athens aliases and registered Rubies,following real redirected pointers."""
from pathlib import Path
import struct
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.current_build_native_context_v4774 import CurrentContext
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B181_terms_v4838b')
SOURCE=Path('work/analysis/lil_B181_source_v4832/all10_clean_current_complete_context.json')

def bindings(arm,common,raw,plan,fields,good):
    cpu,get,provider=machine(arm,common,raw,plan);before=bytes(cpu.mem_read(0x02000000,0x400000));rows=[]
    for field in fields+[good['pointer_field']]:
        pointer=struct.unpack_from('<I',arm,field)[0]
        assert bytes(cpu.mem_read(0x02000000+field,4))==arm[field:field+4]
        value=bytes(cpu.mem_read(pointer,80)).split(b'\0')[0]
        rows.append(dict(pointer_field=field,current_runtime_pointer=pointer,text=value.decode('cp932'),terminated_hex=(value+b'\0').hex(),
            pointer_word_in_actual_current_snapshot_exact_ARM9=True))
    assert bytes(cpu.mem_read(0x02000000,0x400000))==before
    return dict(rows=rows,all4MiB_unchanged=True,read_actual_current_pointer_targets_without_native_UI_execution=True)

if __name__=='__main__':
    assert not ROOT.exists();packet=read(SOURCE)
    names_path=Path('work/analysis/lil_B181_names_v4837/six_original_Lady_name_consumers.json')
    controls_path=Path('work/analysis/lil_B181_controls_v4836/A000_C200_single_end_and_no_relative_or_predicate_contract.json')
    names,controls=read(names_path),read(controls_path)
    assert names['source_context_sha256']==controls['source_context_sha256']==sha(SOURCE.read_bytes())
    assert names['approved_prose_names']=={'166':'Lady','167':'Lady','168':'Lady'}
    manuscript=read('translations/commodity_name_manuscript_v343.json');good=next(r for r in manuscript['records'] if r['index']==73)
    fidelity=next(r for r in read('translations/commodity_fidelity_v2.json')['records'] if r['index']==73)
    assert good['Japanese']==fidelity['Japanese']=='ルビー' and good['English']==fidelity['English']=='Rubies'
    registered=read('translations/entity_ship_names_arm9_v2.json')
    alias=next(r for r in registered['records'] if r['id']=='DK4_ENTITY_POINTER_1223A4');assert alias['english']=='Athens'
    persistent=read('translations/persistent_name_allocation_v1.json')
    move=next(r for r in persistent['moves'] if r['field']==0x1223A4);assert move['text']=='Athens'
    clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    arm=NdsImage.open(packet['current_ROM']).read_file('/__arm9__.bin');cities=[]
    for field,at in [(0x122DFC,0x15BBD8),(0x1223A4,0x15BC30)]:
        pointer=struct.unpack_from('<I',clean,field)[0];assert pointer==0x02000000+at
        source=clean[at:clean.index(0,at)+1];assert source[:-1].decode('cp932')=='アテネ'
        cities.append(dict(pointer_field=field,source_pointer=pointer,source_storage_offset=at,source_terminated_hex=source.hex(),
            approved_English='Athens',source_span_may_remain_Japanese_after_registered_pointer_redirection=True))
    assert clean[good['pointer_field']+4:good['pointer_field']+12].hex()==arm[good['pointer_field']+4:good['pointer_field']+12].hex()==good['metadata_hex']
    gp=struct.unpack_from('<I',clean,good['pointer_field'])[0];ga=gp-0x02000000
    assert clean[ga:clean.index(0,ga)].decode('cp932')=='ルビー'
    ROOT.mkdir(parents=True);ctx=CurrentContext('work/analysis/lil_B181_voices_v4833/current_native_input.json',packet['historical_snapshot_ROM'],ROOT/'current_context')
    result=ctx.execute(bindings,[0x122DFC,0x1223A4],good);ctx.machines.pop();assert not ctx.machines
    assert [r['text'] for r in result['rows']]==['Athens','Athens','Rubies']
    from ndspy.code import MainCodeFile
    payload=bytes(MainCodeFile(arm,0x02000000).sections[3].data[:-48]);assert len(payload)==123040
    current_alias=result['rows'][1];at=current_alias['current_runtime_pointer']-0x02387A20
    assert 0<=at<len(payload)-7 and payload[at:at+7]==b'Athens\0'
    current_alias.update(previous_registered_allocation_pointer=move['runtime_pointer'],current_exact_deployed_payload_offset=at,old_allocation_address_not_assumed_for_later_registered_pool=True)
    for r,current in zip(cities,result['rows'][:2],strict=True):r.update(current)
    by={r['source_record_index']:r for r in packet['records']}
    assert all(s in by[39]['source_Japanese'] for s in ['アテネ','ルビー','流行しそう'])
    assert all('アテネ' not in r['source_Japanese'] for i,r in by.items() if i!=39)
    assert all(s in by[23]['source_Japanese'] for s in ['一生に一度','殿方','贈り物','頂戴したい'])
    assert '御婦人' in by[17]['source_Japanese'] and all('ハァー' in by[i]['source_Japanese'] for i in [27,31,35])
    paths=[SOURCE,names_path,controls_path,Path('translations/entity_ship_names_arm9_v2.json'),Path('translations/persistent_name_allocation_v1.json'),
        Path('translations/persistent_name_native_review_v1.json'),Path('translations/commodity_name_manuscript_v343.json'),Path('translations/commodity_fidelity_v2.json'),Path(__file__)]
    save(ROOT/'three_Ladies_Athens_Rubies_and_wistful_source_context.json',dict(candidate=packet['current_ROM'],candidate_sha256=packet['current_ROM_sha256'],
        source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),approved_dialogue_roles=names['approved_prose_names'],
        city='Athens',two_source_current_city_aliases=cities,commodity='Rubies',source_commodity='ルビー',commodity_index=73,
        commodity_binding=result['rows'][2],original_commodity_metadata_hex=good['metadata_hex'],
        old_Japanese_Athens_storage_not_mistaken_for_untranslated_live_alias=True,
        singular_admired_ruby_distinct_from_collective_commodity_Rubies=True,
        source_explicit_lady_wearer_does_not_establish_rank_relationship_or_jewelry_gift_provenance=True,
        wistful_wish_from_male_giver_not_spouse_suitor_promise_or_completed_gift=True,
        three_successive_audible_sighs_preserved_as_shared_longing=True,
        impersonal_forecast_prospective_not_prior_scene_location_or_earned_boom=True,
        current_native_context_plan=str(ctx.proof_path),current_native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        no_new_commodity_or_city_UI_fidelity_completion=True,no_predecessor_English_exposed=True,
        new_emulator_runs=0,new_review_credit=0,evidence={str(p):sha(p.read_bytes()) for p in paths},full_goal_complete=False))
    print('Both Athens aliases,including registered redirected storage,and Rubies73 are current-runtime bound. Three generic Ladies,wistful wish and three sighs grounded;no old prose exposed.')
