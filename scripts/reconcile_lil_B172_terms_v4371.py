"""Bind B172 title/city/names and preserve the qualified-date and search exchanges."""
import struct
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B172_terms_v4371')
SOURCE=Path('work/analysis/lil_B172_source_v4364/all27_clean_current_complete_context.json')
NAMES=Path('work/analysis/lil_B172_names_v4369/six_original_name_consumers_and_owned_scratch_paths.json')
CONTROL=Path('work/analysis/lil_B172_dispatches_v4366/all27_source_current_dispatches_no_macros_and11_control_leaves.json')
EARLIER=Path('translations/lil_recruits_julian_contextual_final_review_v1.json')
ITEM=Path('translations/all_item_names_arm9_v1.json')
CITY=Path('translations/route_forces_arm9_v1.json')

if __name__=='__main__':
    assert not ROOT.exists()
    source,names,control,earlier=map(read,[SOURCE,NAMES,CONTROL,EARLIER])
    assert names['source_context_sha256']==control['source_context_sha256']==sha(SOURCE.read_bytes())
    current,clean=NdsImage.open(source['current_ROM']),NdsImage.open('work/clean.nds')
    now,jp=[IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks for im in [current,clean]]
    bindings=[]
    for index in [40,47,95,113]:
        row=next(r for r in earlier['records'] if r['block']==78 and r['source_record_index']==index)
        sr,ref=row['source_reference'],row['integrated_reference'];raw,value=bytes.fromhex(row['source_hex']),bytes.fromhex(row['integrated_hex'])
        assert row['file_path']=='/data/SC2.DK4' and ref['block']==78 and '新羅の金冠' in row['source_Japanese'] and 'Silla Gold Crown' in row['english']
        assert jp[78][sr['offset']:sr['offset']+len(raw)]==raw and jp[78][sr['offset']+len(raw)]==0
        assert now[78][ref['offset']:ref['offset']+len(value)]==value and now[78][ref['offset']+len(value)]==0
        assert all(row['review'].values())
        bindings.append(dict(final_review=str(EARLIER),final_review_sha256=sha(EARLIER.read_bytes()),id=row['id'],
            clean_reference=sr,clean_hex=raw.hex(),clean_Japanese=row['source_Japanese'],current_reference=ref,current_hex=value.hex(),
            reviewed_English=row['english'],source_meaning=row['source_meaning'],localization_note=row['localization_note']))
    old_arm,arm=clean.read_file('/__arm9__.bin'),current.read_file('/__arm9__.bin')
    item=next(r for r in read(ITEM)['records'] if r['id']=='DK4_ITEM_POINTER_137');at=item['offset']
    assert old_arm[at:at+4].hex()==item['source_hex'].lower() and arm[at:at+4].hex()==item['replacement_hex'].lower()
    pointers=[struct.unpack_from('<I',b,at)[0] for b in [old_arm,arm]]
    strings=[]
    for b,ptr in zip([old_arm,arm],pointers,strict=True):
        offset=ptr-0x02000000;assert 0<=offset<len(b);value=b[offset:b.index(b'\0',offset)]
        strings.append(dict(pointer=ptr,file_offset=offset,bytes=len(value),hex=value.hex(),text=value.decode('cp932')))
    assert strings[0]['text']=='新羅の金冠' and strings[1]['text']==item['english']=='Silla Gold Crown'
    city=next(r for r in read(CITY)['records'] if r['id']=='DK4_ROUTE_CITY_SEOUL');at=city['offset'];raw=bytes.fromhex(city['source_hex'])
    assert old_arm[at:at+len(raw)]==raw and raw.rstrip(b'\0').decode('cp932')=='京城'
    target=city['english'].encode('ascii')+b'\0';target+=bytes(len(raw)-len(target))
    assert city['english']=='Seoul' and arm[at:at+len(raw)]==target
    assert names['approved_prose_names']=={'2':'Lil','26':'Julian','201':'Mihwa'}
    assert names['progressive_nameplate_values']==names['full_catalogue_values']=={'2':'Lil Argot','26':'Julian Lopes','201':'Mihwa'}
    by={r['source_record_index']:r for r in source['records']}
    for index,phrases in {7:['美華','笑顔のために生きてる'],11:['ユリアンったら'],34:['新羅の金冠','神秘的','貴重'],
        41:['お店では売ってないらしい','京城','聞いた'],55:['パワーの','源','手に入れたら','デート'],
        58:['まだ見つけてもいない','気が早い','考えておいてあげる'],62:['その約束','京城'],
        78:['聞いたけど忘れちゃった','キレイ'],85:['もし手に入ったら','見せてあげる'],88:['自分で見つける','京城'],
        92:['京城のどこ','知らない'],96:['人に話を','探してみる'],100:['手に入れたら','見せてちょうだい']}.items():
        assert all(p in by[index]['source_Japanese'] for p in phrases),index
    assert 'literal again' in by[11]['fresh_source_gloss'] and by[11]['historical_clean_first_gloss']
    ROOT.mkdir(parents=True)
    save(ROOT/'current_crown_Seoul_names_and_qualified_date_reconciliation.json',dict(
        candidate=source['current_ROM'],candidate_sha256=source['current_ROM_sha256'],source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),
        approved_B172_prose_names={'2':'Lil','26':'Julian','201':'Mihwa'},native_full_names_preserved={'2':'Lil Argot','26':'Julian Lopes','201':'Mihwa'},
        Lopes_not_added_to_source_given_name_addresses=True,source1A_and_C9_are_static_actor26_and201_not_literal_prose=True,
        exact_completed_B78_title_bindings=bindings,chosen_crown_title='Silla Gold Crown',
        exact_global_item_pointer_binding=dict(batch=str(ITEM),batch_sha256=sha(ITEM.read_bytes()),id=item['id'],pointer_field_offset=item['offset'],
            source_pointer_hex=item['source_hex'],current_pointer_hex=item['replacement_hex'],source_string=strings[0],current_string=strings[1],
            direct_pointer_and_C_string_bytes_verified_not_a_new_item_UI_or_full_SourceItems_catalogue_review=True),
        exact_Seoul_route_map_string_binding=dict(batch=str(CITY),batch_sha256=sha(CITY.read_bytes()),id=city['id'],offset=at,
            source_hex=raw.hex(),current_hex=target.hex(),source_Japanese='京城',approved_English='Seoul',
            source_and_current_ARM9_hashes=[sha(old_arm),sha(arm)],no_new_town_gameplay_or_graphics_claim=True),
        Silla_identity_preserved_in_title_without_extra_history_item_powers_or_country_exposition=True,
        other_route_older_Golden_Crown_variant_not_used_to_override_completed_current_Lil_item_title=True,
        exact_B78_later_acquisition_transfer_and_Hangzhou_reference_not_imported_into_B172_prose_or_earned_state=True,
        familiar_flirtation_does_not_establish_romantic_partnership_or_kinship=True,
        explicit_conditional_date_request_and_Mihwa_will_think_about_it_are_distinct=True,
        Julian_promise_interpretation_is_his_overeager_response_not_her_confirmed_consent=True,
        smile_as_life_or_power_source_is_flirtatious_hyperbole_not_literal_dependency_or_numeric_skill=True,
        source_stores_absence_city_location_and_preciousness_remain_reported_uncertainty=True,
        unstated_place_from_Julian_realization_not_named_ruin_temple_or_coordinate=True,
        Mihwa_forgot_description_only_remembers_beauty_not_firsthand_sighting=True,
        initial_offer_to_show_Lil_and_final_request_for_Lil_to_show_Mihwa_preserve_role_reversal=True,
        Lil_independent_search_plan_not_completed_travel_or_forced_competition=True,
        SourceItems_LocalProduct_broader_review_and_later_older_record_reaudit_stay_open=True,
        names_proof=str(NAMES),names_proof_sha256=sha(NAMES.read_bytes()),source_no_FI_FA_FO_macros=True,
        evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,NAMES,CONTROL,EARLIER,ITEM,CITY,Path(__file__)]},
        new_emulator_runs=0,source_prose_or_completion_credit_added=0,no_ROM_registry_ledger_change=True,full_goal_complete=False))
    print('B172 Julian/Mihwa,Seoul and Silla Gold Crown bound to exact native strings andfour completed B78 records. Conditional date and offer/request reversal preserved. No credit.')
