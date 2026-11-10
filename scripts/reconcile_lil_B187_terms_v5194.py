"""Bind clean Sailor/Shopkeeper roles,Malacca and Almond before predecessor dialogue."""
from pathlib import Path
import inspect,struct
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.current_build_native_context_v4774 import CurrentContext
from scripts.reconcile_lil_B183_terms_v4931 import bindings
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B187_terms_v5194')
SOURCE=Path('work/analysis/lil_B187_source_v5188/all16_clean_current_complete_context.json')
NAMES=Path('work/analysis/lil_B187_names_v5193/four_original_progressive_and_catalogue_name_consumers.json')
CONTROL=Path('work/analysis/lil_B187_controls_v5192/A000_C200_single_end_and_no_relative_or_predicate_contract.json')
ROLES={'87':'Square Shopkeeper','155':'Sailor'}

if __name__=='__main__':
    assert not ROOT.exists();packet,names,controls=map(read,[SOURCE,NAMES,CONTROL])
    assert names['source_context_sha256']==controls['source_context_sha256']==sha(SOURCE.read_bytes())
    assert names['progressive_nameplate_values']==ROLES
    assert names['full_catalogue_values']=={'87':'Square Shopkeeper','155':'Retainer'}
    native=names['native_four_consumer_cases']['rows'];assert len(native)==4
    assert all(not r['original_scratch_rings'] and not r['original_getter_writes'] and r['all_actor_models_and_unowned4MiB_exact'] for r in native)
    clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    arm=NdsImage.open(packet['current_ROM']).read_file('/__arm9__.bin')
    assert clean[0x7ED88:0x7EE08]==arm[0x7ED88:0x7EE08]
    anchor=next(r for r in read('translations/ordinary_name_fidelity_manuscript_v1.json')['records'] if r['index']==164)
    assert anchor['table_field']==0x122000
    roles=[]
    for ident,field,at,japanese,english in [(87,0x121660,0x15D0E8,'広場の店主','Square Shopkeeper'),(155,0x121EE0,0x15BA18,'配下','Retainer')]:
        assert field==anchor['table_field']+(ident-164)*32
        pointer=struct.unpack_from('<I',clean,field)[0];assert pointer==0x02000000+at
        value=clean[at:clean.index(0,at)+1];assert value[:-1].decode('cp932')==japanese
        roles.append(dict(actor_ID=ident,pointer_field=field,source_pointer=pointer,source_storage_offset=at,
            source_full_catalogue_role=japanese,approved_full_catalogue_role=english,source_terminated_hex=value.hex(),ordinary_name_stride=32))
    special_pointer=struct.unpack_from('<I',clean,0x7EDD0)[0]
    assert special_pointer==struct.unpack_from('<I',arm,0x7EDD0)[0]==0x021484D4
    special_at=special_pointer-0x02000000;special=clean[special_at:clean.index(0,special_at)+1]
    assert special[:-1].decode('cp932')=='水夫'
    assert next(r for r in native if r['actor_ID']==155 and r['consumer']=='progressive-nameplate')['pointer']==special_pointer
    good=next(r for r in read('translations/commodity_name_manuscript_v343.json')['records'] if r['index']==78)
    fidelity=next(r for r in read('translations/commodity_fidelity_v2.json')['records'] if r['index']==78)
    assert good['Japanese']==fidelity['Japanese']=='アーモンド' and good['English']==fidelity['English']=='Almond'
    assert good['pointer_field']==0x15F2C0
    good_ptr=struct.unpack_from('<I',clean,good['pointer_field'])[0];good_at=good_ptr-0x02000000
    assert clean[good_at:clean.index(0,good_at)].decode('cp932')=='アーモンド'
    assert clean[good['pointer_field']+4:good['pointer_field']+12]==arm[good['pointer_field']+4:good['pointer_field']+12]==bytes.fromhex(good['metadata_hex'])
    cities=[]
    for field,at in [(0x122464,0x15C128),(0x123AAC,0x15C2C0)]:
        ptr=struct.unpack_from('<I',clean,field)[0];assert ptr==0x02000000+at
        value=clean[at:clean.index(0,at)+1];assert value[:-1].decode('cp932')=='マラッカ'
        cities.append(dict(pointer_field=field,source_pointer=ptr,source_storage_offset=at,source_text='マラッカ',
            source_terminated_hex=value.hex(),approved_English='Malacca'))
    ROOT.mkdir(parents=True)
    ctx=CurrentContext('work/analysis/lil_B187_voices_v5189/current_native_input.json',packet['historical_snapshot_ROM'],ROOT/'current_context')
    fields=[r['pointer_field'] for r in roles+cities]+[good['pointer_field'],0x7EDD0]
    live=ctx.execute(bindings,fields);ctx.machines.pop();assert not ctx.machines
    assert [r['text'] for r in live['rows']]==['Square Shopkeeper','Retainer','Malacca','Malacca','Almond','Sailor']
    for role,current in zip(roles,live['rows'][:2],strict=True):
        assert {r['pointer'] for r in native if r['actor_ID']==role['actor_ID'] and r['consumer']=='full-catalogue'}=={current['current_runtime_pointer']}
        role.update(current)
    for city,current in zip(cities,live['rows'][2:4],strict=True):city.update(current)
    by={r['source_record_index']:r for r in packet['records']}
    for i,parts in {6:['最近','咳がひどい','ゴホ'],10:['大丈夫'],14:['大丈夫','苦しい','ゴホ'],17:['最近','咳','よく見かける'],
            20:['悪い病気','流行ってんのかな'],24:['どっか','いい薬','聞いた'],27:['何ていう薬','ゴホ'],30:['名前は忘れた','アーモンド','そうだ'],
            33:['アーモンド'],37:['アーモンド','思った','覚えてた'],41:['効くのか','ゴホ'],45:['ウソみたいによく効く','すごく売れてる','ってさ'],
            48:['探してみる'],52:['俺も探してみる'],56:['ありがと','ゴホ'],60:['マラッカ','アーモンド','流行しそう']}.items():
        assert all(s in by[i]['source_Japanese'] for s in parts),i
    assert all('マラッカ' not in r['source_Japanese'] for i,r in by.items() if i!=60)
    paths=[SOURCE,NAMES,CONTROL,Path('translations/ordinary_name_fidelity_manuscript_v1.json'),
        Path('translations/commodity_name_manuscript_v343.json'),Path('translations/commodity_fidelity_v2.json'),Path(__file__)]
    save(ROOT/'Sailor_Square_Shopkeeper_Malacca_Almond_and_reported_remedy_reconciliation.json',dict(
        candidate=packet['current_ROM'],candidate_sha256=packet['current_ROM_sha256'],source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),
        approved_prose_names=ROLES,source_progressive_names=names['progressive_nameplate_values'],full_catalogue_names=names['full_catalogue_values'],
        two_source_full_catalogue_role_fields=roles,
        original_progressive_Sailor_literal=dict(pointer_field=0x7EDD0,source_pointer=special_pointer,source_text='水夫',source_terminated_hex=special.hex(),
            current_binding=live['rows'][5],unchanged_original7ED88_range151_to159_selects_this_literal=True,source_actor155_in_that_range=True),
        Sailor155_progressive_label_does_not_establish_player_employment_or_use_catalogue_Retainer_as_dialogue_rank=True,
        city='Malacca',two_source_current_city_aliases=cities,commodity_index=78,source_commodity='アーモンド',commodity='Almond',
        commodity_binding=live['rows'][4],original_commodity_metadata_hex=good['metadata_hex'],
        natural_dialogue_plural_Almonds_is_inflection_of_approved_Almond_not_UI_rename_or_new_commodity=True,
        cough_observation_and_speculative_illness_question_not_diagnosis_or_verified_outbreak=True,
        remedy_name_explicitly_forgotten_and_almonds_reported_as_ingredient_not_complete_recipe=True,
        surprise_at_almonds_explains_memory_without_expertise_or_invented_joke=True,
        source_explicit_reported_remedy_effectiveness_and_strong_sales_both_must_be_preserved=True,
        remedy_sales_are_hearsay_not_raw_almond_price_shortage_profit_or_verified_medical_effect=True,
        both_later_searches_are_intentions_not_purchase_use_or_recovery=True,
        continuing_cough_and_casual_gratitude_preserved=True,closing_Malacca_Almonds_notice_still_tentative=True,
        no_recipe_dose_ingredient_quantity_medical_role_kinship_or_earlier_scene_location_invented=True,
        source_all19_linear_commands_one_A000_C200_end_and_two_tailzeros_no_predicates_or_relative_sites=True,
        source_owned_pointer_adapter=inspect.getsource(bindings),current_native_context_plan=str(ctx.proof_path),
        current_native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),all16_clean_first_glosses_precede_predecessor_English=True,
        no_predecessor_English_exposed=True,no_new_city_commodity_or_name_widget_fidelity_completion=True,
        new_emulator_runs=0,new_review_credit=0,evidence={str(p):sha(p.read_bytes()) for p in paths},full_goal_complete=False))
    print('Clean Sailor/Retainer distinction,Square Shopkeeper,two Malacca aliases and Almond78 bound. Remedy effectiveness/sales remain hearsay;no old dialogue exposed or credit.')
