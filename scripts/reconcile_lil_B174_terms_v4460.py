"""Bind B174's names, crown, tomb and city to exact current native strings."""
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.reconcile_lil_B173_terms_v4418 import pointer_strings
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B174_terms_v4460')
SOURCE=Path('work/analysis/lil_B174_source_v4453/all33_clean_current_complete_context.json')
NAMES=Path('work/analysis/lil_B174_names_v4458/eight_original_name_consumers_and_owned_scratch_paths.json')
CONTROL=Path('work/analysis/lil_B174_controls_v4459/one_resource_conditional_Emilio_four_spans_two_A000s_C200_and_single_end.json')
PRIOR=Path('work/analysis/lil_B173_terms_v4418/current_crown_tomb_Reika_and_uncertain_Julian_lead_reconciliation.json')
ITEM=Path('translations/all_item_names_arm9_v1.json')
SITE=Path('translations/historic_site_names_v2.json')
CITY=Path('translations/route_forces_arm9_v1.json')

if __name__=='__main__':
    assert not ROOT.exists()
    source,names,control,prior=map(read,[SOURCE,NAMES,CONTROL,PRIOR])
    assert names['source_context_sha256']==control['source_context_sha256']==sha(SOURCE.read_bytes())
    current,clean,previous=[NdsImage.open(p) for p in [source['current_ROM'],'work/clean.nds',prior['candidate']]]
    arm,old=current.read_file('/__arm9__.bin'),clean.read_file('/__arm9__.bin')
    for path in ['/__arm9__.bin','/COMMON/MESFILE.DK4','/data/EV2.DK4','/GRP/KANJI.FNT']:
        assert current.read_file(path)==previous.read_file(path)
    item=next(r for r in read(ITEM)['records'] if r['id']=='DK4_ITEM_POINTER_137')
    at=item['offset'];itemstrings=pointer_strings(old,arm,at)
    assert old[at:at+4].hex()==item['source_hex'].lower() and arm[at:at+4].hex()==item['replacement_hex'].lower()
    assert [s['text'] for s in itemstrings]==['新羅の金冠','Silla Gold Crown']
    site=next(r for r in read(SITE)['records'] if r['site_id']==17)
    sitestrings=pointer_strings(old,arm,site['pointer_field'])
    assert [s['text'] for s in sitestrings]==['武寧王陵','Tomb of King Muryeong']
    assert sitestrings[0]['file_offset']==site['source_offset'] and sitestrings[0]['hex']==site['source_hex']
    city=next(r for r in read(CITY)['records'] if r['id']=='DK4_ROUTE_CITY_SEOUL')
    at=city['offset'];raw=bytes.fromhex(city['source_hex']);value=city['english'].encode('ascii')+b'\0'
    value+=bytes(len(raw)-len(value))
    assert raw.rstrip(b'\0').decode('cp932')=='京城' and city['english']=='Seoul'
    assert old[at:at+len(raw)]==raw and arm[at:at+len(raw)]==value
    assert names['approved_prose_names']=={'2':'Lil','14':'Emilio','26':'Julian','201':'Mihwa'}
    assert names['progressive_nameplate_values']==names['full_catalogue_values']=={
        '2':'Lil Argot','14':'Emilio Ｆerog','26':'Julian Lopes','201':'Mihwa'}
    by={r['source_record_index']:r for r in source['records']}
    for index,phrases in {14:['新羅の金冠','彼女が先に見つけた'],22:['約束どおり','プレゼント'],
        34:['武寧王陵'],46:['冒険家じゃなくて','商売'],50:['船','京城'],54:['走った','酒場','倒れ','休んで'],
        57:['走った','ウソ'],69:['おなか'],78:['また'],87:['祖父','子供'],91:['祖父みたいな冒険家'],
        94:['おじいちゃん','航海の知識'],110:['それ以上','海に投げる'],113:['ユリアン'],116:['美華'],
        120:['他の女を口説ける'],124:['新しい雇い主'],128:['新羅の金冠','手に入れたら','すぐ帰って','デート'],
        132:['期待して待って'],135:['大物かも']}.items():
        assert all(p in by[index]['source_Japanese'] for p in phrases),index
    assert by[69]['source_selector']==14 and by[69]['ancestor_0100_offsets']==[890]
    ROOT.mkdir(parents=True)
    save(ROOT/'current_four_names_crown_tomb_Seoul_and_conditional_date_reconciliation.json',dict(
        candidate=source['current_ROM'],candidate_sha256=source['current_ROM_sha256'],
        source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),
        approved_B174_prose_names=names['approved_prose_names'],native_full_names_preserved=names['full_catalogue_values'],
        source_given_names_not_expanded_with_surnames=True,
        chosen_crown_title='Silla Gold Crown',chosen_site_title='Tomb of King Muryeong',chosen_city='Seoul',
        exact_global_item_pointer_binding=dict(batch=str(ITEM),batch_sha256=sha(ITEM.read_bytes()),
            id=item['id'],pointer_field_offset=item['offset'],source_string=itemstrings[0],current_string=itemstrings[1]),
        exact_global_historic_site_pointer_binding=dict(batch=str(SITE),batch_sha256=sha(SITE.read_bytes()),
            id=site['id'],site_id=17,pointer_field_offset=site['pointer_field'],source_string=sitestrings[0],current_string=sitestrings[1]),
        exact_Seoul_route_map_string_binding=dict(batch=str(CITY),batch_sha256=sha(CITY.read_bytes()),
            id=city['id'],offset=at,source_hex=raw.hex(),current_hex=value.hex(),source_Japanese='京城',approved_English='Seoul'),
        previous_crown_tomb_and_completed_B78_bindings=str(PRIOR),previous_binding_sha256=sha(PRIOR.read_bytes()),
        current_ARM9_COMMON_EV2_font_equal_previous_binding=True,
        pointer_and_fixed_string_checks_not_new_item_site_or_city_UI_or_full_SourceItems_review=True,
        source_here_establishes_Lil_first_discovery_transfer_and_new_employer_not_price_salary_rank=True,
        actual_grandfather_kinship_explicit_in_祖父_not_invented_from_familiar_address=True,
        navigation_knowledge_question_and_promise_not_numeric_skill_or_certification=True,
        Julian_extraordinary_run_to_Seoul_and_Lil_disbelief_preserved_not_repaired_into_sailing=True,
        crown_promised_gift_distinct_from_later_conditional_better_item_return_and_date_proposal=True,
        jealous_courting_does_not_establish_marriage_or_official_romantic_partnership=True,
        Lil_again_aside_licensed_by_source_また_and_big_shot_idiom_not_physical_size_rank_or_reputation=True,
        Emilio_conditional_hunger_aside_not_actual_running_meal_or_new_roster_claim=True,
        source6240_two_A000_C200_end_order_preserved_effect_words_remain_uninterpreted=True,
        broader_SourceItems_LocalProduct_graphics_and_older_record_reaudit_stay_open=True,
        evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,NAMES,CONTROL,PRIOR,ITEM,SITE,CITY,Path(__file__)]},
        new_emulator_runs=0,source_prose_or_completion_credit_added=0,no_ROM_registry_ledger_change=True,full_goal_complete=False))
    print('Bound Lil/Emilio/Julian/Mihwa, Silla Gold Crown, Tomb of King Muryeong and Seoul; source relationships and conditional plan preserved. No credit.')
