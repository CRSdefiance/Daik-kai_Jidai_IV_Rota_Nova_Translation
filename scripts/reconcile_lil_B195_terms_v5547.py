"""Bind source Barkeep/Patron/Port Worker,both Veracruz aliases and individual Cheese8."""
import inspect
import struct
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.current_build_native_context_v4774 import CurrentContext
from scripts.reconcile_lil_B183_terms_v4931 import bindings
from scripts.verify_village_wrap_v608 import read, save

ROOT=Path('work/analysis/lil_B195_terms_v5547')
SOURCE=Path('work/analysis/lil_B195_source_v5541/all20_clean_current_complete_context.json')
NAMES=Path('work/analysis/lil_B195_names_v5546/six_original_progressive_and_catalogue_name_consumers.json')
CONTROL=Path('work/analysis/lil_B195_controls_v5545/A000_C200_single_end_and_no_relative_or_predicate_contract.json')
DISCOVERY=Path('work/analysis/lil_B195_terms_discovery_v5547/three_source_roles_cheese_and_all_Veracruz_pointer_occurrences.json')
ROLES={'92':'Barkeep','103':'Patron','119':'Port Worker'}

if __name__=='__main__':
    assert not ROOT.exists();packet,names,control,discovery=map(read,[SOURCE,NAMES,CONTROL,DISCOVERY])
    assert names['source_context_sha256']==control['source_context_sha256']==sha(SOURCE.read_bytes())
    assert names['progressive_nameplate_values']==names['full_catalogue_values']==ROLES
    native=names['native_six_consumer_cases']['rows']
    assert len(native)==6 and all(not r['original_scratch_rings'] and not r['original_getter_writes']
        and r['all_actor_models_and_unowned4MiB_exact'] for r in native)
    clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    arm=NdsImage.open(packet['current_ROM']).read_file('/__arm9__.bin')
    anchor=next(r for r in read('translations/ordinary_name_fidelity_manuscript_v1.json')['records'] if r['index']==164)
    assert anchor['table_field']==0x122000
    roles=[]
    for item,ident,jp in zip(discovery['roles'],[92,103,119],['酒場の親父','酒場の客','出港所の兄貴'],strict=True):
        field=item['pointer_field'];at=item['source_storage_offset']
        assert item['actor_ID']==ident and field==anchor['table_field']+(ident-164)*32
        assert struct.unpack_from('<I',clean,field)[0]==0x02000000+at
        raw=clean[at:clean.index(0,at)+1]
        assert raw.hex()==item['source_terminated_hex'] and raw[:-1].decode('cp932')==item['source_text']==jp
        roles.append(dict(**item,approved_English=ROLES[str(ident)]))
    good=next(r for r in read('translations/commodity_name_manuscript_v343.json')['records'] if r['index']==8)
    fidelity=next(r for r in read('translations/commodity_fidelity_v2.json')['records'] if r['index']==8)
    assert good['Japanese']==fidelity['Japanese']=='チーズ' and good['English']==fidelity['English']=='Cheese'
    ptr=struct.unpack_from('<I',clean,good['pointer_field'])[0];at=ptr-0x02000000
    assert clean[at:clean.index(0,at)].decode('cp932')=='チーズ'
    assert clean[good['pointer_field']+4:good['pointer_field']+12]==arm[good['pointer_field']+4:good['pointer_field']+12]==bytes.fromhex('b00400db58020100')
    cities=[]
    assert len(discovery['city_occurrences'])==2
    for item in discovery['city_occurrences']:
        at=item['source_storage_offset'];ptr=0x02000000+at;raw=clean[at:clean.index(0,at)+1]
        assert raw.hex()==item['source_terminated_hex'] and raw[:-1].decode('cp932')=='ヴェラクルス'
        fields=[i for i in range(len(clean)-3) if clean[i:i+4]==struct.pack('<I',ptr)]
        assert fields==item['pointer_fields'] and len(fields)==1
        cities.append(dict(pointer_field=fields[0],source_pointer=ptr,source_storage_offset=at,
            source_text='ヴェラクルス',source_terminated_hex=raw.hex(),approved_English='Veracruz'))
    ROOT.mkdir(parents=True)
    ctx=CurrentContext('work/analysis/lil_B195_voices_v5542/current_native_input.json',packet['historical_snapshot_ROM'],ROOT/'current_context')
    live=ctx.execute(bindings,[r['pointer_field'] for r in roles+cities]+[good['pointer_field']]);ctx.machines.pop()
    assert not ctx.machines and [r['text'] for r in live['rows']]==['Barkeep','Patron','Port Worker','Veracruz','Veracruz','Cheese']
    for row,current in zip(roles+cities,live['rows'][:5],strict=True):row.update(current)
    for role in roles:
        assert {r['pointer'] for r in native if r['actor_ID']==role['actor_ID']}=={role['current_runtime_pointer']}
    by={r['source_record_index']:r for r in packet['records']}
    fragments={6:['いい匂い'],9:['くんくん'],13:['親父','何の匂い'],17:['名物料理','チーズたっぷり','おいしい'],
        20:['本当にうまい'],24:['当たり前'],28:['俺たちにも１つ'],32:['ちょっとだけ','すぐにお持ち'],35:['お待ちどう'],
        39:['本当に早い'],43:['だまされたと思って','まずは食って'],46:['そうだな'],50:['モグモグ'],54:['モグモグ'],
        58:['うっめぇ'],62:['いける','すげえ'],65:['そうだろ'],69:['みんなに教えて'],73:['親父','この料理','きっと','大流行'],77:['ヴェラクルス','チーズ','流行しそう']}
    assert set(fragments)==set(by)
    for index,parts in fragments.items():assert all(p in by[index]['source_Japanese'] for p in parts),index
    assert packet['source_macro_counts']==dict(FI=0,FA=0,FO=0)
    assert all('ヴェラクルス' not in r['source_Japanese'] for i,r in by.items() if i!=77)
    evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,NAMES,CONTROL,DISCOVERY,
        Path('translations/ordinary_name_fidelity_manuscript_v1.json'),Path('translations/commodity_name_manuscript_v343.json'),
        Path('translations/commodity_fidelity_v2.json'),Path(__file__)]}
    save(ROOT/'three_roles_both_Veracruz_aliases_Cheese8_and_unnamed_specialty_reconciliation.json',dict(
        candidate=packet['current_ROM'],candidate_sha256=packet['current_ROM_sha256'],source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),
        approved_prose_names=ROLES,full_catalogue_names=names['full_catalogue_values'],source_name_fields=roles,
        six_original_readonly_name_consumers_preserve_all_unowned4MiB=True,
        city='Veracruz',two_source_current_city_aliases=cities,commodity_index=8,source_commodity='チーズ',commodity='Cheese',
        commodity_binding=live['rows'][5],original_commodity_metadata_hex='b00400db58020100',
        source_familiar_oyaji_and_aniki_role_wording_does_not_establish_fatherhood_brotherhood_or_new_kinship=True,
        source_three_original_voice0_roles_without_invented_rank_employment_or_personal_names=True,
        smell_sniff_skepticism_confident_retort_prompt_service_and_enthusiastic_payoff_preserved=True,
        source_unnamed_house_specialty_has_plenty_of_cheese_no_invented_pizza_recipe_cuisine_origin_price_or_health_effect=True,
        one_shared_order_not_two_servings_payment_or_purchase_mechanic=True,
        source_damasareta_idiom_coaxes_a_trial_without_actual_deception_fraud_or_danger=True,
        two_separate_chewing_beats_and_two_enthusiastic_taste_reactions_preserved=True,
        source_taste_praise_and_dish_popularity_certainty_remain_character_claims_not_narrator_guarantees=True,
        tell_everyone_is_future_social_intention_not_completed_advertising_trade_demand_profit_or_reward=True,
        Cheese8_individual_commodity_and_both_Veracruz_aliases_bound_without_new_widget_fidelity_credit=True,
        Cheese8_older_UI_fidelity_review_stays_open_separate_from_dialogue=True,
        tentative_Cheese_Veracruz_FE_not_earlier_location_or_earned_fashion=True,
        source23_linear_commands20_speeches_A000_C200_end_two_tailzeros_no_macros_predicates_or_relatives=True,
        source_A000_packed_effect_semantics_unbound_and_not_inferred=True,
        all20_clean_first_glosses_precede_predecessor_English_prose_comparison=True,
        raw_current_dispatch_hex_is_structural_evidence_not_translation_source=True,predecessor_English_prose_comparison_pending=True,
        source_owned_pointer_adapter=inspect.getsource(bindings),native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        evidence=evidence,new_emulator_runs=0,new_review_credit=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('Barkeep92,Patron103,PortWorker119,both Veracruz aliases and Cheese8 bound;all six name paths readonly. Whole-exchange context/unnamed specialty/familiar address stay source-faithful;zero credit.')
