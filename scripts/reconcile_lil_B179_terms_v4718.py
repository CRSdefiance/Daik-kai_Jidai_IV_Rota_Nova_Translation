"""Bind Sao Jorge/Wine and dialogue identities;retain an untranslated city-alias lead."""
import struct
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B179_terms_v4718')
SOURCE=Path('work/analysis/lil_B179_source_v4708/all14_clean_current_complete_context.json')
NAMES=Path('work/analysis/lil_B179_names_v4713b/six_original_Barkeep_Patron_Retainer_name_consumers.json')
IDENTITY=Path('work/analysis/lil_B179_role_identity_v4715/source_current_progressive_roles_and_distinct_Retainer_catalogue_binding.json')
CONTROL=Path('work/analysis/lil_B179_controls_v4714/one_A000_no_C200_single_end_and2_source_leaves.json')
CITY=Path('translations/route_forces_arm9_v1.json')
COMMODITY=Path('translations/commodity_name_manuscript_v343.json')
RELEASE=Path('work/analysis/lil_B178_release_v4702/registered_release_verification.json')

if __name__=='__main__':
    assert not ROOT.exists()
    source,names,identity,control,release=map(read,[SOURCE,NAMES,IDENTITY,CONTROL,RELEASE])
    assert all(p['source_context_sha256']==sha(SOURCE.read_bytes()) for p in [names,identity,control])
    assert names['approved_prose_names']==identity['approved_dialogue_roles']=={'92':'Barkeep','96':'Patron','152':'Sailor'}
    assert names['full_catalogue_values']=={'92':'Barkeep','96':'Patron','152':'Retainer'}
    city=next(r for r in read(CITY)['records'] if r['id']=='DK4_ROUTE_CITY_SAO_JORGE_POOL')
    assert city['offset']==0x15E64C and bytes.fromhex(city['source_hex']).startswith('サン＝ジョルジェ'.encode('cp932')+b'\0')
    assert bytes.fromhex(city['replacement_hex'])==b'Sao Jorge\0Nagasaki\0\0'
    wine=next(r for r in read(COMMODITY)['records'] if r['Japanese']=='ワイン')
    assert (wine['index'],wine['pointer_field'],wine['English'])==(34,0x15F0B0,'Wine')
    bindings=[];goods=[];aliases=[]
    for label,path in [('clean','work/clean.nds'),('current',source['current_ROM'])]:
        arm=NdsImage.open(path).read_file('/__arm9__.bin')
        if label=='current':assert sha(arm)==release['ARM9_sha256'] and release['candidate_sha256']==source['current_ROM_sha256']
        field=0x123284;pointer=struct.unpack_from('<I',arm,field)[0];assert pointer==0x0215E64C
        value=arm[city['offset']:city['offset']+20]
        assert value==bytes.fromhex(city['source_hex'] if label=='clean' else city['replacement_hex'])
        assert value.split(b'\0')[0].decode('cp932')==('サン＝ジョルジェ' if label=='clean' else 'Sao Jorge')
        bindings.append(dict(version=label,ROM=str(path),ARM9_sha256=sha(arm),approved_record_ID=city['id'],
            pointer_field_offset=field,pointer=pointer,file_offset=city['offset'],complete_owned_span_bytes=20,complete_owned_span_hex=value.hex(),
            text=value.split(b'\0')[0].decode('cp932'),source_pointer_preserved=True,
            source_owned_padding_contains_separately_terminated_Nagasaki_in_current_span=label=='current',no_new_city_widget_test_claimed=True))
        field=wine['pointer_field'];pointer=struct.unpack_from('<I',arm,field)[0];at=pointer-0x02000000;end=arm.index(0,at)
        assert at==(0x15BC88 if label=='clean' else 0x15C897)
        assert arm[at:end].decode('cp932')==('ワイン' if label=='clean' else 'Wine')
        assert arm[field+4:field+12].hex()==wine['metadata_hex']=='6c0705dbe8030100'
        goods.append(dict(version=label,pointer_field_offset=field,pointer=pointer,file_offset=at,complete_terminated_hex=arm[at:end+1].hex(),
            text=arm[at:end].decode('cp932'),metadata_hex=wine['metadata_hex'],actual_pointer_selected_source_or_repacked_current_span=True,
            no_new_commodity_widget_or_full_commodity_fidelity_approval=True))
        field=0x122504;pointer=struct.unpack_from('<I',arm,field)[0];assert pointer==0x0215E5D4
        at=pointer-0x02000000;end=arm.index(0,at);value=arm[at:end+1]
        assert value=='サン＝ジョルジェ'.encode('cp932')+b'\0'
        aliases.append(dict(version=label,pointer_field_offset=field,pointer=pointer,file_offset=at,complete_terminated_hex=value.hex(),
            text='サン＝ジョルジェ',display_consumer_or_unused_alias_status_not_yet_proved=True))
    by={r['source_record_index']:r for r in source['records']}
    phrases={6:['まだ','そんなもん','飲んで'],9:['悪いか'],13:['悪かぁない','ワインだよワイン'],16:['ワイン','うまい'],
        20:['最高'],24:['そんなにうまい'],28:['ワインがあれば','他には何も','いらない'],31:['俺も','マスター','ワイン','１杯'],
        35:['はいよ'],39:['ゴキュ、ゴキュ、ゴキュ'],43:['どうだい'],47:['うっめぇー','マスター','もう１杯'],
        50:['俺にも','持ってきて'],54:['サン＝ジョルジェ','ワイン','流行しそう']}
    for index,parts in phrases.items():assert all(p in by[index]['source_Japanese'] for p in parts),index
    assert by[54]['kind']=='system-FE' and all('サン＝ジョルジェ' not in r['source_Japanese'] for i,r in by.items() if i!=54)
    assert source['source_macro_counts']=={'FI':0,'FA':0,'FO':0} and control['source_has_no_C200_and_no_C200_probe_invented']
    ROOT.mkdir(parents=True)
    lead=dict(id='ARM9-Sao-Jorge-alias-15E5D4-pointer122504',source_current_bindings=aliases,
        finding='Current ARM9 pointer122504 still selects a complete Japanese Sao Jorge alias at15E5D4. The approved route-map spelling is Sao Jorge at a distinct translated alias15E64C.',
        next='Map this specific alias consumer and ownership/display rules,determine whether it is player-facing/live or unused,then review and integrate a source-bound correction if required. Preserve the translated20-byte Sao Jorge/Nagasaki allocation and all other assets.',
        no_dead_storage_or_actual_display_claim=True,no_review_or_completion_credit=True,full_goal_complete=False)
    leadpath=ROOT/'untranslated_Sao_Jorge_alias_reference_lead.json';save(leadpath,lead)
    save(ROOT/'Barkeep_Patron_Sailor_Sao_Jorge_Wine_and_prospective_fashion_reconciliation.json',dict(
        candidate=source['current_ROM'],candidate_sha256=source['current_ROM_sha256'],source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),
        approved_B179_prose_names=names['approved_prose_names'],full_catalogue_roles_preserved=names['full_catalogue_values'],
        dialogue_identity_proof=str(IDENTITY),dialogue_identity_proof_sha256=sha(IDENTITY.read_bytes()),chosen_city='Sao Jorge',chosen_commodity_word='wine',
        exact_city_source_current20_byte_owned_span_and_pointer_bindings=bindings,exact_wine_source_current_pointer_selected_name_and_metadata_bindings=goods,
        separate_untranslated_city_alias_lead=str(leadpath),separate_untranslated_city_alias_lead_sha256=sha(leadpath.read_bytes()),
        previous_drink_unspecified_no_beer_rum_brand_price_or_new_quality_fact=True,
        concession_repeated_questions_personal_hyperbole_one_serving_then_another_three_gulps_and_joining_order_preserved=True,
        Master_is_bound_tavern_Barkeep_address_not_new_master_subordinate_relationship=True,
        Sailor152_dialogue_source_suifu_not_catalogue_Retainer_identity=True,
        closing_FE_retains_prospective_likelihood_city_does_not_prove_earlier_location_or_B178_chronology=True,
        no_added_drunkenness_medical_claim_named_lord_faction_military_rank_kinship_or_completed_commercial_sale=True,
        no_predecessor_story_English_exposed_by_this_binding=True,
        commodity_manuscript_historical_formatting_actual_context_and_fidelity_notes_stay_open=True,
        broad_SourceItems_LocalProduct_graphics_and_later_older_record_reaudit_stay_open=True,
        evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,NAMES,IDENTITY,CONTROL,CITY,COMMODITY,RELEASE,leadpath,Path(__file__)]},
        new_emulator_runs=0,source_prose_or_completion_credit_added=0,no_ROM_registry_ledger_change=True,full_goal_complete=False))
    print('Bound source-dialogue Barkeep/Patron/Sailor,Sao Jorge20-byte route alias and pointer-selected Wine. Separate Japanese alias15E5D4 retained as unresolved reference lead. No credit.')
