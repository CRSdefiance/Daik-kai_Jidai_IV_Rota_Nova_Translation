"""Bind five speaking roles,Basra and Artwork before reading predecessor prose."""
from pathlib import Path
import inspect,struct
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.current_build_native_context_v4774 import CurrentContext
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B183_terms_v4931')
SOURCE=Path('work/analysis/lil_B183_source_v4925/all25_clean_current_complete_context.json')
NAMES=Path('work/analysis/lil_B183_names_v4930/ten_original_progressive_and_catalogue_name_consumers.json')
CONTROL=Path('work/analysis/lil_B183_controls_v4929/A000_C200_single_end_and_no_relative_or_predicate_contract.json')
ROLES={'85':'Square Shopkeeper','110':'Shipwright','132':'Priest','148':'Guildmaster','153':'Sailor'}

def bindings(arm,common,raw,plan,fields):
    cpu,get,provider=machine(arm,common,raw,plan);before=bytes(cpu.mem_read(0x02000000,0x400000));rows=[]
    for field in fields:
        pointer=struct.unpack_from('<I',arm,field)[0]
        assert bytes(cpu.mem_read(0x02000000+field,4))==arm[field:field+4]
        value=bytes(cpu.mem_read(pointer,80)).split(b'\0')[0]
        rows.append(dict(pointer_field=field,current_runtime_pointer=pointer,text=value.decode('cp932'),
            terminated_hex=(value+b'\0').hex(),current_pointer_word_in_actual_snapshot_exact_ARM9=True))
    assert bytes(cpu.mem_read(0x02000000,0x400000))==before
    return dict(rows=rows,all4MiB_unchanged=True,actual_current_pointer_targets_read_without_UI_widget_execution=True,
        current_executed_instruction_addresses=len(provider.executed_current))

if __name__=='__main__':
    assert not ROOT.exists();packet,names,controls=map(read,[SOURCE,NAMES,CONTROL])
    assert names['source_context_sha256']==controls['source_context_sha256']==sha(SOURCE.read_bytes())
    assert names['progressive_nameplate_values']==ROLES
    assert names['full_catalogue_values']=={**ROLES,'153':'Retainer'}
    assert all(not r['original_scratch_rings'] and not r['original_getter_writes'] and r['all_actor_models_and_unowned4MiB_exact']
        for r in names['native_ten_consumer_cases']['rows'])
    manuscript=read('translations/commodity_name_manuscript_v343.json');good=next(r for r in manuscript['records'] if r['index']==57)
    fidelity=next(r for r in read('translations/commodity_fidelity_v2.json')['records'] if r['index']==57)
    assert good['Japanese']==fidelity['Japanese']=='絵画' and good['English']==fidelity['English']=='Artwork'
    fields=[0x122424,0x123698,good['pointer_field']]
    clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    arm=NdsImage.open(packet['current_ROM']).read_file('/__arm9__.bin');cities=[]
    for field,at in [(0x122424,0x15BCD0),(0x123698,0x15BD40)]:
        pointer=struct.unpack_from('<I',clean,field)[0];assert pointer==0x02000000+at
        value=clean[at:clean.index(0,at)+1];assert value[:-1].decode('cp932')=='バスラ'
        cities.append(dict(pointer_field=field,source_pointer=pointer,source_storage_offset=at,source_terminated_hex=value.hex(),
            source_text='バスラ',approved_English='Basra'))
    field=good['pointer_field'];ptr=struct.unpack_from('<I',clean,field)[0];at=ptr-0x02000000
    assert clean[at:clean.index(0,at)].decode('cp932')=='絵画'
    assert clean[field+4:field+12].hex()==arm[field+4:field+12].hex()==good['metadata_hex']
    ROOT.mkdir(parents=True);ctx=CurrentContext('work/analysis/lil_B183_voices_v4926/current_native_input.json',packet['historical_snapshot_ROM'],ROOT/'current_context')
    live=ctx.execute(bindings,fields);ctx.machines.pop();assert not ctx.machines
    assert [r['text'] for r in live['rows']]==['Basra','Basra','Artwork']
    for source,current in zip(cities,live['rows'][:2],strict=True):source.update(current)
    by={r['source_record_index']:r for r in packet['records']}
    assert all(s in by[95]['source_Japanese'] for s in ['バスラ','絵画','流行しそう'])
    assert all('バスラ' not in r['source_Japanese'] for i,r in by.items() if i!=95)
    assert by[53]['source_Japanese']=='バタンッ！' and by[53]['kind']==by[95]['kind']=='system-FE'
    assert all(s in by[18]['source_Japanese'] for s in ['彼','後世','芸術家'])
    assert all(s in by[73]['source_Japanese'] for s in ['最近','絵画','集める','流行ってる'])
    assert all(s in by[80]['source_Japanese'] for s in ['本当に見る目','少ない']) and '秘密' in by[87]['source_Japanese']
    paths=[SOURCE,NAMES,CONTROL,Path('translations/commodity_name_manuscript_v343.json'),Path('translations/commodity_fidelity_v2.json'),Path(__file__)]
    save(ROOT/'five_roles_Basra_Artwork_and_complete_shop_exchange_reconciliation.json',dict(
        candidate=packet['current_ROM'],candidate_sha256=packet['current_ROM_sha256'],source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),
        approved_prose_names=ROLES,source_progressive_nameplates=names['progressive_nameplate_values'],full_catalogue_names=names['full_catalogue_values'],
        source99_is_Sailor153_in_progressive_scene_not_separate_catalogue_Retainer=True,
        no_player_identity_personal_name_nobility_or_kinship_inferred_from_generic_roles=True,
        two_source_current_city_aliases=cities,city='Basra',commodity_index=57,source_commodity='絵画',commodity='Artwork',
        commodity_binding=live['rows'][2],original_commodity_metadata_hex=good['metadata_hex'],
        specific_paintings_in_conversation_distinct_from_collective_trade_label_Artwork=True,
        FE_impact_sound_distinct_from_spoken_roles_and_final_prospective_notice=True,
        courteous_sale_service_then_private_skepticism_candor_laughter_and_discretion_preserved=True,
        competing_art_judgments_not_narrator_quality_or_guaranteed_fame_investment_or_profit=True,
        no_artist_name_painting_title_price_currency_or_unshown_pointing_direction=True,
        recent_collecting_fashion_is_character_speech_final_Basra_forecast_still_prospective=True,
        no_previous_shop_location_earned_boom_shortage_or_demand_mechanic_inferred=True,
        all25_clean_first_glosses_precede_predecessor_English=True,no_predecessor_English_exposed=True,
        source_owned_pointer_adapter=inspect.getsource(bindings),current_native_context_plan=str(ctx.proof_path),
        current_native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),no_new_commodity_city_or_name_widget_fidelity_completion=True,
        new_emulator_runs=0,new_review_credit=0,evidence={str(p):sha(p.read_bytes()) for p in paths},full_goal_complete=False))
    print('Five progressive roles,two Basra aliases and Artwork57 bound. Sailor153/catalogue Retainer distinction and both FE objects preserved;no old dialogue exposed.')
