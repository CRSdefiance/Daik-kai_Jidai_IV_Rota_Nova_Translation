"""Bind four source roles,Hamburg and the ceramics/legacy UI China distinction."""
from pathlib import Path
import inspect,struct
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.current_build_native_context_v4774 import CurrentContext
from scripts.reconcile_lil_B183_terms_v4931 import bindings
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B189_terms_v5279')
SOURCE=Path('work/analysis/lil_B189_source_v5273b/all17_clean_current_complete_context.json')
NAMES=Path('work/analysis/lil_B189_names_v5278b/eight_original_progressive_and_catalogue_name_consumers.json')
CONTROL=Path('work/analysis/lil_B189_controls_v5277b/A000_C200_single_end_and_no_relative_or_predicate_contract.json')
ROLES={'82':'Square Shopkeeper','104':'Trader','113':'Port Worker','147':'Guildmaster'}
if __name__=='__main__':
    assert not ROOT.exists();packet,names,control=map(read,[SOURCE,NAMES,CONTROL])
    assert names['source_context_sha256']==control['source_context_sha256']==sha(SOURCE.read_bytes())
    assert names['progressive_nameplate_values']==names['full_catalogue_values']==ROLES
    native=names['native_eight_consumer_cases']['rows'];assert len(native)==8
    assert all(not r['original_scratch_rings'] and not r['original_getter_writes'] and r['all_actor_models_and_unowned4MiB_exact'] for r in native)
    clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin');arm=NdsImage.open(packet['current_ROM']).read_file('/__arm9__.bin')
    assert clean[0x7ED88:0x7EE08]==arm[0x7ED88:0x7EE08]
    anchor=next(r for r in read('translations/ordinary_name_fidelity_manuscript_v1.json')['records'] if r['index']==164);assert anchor['table_field']==0x122000
    roles=[]
    for ident,field,at,japanese in [(82,0x1215C0,0x15D088,'広場の店主'),(104,0x121880,0x15DAC4,'交易所の親父'),
        (113,0x1219A0,0x15DB74,'出港所の兄貴'),(147,0x121DE0,0x15E304,'ギルドの元締め')]:
        assert field==anchor['table_field']+(ident-164)*32
        pointer=struct.unpack_from('<I',clean,field)[0];assert pointer==0x02000000+at
        value=clean[at:clean.index(0,at)+1];assert value[:-1].decode('cp932')==japanese
        roles.append(dict(actor_ID=ident,source_selector_hex=format(ident,'02X'),pointer_field=field,source_pointer=pointer,source_storage_offset=at,
            clean_Japanese=japanese,approved_English=ROLES[str(ident)],source_terminated_hex=value.hex(),ordinary_name_stride=32))
    good=next(r for r in read('translations/commodity_name_manuscript_v343.json')['records'] if r['index']==42)
    fidelity=next(r for r in read('translations/commodity_fidelity_v2.json')['records'] if r['index']==42)
    assert good['Japanese']==fidelity['Japanese']=='陶磁器' and good['English']==fidelity['English']=='China'
    assert good['pointer_field']==0x15F110
    ptr=struct.unpack_from('<I',clean,good['pointer_field'])[0];at=ptr-0x02000000
    assert clean[at:clean.index(0,at)].decode('cp932')=='陶磁器'
    assert clean[good['pointer_field']+4:good['pointer_field']+12]==arm[good['pointer_field']+4:good['pointer_field']+12]==bytes.fromhex(good['metadata_hex'])
    cities=[]
    for field,at in [(0x122304,0x15CA34),(0x1227A4,0x15CBA8)]:
        ptr=struct.unpack_from('<I',clean,field)[0];assert ptr==0x02000000+at
        value=clean[at:clean.index(0,at)+1];assert value[:-1].decode('cp932')=='ハンブルク'
        cities.append(dict(pointer_field=field,source_pointer=ptr,source_storage_offset=at,source_text='ハンブルク',source_terminated_hex=value.hex(),approved_English='Hamburg'))
    ROOT.mkdir(parents=True)
    ctx=CurrentContext('work/analysis/lil_B189_voices_v5274b/current_native_input.json',packet['historical_snapshot_ROM'],ROOT/'current_context')
    live=ctx.execute(bindings,[r['pointer_field'] for r in roles+cities]+[good['pointer_field']]);ctx.machines.pop();assert not ctx.machines
    assert [r['text'] for r in live['rows']]==['Square Shopkeeper','Trader','Port Worker','Guildmaster','Hamburg','Hamburg','China']
    for role,current in zip(roles,live['rows'][:4],strict=True):
        assert {r['pointer'] for r in native if r['actor_ID']==role['actor_ID']}=={current['current_runtime_pointer']};role.update(current)
    for city,current in zip(cities,live['rows'][4:6],strict=True):city.update(current)
    by={r['source_record_index']:r for r in packet['records']}
    for i,parts in {6:['この間','やっと','手に入れ'],9:['陶磁器'],13:['思ったとおり','最高'],16:['拝見'],19:['拙宅','足をお運び'],
        22:['最近','陶磁器収集','流行','手に入りにくく'],26:['価値の分からん輩','買いあさってる','らしい'],30:['迷惑'],34:['全くその通り'],
        38:['あそこの男たち'],42:['２人連れ'],46:['値打ちのねえ陶磁器','嘘みたいな値','購入してくれた'],
        49:['お得意さん','懐もさみしい','声掛けて'],53:['いいね'],57:['決まり','行こう'],61:['だんなぁ'],65:['ハンブルク','陶磁器','流行しそう']}.items():assert all(s in by[i]['source_Japanese'] for s in parts),i
    assert all('ハンブルク' not in r['source_Japanese'] for i,r in by.items() if i!=65)
    correction=Path('work/analysis/lil_B189_source_tools_v5273/hex_decimal_selector_correction.json')
    paths=[SOURCE,NAMES,CONTROL,correction,Path('translations/ordinary_name_fidelity_manuscript_v1.json'),Path('translations/commodity_name_manuscript_v343.json'),Path('translations/commodity_fidelity_v2.json'),Path(__file__)]
    save(ROOT/'four_roles_Hamburg_ceramics_UI_China_and_two_pair_irony_reconciliation.json',dict(
        candidate=packet['current_ROM'],candidate_sha256=packet['current_ROM_sha256'],source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),
        approved_prose_names=ROLES,source_progressive_names=names['progressive_nameplate_values'],full_catalogue_names=names['full_catalogue_values'],complete_clean_current_role_bindings=roles,
        actual_source_selectors_hex=['93','52','68','71'],actual_source_selectors_decimal=[147,82,104,113],historical_wrong_decimal_list_superseded_by_exact_source_octets=True,
        city='Hamburg',two_source_current_city_aliases=cities,commodity_index=42,source_commodity='陶磁器',commodity_UI='China',source_supported_prose_collective='ceramics',
        commodity_binding=live['rows'][6],original_commodity_metadata_hex=good['metadata_hex'],
        ceramics_is_broad_source_term_not_a_new_commodity_UI_rename_or_Chinese_origin_claim=True,
        legacy_UI_China42_older_fidelity_review_remains_open_no_defect_or_new_widget_completion_claim=True,
        Guildmaster_and_Square_Shopkeeper_collection_discussion_then_Trader_and_Port_Worker_private_exchange_preserved=True,
        source_role_familiar_forms_do_not_establish_father_brother_master_kinship_or_new_rank=True,
        completed_first_acquisition_and_reported_first_sale_preserved_without_invented_price_quantity_shape_or_origin=True,
        source_explicit_collecting_craze_good_piece_scarcity_and_hearsay_buying_up_preserved_as_character_claims=True,
        dramatic_irony_between_collector_praise_and_sellers_private_worthless_ware_unbelievable_price_claim_preserved=True,
        no_narrator_verified_value_authenticity_forgery_or_market_state=True,
        second_pairs_short_funds_belong_to_Trader_Port_Worker_not_collector_customers=True,
        good_customers_does_not_require_repeated_prior_sales=True,proposed_approach_and_final_hail_not_second_sale_threat_or_robbery=True,
        humble_home_invitation_not_mansion_or_completed_visit=True,ingratiating_danna_hail_not_employment_marriage_or_kinship=True,
        tentative_ceramics_Hamburg_FE_distinct_from_character_market_claims_earlier_location_and_earned_state=True,
        source_all20_linear_commands_one_A000_C200_end_and_two_tailzeros_no_predicates_or_relative_sites=True,
        source_owned_pointer_adapter=inspect.getsource(bindings),current_native_context_plan=str(ctx.proof_path),current_native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        all17_clean_first_glosses_precede_predecessor_English=True,no_predecessor_English_exposed=True,no_new_city_commodity_or_name_widget_fidelity_completion=True,
        new_emulator_runs=0,new_review_credit=0,evidence={str(p):sha(p.read_bytes()) for p in paths},full_goal_complete=False))
    print('Four exact roles/eight names,two Hamburg aliases and UI China42 bound. Ceramics is source-supported prose;both pairs,irony,market claims and short-funds antecedent preserved. No old prose or credit.')
