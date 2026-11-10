"""Bind shopkeeper,Sailor/Retainer,two Calicut aliases and source dye category14."""
from pathlib import Path
import inspect,struct
from scripts.current_build_native_context_v4774 import CurrentContext
from scripts.native_machine_scoped_v764 import machine as clean_machine
from scripts.reconcile_lil_B183_terms_v4931 import bindings
from scripts.verify_category_lookup_v754 import getter,UI_RETURNS
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/lil_B191_terms_v5364b')
SOURCE=Path('work/analysis/lil_B191_source_v5356/all13_clean_current_complete_context.json')
NAMES=Path('work/analysis/lil_B191_names_v5361/four_original_progressive_and_catalogue_name_consumers.json')
CONTROL=Path('work/analysis/lil_B191_controls_v5363/three_predicates_four_A000_C200_sixteen_relative_sites_and_single_end.json')
ROLES={'86':'Square Shopkeeper','154':'Sailor'}

def category14(arm,common,raw,plan):
    cpu,get,provider=machine(arm,common,raw,plan);before=bytes(cpu.mem_read(0x02000000,0x400000));rows=[]
    for parent in [*UI_RETURNS,0x0205FC48]:
        pointer=getter(cpu,14,parent);value=bytes(cpu.mem_read(pointer,80)).split(b'\0')[0];assert value==b'Dyes'
        rows.append(dict(index=14,native_return_PC=parent,pointer=pointer,text='Dyes',terminated_hex=(value+b'\0').hex()))
    assert bytes(cpu.mem_read(0x02000000,0x400000))==before
    return dict(rows=rows,all4MiB_unchanged=True,current_executed_instruction_addresses=len(provider.executed_current))

if __name__=='__main__':
    assert not ROOT.exists();packet,names,control=map(read,[SOURCE,NAMES,CONTROL])
    assert names['source_context_sha256']==control['source_context_sha256']==sha(SOURCE.read_bytes())
    assert names['progressive_nameplate_values']==ROLES and names['full_catalogue_values']=={'86':'Square Shopkeeper','154':'Retainer'}
    native=names['native_four_consumer_cases']['rows'];assert len(native)==4
    assert all(not r['original_scratch_rings'] and not r['original_getter_writes'] and r['all_actor_models_and_unowned4MiB_exact'] for r in native)
    clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin');arm=NdsImage.open(packet['current_ROM']).read_file('/__arm9__.bin')
    assert clean[0x7ED88:0x7EE08]==arm[0x7ED88:0x7EE08]
    anchor=next(r for r in read('translations/ordinary_name_fidelity_manuscript_v1.json')['records'] if r['index']==164);assert anchor['table_field']==0x122000
    roles=[]
    for ident,field,at,japanese,english in [(86,0x121640,0x15D0DC,'広場の店主','Square Shopkeeper'),(154,0x121EC0,0x15B830,'配下','Retainer')]:
        assert field==anchor['table_field']+(ident-164)*32 and struct.unpack_from('<I',clean,field)[0]==0x02000000+at
        value=clean[at:clean.index(0,at)+1];assert value[:-1].decode('cp932')==japanese
        roles.append(dict(actor_ID=ident,source_selector_hex=format(ident,'02X'),pointer_field=field,source_storage_offset=at,
            source_full_catalogue_role=japanese,approved_full_catalogue_role=english,source_terminated_hex=value.hex()))
    special=struct.unpack_from('<I',clean,0x7EDD0)[0];assert special==struct.unpack_from('<I',arm,0x7EDD0)[0]==0x021484D4
    at=special-0x02000000;specialbytes=clean[at:clean.index(0,at)+1];assert specialbytes[:-1].decode('cp932')=='水夫'
    assert next(r for r in native if r['actor_ID']==154 and r['consumer']=='progressive-nameplate')['pointer']==special
    cities=[]
    for field,at in [(0x122444,0x15CADC),(0x123868,0x15CD88)]:
        pointer=struct.unpack_from('<I',clean,field)[0];assert pointer==0x02000000+at
        value=clean[at:clean.index(0,at)+1];assert value[:-1].decode('cp932')=='カリカット'
        assert [i for i in range(len(clean)-3) if clean[i:i+4]==struct.pack('<I',pointer)]==[field]
        cities.append(dict(pointer_field=field,source_pointer=pointer,source_storage_offset=at,source_text='カリカット',source_terminated_hex=value.hex(),approved_English='Calicut'))
    cpu=clean_machine(clean);categories=[]
    for parent in [*UI_RETURNS,0x0205FC48]:
        p=getter(cpu,14,parent);value=bytes(cpu.mem_read(p,80)).split(b'\0')[0];assert value.decode('cp932')=='染料'
        categories.append(dict(version='clean',index=14,native_return_PC=parent,pointer=p,text='染料',terminated_hex=(value+b'\0').hex()))
    ROOT.mkdir(parents=True);ctx=CurrentContext('work/analysis/lil_B191_voices_v5357/current_native_input.json',packet['historical_snapshot_ROM'],ROOT/'current_context')
    live=ctx.execute(bindings,[r['pointer_field'] for r in roles+cities]+[0x7EDD0]);ctx.machines.pop()
    assert [r['text'] for r in live['rows']]==['Square Shopkeeper','Retainer','Calicut','Calicut','Sailor']
    for role,current in zip(roles,live['rows'][:2],strict=True):
        assert {r['pointer'] for r in native if r['actor_ID']==role['actor_ID'] and r['consumer']=='full-catalogue'}=={current['current_runtime_pointer']};role.update(current)
    for city,current in zip(cities,live['rows'][2:4],strict=True):city.update(current)
    category=ctx.execute(category14);ctx.machines.pop();assert not ctx.machines
    categories.extend(dict(version='current',**r) for r in category['rows']);assert len(categories)==12
    by={r['source_record_index']:r for r in packet['records']}
    for i,parts in {53:['この色','あの染料'],56:['今のうち','他の店','買い占め'],60:['でも'],64:['悠長','売り切れ'],68:['今あわてて','売り切れる'],
        72:['すごい人気','すぐなくな'],76:['そうかなあ'],80:['そうです'],84:['分かった','任せる'],88:['親父さん','すねない','この色','絶対に儲かります'],92:['そうかなあ'],96:['そうですって'],100:['カリカット','染料','流行しそう']}.items():assert all(part in by[i]['source_Japanese'] for part in parts),i
    assert by[76]['source_Japanese']==by[92]['source_Japanese'] and all('カリカット' not in r['source_Japanese'] for i,r in by.items() if i!=100)
    paths=[SOURCE,NAMES,CONTROL,Path('translations/ordinary_name_fidelity_manuscript_v1.json'),Path('dk4tool/patch/category_dialogue_lookup.py'),Path(__file__)]
    save(ROOT/'Square_Shopkeeper_Sailor_Calicut_Dyes_and_persuasive_claims.json',dict(candidate=packet['current_ROM'],candidate_sha256=packet['current_ROM_sha256'],source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),
        approved_prose_names=ROLES,source_progressive_names=names['progressive_nameplate_values'],full_catalogue_names=names['full_catalogue_values'],two_source_full_catalogue_role_fields=roles,
        original_progressive_Sailor_literal=dict(pointer_field=0x7EDD0,source_pointer=special,source_text='水夫',source_terminated_hex=specialbytes.hex(),current_binding=live['rows'][4],unchanged_original_range151_to159_selects_actor154=True),
        city='Calicut',two_source_current_city_aliases=cities,category_index=14,source_category='染料',approved_full_category='Dyes',compact_UI_category='Dyes',
        all12_category14_native_bindings=categories,current_category_binding=category,source_owned_category_adapter=inspect.getsource(category14),
        source_dyes_category14_not_single_named_pigment_garment_recipe_or_UI_rename=True,
        Sailor154_catalogue_Retainer_does_not_prove_player_employment_master_rank_or_kinship=True,
        familiar_oyajisan_does_not_prove_fatherhood_age_or_employment_relation=True,
        exclusive_color_competitor_buyout_popularity_imminent_sellout_and_conditional_profit_are_source_explicit_character_claims=True,
        no_narrator_verified_shortage_stock_price_rise_guaranteed_profit_or_earned_game_mechanic=True,
        admired_color_hesitation_urgency_doubt_reluctant_delegation_and_final_repeated_doubt_insistence_progression_preserved=True,
        two_identical_soukanaa_doubts_and_distinct_soudesu_soudesutte_replies_preserved=True,
        delegation_and_sulking_request_not_completed_purchase_delivery_recovery_or_new_relationship=True,
        no_named_pigment_ingredient_recipe_garment_quantity_price_or_new_source_town_invented=True,
        tentative_Dyes_Calicut_FE_distinct_from_character_pitch_prior_location_and_earned_state=True,
        source_three_predicates16_branches_four_effects_and_no_effect_paths_not_flattened=True,
        all13_clean_first_glosses_precede_predecessor_English=True,no_predecessor_English_exposed=True,no_new_name_category_city_widget_fidelity_credit=True,
        source_owned_pointer_adapter=inspect.getsource(bindings),current_native_context_plan=str(ctx.proof_path),current_native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        new_emulator_runs=0,new_review_credit=0,evidence={str(p):sha(p.read_bytes()) for p in paths},full_goal_complete=False))
    print('Shopkeeper86,Sailor154/Retainer154,two Calicut aliases and12 Dyes14 bindings pass. Persuasive profit/shortage claims and repeated doubts remain character statements;zero credit.')
