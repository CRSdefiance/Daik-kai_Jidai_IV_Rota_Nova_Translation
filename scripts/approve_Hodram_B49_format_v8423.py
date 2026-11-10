"""Approve individual formatting after complete native/stored andrepresentative/focused actual review;credit waits forrelease."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/Hodram_B49_format_v8423')
OLD=Path('translations/hodram_B49_editorial_manuscript_v2.json')
DOC=Path('translations/hodram_B49_editorial_manuscript_v3.json')
OLD_NAMES=Path('translations/hodram_B49_speaker_name_review_v1.json')
NAMES=Path('translations/hodram_B49_speaker_name_review_v2.json')
PROOFS={
 'native_view':'work/analysis/Hodram_B49_native_review_v8397/native_body_review.json',
 'relocation':'work/analysis/Hodram_B49_relocation_v8398/reconstruction.json',
 'stored':'work/analysis/Hodram_B49_stored_v8399/stored_bodies.json',
 'controls':'work/analysis/Hodram_B49_controls_v8401d/stored_controls.json',
 'independent':'work/analysis/Hodram_B49_independent_v8402/independent_reconstruction.json',
 'reference':'work/analysis/Hodram_B49_reference_v8403/research_image_receipt.json',
 'references':'work/analysis/Hodram_B49_references_v8405b/references.json',
 'whole_actual':'work/analysis/Hodram_B49_actual_v8409/B49/paired_actual_dialogue_headers_flow_returns.json',
 'whole_view':'work/analysis/Hodram_B49_actual_review_v8412/selected_path_review.json',
 'tail_fixture':'work/analysis/Hodram_B49_tail_v8415/bounded_tail_fixtures.json',
 'tail_actual':'work/analysis/Hodram_B49_tail_actual_v8417/bounded_tail_actual.json',
 'menu_actual':'work/analysis/Hodram_B49_menu_actual_v8418/four_actual_menus12_full_owned_backing_andhighlight_samples.json',
 'FE_binding':'work/analysis/Hodram_B49_FE_binding_v8420/two_original_FE_paint_snapshots_four_exact_bitmap_palette_RGB_holds.json',
 'tail_comparison':'work/analysis/Hodram_B49_tail_comparison_v8421/both_bounded_tail_comparisons.json',
 'tail_differences':'work/analysis/Hodram_B49_tail_diff_view_v8422/sheet.json',
}

if __name__=='__main__':
    assert not ROOT.exists() and not DOC.exists() and not NAMES.exists();old,names=map(read,[OLD,OLD_NAMES]);data={k:read(p) for k,p in PROOFS.items()}
    assert data['native_view']['manuscript_sha256']==data['relocation']['manuscript_sha256']==sha(OLD.read_bytes())
    assert len(old['records'])==14 and len(old['typed_choice_records'])==2
    assert all(all(r['review'][g] for g in ['source','context','localization','naturalness']) and not r['review']['formatting'] for r in old['records']+old['typed_choice_records'])
    assert data['stored']['all14_ink_planes_exact_to_already_viewed'] and data['independent']['whole_target_block_andarchive_byte_equal_to_sparse_rebuild'] and data['references']['external_references_complete']
    assert not data['whole_actual']['unresolved'] and data['whole_view']['all_four_sheets_directly_viewed']
    assert not data['tail_actual']['unresolved'] and not data['menu_actual']['unresolved'] and data['tail_actual']['unique_tail_speeches']==8
    assert data['tail_actual']['actual_source_English_page_occurrences']==22 and data['tail_actual']['complete_body_name_orabsent_FE_header_holds']==134
    assert data['FE_binding']['all_actual_FE_typed_descriptors_palette_complete_bitmap_andphysical_RGB_match_independent_model'] and data['FE_binding']['focused_actual_frames']==9862
    sheets=[]
    for g in data['tail_actual']['groups']:sheets+=g['review_sheets']+g['transition_sheets']
    sheets+=[data['menu_actual']['review_sheet']]+data['tail_comparison']['review_sheets']+[data['tail_differences']['sheet']]
    assert len(sheets)==14
    for s in sheets:assert sha(Path(s['path']).read_bytes())==s['sha256']
    observed={r['id'] for g in data['whole_actual']['groups'] for r in g['speeches']}|{r['id'] for g in data['tail_actual']['groups'] for r in g['speeches']}
    assert observed=={r['id'] for r in old['records']}
    comp={g['choice']:g for g in data['tail_comparison']['groups']}
    assert comp['accept']['final_PRNG_seeds']==[996112413,155404999] and comp['decline']['final_PRNG_seeds']==[3478759668,3478759668]
    assert comp['accept']['later_RGB_difference_count']==3 and len(comp['accept']['later_RGB_comparisons'])==81
    assert comp['decline']['later_RGB_difference_count']==0 and len(comp['decline']['later_RGB_comparisons'])==69
    assert all(all(g['five_native_component_equality'].values()) and g['whole_actors_equal'] and not g['UI_request_differences'] for g in comp.values())
    doc=deepcopy(old);ng=deepcopy(names);mapping=data['relocation']['groups'][0]
    for row in doc['records']:
        ref=next(r for r in mapping['text_records'] if r['id']==row['id']);stored=next(r for r in data['stored']['records'] if r['id']==row['id'])
        assert row['compiled_hex']==ref['compiled_hex']==stored['compiled_hex']
        actual=[]
        for source,proof in [('whole-script-opening',data['whole_actual']),('bounded-possession-dialogue-tail',data['tail_actual'])]:
            for g in proof['groups']:
                for s in g['speeches']:
                    if s['id']==row['id']:
                        assert s['complete_holds'] and s['selected_capture'];actual.append(dict(scope=source,version=g['version'],choice=g.get('choice'),source_selector=s['source_selector'],selected_capture=s['selected_capture'],complete_holds=len(s['complete_holds']),name=s['name']))
        assert {a['version'] for a in actual}=={'clean_Japanese','revised_English'}
        row.update(final_reference=dict(file_path='/data/SC1.DK4',block=49,offset=ref['new_offset'],bytes=ref['new_length'],header_offset=ref['new_offset']-5,record_index=ref['new_record_index'],target_block_sha256=mapping['target_block_sha256']),final_hex=ref['target_hex'],stored_hex=ref['target_hex'],compiler_owned_parity_space=ref['parity_space_added'],actual_display_evidence=actual,formatting_approval_reason=row['native_body_review_reason']+' Complete stored-body planes remain exact after compiler parity handling;all original preambles/branches/controls andwhole source/current inverses pass. Actual source/English body/name-orabsent-FE-header masks andnormal flow pass in the explicitly scoped captures. No authored breaks,prose shortening,viewport/font changes,extra pages orQA waivers.',formatting_registered_release_pending=True)
        row['review']['formatting']=True
        row['formatting_stored_actual_choice_UI_policy_andregistered_release_pending']=False
        row['native_formatting_actual_UI_effects_andregistered_integration_pending']=False
        row['source_presentation_consumer_not_yet_approved']=False
        if row['source_record_index']==67:row['formatting_approval_reason']+=' The original leading CP932 ellipsis plusfollowing ASCII iscomplete inactual Hodram progressive display;it isnot replaced by ASCII dots orallowed globally.'
        if row['source_record_index']==81:row['formatting_approval_reason']+=' Fresh original FE paint CPU/WRAM/TCM objects bind228x48/288stride/6x12/16pitch,actual palette andbank-D VRAM;every held native inkpixel matchesRGB. This outgoing-wristband message remains distinct fromthe following original item148 acquisition UI.'
    menu=mapping['choice_commands'][0]
    for row,ref in zip(doc['typed_choice_records'],menu['label_references'],strict=True):
        assert row['id']==ref['id'] and row['english'].encode('ascii').hex()==ref['target_hex']
        row.update(compiled_hex=ref['target_hex'],compiled_bytes=ref['new_length'],final_hex=ref['target_hex'],final_reference=dict(file_path='/data/SC1.DK4',block=49,offset=ref['new_offset'],bytes=ref['new_length'],header_offset=menu['new_offset'],command_offset=menu['new_offset'],record_index=ref['new_record_index'],option_index=ref['option_index'],target_block_sha256=mapping['target_block_sha256']),native_menu_header_reference=dict(offset=menu['new_offset'],bytes=menu['new_length'],hex=menu['target_hex']),relative_table_field=ref['relative_table_field'],relative_base=ref['relative_base'],relative_offset=ref['relative_offset'],qa_waivers=[],qa_waiver_scope=[],formatting_approval_reason='Retain the reviewed short choice wording/order. Original2100 table,NULs/evenzeroalignment,getters,constructor60pxwidth/rectangle andstoredreferences pass. Fouractual menus/twelve held owned-caption backings/twenty-four complete visible labels match independent CP932/ASCII glyphs,bounds/backgrounds. Both input-selected highlights,original state2 indices0/1 andnormal dismissals/returnvalue carry areobserved. No authored padding or menu redesign.',current_body_not_contextually_approved=False,native_formatting_actual_UI_effects_andregistered_integration_pending=False,formatting_registered_release_pending=True)
        row['review']['formatting']=True
    for row in ng['records']:
        actor=row['actor_ID'];assert actor in [1,2] and row['decision']=='retention'
        row['review']['formatting']=True
        row.update(formatting_approval_reason='Retain the source-qualified approved identity andexisting consumer behavior. Exact source/current fields,progressive/full-name getters,complete native style11glyphs anddefault-name actor/code/font binding were preserved. Actual whole/ bounded-tail headers showcomplete '+('Hodram Bergstrom;the separate full-name getter retains Joakim.' if actor==1 else 'Lil Argot,including its final t.')+' No rank,relationship orbiography isadded;FE hasno actor254name. This isscoped default-name review,not completion ofall207actors/customnames.',actual_body_name_proofs=[PROOFS['whole_actual'],PROOFS['tail_actual']],registered_name_asset_change=False,no_new_name_asset_or207_catalogue_completion=True)
    ng.update(predecessor=str(OLD_NAMES),predecessor_sha256=sha(OLD_NAMES.read_bytes()),current_B49_name_header_context_binding_andformatting_pending=False,scoped_two_names_all_five_gates_true=True,all207_names_andcustom_name_risks_still_open=True,new_credit=0,full_goal_complete=False)
    ROOT.mkdir(parents=True);save(NAMES,ng)
    doc.update(predecessor_manuscript=str(OLD),predecessor_manuscript_sha256=sha(OLD.read_bytes()),names_packet=str(NAMES),names_packet_sha256=sha(NAMES.read_bytes()),formatting_review_pending=False,all16_formatting_gates_remain_false=False,typed_choice_UI_fullglyphs_geometry_backing_selection_stored_andactual_tests_pending=False,all16_individual_five_gates_true=True,all14_complete_preambles8_relative_sites_one_query_one_menu_opaque_effects_fullterminal_andtails_bound=True,source_current_final_references_complete=True,reference_ROM=data['reference']['research_ROM'],reference_ROM_sha256=data['reference']['research_ROM_sha256'],actual_display_source_andEnglish_all14_unique_speeches_andboth_menu_choices_observed_in_scoped_fixtures=True,actual_whole_script_frames=20002,actual_bounded_tail_frames=40004,actual_focused_FE_frames=9862,total_actual_frames=69868,actual_emulator_runs=8,whole_event_activation_original_location_earned_inventory_trade_mechanics_fullroute_hardware_andcustomnames_not_claimed=True,remaining_required_work='Frozen source-qualified natural-dialogue-v2 policy andmeaningful rejection cases,independent production/one-complete-ROM atomic commit,registered cumulative release/exact clean-input patch andown startup beforeonce-only16credit.',frozen_policy_atomic_andregistered_release_pending=True,no_new_ROM_registered_integration_orcompletion_credit=False,no_new_registered_ROM_orcompletion_credit=True,formatting_evidence={k:dict(path=p,sha256=sha(Path(p).read_bytes())) for k,p in PROOFS.items()},measured_timing_RNG_calendar_component_andRGB_limits_preserved=True,new_credit=0,full_goal_complete=False)
    assert [r['english'] for r in doc['records']+doc['typed_choice_records']]==[r['english'] for r in old['records']+old['typed_choice_records']]
    assert all(all(r['review'].values()) for r in doc['records']+doc['typed_choice_records'])
    save(DOC,doc)
    limits=dict(whole_script=read(PROOFS['whole_view']),bounded_tail_comparisons=data['tail_comparison'],direct_view_tail_accept_difference_findings=['5590:later original A-button prompt visibility differs.','6130:later original sailing-menu first-row highlight differs.','7750:later original Depart-menu first-row highlight differs.'],accept_no_original_script_boundary_RNG_difference_but_final_seed_differs=True,decline_twelve_original_script_boundary_RNG_differences_despite_equal_final_seed=True,no_future_random_outcome_broad_simulation_everyframe_causality_orhardware_equivalence_claim=True)
    save(ROOT/'formatting_approval.json',dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),predecessor=str(OLD),predecessor_sha256=sha(OLD.read_bytes()),names=str(NAMES),names_sha256=sha(NAMES.read_bytes()),individual_speech_approvals=14,individual_typed_choice_approvals=2,scoped_name_retentions=2,all16_five_gates_true=True,all_original_source_current_final_references_bound=True,directly_viewed_sheets=sheets,all14_sheets_directly_viewed=True,actual_unique_speech_IDs=sorted(observed),actual_tail_page_occurrences=22,actual_tail_complete_holds=134,actual_whole_script_frames=20002,actual_bounded_tail_frames=40004,actual_focused_FE_frames=9862,total_actual_frames=69868,actual_emulator_runs=8,complete_actual_menu_owned_backing12_samples24_visible_labels_both_highlights_andresults=True,FE_original_paint_two_snapshots_four_VRAM_palette_RGB_holds=True,mixed_source_ellipsis_plusEnglish_actual_page_pass=True,measured_limits=limits,registered_policy_atomic_build_patch_startup_andonceonly_credit_still_pending=True,no_prose_word_orcontrol_change_andzero_credit=True,new_credit=0,full_goal_complete=False,evidence={str(p):sha(p.read_bytes()) for p in [OLD,OLD_NAMES,*map(Path,PROOFS.values()),Path(__file__)]}))
    print('B49 formatting approved individually:14speeches+2choices/two scoped names;source/current/finalrefs complete.Allwords unchanged. Actual69868frames/8runs withalltiming/RNG/RGBlimits retained. Policy/atomic/registeredrelease pending;zero credit.')
