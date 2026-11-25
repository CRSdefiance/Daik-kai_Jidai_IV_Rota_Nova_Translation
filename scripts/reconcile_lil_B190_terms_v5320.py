"""Bind Sailor/Retainer,Port Worker,Havana and the source medicine category."""
from pathlib import Path
import inspect,struct
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.current_build_native_context_v4774 import CurrentContext
from scripts.native_machine_scoped_v764 import machine as clean_machine
from scripts.reconcile_lil_B183_terms_v4931 import bindings
from scripts.verify_category_lookup_v754 import getter,UI_RETURNS
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B190_terms_v5320')
SOURCE=Path('work/analysis/lil_B190_source_v5314/all17_clean_current_complete_context.json')
NAMES=Path('work/analysis/lil_B190_names_v5319/four_original_progressive_and_catalogue_name_consumers.json')
CONTROL=Path('work/analysis/lil_B190_controls_v5318/one_predicate_three_A000_C200_six_relative_sites_and_single_end.json')
ROLES={'119':'Port Worker','159':'Sailor'}

def category13(arm,common,raw,plan):
    cpu,get,provider=machine(arm,common,raw,plan);before=bytes(cpu.mem_read(0x02000000,0x400000));rows=[]
    for parent in [*UI_RETURNS,0x0205FC48]:
        pointer=getter(cpu,13,parent);value=bytes(cpu.mem_read(pointer,80)).split(b'\0')[0]
        expected=b'Medicine' if parent==0x0205FC48 else b'Med';assert value==expected
        rows.append(dict(index=13,native_return_PC=parent,pointer=pointer,text=value.decode('ascii'),terminated_hex=(value+b'\0').hex()))
    assert bytes(cpu.mem_read(0x02000000,0x400000))==before
    return dict(rows=rows,all4MiB_unchanged=True,current_executed_instruction_addresses=len(provider.executed_current))

if __name__=='__main__':
    assert not ROOT.exists();packet,names,controls=map(read,[SOURCE,NAMES,CONTROL])
    assert names['source_context_sha256']==controls['source_context_sha256']==sha(SOURCE.read_bytes())
    assert names['progressive_nameplate_values']==ROLES and names['full_catalogue_values']=={'119':'Port Worker','159':'Retainer'}
    native=names['native_four_consumer_cases']['rows'];assert len(native)==4
    assert all(not r['original_scratch_rings'] and not r['original_getter_writes'] and r['all_actor_models_and_unowned4MiB_exact'] for r in native)
    clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin');arm=NdsImage.open(packet['current_ROM']).read_file('/__arm9__.bin')
    assert clean[0x7ED88:0x7EE08]==arm[0x7ED88:0x7EE08]
    anchor=next(r for r in read('translations/ordinary_name_fidelity_manuscript_v1.json')['records'] if r['index']==164);assert anchor['table_field']==0x122000
    roles=[]
    for ident,field,at,japanese,english in [(119,0x121A60,0x15DBD4,'出港所の兄貴','Port Worker'),(159,0x121F60,0x15B978,'配下','Retainer')]:
        assert field==anchor['table_field']+(ident-164)*32
        pointer=struct.unpack_from('<I',clean,field)[0];assert pointer==0x02000000+at
        value=clean[at:clean.index(0,at)+1];assert value[:-1].decode('cp932')==japanese
        roles.append(dict(actor_ID=ident,source_selector_hex=format(ident,'02X'),pointer_field=field,source_pointer=pointer,source_storage_offset=at,
            source_full_catalogue_role=japanese,approved_full_catalogue_role=english,source_terminated_hex=value.hex(),ordinary_name_stride=32))
    special_pointer=struct.unpack_from('<I',clean,0x7EDD0)[0];assert special_pointer==struct.unpack_from('<I',arm,0x7EDD0)[0]==0x021484D4
    at=special_pointer-0x02000000;special=clean[at:clean.index(0,at)+1];assert special[:-1].decode('cp932')=='水夫'
    assert next(r for r in native if r['actor_ID']==159 and r['consumer']=='progressive-nameplate')['pointer']==special_pointer
    field,at=0x124104,0x15BCC8;ptr=struct.unpack_from('<I',clean,field)[0];assert ptr==0x02000000+at
    city=clean[at:clean.index(0,at)+1];assert city[:-1].decode('cp932')=='ハバナ'
    assert [i for i in range(len(clean)-3) if clean[i:i+4]==struct.pack('<I',ptr)]==[field]
    cityrow=dict(pointer_field=field,source_pointer=ptr,source_storage_offset=at,source_text='ハバナ',source_terminated_hex=city.hex(),approved_English='Havana')
    cpu=clean_machine(clean);category_rows=[]
    for parent in [*UI_RETURNS,0x0205FC48]:
        p=getter(cpu,13,parent);value=bytes(cpu.mem_read(p,80)).split(b'\0')[0];assert value.decode('cp932')=='薬'
        category_rows.append(dict(version='clean',index=13,native_return_PC=parent,pointer=p,text='薬',terminated_hex=(value+b'\0').hex()))
    ROOT.mkdir(parents=True)
    ctx=CurrentContext('work/analysis/lil_B190_voices_v5315/current_native_input.json',packet['historical_snapshot_ROM'],ROOT/'current_context')
    live=ctx.execute(bindings,[r['pointer_field'] for r in roles]+[field,0x7EDD0]);ctx.machines.pop()
    assert [r['text'] for r in live['rows']]==['Port Worker','Retainer','Havana','Sailor']
    for role,current in zip(roles,live['rows'][:2],strict=True):
        assert {r['pointer'] for r in native if r['actor_ID']==role['actor_ID'] and r['consumer']=='full-catalogue'}=={current['current_runtime_pointer']};role.update(current)
    cityrow.update(live['rows'][2]);cat=ctx.execute(category13);ctx.machines.pop();assert not ctx.machines
    category_rows.extend(dict(version='current',**r) for r in cat['rows']);assert len(category_rows)==12
    by={r['source_record_index']:r for r in packet['records']}
    for i,parts in {24:['知ってる'],28:['何を'],32:['お屋敷','旦那'],36:['原因不明','病気'],40:['そうそう'],44:['誰だって知ってる'],
        48:['その後'],52:['その後'],56:['一発で治した','市販の薬','ってさ'],59:['市販の薬','原因不明','治った'],63:['すごい話'],
        67:['だが','本当か'],71:['本当らしい','万病に効く','評判'],74:['すげえ','俺も欲しい'],77:['買いに行って'],81:['行こう'],85:['ハバナ','薬','流行しそう']}.items():assert all(s in by[i]['source_Japanese'] for s in parts),i
    assert all('ハバナ' not in r['source_Japanese'] for i,r in by.items() if i!=85)
    paths=[SOURCE,NAMES,CONTROL,Path('translations/ordinary_name_fidelity_manuscript_v1.json'),Path('dk4tool/patch/category_dialogue_lookup.py'),Path(__file__)]
    save(ROOT/'Sailor_Port_Worker_Havana_Medicine_and_reported_cure_reconciliation.json',dict(
        candidate=packet['current_ROM'],candidate_sha256=packet['current_ROM_sha256'],source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),
        approved_prose_names=ROLES,source_progressive_names=names['progressive_nameplate_values'],full_catalogue_names=names['full_catalogue_values'],two_source_full_catalogue_role_fields=roles,
        original_progressive_Sailor_literal=dict(pointer_field=0x7EDD0,source_pointer=special_pointer,source_text='水夫',source_terminated_hex=special.hex(),current_binding=live['rows'][3],
            unchanged_original7ED88_range151_to159_selects_this_literal=True,source_actor159_is_inclusive_upper_bound_of_range=True),
        Sailor159_does_not_establish_player_employment_or_use_catalogue_Retainer_as_dialogue_rank=True,
        Port_Worker119_familiar_aniki_role_does_not_establish_brother_or_kinship=True,city='Havana',one_source_current_city_alias=cityrow,
        no_unproved_second_city_alias_or_new_city_widget_completion=True,category_index=13,source_category='薬',approved_full_category='Medicine',compact_UI_category='Med',
        all12_category13_native_bindings=category_rows,current_category_binding=cat,source_owned_category_adapter=inspect.getsource(category13),
        medicine_is_source_category13_and_unnamed_remedy_not_single_commodity_brand_or_new_UI_name=True,
        no_all_category_members_boom_price_shortage_profit_or_packed_effect_semantics_claim=True,
        residence_owner_danna_not_proven_lord_employer_husband_master_kinship_or_personal_name=True,
        unknown_cause_not_named_diagnosis_or_supernatural_explanation=True,
        source_explicit_publicly_sold_medicine_one_go_cure_and_panacea_reputation_preserved_as_hearsay=True,
        surprise_then_explicit_truth_question_then_reported_apparent_truth_kept_distinct=True,
        common_knowledge_claim_and_speakers_confidence_not_narrator_verification=True,
        no_verified_efficacy_guaranteed_mechanic_medical_role_recipe_dose_ingredient_brand_or_price_invented=True,
        final_shopping_wish_and_proposal_not_completed_purchase_use_or_recovery=True,
        separate_tentative_Medicine_Havana_notice_not_earlier_location_or_earned_fashion=True,
        source29_commands_one500_predicate_at8_six_relative_sites_three_alternatives_and_two_tailzeros=True,
        source_owned_pointer_adapter=inspect.getsource(bindings),current_native_context_plan=str(ctx.proof_path),current_native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        all17_clean_first_glosses_precede_predecessor_English=True,no_predecessor_English_exposed=True,no_new_city_category_or_name_widget_fidelity_completion=True,
        new_emulator_runs=0,new_review_credit=0,evidence={str(p):sha(p.read_bytes()) for p in paths},full_goal_complete=False))
    print('Port Worker119,Sailor159/Retainer159,Havana and12 original Medicine13/compactMed bindings pass. Cure/panacea claims remain hearsay;no old prose or credit.')
