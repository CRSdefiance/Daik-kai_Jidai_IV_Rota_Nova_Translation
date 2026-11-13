"""Bind London and the Gems category without guessing the unknown gemstone."""
from pathlib import Path
import inspect
import struct
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.current_build_native_context_v4774 import CurrentContext
from scripts.verify_category_lookup_v754 import cpu_for,getter,UI_RETURNS
from scripts.native_machine_scoped_v764 import machine as clean_machine
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B182_terms_v4885')
SOURCE=Path('work/analysis/lil_B182_source_v4878/all8_clean_current_complete_context.json')
FIELDS=[0x122560,0x1222E4]

def live_bindings(arm,common,raw,plan):
    cpu,get,provider=machine(arm,common,raw,plan)
    before=bytes(cpu.mem_read(0x02000000,0x400000));cities=[];categories=[]
    for field in FIELDS:
        pointer=struct.unpack_from('<I',arm,field)[0]
        assert bytes(cpu.mem_read(0x02000000+field,4))==arm[field:field+4]
        value=bytes(cpu.mem_read(pointer,80)).split(b'\0')[0]
        assert value==b'London'
        cities.append(dict(pointer_field=field,current_runtime_pointer=pointer,
            text=value.decode('ascii'),terminated_hex=(value+b'\0').hex(),
            current_ARM9_pointer_word_matches_actual_snapshot=True))
    for parent in [*UI_RETURNS,0x0205FC48]:
        pointer=getter(cpu,12,parent);value=bytes(cpu.mem_read(pointer,80)).split(b'\0')[0]
        assert value==b'Gems'
        categories.append(dict(version='current',category_lookup_index=12,native_return_PC=parent,
            pointer=pointer,text='Gems',terminated_hex=(value+b'\0').hex(),
            original_stack_saved_registers_and_return_ABI_checked=True))
    assert bytes(cpu.mem_read(0x02000000,0x400000))==before
    return dict(cities=cities,categories=categories,all4MiB_preserved=True,
        executed_current_instruction_addresses=len(provider.executed_current))

if __name__=='__main__':
    assert not ROOT.exists();packet=read(SOURCE)
    np=Path('work/analysis/lil_B182_names_v4884/four_original_Lady_name_consumers.json')
    cp=Path('work/analysis/lil_B182_controls_v4883/two_predicates_three_A000_C200_ten_relative_sites_and_single_end.json')
    names,controls=read(np),read(cp)
    assert names['source_context_sha256']==controls['source_context_sha256']==sha(SOURCE.read_bytes())
    assert names['approved_prose_names']=={'166':'Lady','167':'Lady'}
    aliases=read('translations/entity_ship_names_arm9_v2.json')
    registered=next(r for r in aliases['records'] if r['offset']==0x1222E4)
    assert registered['english']=='London'
    clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin');cities=[];category=[]
    for field,at in zip(FIELDS,[0x15C62C,0x15C6BC],strict=True):
        pointer=struct.unpack_from('<I',clean,field)[0];assert pointer==0x02000000+at
        value=clean[at:clean.index(0,at)+1];assert value[:-1].decode('cp932')=='ロンドン'
        cities.append(dict(pointer_field=field,source_pointer=pointer,source_storage_offset=at,
            source_text='ロンドン',source_terminated_hex=value.hex(),approved_English='London'))
    cpu=clean_machine(clean)
    for parent in [*UI_RETURNS,0x0205FC48]:
        ptr=getter(cpu,12,parent);value=bytes(cpu.mem_read(ptr,80)).split(b'\0')[0]
        assert value.decode('cp932')=='宝石'
        category.append(dict(version='clean',category_lookup_index=12,native_return_PC=parent,
            pointer=ptr,text='宝石',terminated_hex=(value+b'\0').hex(),
            original_stack_saved_registers_and_return_ABI_checked=True))
    ROOT.mkdir(parents=True)
    ctx=CurrentContext('work/analysis/lil_B182_voices_v4879/current_native_input.json',packet['historical_snapshot_ROM'],ROOT/'current_context')
    live=ctx.execute(live_bindings);ctx.machines.pop();assert not ctx.machines
    for source,current in zip(cities,live['cities'],strict=True):source.update(current)
    category+=live['categories'];assert len(category)==12
    by={r['source_record_index']:r for r in packet['records']}
    assert all(s in by[62]['source_Japanese'] for s in ['ロンドン','宝石','流行しそう'])
    assert all('ロンドン' not in r['source_Japanese'] for i,r in by.items() if i!=62)
    for i,parts in {5:['王女様','ご婚約','ですって'],8:['公爵様','ご子息','ですって'],
        11:['婚約指輪','山ひとつ','お値段','だとか'],14:['公爵様','王女様','宝石'],
        17:['宝石','婦人','増えます','きっと'],21:['流行してからでは遅い','宝石','ご存じ'],
        25:['存じません','さっそく聞きに']}.items():
        assert all(s in by[i]['source_Japanese'] for s in parts),i
    deps=[SOURCE,np,cp,Path('translations/entity_ship_names_arm9_v2.json'),
        Path('dk4tool/patch/category_dialogue_lookup.py'),Path('work/analysis/category_dialogue_v754/lookup_native_ABI.json'),Path(__file__)]
    save(ROOT/'Lady_London_Gems_reported_engagement_and_unknown_stone.json',dict(
        candidate=packet['current_ROM'],candidate_sha256=packet['current_ROM_sha256'],
        source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),
        approved_dialogue_roles=names['approved_prose_names'],city='London',two_source_current_city_aliases=cities,
        category='Gems',source_category='宝石',category_index=12,all12_native_category_getter_bindings=category,
        current_actual_snapshot_binding=live,source_owned_adapter=inspect.getsource(live_bindings),
        current_native_context_plan=str(ctx.proof_path),current_native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        source_explicit_princess_duke_and_dukes_son_preserved=True,
        engagement_and_extravagant_ring_price_are_reported_not_verified_narration=True,
        royal_or_ducal_names_houses_nationality_age_marriage_date_currency_and_specific_gem_unknown=True,
        comic_gossip_knowledge_gap_and_urgent_intention_to_ask_preserved=True,
        anticipated_imitation_is_speaker_prediction_not_already_active_boom_shortage_price_or_profit=True,
        closing_forecast_prospective_and_not_proof_of_earlier_scene_location=True,
        no_prior_scene_Ruby_or_unproved_commodity_demand_mechanic_inherited=True,
        no_new_city_or_category_widget_fidelity_completion=True,no_predecessor_English_exposed=True,
        new_emulator_runs=0,new_review_credit=0,evidence={str(p):sha(p.read_bytes()) for p in deps},full_goal_complete=False))
    print('London aliases and Gems12 bound:12 native category lookups; source-explicit ranks/kinship,hearsay and unknown stone preserved. No credit.')
