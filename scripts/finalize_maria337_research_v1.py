"""Seal337 original source reviews after complete display/storage and focused gameplay."""
from collections import Counter
from copy import deepcopy
from pathlib import Path
import re
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from scripts.meaning_maria337_clean_v1 import ROOT
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest


def main():
    finalpath=Path('translations/maria_B125_B136_final_review_v1.json')
    finalnames=Path('translations/maria_B125_B136_scoped_names_final_v1.json')
    out=ROOT/'research_completion_v1';assert not any(p.exists() for p in [out,finalpath,finalnames])
    paths=dict(source=ROOT/'formatting_v1/formatting_input.json',prose=Path('translations/maria_B125_B136_contextual_review_v1.json'),
        plan=ROOT/'plan_visual_v5/automatic_plans.json',native=ROOT/'final_native_v1.json',rebuilt=ROOT/'reconstruction_v1/reconstruction.json',
        stored=ROOT/'stored_v1/stored_native_verification.json',catalogue=ROOT/'stored_catalogue_all_v1/all335_stored_effective_body_bindings.json',
        loaders=ROOT/'loaders_v1/verification.json',visual=ROOT/'offline_display_approval_v1.json',actual=ROOT/'gameplay_review_v1.json',
        styles=ROOT/'compiled_styles_v1/compiled_style_objects.json',menus=ROOT/'menu_native_approved_v1.json',
        names=ROOT/'name_inputs_v1/review.json',name_planes=ROOT/'name_planes_v1/native_name_planes.json',
        macros=ROOT/'formatting_v1/native_macro_measurements.json',roles=ROOT/'formatting_v1/role_bindings.json',terms=ROOT/'scoped_terms_reference_v1.json')
    d={k:load(p) for k,p in paths.items()};doc=deepcopy(d['source']);original=deepcopy(doc)
    rebuilt,stored,native,plan,actual=[d[k] for k in ['rebuilt','stored','native','plan','actual']]
    assert len(doc['records'])==337 and Counter(r['decision'] for r in doc['records'])=={'revision':224,'retention':113}
    assert len(native['records'])==len(plan['records'])==len(d['catalogue']['records'])==335
    assert native['pages']==stored['complete_stored_pages']==339 and len(stored['records'])==335
    assert not stored['style_records'] and stored['typed_labels_checked']==2
    assert (stored['fresh_parity_dependent_pages'],stored['exact_compiled_pages_reused'],stored['fresh_relocated_native_relative_cases'])==(176,163,430)
    assert stored['every_byte_consumed_andall_first_internal_final_glyphs_bounds_canaries_andpagination_pass']
    assert stored['all_stored_planes_equal_directly_viewed_compiled_planes']
    assert native['manuscript_sha256']==d['styles']['manuscript_sha256']==digest(paths['source'])
    assert native['plan_sha256']==d['styles']['plan_sha256']==digest(paths['plan'])
    assert all(d[k]['runtime']==native['runtime'] for k in ['source','stored','catalogue','styles','menus','name_planes','macros','roles'])
    assert stored['reconstruction_sha256']==d['loaders']['reconstruction_sha256']==digest(paths['rebuilt'])
    assert d['catalogue']['stored_sha256']==digest(paths['stored']) and d['catalogue']['all335_physical_bodies_checked']
    assert d['catalogue']['all_new_effective_bodies_byte_exact_before_original_macro_expansion']
    assert (d['loaders']['fresh_whole_archive_loads_andcache_hits'],d['loaders']['fresh_parent_cases'])==(303,606)
    assert d['visual']['all339_final_pages_directly_viewed'] and d['visual']['all_names_andtwo_captions_directly_viewed']
    assert (d['visual']['tutorial_page_boundary_fixes'],d['visual']['additional_phrase_wrap_fixes'],d['visual']['pages_reclaimed'])==(4,8,0)
    assert not plan['failures'] and not any(i['severity'] in ['warning','error'] for r in plan['records'] for i in r['base_QA']['issues'])
    assert (actual['frames'],actual['initialized_runs'],actual['distinct_source_body_objects'],actual['distinct_body_pages'])==(33202,2,48,52)
    assert actual['all52_selected_pages_two_captions_andboth_host_transitions_directly_viewed']
    assert actual['all_four_two_page_tutorial_A_andfollowing_returns_observed']
    assert actual['all_six_FE_panels_andnamed_returns_observed'] and actual['both_mixed_font_Latin_I_repairs_observed']
    assert actual['complete_source_QA_hosts_return_to_resupply_andordinary_sailing']
    assert not any(actual[k] for k in ['natural_activation','original_location','earned_chronology','full_route','hardware'])
    assert not d['styles']['objects'] and not d['styles']['physical_alternatives'] and not d['styles']['native_target_slot_cases']
    assert len(d['menus']['menus'])==1 and actual['actual_menus']==1 and actual['actual_caption_strings']==2
    assert rebuilt['full_clean_current_block_archive_andserialized_NDS_inverses_exact'] and rebuilt['source_editorial_objects']==337
    assert rebuilt['FE_continuation_owners']==rebuilt['FE_inserted_commands']==0
    for collection in [d['visual']['evidence'],actual['evidence']]:
        for p,h in collection.items():assert digest(p)==h
    assert digest(rebuilt['target_archive'])==rebuilt['target_archive_sha256']
    bank=IlnkContainer.parse(Path(rebuilt['target_archive']).read_bytes()).blocks
    bodies={r['id']:r for r in stored['records']}
    captions={r['id']:(o,r) for o in stored['typed_objects'] for r in o['label_references']}
    plans={r['id']:r for r in plan['records']};prose={r['id']:r for r in d['prose']['records']}
    seen=set(actual['observed_body_IDs']);seen_captions=set(actual['observed_caption_IDs']);sourceplans=[]
    for row in doc['records']:
        ident=row['id'];block=bank[row['block']];prior=prose[ident]
        assert re.sub(r'\{MACRO:([A-Z]{2})\}',lambda m:m[1],row['english'])==prior['proposed_English']
        assert all(row[k]==prior[k] for k in ['source_hex','current_hex','source_reference','current_reference','decision','finding'])
        assert row['review']==dict(source=True,context=True,localization=True,naturalness=True,formatting=False)
        if row['kind']=='typed-choice-label':
            obj,item=captions[ident];at=item['offset'];raw=bytes.fromhex(item['stored_hex'])
            assert raw.decode('ascii')==row['english'] and block[at:at+len(raw)+1]==raw+b'\0'
            ref=dict(file_path=row['file_path'],block=row['block'],offset=at,command_offset=obj['offset'],source_index=item['source_index'],
                record_index=item['record_index'],exact_stored_hex=raw.hex(),target_archive_sha256=rebuilt['target_archive_sha256'])
            observed=ident in seen_captions;row['actual_caption_display_observed_in_disclosed_fixture']=observed
        else:
            item=bodies[ident];at=item['new_offset'];raw=bytes.fromhex(item['stored_hex'])
            assert block[at:at+len(raw)+1]==raw+b'\0' and block[at-5:at+1].hex()==row['source_complete_preamble_hex']
            ref=dict(file_path=row['file_path'],block=row['block'],offset=at,header_offset=at-5,record_index=item['new_record_index'],
                exact_stored_hex=raw.hex(),target_archive_sha256=rebuilt['target_archive_sha256'])
            selected=deepcopy(plans[ident]);assert selected['logical_English']==row['english']
            row['planned_English_markup']=selected['formatted_markup'];sourceplans.append(selected)
            observed=ident in seen;row['actual_utterance_observed_in_disclosed_fixture']=observed
        row['planned_integrated_reference']=ref;row['review']['formatting']=True
        row.update(fresh_formatting_binding_pending=False,registered_release_andcompletion_credit_pending=True,new_credit=0,
            review_evidence=dict(offline_visual=str(paths['visual']),stored=str(paths['stored']),gameplay=str(paths['actual']),
                coverage='observed-disclosed-QA' if observed else 'offline-native-andstored-only'))
    assert len(sourceplans)==335
    doc.update(encoder='dialogue-relocatable-v1',review_gates=['source','context','localization','naturalness','formatting'],
        all_individual_five_gates_pass=True,all337_individual_five_gates_pass=True,all_fifth_formatting_gates_pending=False,
        native_body_pages=339,source_editorial_body_objects=335,actual_source_body_objects=48,actual_body_pages=52,
        offline_only_source_body_objects=287,actual_caption_strings=2,offline_only_caption_strings=0,
        registered_release_andcompletion_credit_pending=True,parent_manuscript=str(paths['source']),parent_manuscript_sha256=digest(paths['source']),
        no_new_formatted_pages_orbatch_gameplay_orintegration_claim=False,native_macro_tokens_still_require_formatter_marking=False,new_credit=0,full_goal_complete=False)
    assert all(a['english']==b['english'] and a['finding']==b['finding'] for a,b in zip(original['records'],doc['records'],strict=True))
    validate_natural_dialogue_batch(doc)
    names=deepcopy(d['names']);actors={h['expected_actor_ID'] for h in actual['name_headers']};texts={r['text'] for r in d['name_planes']['planes']}
    assert len(names['records'])==21
    for row in names['records']:
        assert row['review']==dict(source=True,context=True,localization=True,naturalness=True,formatting=False)
        assert all(c['text'] in texts for c in row['current_consumers'])
        row['review']['formatting']=True
        row.update(actual_progressive_header_observed_in_disclosed_fixture=row['actor_ID'] in actors,
            full_catalogue_UI_layout_unvisited=True,full_catalogue_string_font_only_not_UI_layout_approval=True,
            name_localization_andfresh_display_approval_pending=False,fresh_native_display_orcompatible_proof_binding_pending=False,
            registered_release_andcompletion_credit_pending=True,new_credit=0)
    names.update(encoder='dialogue-relocatable-v1',review_gates=['source','context','localization','naturalness','formatting'],
        all21_individual_five_gates_pass_in_scoped_context=True,all_name_formatting_gates_pending=False,
        full_catalogue_UI_andfuture_role_assignments_unvisited=True,actual_review=str(paths['actual']),actual_review_sha256=digest(paths['actual']))
    validate_natural_dialogue_batch(names)
    out.mkdir();save(finalpath,doc);save(finalnames,names)
    sourceplan=out/'source335_release_plans.json'
    save(sourceplan,dict(records=sourceplans,failures=[],manuscript=str(finalpath),manuscript_sha256=digest(finalpath),
        source_editorial_objects=337,source_body_objects=335,physical_native_bodies=335,new_credit=0))
    save(out/'research_completion.json',dict(manuscript=str(finalpath),manuscript_sha256=digest(finalpath),names=str(finalnames),names_sha256=digest(finalnames),
        source_release_plans=str(sourceplan),source_release_plans_sha256=digest(sourceplan),all_individual_five_gates_pass=True,
        records=337,revisions=224,retentions=113,complete_exchanges=12,physical_body_candidates=335,native_body_pages=339,typed_labels=2,scoped_names=21,name_strings=28,
        source_FE_records=6,physical_FE_panels=6,FE_continuation_owners=0,additional_native_commands=0,source_credit_not_duplicated=True,
        tutorial_page_boundary_fixes=4,additional_phrase_wrap_fixes=8,pages_reclaimed=0,mixed_font_Latin_records_corrected=2,mixed_font_I_characters_corrected=3,
        corrupt_choice_captions_corrected=2,actual_source_body_objects=48,actual_native_candidates=48,actual_pages=52,actual_caption_strings=2,
        offline_only_source_body_objects=287,offline_only_caption_strings=0,actual_frames=33202,actual_runs=2,actual_menus=1,
        original_optional_conditions_locations_minigame_cutscene_effects_andhardware_unvisited=True,registered_integration_pending=True,
        main_unchanged=True,new_credit=0,full_goal_complete=False,evidence={str(p):digest(p) for p in [*paths.values(),finalpath,finalnames,sourceplan,Path(__file__)]}))
    print('Sealed337 five-gate reviews and21 scoped names:224 revisions/113 retentions. Registration/once-only credit remain.')


if __name__=='__main__':main()
