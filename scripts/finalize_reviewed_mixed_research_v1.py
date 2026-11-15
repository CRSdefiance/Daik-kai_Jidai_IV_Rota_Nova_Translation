"""Seal individually reviewed mixed-scene research, preserving exact observed/offline scope."""
import argparse
from copy import deepcopy
from pathlib import Path
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save


def main():
    p=argparse.ArgumentParser(description=__doc__)
    for key in ['reconstruction','stored','catalogue','loaders','offline-visual','body-visual','names','name-decisions','out','final','final-names']:
        p.add_argument('--'+key,type=Path,required=True)
    for key in ['actual-proofs','contacts','actual-menus','terminals']:
        p.add_argument('--'+key,type=Path,nargs='+',required=True)
    args=p.parse_args();assert not any(x.exists() for x in [args.out,args.final,args.final_names])
    rebuilt,stored,cat,loaders,offline,body,names,name_doc=map(load,[args.reconstruction,args.stored,args.catalogue,args.loaders,args.offline_visual,args.body_visual,args.names,args.name_decisions])
    doc,plan,native,menu,styles=map(load,[rebuilt['manuscript'],rebuilt['plan'],rebuilt['native'],rebuilt['menu'],rebuilt['styles']])
    count=len(doc['records']);assert count==doc['source_objects']
    assert len(native['records'])==len(plan['records'])==doc['physical_speech_objects']
    assert native['runtime']==menu['runtime']==styles['runtime']==names['runtime']==stored['runtime']
    assert rebuilt['manuscript_sha256']==sha(Path(rebuilt['manuscript']).read_bytes())==native['manuscript_sha256']==menu['manuscript_sha256']==styles['manuscript_sha256']
    assert stored['reconstruction_sha256']==sha(args.reconstruction.read_bytes()) and stored['native_sha256']==sha(Path(rebuilt['native']).read_bytes())
    assert stored['every_byte_consumed_andall_first_internal_final_glyphs_bounds_canaries_andpagination_pass']
    assert stored['all_stored_planes_equal_directly_viewed_compiled_planes']
    assert len(stored['records'])==doc['ordinary_speech_objects']==rebuilt['speech_count']
    assert len(stored['style_records'])==doc['style_physical_speech_objects']==rebuilt['style_physical_speech_count']
    assert len(stored['records'])+len(stored['style_records'])==len(cat['records'])==len(plan['records'])
    assert cat['all_new_effective_bodies_byte_exact_before_original_macro_expansion']
    assert stored['typed_labels_checked']==doc['typed_choice_objects']==rebuilt['typed_choice_count']
    assert stored['complete_stored_pages']==native['pages']==body['final_body_pages']
    assert body['all344_final_body_pages_directly_viewed'] and offline['all344_body_pages_directly_viewed']
    assert offline['all5_menu_sheets_and2_public_name_sheets_directly_viewed']
    assert names['offline_visual_approved'] and not names['direct_visual_review_pending']
    assert menu['offline_visual_approved'] and not menu['direct_view_pending']
    assert styles['native_target_slot_cases']==8*doc['style_command_objects']
    assert sum(len(x['rejected']) for x in styles['compiler_negatives'])==9*doc['style_command_objects']
    assert loaders['reconstruction_sha256']==sha(args.reconstruction.read_bytes())
    assert loaders['fresh_parent_cases']==2*len(rebuilt['changed_blocks'])
    assert loaders['fresh_parent_cases']+loaders['exact_reused_parent_cases']==2*loaders['fresh_whole_archive_loads_andcache_hits']
    assert all(r['review']==dict(source=True,context=True,localization=True,naturalness=True,formatting=False) for r in doc['records'])
    for path in args.terminals:
        t=load(path);assert t['terminal'] and t['completed_without_exception'] and t['all_locked_sources_unchanged']
        assert not t['garbage_collection']['errors']
    actuals=list(map(load,args.actual_proofs));contacts=list(map(load,args.contacts));actual_menus=list(map(load,args.actual_menus))
    sourceids=set();pageids=set();actorids=set();selectors=set();public=set();sheets=[]
    for path,actual in zip(args.actual_proofs,actuals,strict=True):
        for ref,digest in actual['evidence'].items():assert sha(Path(ref).read_bytes())==digest
        assert actual['all_selected_pages_observed_in_exact_fixture_order'] and actual['all_complete_native_body_andheader_planes_andblank_guards_match']
        assert not any(actual[k] for k in ['natural_activation','original_location','earned_chronology','full_route','hardware'])
        sourceids.update(r['id'] for r in actual['body_pages']);pageids.update((r['id'],r['page']) for r in actual['body_pages'])
        actorids.update(h['expected_actor_ID'] for h in actual['headers']);selectors.update(h['source_selector'] for h in actual['headers']);public.update(h['text'] for h in actual['headers'])
        assert all(h['expected_ID_from_offline_role_proof_not_pixels'] for h in actual['headers'])
    for contact in contacts:
        assert sha(Path(contact['actual_pixel_proof']).read_bytes())==contact['actual_pixel_proof_sha256']
        sheets+=contact['bottom_screen_sheets']+contact['full_scene_sheets']
    live_menu_commands=[]
    for actual in actual_menus:
        assert actual['all_declared_native_menus_have_complete_pixel_centering_bounds_andbackground_matches']
        assert actual['native_return_values_andbranch_sites_proved_separately_offline'] and actual['numeric_modal_return_register_original_story_branches_andcancellation_unvisited']
        sheets.append(actual['review_sheet']);live_menu_commands+=actual['menus']
    assert len(live_menu_commands)==doc['typed_choice_commands']
    assert sum(m['count'] for m in live_menu_commands)==doc['typed_choice_objects']
    assert all(m['count']==2 and m['observed_selected_options']==[0] for m in live_menu_commands)
    for sheet in sheets:assert sha(Path(sheet['path']).read_bytes())==sheet['sha256']
    allids={r['id'] for r in native['records']};assert sourceids<=allids
    assert (len(sourceids),len(pageids),sum(a['frames'] for a in actuals))==(132,134,43282)
    assert {207,208,209,214,215,220}<=set(int(k) for k in native['dynamic_role_bindings'])
    styleids={r['id'] for r in doc['records'] if r.get('native_object_kind')=='4100-style-alternative'}
    assert len(sourceids&styleids)==6 and len(styleids-sourceids)==28
    args.out.mkdir(parents=True)
    visual=args.out/'complete_visual_approval.json'
    save(visual,dict(native_body_pages=native['pages'],all344_body_pages_10_captions_22_public_names_approved=True,
        offline_visual=str(args.offline_visual),offline_visual_sha256=sha(args.offline_visual.read_bytes()),
        body_visual=str(args.body_visual),body_visual_sha256=sha(args.body_visual.read_bytes()),
        all134_observed_body_pages_andall5_menu_captures_directly_viewed=True,all12_compact_2_fullscene_2_menu_sheets_directly_viewed=True,
        reviewed_sheets=sheets,all_prose_retained_after_actual_review=True,
        retention_note='The rescue preserves actual grandfather/grandson kinship andgeneric mister for the rescuer. Cristina/Clau andthe private asides stay distinct. The legend remains qualified while Rafael draws his own conclusion. Retain the documented realization beat andthe exact menu/item names. The repaired FE guard andboth sampled page transitions show complete glyphs.',
        menu_cursor_states_observed=[0],other_menu_states_returns_andbranches_offline_only=True,
        initialized_background_not_original_locations=True,new_credit=0,guide_photos=False))
    actual_path=args.out/'actual_review.json'
    save(actual_path,dict(total_frames=sum(a['frames'] for a in actuals),initialized_fixture_runs=len(actuals),
        source_speech_variants_observed=len(sourceids),native_body_pages_observed=len(pageids),actual_choice_labels=doc['typed_choice_objects'],
        source_editorial_objects_observed=len(sourceids)+doc['typed_choice_objects'],offline_only_speech_variants=len(allids-sourceids),
        ordinary_speeches_observed=len(sourceids-styleids),physical_style_variants_observed=len(sourceids&styleids),
        source_IDs_observed=sorted(sourceids),offline_only_source_IDs=sorted(allids-sourceids),
        observed_source_selectors=sorted(selectors),matched_public_names=sorted(public),
        expected_actor_IDs_from_offline_binding_not_inferred_pixels=sorted(actorids),
        complete_body_holds=sum(a['complete_body_planes'] for a in actuals),complete_header_holds=sum(a['complete_header_planes'] for a in actuals),
        all_six_complete_style_commands_observed_under_unmodified_default_roles=True,
        all_five_menus_default_selected_state_observed=True,other_cursor_states_VM_returns_branches_andcancellation_offline_only=True,
        no_original_sailing_recruitment_investment_orquest_state_activation_claim=True,
        natural_activation=False,original_location=False,earned_chronology=False,full_route=False,hardware=False,
        evidence={str(x):sha(x.read_bytes()) for x in [*args.actual_proofs,*args.contacts,*args.actual_menus,visual]},new_credit=0,guide_photos=False))
    name_doc=deepcopy(name_doc)
    for row in name_doc['records']:
        assert row['kind']=='progressive-nameplate'
        row['review']['formatting']=True;row['actual_header_observed_in_disclosed_fixture']=row['actor_ID'] in actorids
    name_doc.update(review_gates=['source','context','localization','naturalness','formatting'],
        all22_individual_five_gates_pass_for_public_nameplanes=True,full_catalogue_andglobal207_review_still_open=True,
        two_full_catalogue_particle_corrections_still_pending=True,actor_IDs_unvisited_in_current_fixtures=sorted({r['actor_ID'] for r in name_doc['records']}-actorids),
        actual_review=str(actual_path),actual_review_sha256=sha(actual_path.read_bytes()))
    validate_natural_dialogue_batch(name_doc);save(args.final_names,name_doc)
    archive=Path(rebuilt['target_archive']).read_bytes();assert sha(archive)==rebuilt['target_archive_sha256'];blocks=IlnkContainer.parse(archive).blocks
    stored_rows={r['id']:r for r in stored['records']+stored['style_records']};labels={r['id']:(obj,r) for obj in stored['typed_objects'] for r in obj['label_references']};plans={r['id']:r for r in plan['records']}
    before=deepcopy(doc)
    for row in doc['records']:
        if row['id'] in stored_rows:
            item=stored_rows[row['id']];at=item['new_offset'];raw=bytes.fromhex(item['stored_hex'])
            ref=dict(file_path=row['file_path'],block=row['block'],offset=at,record_index=item['new_record_index'],exact_stored_hex=raw.hex(),target_archive_sha256=sha(archive))
            if row.get('native_object_kind')=='4100-style-alternative':
                ref.update(command_offset=item['final_command_offset'],source_style_indices=item['source_style_indices'],exact_command_header_hex=item['final_header_hex'],virtual_prefix_not_stored=True)
                head=bytes.fromhex(item['final_header_hex']);assert blocks[row['block']][item['final_command_offset']:item['final_command_offset']+len(head)]==head
            else:
                ref['header_offset']=at-5;assert blocks[row['block']][at-5:at+1].hex()==row['source_complete_preamble_hex']
            row['planned_English_markup']=plans[row['id']]['formatted_markup'];row['actual_utterance_observed_in_disclosed_fixture']=row['id'] in sourceids
        else:
            obj,item=labels[row['id']];at=item['offset'];raw=bytes.fromhex(item['stored_hex']);assert raw.decode('ascii')==row['english']
            ref=dict(file_path=row['file_path'],block=row['block'],offset=at,command_offset=obj['offset'],source_index=item['source_index'],record_index=item['record_index'],exact_stored_hex=raw.hex(),target_archive_sha256=sha(archive))
            row['actual_caption_default_cursor_state_observed']=True;row['other_cursor_andreturn_cases_verified_offline']=True
        assert blocks[row['block']][at:at+len(raw)+1]==raw+b'\0'
        row.update(planned_integrated_reference=ref,fresh_formatting_binding_pending=False,
            fresh_display_stored_gameplay_andregistered_integration_pending=False,registered_release_andcompletion_credit_pending=True,new_credit=0)
        for key in ['all_five_review_gates_pending','source_context_localization_formatting_gates_pending',
                'source_names_roles_terms_anddynamic_bindings_pending','source_names_roles_terms_controls_anddynamic_bindings_pending',
                'source_name_term_control_andformatting_binding_pending','native_name_controls_andterm_binding_pending',
                'UI_label_ornamed_item_binding_pending','clean_tutorial_meaning_saved_native_controls_andUI_label_comparison_pending',
                'native_style_dispatch_andall_five_review_gates_pending']:
            if key in row:row[key]=False
        row['review']['formatting']=True
    assert all((a['english'],a['decision'],a['finding'])==(b['english'],b['decision'],b['finding']) for a,b in zip(before['records'],doc['records'],strict=True))
    doc.update(all_fifth_formatting_gates_pending=False,all_individual_five_gates_pass=True,**{f'all{count}_individual_five_gates_pass':True},
        source_context_localization_formatting_gates_pending=False,all_scoped_name_planes_andtwo_full_name_particle_fixes_pending=False,
        all_previous_four_prose_gates_wording_decisions_andfindings_exact=True,
        all_contextual_findings_wording_andindividual_gate_values_exact_preserved=False,
        no_original_conditional_activation_or_new_gameplay_claim=False,no_original_conditional_activation_claim=True,
        only_disclosed_fixture_gameplay_observed=True,
        registered_release_andcompletion_credit_pending=True,native_body_pages=native['pages'],
        actual_source_speech_variants=len(sourceids),actual_body_pages=len(pageids),offline_only_source_speech_variants=len(allids-sourceids),
        scoped_name_review=str(args.final_names),scoped_name_review_sha256=sha(args.final_names.read_bytes()),
        parent_manuscript=rebuilt['manuscript'],parent_manuscript_sha256=rebuilt['manuscript_sha256'],
        formatting_evidence=dict(native=rebuilt['native'],stored=str(args.stored),catalogue=str(args.catalogue),loaders=str(args.loaders),visual=str(visual),actual=str(actual_path)))
    validate_natural_dialogue_batch(doc);save(args.final,doc)
    plan.update(manuscript=str(args.final),manuscript_sha256=sha(args.final.read_bytes()),exact_all_prose_andcompiled_bytes_unchanged=True)
    save(args.out/'release_plans.json',plan)
    save(args.out/'research_completion.json',dict(manuscript=str(args.final),manuscript_sha256=sha(args.final.read_bytes()),
        all_individual_five_gates_pass=True,records=count,revisions=sum(r['decision']=='revision' for r in doc['records']),
        retentions=sum(r['decision']=='retention' for r in doc['records']),body_pages=native['pages'],typed_labels=doc['typed_choice_objects'],
        scoped_public_names=len(name_doc['records']),two_full_catalogue_particle_fixes_pending=True,
        actual_source_variants=len(sourceids),actual_pages=len(pageids),offline_only_source_variants=len(allids-sourceids),
        registered_integration_pending=True,main_unchanged=True,new_credit=0,full_goal_complete=False,
        evidence={str(x):sha(x.read_bytes()) for x in [args.final,args.final_names,args.reconstruction,args.stored,args.catalogue,args.loaders,args.offline_visual,args.body_visual,args.names,*args.actual_proofs,*args.contacts,*args.actual_menus,*args.terminals,visual,actual_path,Path(__file__)]}))
    print(f'Sealed{count} individual five-gate research reviews;{len(sourceids)} observed variants/{len(pageids)} pages,{len(allids-sourceids)} variants offline-only. Registered integration andtwo catalogue particles remain;no credit orpromotion.')


if __name__=='__main__':main()
