"""Bind Julio,Sailor,Port Worker,Sake37,Hangzhou and the original FI title address."""
from pathlib import Path
import inspect,struct
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.current_build_native_context_v4774 import CurrentContext
from scripts.reconcile_lil_B183_terms_v4931 import bindings
from scripts.verify_lil_B174_fonts_v4470 import expand
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B194_terms_v5496')
SOURCE=Path('work/analysis/lil_B194_source_v5489/all11_clean_current_complete_context.json')
NAMES=Path('work/analysis/lil_B194_names_v5494/six_original_progressive_and_catalogue_name_consumers.json')
CONTROL=Path('work/analysis/lil_B194_controls_v5495/one_unforced_predicate_resource42_two_C200_paths_and6_source_leaves.json')
ROLES={'6':'Julio Erneco','117':'Port Worker','156':'Sailor'}
if __name__=='__main__':
    assert not ROOT.exists();packet,names,control=map(read,[SOURCE,NAMES,CONTROL])
    assert names['source_context_sha256']==control['source_context_sha256']==sha(SOURCE.read_bytes())
    assert names['progressive_nameplate_values']==ROLES and names['full_catalogue_values']=={'6':'Julio Erneco','117':'Port Worker','156':'Retainer'}
    native=names['native_six_consumer_cases']['rows'];assert len(native)==6 and all(r['all_actor_models_and_unowned4MiB_exact'] for r in native)
    assert all(len(r['original_scratch_rings'])==1 and r['original_getter_writes'] for r in native if r['actor_ID']==6)
    assert all(not r['original_scratch_rings'] and not r['original_getter_writes'] for r in native if r['actor_ID']!=6)
    clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin');arm=NdsImage.open(packet['current_ROM']).read_file('/__arm9__.bin')
    assert clean[0x7ED88:0x7EE08]==arm[0x7ED88:0x7EE08]
    fields=[(6,0x120C40,0x15BF28,'フリオ','Julio'),(6,0x120C44,0x15C20C,'エルネコ','Erneco'),
        (117,0x121A20,0x15DBB4,'出港所の兄貴','Port Worker'),(156,0x121F00,0x15BB78,'配下','Retainer')]
    rows=[]
    for ident,field,at,jp,en in fields:
        assert struct.unpack_from('<I',clean,field)[0]==0x02000000+at
        raw=clean[at:clean.index(0,at)+1];assert raw[:-1].decode('cp932')==jp
        rows.append(dict(actor_ID=ident,pointer_field=field,source_storage_offset=at,source_text=jp,source_terminated_hex=raw.hex(),approved_English=en))
    assert clean[0x120C48:0x120C4C]==arm[0x120C48:0x120C4C]==bytes(4)
    special=struct.unpack_from('<I',clean,0x7EDD0)[0];assert special==struct.unpack_from('<I',arm,0x7EDD0)[0]==0x021484D4
    at=special-0x02000000;assert clean[at:clean.index(0,at)].decode('cp932')=='水夫'
    good=next(r for r in read('translations/commodity_name_manuscript_v343.json')['records'] if r['index']==37)
    fidelity=next(r for r in read('translations/commodity_fidelity_v2.json')['records'] if r['index']==37)
    assert good['Japanese']==fidelity['Japanese']=='清酒' and good['English']==fidelity['English']=='Sake'
    ptr=struct.unpack_from('<I',clean,good['pointer_field'])[0];at=ptr-0x02000000;assert clean[at:clean.index(0,at)].decode('cp932')=='清酒'
    assert clean[good['pointer_field']+4:good['pointer_field']+12]==arm[good['pointer_field']+4:good['pointer_field']+12]==bytes.fromhex(good['metadata_hex'])
    field,at=0x123DD8,0x15BB20;cityptr=struct.unpack_from('<I',clean,field)[0];assert cityptr==0x02000000+at
    city=clean[at:clean.index(0,at)+1];assert city[:-1].decode('cp932')=='杭州'
    assert [i for i in range(len(clean)-3) if clean[i:i+4]==struct.pack('<I',cityptr)]==[field]
    cityrow=dict(pointer_field=field,source_storage_offset=at,source_text='杭州',source_terminated_hex=city.hex(),approved_English='Hangzhou')
    ROOT.mkdir(parents=True);ctx=CurrentContext('work/analysis/lil_B194_voices_v5490/current_native_input.json',packet['historical_snapshot_ROM'],ROOT/'current_context')
    live=ctx.execute(bindings,[r['pointer_field'] for r in rows]+[field,good['pointer_field'],0x7EDD0]);ctx.machines.pop()
    assert [r['text'] for r in live['rows']]==['Julio','Erneco','Port Worker','Retainer','Hangzhou','Sake','Sailor']
    for r,current in zip(rows,live['rows'][:4],strict=True):r.update(current)
    cityrow.update(live['rows'][4]);fi=ctx.execute(expand,b'FI',6);ctx.machines.pop();assert not ctx.machines
    assert fi['original_selector']==6 and fi['captain']==2 and fi['no_model_event_RNG_or_roster_mutation']
    assert len(fi['cases'])==4 and all(bytes.fromhex(c['output_hex'])==b'Lil' for c in fi['cases'])
    by={r['source_record_index']:r for r in packet['records']}
    for i,parts in {6:['この間','清酒','飲んだ'],10:['俺も飲んだ'],14:['なかなか','いける'],18:['米','できているらしい'],22:['そんなもんで'],26:['話していたら','飲みたく','これから１杯'],30:['いいねえ'],34:['決まったら','早く行こう'],46:['な、なんと','きっと','幻の酒','FI提督','聞いたか'],49:['こうしては','おれんぞ','さっそく','清酒','買いに行く'],56:['杭州','清酒','流行しそう']}.items():assert all(part in by[i]['source_Japanese'] for part in parts),i
    assert packet['source_macro_counts']==dict(FI=1,FA=0,FO=0)
    assert all('杭州' not in r['source_Japanese'] for i,r in by.items() if i!=56)
    paths=[SOURCE,NAMES,CONTROL,Path('translations/commodity_name_manuscript_v343.json'),Path('translations/commodity_fidelity_v2.json'),Path(__file__)]
    save(ROOT/'Julio_Sailor_Port_Worker_Hangzhou_Sake_and_FI_title_reconciliation.json',dict(candidate=packet['current_ROM'],candidate_sha256=packet['current_ROM_sha256'],source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),
        approved_prose_names=ROLES,full_catalogue_names=names['full_catalogue_values'],source_name_fields=rows,Julio_original_null_middle_name_field=0x120C48,
        two_owned_Julio_scratch_consumers_and_four_original_readonly_role_consumers_preserve_unowned4MiB=True,
        original_progressive_Sailor_literal=dict(pointer_field=0x7EDD0,source_pointer=special,current_binding=live['rows'][6],unchanged_source_range151_to159_includes156=True),
        city='Hangzhou',one_source_current_city_alias=cityrow,commodity_index=37,source_commodity='清酒',commodity='Sake',commodity_binding=live['rows'][5],original_commodity_metadata_hex=good['metadata_hex'],
        original_default_captain_FI_four_alignment_cases=fi,FI_default_expansion='Lil',FI_default_ASCII_bytes=3,source_title='提督',source_supported_English_title='Admiral',
        source_recent_experiences_casual_taste_rice_hearsay_surprise_thirst_invitation_acceptance_and_urgency_preserved=True,
        rice_ingredient_remains_reported_not_recipe_technical_process_origin_or_narrator_fact=True,
        legendary_liquor_is_Julios_excited_inference_not_certified_identity_award_or_earned_item=True,
        conditional_Julio5_voice_and_source_explicit_FI_Admiral_address_not_invented_kinship_or_new_rank=True,
        no_invented_brotherhood_player_employment_shared_drinking_history_or_new_personal_name=True,
        source_now_drink_invitation_and_later_urgent_purchase_are_intentions_not_completed_actions=True,
        no_price_amount_measured_serving_venue_recipe_origin_health_effect_intoxication_or_reward_invented=True,
        Sake37_individual_commodity_and_one_Hangzhou_alias_not_category_or_new_UI_fidelity_credit=True,
        Sake37_older_UI_fidelity_review_remains_open_separate_from_dialogue=True,
        tentative_Sake_Hangzhou_FE_not_earlier_location_or_earned_fashion=True,
        source21_commands_one_predicate_four_relatives_resource42_two_C200_one_FI_and_single_end_preserved=True,
        all11_clean_first_glosses_precede_predecessor_English_prose_comparison=True,
        raw_current_dispatch_hex_is_structural_evidence_not_translation_source=True,predecessor_English_prose_comparison_pending=True,
        default_captain_binding_not_all_custom_name_lengths_or_actual_B194_gameplay=True,
        source_owned_pointer_adapter=inspect.getsource(bindings),native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        new_emulator_runs=0,new_review_credit=0,evidence={str(p):sha(p.read_bytes()) for p in paths},full_goal_complete=False))
    print('Julio Erneco6 voice5,Sailor156/Retainer,PortWorker117,Sake37,Hangzhou and four FI-to-Lil alignments bound. Source Admiral title and character beliefs preserved;zero credit.')
