"""Seal328 individual reviews after complete storage checks and representative actual display QA."""
from collections import Counter
from copy import deepcopy
from pathlib import Path
import re
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from scripts.meaning_maria328_clean_v1 import ROOT
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

def main():
    finalpath=Path('translations/maria_B73_B95_final_review_v1.json')
    finalnames=Path('translations/maria_B73_B95_scoped_names_final_v1.json')
    out=ROOT/'research_completion_v1';assert not out.exists() and not finalpath.exists() and not finalnames.exists()
    paths=dict(source=ROOT/'formatting_v1/formatting_input.json',prose=Path('translations/maria_B73_B95_contextual_review_v1.json'),
        physical=ROOT/'formatting_FE_v1/physical_manuscript.json',plan=ROOT/'plan_visual_v6/automatic_plans.json',
        native=ROOT/'reconstruction_v1/native_pages.json',rebuilt=ROOT/'reconstruction_v1/reconstruction.json',
        stored=ROOT/'stored_v1/stored_native_verification.json',catalogue=ROOT/'stored_catalogue_all_v1/all314_stored_effective_body_bindings.json',
        loaders=ROOT/'loaders_v1/verification.json',visual=ROOT/'offline_display_approval_v1.json',actual=ROOT/'gameplay_review_v1.json',
        styles=ROOT/'compiled_styles_v1/compiled_style_objects.json',menus=ROOT/'menu_native_v1/menu_provider_and_planes.json',
        names=ROOT/'scoped24_names_editorial_review_v1.json',name_planes=ROOT/'name_planes_v1/native_name_planes.json',
        macros=ROOT/'formatting_v1/native_macro_measurements.json',roles=ROOT/'formatting_v1/role_bindings.json',terms=ROOT/'scoped_terms_reference_v1.json')
    data={k:load(p) for k,p in paths.items()};doc=deepcopy(data['source']);original=deepcopy(doc)
    rebuilt,stored,native,plan,actual=[data[k] for k in ['rebuilt','stored','native','plan','actual']]
    assert len(doc['records'])==328 and Counter(r['decision'] for r in doc['records'])=={'revision':143,'retention':185}
    assert len(native['records'])==len(plan['records'])==len(data['catalogue']['records'])==314
    assert native['pages']==stored['complete_stored_pages']==321
    assert (len(stored['records']),len(stored['style_records']),stored['typed_labels_checked'])==(290,24,15)
    assert (stored['fresh_parity_dependent_pages'],stored['exact_compiled_pages_reused'],stored['fresh_relocated_native_relative_cases'])==(148,173,315)
    assert stored['every_byte_consumed_andall_first_internal_final_glyphs_bounds_canaries_andpagination_pass']
    assert stored['all_stored_planes_equal_directly_viewed_compiled_planes']
    assert native['manuscript_sha256']==data['styles']['manuscript_sha256']==digest(rebuilt['manuscript'])
    assert native['plan_sha256']==data['styles']['plan_sha256']==digest(paths['plan'])
    assert all(data[k]['runtime']==native['runtime'] for k in ['source','stored','catalogue','styles','menus','name_planes','macros','roles','terms'])
    assert stored['reconstruction_sha256']==data['loaders']['reconstruction_sha256']==digest(paths['rebuilt'])
    assert data['catalogue']['stored_sha256']==digest(paths['stored']) and data['catalogue']['all314_physical_bodies_checked']
    assert data['catalogue']['all_new_effective_bodies_byte_exact_before_original_macro_expansion']
    assert (data['loaders']['fresh_whole_archive_loads_andcache_hits'],data['loaders']['fresh_parent_cases'])==(303,606)
    assert data['visual']['all321_final_pages_directly_viewed'] and data['visual']['all_names_and15_captions_directly_viewed']
    assert len(data['visual']['layout_changes'])==12 and data['visual']['pages_reclaimed']==1
    assert not plan['failures'] and not any(i['severity'] in ['warning','error'] for r in plan['records'] for i in r['base_QA']['issues'])
    assert (actual['frames'],actual['distinct_source_body_objects'],actual['distinct_native_body_candidates'],actual['distinct_body_pages'])==(22001,43,44,48)
    assert actual['all48_selected_pages_six_captions_andhost_transitions_directly_viewed']
    assert actual['source_owned_FE_continuation_A_then_menu_then_named_return_observed'] and actual['no_extra_blank_FE_panel_observed']
    assert actual['complete_source_QA_host_returns_to_resupply_andordinary_sailing']
    assert actual['repaired_bean_FE_rows_andfour_progressive_two_page_layouts_observed']
    assert actual['corrected_corrupt_style_observed']=='SC3_B95_STYLE_400_42'
    assert (data['styles']['physical_alternatives'],data['styles']['native_target_slot_cases'])==(24,32)
    assert sum(len(n['rejected']) for n in data['styles']['compiler_negatives'])==36
    assert len(data['menus']['menus'])==5 and actual['actual_menus']==2 and actual['actual_caption_strings']==6
    assert rebuilt['full_clean_current_block_archive_andserialized_NDS_inverses_exact'] and len(rebuilt['seven_FE_pagination_invalid_cases_rejected'])==7
    assert rebuilt['source_owned_exact_FE_control_repeated_once'] and rebuilt['source_editorial_objects']==328
    for collection in [data['visual']['evidence'],actual['evidence']]:
        for p,h in collection.items():assert digest(p)==h
    archive=Path(rebuilt['target_archive']).read_bytes();assert digest(rebuilt['target_archive'])==rebuilt['target_archive_sha256']
    bank=IlnkContainer.parse(archive).blocks
    bodies={r['id']:r for r in stored['records']+stored['style_records']}
    captions={r['id']:(o,r) for o in stored['typed_objects'] for r in o['label_references']}
    plans={r['id']:r for r in plan['records']};byprose={r['id']:r for r in data['prose']['records']}
    owner=data['physical']['pagination_owners'][0];assert owner['source_ID']=='DK4_MES_B87_R0139'
    seen=set(actual['observed_body_IDs']);seen_captions=set(actual['observed_caption_IDs'])
    sourceplans=[]
    for row in doc['records']:
        ident=row['id'];block=bank[row['block']];prior=byprose[ident]
        assert re.sub(r'\{MACRO:([A-Z]{2})\}',lambda m:m[1],row['english'])==prior['english']
        assert all(row[k]==prior[k] for k in ['source_hex','current_hex','source_reference','current_reference','decision','finding'])
        assert row['review']==dict(source=True,context=True,localization=True,naturalness=True,formatting=False)
        if row['kind']=='typed-choice-label':
            obj,item=captions[ident];at=item['offset'];raw=bytes.fromhex(item['stored_hex'])
            assert raw.decode('ascii')==row['english'] and block[at:at+len(raw)+1]==raw+b'\0'
            ref=dict(file_path=row['file_path'],block=row['block'],offset=at,command_offset=obj['offset'],source_index=item['source_index'],
                record_index=item['record_index'],exact_stored_hex=raw.hex(),target_archive_sha256=rebuilt['target_archive_sha256'])
            row['planned_integrated_reference']=ref;observed=ident in seen_captions
            row['actual_caption_display_observed_in_disclosed_fixture']=observed
        else:
            ids=owner['child_IDs'] if ident==owner['source_ID'] else [ident];refs=[]
            for nativeid in ids:
                item=bodies[nativeid];at=item['new_offset'];raw=bytes.fromhex(item['stored_hex'])
                assert block[at:at+len(raw)+1]==raw+b'\0'
                ref=dict(file_path=row['file_path'],block=row['block'],offset=at,record_index=item['new_record_index'],exact_stored_hex=raw.hex(),
                    native_panel_ID=nativeid,target_archive_sha256=rebuilt['target_archive_sha256'])
                if row.get('native_object_kind')=='4100-style-alternative':
                    header=bytes.fromhex(item['final_header_hex']);assert block[item['final_command_offset']:item['final_command_offset']+len(header)]==header
                    ref.update(command_offset=item['final_command_offset'],source_style_indices=item['source_style_indices'],
                        exact_command_header_hex=item['final_header_hex'],virtual_prefix_not_stored=True)
                else:
                    assert block[at-5:at+1].hex()==row['source_complete_preamble_hex'];ref['header_offset']=at-5
                assert nativeid in plans;refs.append(ref)
            selectedplan=deepcopy(plans[ids[0]]);row['planned_English_markup']=selectedplan['formatted_markup']
            row['planned_integrated_reference']=refs[0]
            if len(ids)==2:
                assert ' '.join(plans[i]['logical_English'] for i in ids)==row['english']
                row.update(planned_integrated_native_pages=refs,formatter_owned_FE_pagination=owner,
                    first_encoded_hex_represents_first_native_panel_only=True,complete_paragraph_has_two_source_owned_native_FE_panels=True)
                selectedplan.update(id=ident,logical_English=row['english'],expected_native_pages=2,
                    native_FE_child_pages=[plans[i] for i in ids],encoded_hex_is_first_native_panel_only=True,
                    complete_paragraph_owned_by_two_native_FE_commands=True)
            sourceplans.append(selectedplan);observed=all(i in seen for i in ids)
            row['actual_utterance_observed_in_disclosed_fixture']=observed
        row['review']['formatting']=True
        row.update(fresh_formatting_binding_pending=False,registered_release_andcompletion_credit_pending=True,new_credit=0,
            review_evidence=dict(offline_visual=str(paths['visual']),stored=str(paths['stored']),gameplay=str(paths['actual']),
                coverage='observed-disclosed-QA' if observed else 'offline-native-andstored-only'))
    assert len(sourceplans)==313
    doc.update(encoder='dialogue-relocatable-v1',review_gates=['source','context','localization','naturalness','formatting'],
        all_individual_five_gates_pass=True,all328_individual_five_gates_pass=True,all_fifth_formatting_gates_pending=False,
        no_new_formatted_pages_orbatch_gameplay_orintegration_claim=False,native_macro_tokens_still_require_formatter_marking=False,
        native_body_pages=321,physical_native_body_candidates_after_pagination=314,source_editorial_body_objects=313,
        actual_source_body_objects=43,actual_physical_body_candidates=44,actual_body_pages=48,offline_only_source_body_objects=270,
        actual_caption_strings=6,offline_only_caption_strings=9,registered_release_andcompletion_credit_pending=True,
        parent_manuscript=str(paths['source']),parent_manuscript_sha256=digest(paths['source']),new_credit=0,full_goal_complete=False)
    assert all(a['english']==b['english'] and a['finding']==b['finding'] for a,b in zip(original['records'],doc['records'],strict=True))
    validate_natural_dialogue_batch(doc)
    names=deepcopy(data['names']);observedactors={h['expected_actor_ID'] for h in actual['name_headers']}
    planetexts={r['text'] for r in data['name_planes']['planes']}
    assert len(names['records'])==24
    for row in names['records']:
        assert row['review']==dict(source=True,context=True,localization=True,naturalness=True,formatting=False)
        assert all(c['text'] in planetexts for c in row['current_consumers'])
        row['review']['formatting']=True
        row.update(actual_progressive_header_observed_in_disclosed_fixture=row['actor_ID'] in observedactors,
            full_catalogue_UI_layout_unvisited=True,full_catalogue_string_font_only_not_UI_layout_approval=True,
            name_localization_andfresh_display_approval_pending=False,fresh_native_display_orcompatible_proof_binding_pending=False,
            registered_release_andcompletion_credit_pending=True,new_credit=0)
    names.update(encoder='dialogue-relocatable-v1',review_gates=['source','context','localization','naturalness','formatting'],
        all24_individual_five_gates_pass_in_scoped_context=True,all_name_formatting_gates_pending=False,
        full_catalogue_UI_andfuture_role_assignments_unvisited=True,actual_review=str(paths['actual']),actual_review_sha256=digest(paths['actual']))
    validate_natural_dialogue_batch(names)
    out.mkdir();save(finalpath,doc);save(finalnames,names)
    sourceplanpath=out/'source313_release_plans.json'
    save(sourceplanpath,dict(records=sourceplans,failures=[],manuscript=str(finalpath),manuscript_sha256=digest(finalpath),
        source_editorial_objects=328,source_body_objects=313,physical_native_bodies=314,new_credit=0))
    releaseplan=out/'physical_release_plans.json';save(releaseplan,dict(plan,source_review_manuscript=str(finalpath),source_review_manuscript_sha256=digest(finalpath)))
    save(out/'research_completion.json',dict(manuscript=str(finalpath),manuscript_sha256=digest(finalpath),names=str(finalnames),names_sha256=digest(finalnames),
        source_release_plans=str(sourceplanpath),source_release_plans_sha256=digest(sourceplanpath),
        all_individual_five_gates_pass=True,records=328,revisions=143,retentions=185,complete_exchanges=21,
        physical_body_candidates=314,native_body_pages=321,typed_labels=15,scoped_names=24,name_strings=28,
        source_FE_records=27,physical_FE_panels=28,FE_continuation_owners=1,additional_native_commands=1,source_credit_not_duplicated=True,
        layout_improvements=12,pages_reclaimed=1,nonASCII_targets_corrected=20,corrupt_style_replies_corrected=2,
        actual_source_body_objects=43,actual_native_candidates=44,actual_pages=48,actual_caption_strings=6,
        offline_only_source_body_objects=270,offline_only_caption_strings=9,actual_frames=22001,actual_runs=1,actual_menus=2,
        original_optional_conditions_locations_cutscene_effects_andhardware_unvisited=True,
        registered_integration_pending=True,main_unchanged=True,new_credit=0,full_goal_complete=False,
        evidence={str(p):digest(p) for p in [*paths.values(),finalpath,finalnames,sourceplanpath,releaseplan,Path(__file__)]}))
    print('Sealed328 five-gate reviews and24 scoped names:143 revisions/185 retentions. Registered integration/once-only credit remain.')

if __name__=='__main__':main()
