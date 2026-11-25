"""Bind Sailor/Retainer,Port Worker,Tobacco33 and the one Istanbul alias."""
from pathlib import Path
import inspect,struct
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.current_build_native_context_v4774 import CurrentContext
from scripts.reconcile_lil_B183_terms_v4931 import bindings
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B192_terms_v5412')
SOURCE=Path('work/analysis/lil_B192_source_v5406/all8_clean_current_complete_context.json')
NAMES=Path('work/analysis/lil_B192_names_v5411/four_original_progressive_and_catalogue_name_consumers.json')
CONTROL=Path('work/analysis/lil_B192_controls_v5410/A000_C200_single_end_and_no_relative_or_predicate_contract.json')
ROLES={'115':'Port Worker','153':'Sailor'}
if __name__=='__main__':
    assert not ROOT.exists();packet,names,controls=map(read,[SOURCE,NAMES,CONTROL])
    assert names['source_context_sha256']==controls['source_context_sha256']==sha(SOURCE.read_bytes())
    assert names['progressive_nameplate_values']==ROLES and names['full_catalogue_values']=={'115':'Port Worker','153':'Retainer'}
    native=names['native_four_consumer_cases']['rows'];assert len(native)==4
    assert all(not r['original_scratch_rings'] and not r['original_getter_writes'] and r['all_actor_models_and_unowned4MiB_exact'] for r in native)
    clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin');arm=NdsImage.open(packet['current_ROM']).read_file('/__arm9__.bin')
    assert clean[0x7ED88:0x7EE08]==arm[0x7ED88:0x7EE08]
    anchor=next(r for r in read('translations/ordinary_name_fidelity_manuscript_v1.json')['records'] if r['index']==164);assert anchor['table_field']==0x122000
    roles=[]
    for ident,field,at,japanese,english in [(115,0x1219E0,0x15DB94,'出港所の兄貴','Port Worker'),(153,0x121EA0,0x15B928,'配下','Retainer')]:
        assert field==anchor['table_field']+(ident-164)*32 and struct.unpack_from('<I',clean,field)[0]==0x02000000+at
        value=clean[at:clean.index(0,at)+1];assert value[:-1].decode('cp932')==japanese
        roles.append(dict(actor_ID=ident,source_selector_hex=format(ident,'02X'),pointer_field=field,source_storage_offset=at,
            source_full_catalogue_role=japanese,approved_full_catalogue_role=english,source_terminated_hex=value.hex()))
    special=struct.unpack_from('<I',clean,0x7EDD0)[0];assert special==struct.unpack_from('<I',arm,0x7EDD0)[0]==0x021484D4
    at=special-0x02000000;specialbytes=clean[at:clean.index(0,at)+1];assert specialbytes[:-1].decode('cp932')=='水夫'
    assert next(r for r in native if r['actor_ID']==153 and r['consumer']=='progressive-nameplate')['pointer']==special
    good=next(r for r in read('translations/commodity_name_manuscript_v343.json')['records'] if r['index']==33)
    fidelity=next(r for r in read('translations/commodity_fidelity_v2.json')['records'] if r['index']==33)
    assert good['Japanese']==fidelity['Japanese']=='タバコ' and good['English']==fidelity['English']=='Tobacco'
    assert good['pointer_field']==0x15F0A4
    pointer=struct.unpack_from('<I',clean,good['pointer_field'])[0];at=pointer-0x02000000
    assert clean[at:clean.index(0,at)].decode('cp932')=='タバコ'
    assert clean[good['pointer_field']+4:good['pointer_field']+12]==arm[good['pointer_field']+4:good['pointer_field']+12]==bytes.fromhex(good['metadata_hex'])
    field,at=0x122F58,0x15DFE4;cityptr=struct.unpack_from('<I',clean,field)[0];assert cityptr==0x02000000+at
    city=clean[at:clean.index(0,at)+1];assert city[:-1].decode('cp932')=='イスタンブール'
    assert [i for i in range(len(clean)-3) if clean[i:i+4]==struct.pack('<I',cityptr)]==[field]
    cityrow=dict(pointer_field=field,source_pointer=cityptr,source_storage_offset=at,source_text='イスタンブール',source_terminated_hex=city.hex(),approved_English='Istanbul')
    ROOT.mkdir(parents=True);ctx=CurrentContext('work/analysis/lil_B192_voices_v5407/current_native_input.json',packet['historical_snapshot_ROM'],ROOT/'current_context')
    live=ctx.execute(bindings,[r['pointer_field'] for r in roles]+[field,good['pointer_field'],0x7EDD0]);ctx.machines.pop();assert not ctx.machines
    assert [r['text'] for r in live['rows']]==['Port Worker','Retainer','Istanbul','Tobacco','Sailor']
    for role,current in zip(roles,live['rows'][:2],strict=True):
        assert {r['pointer'] for r in native if r['actor_ID']==role['actor_ID'] and r['consumer']=='full-catalogue'}=={current['current_runtime_pointer']};role.update(current)
    cityrow.update(live['rows'][2]);by={r['source_record_index']:r for r in packet['records']}
    for i,parts in {6:['タバコ','吸ったこと'],10:['もしかして','まだ吸ってない'],13:['機会がなくて','実はまだ'],16:['こんなに流行','この街','きっと','おまえぐらい'],
        20:['そ、そうかな','俺も吸ってみたい'],23:['吸わせてやる','ついて来い'],26:['う、うん'],30:['イスタンブール','タバコ','流行しそう']}.items():assert all(part in by[i]['source_Japanese'] for part in parts),i
    assert all('イスタンブール' not in r['source_Japanese'] for i,r in by.items() if i!=30)
    paths=[SOURCE,NAMES,CONTROL,Path('translations/ordinary_name_fidelity_manuscript_v1.json'),Path('translations/commodity_name_manuscript_v343.json'),Path('translations/commodity_fidelity_v2.json'),Path(__file__)]
    save(ROOT/'Sailor_Port_Worker_Istanbul_Tobacco_and_curiosity_reconciliation.json',dict(candidate=packet['current_ROM'],candidate_sha256=packet['current_ROM_sha256'],
        source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),approved_prose_names=ROLES,
        source_progressive_names=names['progressive_nameplate_values'],full_catalogue_names=names['full_catalogue_values'],two_source_full_catalogue_role_fields=roles,
        original_progressive_Sailor_literal=dict(pointer_field=0x7EDD0,source_pointer=special,source_text='水夫',source_terminated_hex=specialbytes.hex(),current_binding=live['rows'][4],unchanged_original_range151_to159_selects_actor153=True),
        city='Istanbul',one_source_current_city_alias=cityrow,commodity_index=33,source_commodity='タバコ',commodity='Tobacco',commodity_binding=live['rows'][3],original_commodity_metadata_hex=good['metadata_hex'],
        tobacco_is_individual_commodity33_not_category_or_new_UI_name=True,no_unproved_second_Istanbul_alias_or_new_widget_completion=True,
        Sailor153_catalogue_Retainer_does_not_prove_player_employment_rank_or_smoking_experience=True,
        Port_Worker115_familiar_aniki_role_does_not_prove_brotherhood_or_kinship=True,
        question_reversal_lack_of_opportunity_popularity_hyperbole_stammered_curiosity_offer_and_hesitant_assent_preserved=True,
        probably_only_person_in_this_town_is_character_hyperbole_not_narrator_statistics_or_named_location=True,
        source_tobacco_and_smoking_not_sanitized_or_changed_to_pipe_cigar_cigarette_or_brand=True,
        no_invented_age_rank_employment_smoking_history_dependence_coercion_or_health_claim=True,
        offer_and_follow_me_assent_not_completed_smoking_purchase_gift_or_specific_destination=True,
        tentative_Tobacco_Istanbul_FE_distinct_from_character_popularity_claim_prior_location_or_earned_fashion=True,
        source11_linear_commands_one_A000_C200_end_two_tailzeros_no_predicates_or_relatives=True,
        all8_clean_first_glosses_precede_predecessor_English=True,no_predecessor_English_exposed=True,no_new_city_commodity_or_name_widget_fidelity_completion=True,
        source_owned_pointer_adapter=inspect.getsource(bindings),current_native_context_plan=str(ctx.proof_path),current_native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        new_emulator_runs=0,new_review_credit=0,evidence={str(p):sha(p.read_bytes()) for p in paths},full_goal_complete=False))
    print('Port Worker115,Sailor153/Retainer153,one Istanbul alias and Tobacco33 bound. Curiosity,popularity rhetoric and intentions remain distinct;zero credit.')
