"""Bind three Ladies,both Seoul aliases and source chili-pepper cooking context."""
from pathlib import Path
import inspect,struct
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.current_build_native_context_v4774 import CurrentContext
from scripts.reconcile_lil_B183_terms_v4931 import bindings
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B193_terms_v5453')
SOURCE=Path('work/analysis/lil_B193_source_v5447/all15_clean_current_complete_context.json')
NAMES=Path('work/analysis/lil_B193_names_v5452/six_original_progressive_and_catalogue_name_consumers.json')
CONTROL=Path('work/analysis/lil_B193_controls_v5451/A000_C200_single_end_and_no_relative_or_predicate_contract.json')
ROLES={'166':'Lady','167':'Lady','168':'Lady'}
if __name__=='__main__':
    assert not ROOT.exists();packet,names,control=map(read,[SOURCE,NAMES,CONTROL])
    assert names['source_context_sha256']==control['source_context_sha256']==sha(SOURCE.read_bytes())
    assert names['progressive_nameplate_values']==names['full_catalogue_values']==ROLES
    native=names['native_six_consumer_cases']['rows'];assert len(native)==6
    assert all(not r['original_scratch_rings'] and not r['original_getter_writes'] and r['all_actor_models_and_unowned4MiB_exact'] for r in native)
    clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin');arm=NdsImage.open(packet['current_ROM']).read_file('/__arm9__.bin')
    anchor=next(r for r in read('translations/ordinary_name_fidelity_manuscript_v1.json')['records'] if r['index']==164);assert anchor['table_field']==0x122000
    roles=[]
    for ident,field,at in [(166,0x122040,0x15BC70),(167,0x122060,0x15BF00),(168,0x122080,0x15BD78)]:
        assert field==anchor['table_field']+(ident-164)*32 and struct.unpack_from('<I',clean,field)[0]==0x02000000+at
        value=clean[at:clean.index(0,at)+1];assert value[:-1].decode('cp932')=='貴婦人'
        roles.append(dict(actor_ID=ident,source_selector_hex=format(ident,'02X'),pointer_field=field,source_storage_offset=at,source_full_catalogue_role='貴婦人',approved_full_catalogue_role='Lady',source_terminated_hex=value.hex()))
    good=next(r for r in read('translations/commodity_name_manuscript_v343.json')['records'] if r['index']==29)
    fidelity=next(r for r in read('translations/commodity_fidelity_v2.json')['records'] if r['index']==29)
    assert good['Japanese']==fidelity['Japanese']=='トウガラシ' and good['English']==fidelity['English']=='Chili'
    pointer=struct.unpack_from('<I',clean,good['pointer_field'])[0];at=pointer-0x02000000
    assert clean[at:clean.index(0,at)].decode('cp932')=='トウガラシ'
    assert clean[good['pointer_field']+4:good['pointer_field']+12]==arm[good['pointer_field']+4:good['pointer_field']+12]==bytes.fromhex(good['metadata_hex'])
    cities=[]
    for field,at in [(0x1224C4,0x15B870),(0x123F34,0x15B920)]:
        ptr=struct.unpack_from('<I',clean,field)[0];assert ptr==0x02000000+at
        value=clean[at:clean.index(0,at)+1];assert value[:-1].decode('cp932')=='京城'
        assert [i for i in range(len(clean)-3) if clean[i:i+4]==struct.pack('<I',ptr)]==[field]
        cities.append(dict(pointer_field=field,source_pointer=ptr,source_storage_offset=at,source_text='京城',source_terminated_hex=value.hex(),approved_English='Seoul'))
    ROOT.mkdir(parents=True);ctx=CurrentContext('work/analysis/lil_B193_voices_v5448/current_native_input.json',packet['historical_snapshot_ROM'],ROOT/'current_context')
    live=ctx.execute(bindings,[r['pointer_field'] for r in roles+cities]+[good['pointer_field']]);ctx.machines.pop();assert not ctx.machines
    assert [r['text'] for r in live['rows']]==['Lady']*3+['Seoul']*2+['Chili']
    for row,current in zip(roles+cities,live['rows'][:5],strict=True):row.update(current)
    for role in roles:assert {r['pointer'] for r in native if r['actor_ID']==role['actor_ID']}=={role['current_runtime_pointer']}
    by={r['source_record_index']:r for r in packet['records']}
    for i,parts in {6:['初めて','素晴らしい料理'],10:['刺激的なお味'],14:['どうしたら','作れる'],17:['秘密はこれ'],21:['？'],25:['トウガラシ','香辛料','なんですって','この辺り','食材'],29:['お高い'],33:['そうでもありません'],37:['安心','今晩','使ってみようかしら'],40:['わたしも作りたい'],44:['今から','料理の仕方','教えて'],47:['本当に'],51:['ご親切'],55:['お友達','当然'],59:['京城','トウガラシ','流行しそう']}.items():
        assert all(part in by[i]['source_Japanese'] for part in parts),i
    assert all('京城' not in r['source_Japanese'] for i,r in by.items() if i!=59)
    paths=[SOURCE,NAMES,CONTROL,Path('translations/ordinary_name_fidelity_manuscript_v1.json'),Path('translations/commodity_name_manuscript_v343.json'),Path('translations/commodity_fidelity_v2.json'),Path(__file__)]
    save(ROOT/'three_Ladies_Seoul_Chili_and_cooking_friendship_reconciliation.json',dict(candidate=packet['current_ROM'],candidate_sha256=packet['current_ROM_sha256'],source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),
        approved_prose_names=ROLES,source_progressive_names=names['progressive_nameplate_values'],full_catalogue_names=names['full_catalogue_values'],three_source_full_catalogue_role_fields=roles,
        city='Seoul',two_source_current_city_aliases=cities,commodity_index=29,source_commodity='トウガラシ',commodity='Chili',source_supported_prose='chili peppers',commodity_binding=live['rows'][5],original_commodity_metadata_hex=good['metadata_hex'],
        three_distinct_source_Ladies_and_original_voice0_without_invented_personal_names_or_new_titles=True,
        source_cooking_preparation_question_and_immediate_teaching_offer_not_trade_advice=True,
        first_time_meal_praise_stimulating_flavor_reported_spice_classification_and_local_ingredient_compatibility_preserved=True,
        source_price_question_and_relative_reassurance_preserved_as_character_claims_without_amount_scarcity_or_profit=True,
        tonight_tentative_household_use_and_now_teaching_offer_not_completed_purchase_cooking_or_lesson=True,
        friendship_explicit_in_otomodachi_preserved_without_invented_kinship_romance_marriage_employment_or_prior_history=True,
        Chili29_individual_commodity_not_category_or_chili_stew_powder_recipe_origin_or_specific_quantity=True,
        existing_Chili29_older_fidelity_review_remains_open_no_UI_rename_or_new_widget_credit=True,
        both_Seoul_aliases_bound_to_source_Keijo_without_unapproved_place_rename=True,
        tentative_Chili_Seoul_FE_does_not_establish_earlier_location_or_earned_fashion=True,
        source18_linear_commands_one_A000_C200_end_two_tailzeros_no_predicates_relatives_or_item_presentation=True,
        all15_clean_first_glosses_precede_predecessor_English=True,no_predecessor_English_exposed=True,
        source_owned_pointer_adapter=inspect.getsource(bindings),current_native_context_plan=str(ctx.proof_path),current_native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        new_emulator_runs=0,new_review_credit=0,evidence={str(p):sha(p.read_bytes()) for p in paths},full_goal_complete=False))
    print('Three Ladies,both source Seoul aliases and Chili29 bound. Cooking,price concern,teaching offer and explicit friendship preserved;zero credit.')
