"""Seal330 original source reviews; two FE owners never add editorial credit."""
from collections import Counter
from copy import deepcopy
from pathlib import Path
import re
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from scripts.meaning_maria330_clean_v1 import ROOT
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

def main():
    finalpath=Path('translations/maria_B96_B124_final_review_v1.json')
    finalnames=Path('translations/maria_B96_B124_scoped_names_final_v1.json')
    out=ROOT/'research_completion_v1'; assert not any(p.exists() for p in [out,finalpath,finalnames])
    paths=dict(source=ROOT/'formatting_v1/formatting_input.json',prose=Path('translations/maria_B96_B124_contextual_review_v2.json'),
        physical=ROOT/'formatting_FE_v2/physical_manuscript.json',plan=ROOT/'plan_continuity_v10/automatic_plans.json',
        native=ROOT/'reconstruction_v2/native_pages.json',rebuilt=ROOT/'reconstruction_v2/reconstruction.json',
        stored=ROOT/'stored_v1/stored_native_verification.json',catalogue=ROOT/'stored_catalogue_all_v1/all330_stored_effective_body_bindings.json',
        loaders=ROOT/'loaders_v1/verification.json',visual=ROOT/'offline_display_approval_v1.json',actual=ROOT/'gameplay_review_v1.json',
        styles=ROOT/'compiled_styles_v1/compiled_style_objects.json',menus=ROOT/'menu_native_approved_v1.json',
        names=ROOT/'name_inputs_v2/review.json',name_planes=ROOT/'name_planes_v2/native_name_planes.json',
        macros=ROOT/'formatting_v1/native_macro_measurements.json',roles=ROOT/'formatting_v1/role_bindings.json',terms=ROOT/'scoped_item_stat_reference_v1.json',
        story_terms=ROOT/'registered_story_terms_reference_v1.json')
    data={k:load(p) for k,p in paths.items()}; doc=deepcopy(data['source']); original=deepcopy(doc)
    rebuilt,stored,native,plan,actual=[data[k] for k in ['rebuilt','stored','native','plan','actual']]
    assert len(doc['records'])==330 and Counter(r['decision'] for r in doc['records'])=={'revision':249,'retention':81}
    assert len(native['records'])==len(plan['records'])==len(data['catalogue']['records'])==330
    assert native['pages']==stored['complete_stored_pages']==338
    assert (len(stored['records']),len(stored['style_records']),stored['typed_labels_checked'])==(295,35,2)
    assert (stored['fresh_parity_dependent_pages'],stored['exact_compiled_pages_reused'],stored['fresh_relocated_native_relative_cases'])==(156,182,380)
    assert stored['every_byte_consumed_andall_first_internal_final_glyphs_bounds_canaries_andpagination_pass']
    assert stored['all_stored_planes_equal_directly_viewed_compiled_planes']
    assert native['manuscript_sha256']==data['styles']['manuscript_sha256']==digest(rebuilt['manuscript'])
    assert native['plan_sha256']==data['styles']['plan_sha256']==digest(paths['plan'])
    assert all(data[k]['runtime']==native['runtime'] for k in ['source','stored','catalogue','styles','menus','name_planes','macros','roles','terms'])
    assert stored['reconstruction_sha256']==data['loaders']['reconstruction_sha256']==digest(paths['rebuilt'])
    assert data['catalogue']['stored_sha256']==digest(paths['stored']) and data['catalogue']['all330_physical_bodies_checked']
    assert data['catalogue']['all_new_effective_bodies_byte_exact_before_original_macro_expansion']
    assert (data['loaders']['fresh_whole_archive_loads_andcache_hits'],data['loaders']['fresh_parent_cases'])==(303,606)
    assert data['visual']['all338_final_pages_directly_viewed'] and data['visual']['all_names_andtwo_captions_directly_viewed']
    assert data['visual']['pages_reclaimed']==3 and data['visual']['closing_clause_boundary_fixes']==7
    assert not plan['failures'] and not any(i['severity'] in ['warning','error'] for r in plan['records'] for i in r['base_QA']['issues'])
    assert (actual['frames'],actual['initialized_runs'],actual['distinct_source_body_objects'],actual['distinct_native_body_candidates'],actual['distinct_body_pages'])==(34402,2,53,55,58)
    assert actual['all58_selected_pages_two_captions_andboth_host_transitions_directly_viewed']
    assert actual['both_source_owned_FE_continuation_A_andfollowing_returns_observed'] and actual['no_extra_blank_FE_panel_observed']
    assert actual['complete_source_QA_hosts_return_to_resupply_andordinary_sailing']
    assert actual['all_three_mixed_font_Latin_repairs_andformer_Japanese_grant_observed']
    assert (data['styles']['physical_alternatives'],data['styles']['native_target_slot_cases'])==(35,48)
    assert sum(len(n['rejected']) for n in data['styles']['compiler_negatives'])==54
    assert len(data['menus']['menus'])==1 and actual['actual_menus']==1 and actual['actual_caption_strings']==2
    assert rebuilt['full_clean_current_block_archive_andserialized_NDS_inverses_exact']
    assert len(rebuilt['per_owner_FE_pagination_rejections'])==2 and all(len(r['rejected'])==7 for r in rebuilt['per_owner_FE_pagination_rejections'])
    assert rebuilt['source_owned_exact_FE_controls_repeated_once_per_owner'] and rebuilt['source_editorial_objects']==330
    for collection in [data['visual']['evidence'],actual['evidence']]:
        for p,h in collection.items():assert digest(p)==h
    archive=Path(rebuilt['target_archive']).read_bytes(); assert digest(rebuilt['target_archive'])==rebuilt['target_archive_sha256']
    bank=IlnkContainer.parse(archive).blocks
    bodies={r['id']:r for r in stored['records']+stored['style_records']}
    captions={r['id']:(o,r) for o in stored['typed_objects'] for r in o['label_references']}
    plans={r['id']:r for r in plan['records']}; byprose={r['id']:r for r in data['prose']['records']}
    owners={o['source_ID']:o for o in data['physical']['pagination_owners']}
    assert set(owners)=={'DK4_MES_B116_R0041','DK4_MES_B116_R0051'}
    seen=set(actual['observed_body_IDs']); seen_captions=set(actual['observed_caption_IDs']); sourceplans=[]
    for row in doc['records']:
        ident=row['id']; block=bank[row['block']]; prior=byprose[ident]
        assert re.sub(r'\{MACRO:([A-Z]{2})\}',lambda m:m[1],row['english'])==prior['english']
        assert all(row[k]==prior[k] for k in ['source_hex','current_hex','source_reference','current_reference','decision','finding'])
        assert row['review']==dict(source=True,context=True,localization=True,naturalness=True,formatting=False)
        if row['kind']=='typed-choice-label':
            obj,item=captions[ident]; at=item['offset']; raw=bytes.fromhex(item['stored_hex'])
            assert raw.decode('ascii')==row['english'] and block[at:at+len(raw)+1]==raw+b'\0'
            ref=dict(file_path=row['file_path'],block=row['block'],offset=at,command_offset=obj['offset'],source_index=item['source_index'],
                record_index=item['record_index'],exact_stored_hex=raw.hex(),target_archive_sha256=rebuilt['target_archive_sha256'])
            row['planned_integrated_reference']=ref; observed=ident in seen_captions
            row['actual_caption_display_observed_in_disclosed_fixture']=observed
        else:
            owner=owners.get(ident); ids=owner['child_IDs'] if owner else [ident]; refs=[]
            for nativeid in ids:
                item=bodies[nativeid]; at=item['new_offset']; raw=bytes.fromhex(item['stored_hex'])
                assert block[at:at+len(raw)+1]==raw+b'\0'
                ref=dict(file_path=row['file_path'],block=row['block'],offset=at,record_index=item['new_record_index'],exact_stored_hex=raw.hex(),
                    native_panel_ID=nativeid,target_archive_sha256=rebuilt['target_archive_sha256'])
                if row.get('native_object_kind')=='4100-style-alternative':
                    header=bytes.fromhex(item['final_header_hex']); assert block[item['final_command_offset']:item['final_command_offset']+len(header)]==header
                    ref.update(command_offset=item['final_command_offset'],source_style_indices=item['source_style_indices'],exact_command_header_hex=item['final_header_hex'],virtual_prefix_not_stored=True)
                else:
                    assert block[at-5:at+1].hex()==row['source_complete_preamble_hex']; ref['header_offset']=at-5
                assert nativeid in plans; refs.append(ref)
            selectedplan=deepcopy(plans[ids[0]]); row['planned_English_markup']=selectedplan['formatted_markup']; row['planned_integrated_reference']=refs[0]
            if owner:
                assert ' '.join(plans[i]['logical_English'] for i in ids)==row['english']
                row.update(planned_integrated_native_pages=refs,formatter_owned_FE_pagination=owner,
                    first_encoded_hex_represents_first_native_panel_only=True,complete_paragraph_has_two_source_owned_native_FE_panels=True)
                selectedplan.update(id=ident,logical_English=row['english'],expected_native_pages=2,native_FE_child_pages=[plans[i] for i in ids],
                    encoded_hex_is_first_native_panel_only=True,complete_paragraph_owned_by_two_native_FE_commands=True)
            sourceplans.append(selectedplan); observed=all(i in seen for i in ids); row['actual_utterance_observed_in_disclosed_fixture']=observed
        row['review']['formatting']=True
        row.update(fresh_formatting_binding_pending=False,registered_release_andcompletion_credit_pending=True,new_credit=0,
            review_evidence=dict(offline_visual=str(paths['visual']),stored=str(paths['stored']),gameplay=str(paths['actual']),coverage='observed-disclosed-QA' if observed else 'offline-native-andstored-only'))
    assert len(sourceplans)==328
    doc.update(encoder='dialogue-relocatable-v1',review_gates=['source','context','localization','naturalness','formatting'],
        all_individual_five_gates_pass=True,all330_individual_five_gates_pass=True,all_fifth_formatting_gates_pending=False,
        no_new_formatted_pages_orbatch_gameplay_orintegration_claim=False,native_macro_tokens_still_require_formatter_marking=False,
        native_body_pages=338,physical_native_body_candidates_after_pagination=330,source_editorial_body_objects=328,
        actual_source_body_objects=53,actual_physical_body_candidates=55,actual_body_pages=58,offline_only_source_body_objects=275,
        actual_caption_strings=2,offline_only_caption_strings=0,registered_release_andcompletion_credit_pending=True,
        parent_manuscript=str(paths['source']),parent_manuscript_sha256=digest(paths['source']),new_credit=0,full_goal_complete=False)
    assert all(a['english']==b['english'] and a['finding']==b['finding'] for a,b in zip(original['records'],doc['records'],strict=True))
    validate_natural_dialogue_batch(doc)
    names=deepcopy(data['names']); observedactors={h['expected_actor_ID'] for h in actual['name_headers']}; planetexts={r['text'] for r in data['name_planes']['planes']}
    assert len(names['records'])==26
    for row in names['records']:
        assert row['review']==dict(source=True,context=True,localization=True,naturalness=True,formatting=False)
        assert all(c['text'] in planetexts for c in row['current_consumers'])
        row['review']['formatting']=True
        row.update(actual_progressive_header_observed_in_disclosed_fixture=row['actor_ID'] in observedactors,
            full_catalogue_UI_layout_unvisited=True,full_catalogue_string_font_only_not_UI_layout_approval=True,
            name_localization_andfresh_display_approval_pending=False,fresh_native_display_orcompatible_proof_binding_pending=False,
            registered_release_andcompletion_credit_pending=True,new_credit=0)
    names.update(encoder='dialogue-relocatable-v1',review_gates=['source','context','localization','naturalness','formatting'],
        all26_individual_five_gates_pass_in_scoped_context=True,all_name_formatting_gates_pending=False,
        full_catalogue_UI_andfuture_role_assignments_unvisited=True,actual_review=str(paths['actual']),actual_review_sha256=digest(paths['actual']))
    validate_natural_dialogue_batch(names)
    out.mkdir(); save(finalpath,doc); save(finalnames,names)
    sourceplanpath=out/'source328_release_plans.json'; releaseplan=out/'physical_release_plans.json'
    save(sourceplanpath,dict(records=sourceplans,failures=[],manuscript=str(finalpath),manuscript_sha256=digest(finalpath),source_editorial_objects=330,source_body_objects=328,physical_native_bodies=330,new_credit=0))
    save(releaseplan,dict(plan,source_review_manuscript=str(finalpath),source_review_manuscript_sha256=digest(finalpath)))
    save(out/'research_completion.json',dict(manuscript=str(finalpath),manuscript_sha256=digest(finalpath),names=str(finalnames),names_sha256=digest(finalnames),
        source_release_plans=str(sourceplanpath),source_release_plans_sha256=digest(sourceplanpath),all_individual_five_gates_pass=True,
        records=330,revisions=249,retentions=81,complete_exchanges=26,physical_body_candidates=330,native_body_pages=338,typed_labels=2,scoped_names=26,name_strings=29,
        source_FE_records=8,physical_FE_panels=10,FE_continuation_owners=2,additional_native_commands=2,source_credit_not_duplicated=True,
        closing_clause_boundary_fixes=7,pages_reclaimed=3,orphan_See_repaired=True,mixed_font_Latin_targets_corrected=3,former_Japanese_grant_translated=True,
        actual_source_body_objects=53,actual_native_candidates=55,actual_pages=58,actual_caption_strings=2,offline_only_source_body_objects=275,offline_only_caption_strings=0,
        actual_frames=34402,actual_runs=2,actual_menus=1,original_optional_conditions_locations_cutscene_effects_andhardware_unvisited=True,
        registered_integration_pending=True,main_unchanged=True,new_credit=0,full_goal_complete=False,
        evidence={str(p):digest(p) for p in [*paths.values(),finalpath,finalnames,sourceplanpath,releaseplan,Path(__file__)]}))
    print('Sealed330 five-gate reviews and26 scoped names:249 revisions/81 retentions. Registration/once-only credit remain.')

if __name__=='__main__':main()
