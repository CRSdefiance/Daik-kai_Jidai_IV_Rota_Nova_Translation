"""Bind clean Owner/Cook roles, Alexandria aliases and source sweet-things scope."""
from pathlib import Path
import inspect,struct

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.current_build_native_context_v4774 import CurrentContext
from scripts.native_machine_scoped_v764 import machine as clean_machine
from scripts.reconcile_lil_B183_terms_v4931 import bindings
from scripts.verify_category_lookup_v754 import getter,UI_RETURNS
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B186_terms_v5139')
SOURCE=Path('work/analysis/lil_B186_source_v5132/all12_clean_current_complete_context.json')
NAMES=Path('work/analysis/lil_B186_names_v5137/four_original_progressive_and_catalogue_name_consumers.json')
CONTROL=Path('work/analysis/lil_B186_controls_v5138/one_predicate_three_A000_C200_six_relative_sites_and_single_end.json')
GLOSS=Path('work/analysis/lil_B186_clean_context_v5131/all12_clean_exchange_and_fresh_glosses.json')
ROLES={'174':'Owner','175':'Cook'}

def category(arm,common,raw,plan):
    cpu,get,provider=machine(arm,common,raw,plan)
    before=bytes(cpu.mem_read(0x02000000,0x400000));rows=[]
    for parent in [*UI_RETURNS,0x0205FC48]:
        pointer=getter(cpu,4,parent);value=bytes(cpu.mem_read(pointer,80)).split(b'\0')[0]
        assert value==b'Treats'
        rows.append(dict(index=4,native_return_PC=parent,pointer=pointer,text='Treats',terminated_hex=(value+b'\0').hex()))
    assert bytes(cpu.mem_read(0x02000000,0x400000))==before
    return dict(rows=rows,all4MiB_unchanged=True,current_executed_instruction_addresses=len(provider.executed_current))

if __name__=='__main__':
    assert not ROOT.exists();packet,names,controls,gloss=map(read,[SOURCE,NAMES,CONTROL,GLOSS])
    assert names['source_context_sha256']==controls['source_context_sha256']==sha(SOURCE.read_bytes())
    assert names['progressive_nameplate_values']==names['full_catalogue_values']==ROLES
    assert all(not r['original_scratch_rings'] and not r['original_getter_writes'] and r['all_actor_models_and_unowned4MiB_exact'] for r in names['native_four_consumer_cases']['rows'])
    clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    arm=NdsImage.open(packet['current_ROM']).read_file('/__arm9__.bin')
    assert arm[0x7ED88:0x7EDD4]==clean[0x7ED88:0x7EDD4]
    anchor=next(r for r in read('translations/ordinary_name_fidelity_manuscript_v1.json')['records'] if r['index']==164)
    assert anchor['table_field']==0x122000
    roles=[]
    for ident,field,at,source,approved in [(174,0x122140,0x15C0C8,'オーナー','Owner'),(175,0x122160,0x15BC00,'コック','Cook')]:
        assert field==anchor['table_field']+(ident-anchor['index'])*32
        pointer=struct.unpack_from('<I',clean,field)[0];assert pointer==0x02000000+at
        value=clean[at:clean.index(0,at)+1];assert value[:-1].decode('cp932')==source
        roles.append(dict(actor_ID=ident,pointer_field=field,source_pointer=pointer,source_storage_offset=at,source_role=source,source_terminated_hex=value.hex(),approved_role=approved,ordinary_name_stride=32,anchor_index=164))
    cities=[]
    for field,at in [(0x1223E4,0x15E4D0),(0x1230B4,0x15E624)]:
        pointer=struct.unpack_from('<I',clean,field)[0];assert pointer==0x02000000+at
        value=clean[at:clean.index(0,at)+1];assert value[:-1].decode('cp932')=='アレキサンドリア'
        cities.append(dict(pointer_field=field,source_pointer=pointer,source_storage_offset=at,source_text='アレキサンドリア',source_terminated_hex=value.hex(),approved_English='Alexandria'))
    cpu=clean_machine(clean);category_rows=[]
    for parent in [*UI_RETURNS,0x0205FC48]:
        pointer=getter(cpu,4,parent);value=bytes(cpu.mem_read(pointer,80)).split(b'\0')[0]
        assert value.decode('cp932')=='嗜好品'
        category_rows.append(dict(version='clean',index=4,native_return_PC=parent,pointer=pointer,text='嗜好品',terminated_hex=(value+b'\0').hex()))
    ROOT.mkdir(parents=True)
    ctx=CurrentContext('work/analysis/lil_B186_voices_v5133/current_native_input.json',packet['historical_snapshot_ROM'],ROOT/'current_context')
    fields=[r['pointer_field'] for r in roles+cities]
    live=ctx.execute(bindings,fields);ctx.machines.pop()
    assert [r['text'] for r in live['rows']]==['Owner','Cook','Alexandria','Alexandria']
    for role,current in zip(roles,live['rows'][:2],strict=True):
        assert {r['pointer'] for r in names['native_four_consumer_cases']['rows'] if r['actor_ID']==role['actor_ID']}=={current['current_runtime_pointer']}
        role.update(current)
    for city,current in zip(cities,live['rows'][2:],strict=True):city.update(current)
    native_category=ctx.execute(category);ctx.machines.pop();assert not ctx.machines
    category_rows += [dict(version='current',**r) for r in native_category['rows']]
    assert len(category_rows)==12
    by={r['source_record_index']:r for r in packet['records']}
    for index,parts in {5:['何か足りない','甘いもの','甘み'],9:['甘みですか'],13:['さっぱり','お客様','スっウィート','スウィート'],16:['そうですかね'],20:['わたしがそう言う','絶対'],23:['甘さを増やす','どうしたら'],26:['考える','お仕事'],29:['へいへい'],33:['甘いもの','流行る','確実'],36:['へいへい'],40:['スウィート','がんばって','おっほほ'],63:['アレキサンドリア','甘い物','流行しそう']}.items():
        assert all(s in by[index]['source_Japanese'] for s in parts),index
    assert all('アレキサンドリア' not in r['source_Japanese'] for index,r in by.items() if index!=63)
    assert all('嗜好品' not in r['source_Japanese'] for r in by.values())
    assert len(gloss['records'])==12 and gloss['read_no_predecessor_English']
    paths=[SOURCE,NAMES,CONTROL,GLOSS,Path('translations/ordinary_name_fidelity_manuscript_v1.json'),Path('dk4tool/patch/category_dialogue_lookup.py'),Path(__file__)]
    save(ROOT/'Owner_Cook_Alexandria_and_sweet_things_context_reconciliation.json',dict(
        candidate=packet['current_ROM'],candidate_sha256=packet['current_ROM_sha256'],source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),
        approved_prose_names=ROLES,two_original_role_fields=roles,two_source_current_city_aliases=cities,city='Alexandria',
        current_actual_pointer_binding=live,source_owned_pointer_adapter=inspect.getsource(bindings),
        category4_source='嗜好品',category4_approved='Treats',all12_category4_native_bindings=category_rows,current_category_binding=native_category,source_owned_category_adapter=inspect.getsource(category),
        source_notice_says_sweet_things_not_UI_category4=True,notice_sweet_things_English='Sweets',
        Sweets_is_broad_source_supported_collective_not_a_single_commodity_ID_or_new_UI_category=True,
        no_category4_all_goods_Sugar_Honey_Cacao_or_packed_effect_bitfield_semantics_claim=True,
        customer_wording_supported_by_explicit_ookyaku_and_clean_Owner_Cook_roles=True,
        light_clean_flavor_is_Owners_judgment_not_narrator_verdict=True,
        missing_sweetness_is_food_flavor_preparation_not_trade_advice=True,
        no_dish_recipe_ingredient_amount_relationship_rank_nobility_or_customer_identity_invented=True,
        stretched_English_loan_sweet_repetition_and_stylized_confident_laugh_require_comic_delivery=True,
        Owners_self_authority_and_confident_future_prediction_are_character_claims=True,
        Cooks_doubt_then_practical_question_and_two_perfunctory_replies_remain_distinct=True,
        final_Alexandria_notice_tentative_without_earlier_scene_location_or_earned_boom_claim=True,
        all12_clean_first_glosses_preceded_any_predecessor_dialogue_exposure=True,
        no_predecessor_English_exposed=False,
        exposure_disclosure='A terminology search after all12 clean glosses and the role/voice/control bindings incidentally displayed the older closing FE Sweets may catch on in Alexandria and parallel route notices. The preceding11 spoken B186 lines have not been exposed before this reconciliation. Those older notices are not evidence for commodity/category mechanics.',
        no_new_city_category_or_name_widget_fidelity_completion=True,new_emulator_runs=0,new_review_credit=0,
        current_native_context_plan=str(ctx.proof_path),current_native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        evidence={str(p):sha(p.read_bytes()) for p in paths},full_goal_complete=False))
    print('Owner/Cook and two Alexandria aliases bound; twelve category calls distinguish broad Sweets from Treats4. Incidental old FE exposure disclosed; no credit.')
