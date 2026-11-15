"""Bind source Daimyo/Guildmaster,Osaka,Glass and the explicit giyaman gloss."""
from pathlib import Path
import inspect,struct
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.current_build_native_context_v4774 import CurrentContext
from scripts.reconcile_lil_B183_terms_v4931 import bindings
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B188_terms_v5238')
SOURCE=Path('work/analysis/lil_B188_source_v5232/all11_clean_current_complete_context.json')
NAMES=Path('work/analysis/lil_B188_names_v5237/four_original_progressive_and_catalogue_name_consumers.json')
CONTROL=Path('work/analysis/lil_B188_controls_v5236/A000_C200_single_end_and_no_relative_or_predicate_contract.json')
ROLES={'130':'Daimyo','150':'Guildmaster'}
if __name__=='__main__':
    assert not ROOT.exists();packet,names,control=map(read,[SOURCE,NAMES,CONTROL])
    assert names['source_context_sha256']==control['source_context_sha256']==sha(SOURCE.read_bytes())
    assert names['progressive_nameplate_values']==names['full_catalogue_values']==ROLES
    native=names['native_four_consumer_cases']['rows'];assert len(native)==4
    assert all(not r['original_scratch_rings'] and not r['original_getter_writes'] and r['all_actor_models_and_unowned4MiB_exact'] for r in native)
    clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin');arm=NdsImage.open(packet['current_ROM']).read_file('/__arm9__.bin')
    assert clean[0x7ED88:0x7EE08]==arm[0x7ED88:0x7EE08]
    anchor=next(r for r in read('translations/ordinary_name_fidelity_manuscript_v1.json')['records'] if r['index']==164)
    assert anchor['table_field']==0x122000
    roles=[]
    for ident,field,at,japanese in [(130,0x121BC0,0x15BA00,'大名'),(150,0x121E40,0x15E344,'ギルドの元締め')]:
        assert field==anchor['table_field']+(ident-164)*32
        pointer=struct.unpack_from('<I',clean,field)[0];assert pointer==0x02000000+at
        value=clean[at:clean.index(0,at)+1];assert value[:-1].decode('cp932')==japanese
        roles.append(dict(actor_ID=ident,pointer_field=field,source_pointer=pointer,source_storage_offset=at,
            clean_Japanese=japanese,approved_English=ROLES[str(ident)],source_terminated_hex=value.hex(),ordinary_name_stride=32))
    good=next(r for r in read('translations/commodity_name_manuscript_v343.json')['records'] if r['index']==41)
    fidelity=next(r for r in read('translations/commodity_fidelity_v2.json')['records'] if r['index']==41)
    assert good['Japanese']==fidelity['Japanese']=='ガラス' and good['English']==fidelity['English']=='Glass'
    assert good['pointer_field']==0x15F104
    ptr=struct.unpack_from('<I',clean,good['pointer_field'])[0];at=ptr-0x02000000
    assert at==0x15BCB8 and clean[at:clean.index(0,at)].decode('cp932')=='ガラス'
    assert clean[good['pointer_field']+4:good['pointer_field']+12]==arm[good['pointer_field']+4:good['pointer_field']+12]==bytes.fromhex(good['metadata_hex'])
    cities=[]
    for field,at in [(0x1224E4,0x15BA60),(0x12401C,0x15B910)]:
        ptr=struct.unpack_from('<I',clean,field)[0];assert ptr==0x02000000+at
        value=clean[at:clean.index(0,at)+1];assert value[:-1].decode('cp932')=='大坂'
        cities.append(dict(pointer_field=field,source_pointer=ptr,source_storage_offset=at,source_text='大坂',source_terminated_hex=value.hex(),approved_English='Osaka'))
    ROOT.mkdir(parents=True)
    ctx=CurrentContext('work/analysis/lil_B188_voices_v5233/current_native_input.json',packet['historical_snapshot_ROM'],ROOT/'current_context')
    live=ctx.execute(bindings,[r['pointer_field'] for r in roles+cities]+[good['pointer_field']]);ctx.machines.pop();assert not ctx.machines
    assert [r['text'] for r in live['rows']]==['Daimyo','Guildmaster','Osaka','Osaka','Glass']
    for role,current in zip(roles,live['rows'][:2],strict=True):
        assert {r['pointer'] for r in native if r['actor_ID']==role['actor_ID']}=={current['current_runtime_pointer']};role.update(current)
    for city,current in zip(cities,live['rows'][2:4],strict=True):city.update(current)
    by={r['source_record_index']:r for r in packet['records']}
    for i,parts in {6:['素晴らしい','芸術'],10:['仰せの通り'],14:['名の通った職人','作った','あろう'],18:['さよう'],
        22:['流行して','知らなんだ'],26:['何というもの'],30:['ギヤマン（ガラス）'],34:['ギヤマン'],38:['収集','街中のギヤマン','集めてまいれ'],
        41:['御意のまま'],45:['大坂','ガラス','流行しそう']}.items():assert all(s in by[i]['source_Japanese'] for s in parts),i
    assert all('大坂' not in r['source_Japanese'] for i,r in by.items() if i!=45)
    paths=[SOURCE,NAMES,CONTROL,Path('translations/ordinary_name_fidelity_manuscript_v1.json'),Path('translations/commodity_name_manuscript_v343.json'),Path('translations/commodity_fidelity_v2.json'),Path(__file__)]
    save(ROOT/'Daimyo_Guildmaster_Osaka_Glass_and_giyaman_collection_reconciliation.json',dict(
        candidate=packet['current_ROM'],candidate_sha256=packet['current_ROM_sha256'],source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),
        approved_prose_names=ROLES,source_progressive_names=names['progressive_nameplate_values'],full_catalogue_names=names['full_catalogue_values'],complete_clean_current_role_bindings=roles,
        city='Osaka',two_source_current_city_aliases=cities,commodity_index=41,source_commodity='ガラス',commodity='Glass',commodity_binding=live['rows'][4],original_commodity_metadata_hex=good['metadata_hex'],
        source_explicit_giyaman_parenthetical_glass_and_new_name_echo_preserved=True,giyaman_is_scene_vocabulary_not_new_commodity_UI_rename_or_asserted_etymology=True,
        praise_and_famous_craftsman_attribution_are_character_judgment_and_conjecture_not_named_maker_or_proven_origin=True,
        source_Daimyo_role_bound_without_invented_personal_name_kinship_or_extra_rank=True,
        source_Guildmaster_deference_does_not_require_invented_address_or_relationship=True,
        source_explicit_collection_decision_and_order_to_gather_all_giyaman_in_town_preserved=True,
        gather_not_explicit_buy_no_price_payment_museum_donation_shortage_item_shape_or_completed_collection_invented=True,
        existing_fashion_in_character_discovery_distinct_from_tentative_Glass_Osaka_FE=True,
        source_all14_linear_commands_one_A000_C200_end_and_two_tailzeros_no_predicates_or_relative_sites=True,
        source_owned_pointer_adapter=inspect.getsource(bindings),current_native_context_plan=str(ctx.proof_path),current_native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        all11_clean_first_glosses_precede_predecessor_English=True,no_predecessor_English_exposed=True,no_new_city_commodity_or_name_widget_fidelity_completion=True,
        new_emulator_runs=0,new_review_credit=0,evidence={str(p):sha(p.read_bytes()) for p in paths},full_goal_complete=False))
    print('Daimyo130/Guildmaster150,two Osaka aliases andGlass41 bound. Explicit giyaman/glass and collection order preserved;no old prose read or credit.')
