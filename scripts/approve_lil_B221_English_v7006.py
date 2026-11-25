"""Approve complete B221 speech/choice display after native masks and explicit source/English views."""
from collections import Counter
from copy import deepcopy
from pathlib import Path
from PIL import Image
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.dialogue.lil_B221_profile_v1 import contract,profile_for
from dk4tool.dialogue.lil_B221_layout_v1 import encode_relocatable_dialogue,audit_relocatable_dialogue_record
from dk4tool.dialogue.lil_B221_choices_v1 import compile_choices
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B221_English_approval_v7006')
OLD=Path('translations/lil_B221_editorial_manuscript_v1.json');NEW=Path('translations/lil_B221_editorial_manuscript_v2.json')
OLD_CHOICE=Path('translations/lil_B221_choice_manuscript_v1.json');NEW_CHOICE=Path('translations/lil_B221_choice_manuscript_v2.json')
OLD_NAME=Path('translations/lil_B221_speaker_name_review_v1.json');NEW_NAME=Path('translations/lil_B221_speaker_name_review_v2.json')
ACTUAL=Path('work/analysis/lil_B221_English_actual_v7004/two_English_choices_all14_speeches30_native_pages_complete_masks_and_source_differences.json')
LATER=Path('work/analysis/lil_B221_later_v7005/both_choices_final_components_and_measured_timing_RNG_RGB_limits.json')
STORED=Path('work/analysis/lil_B221_stored_v6995/all14_final_stored_targets56_alignments16_complete_pages.json')
POLICY=Path('work/analysis/lil_B221_policy_validation_v6993b/fourteen_paragraphs_one_typed_menu36_distinct_rejections_seven_row_reasons.json')

if __name__=='__main__':
    assert not ROOT.exists() and all(not p.exists() for p in [NEW,NEW_CHOICE,NEW_NAME])
    actual,later=map(read,[ACTUAL,LATER])
    assert not actual['failures'] and actual['actual_unique_speeches']==14 and actual['actual_speech_observations']==26
    assert actual['actual_complete_native_page_observations']==30
    assert actual['actual_complete_body_holds']==actual['actual_complete_name_holds']==118
    assert actual['all30_stored_commands_executed_in_union'] and actual['all_jobs_terminal_and_reaped']
    assert later['actual_proof_sha256']==sha(ACTUAL.read_bytes()) and later['all_measured_differences_retained_for_later_older_record_technical_reaudit']
    images=[];checks=[];namecounts=Counter();panels={};transitions=[]
    for version in actual['versions']:
        choice=version['selected_original_option'];images.extend(version['review_sheets']+[version['transition_sheet']])
        assert version['normal_terminal_result']==[0,choice] and version['exit_frame']==6693 and version['normal_port_sample_frame']==6790
        assert len(version['actual_menu']['holds'])==[4,2][choice]
        flattened=[]
        for panel in version['actual_panels']:
            assert not panel['partial_or_transition_holds']
            assert all(p['upper_scene_RGB_equal'] and p['portrait_RGB_equal'] for p in panel['semantic_source_scene_portrait_pairs'])
            panels.setdefault(panel['id'],[]).append(dict(choice=choice,panel=panel))
            namecounts[panel['source_selector']]+=len(panel['complete_name_holds'])
            for index,holds in enumerate(panel['actual_complete_page_holds']):
                assert holds;flattened.append((panel['id'],index+1,holds[-1]))
            for item in panel['ordinary_page_transitions']:
                transitions.append(dict(choice=choice,id=panel['id'],**item))
        assert len(flattened)==15
        for index,(ident,page,photo) in enumerate(flattened):
            spec=version['review_sheets'][index//6]
            sheet=Image.open(spec['path']).convert('RGB');full=Image.open(photo['capture']).convert('RGB')
            assert sha(Path(photo['capture']).read_bytes())==photo['sha256']
            pane=full.crop((0,192,256,384)).resize((512,384),Image.Resampling.NEAREST)
            cell=index%6;x=cell%3*520+4;y=cell//3*416+24
            assert sheet.crop((x,y,x+512,y+384)).tobytes()==pane.tobytes()
            checks.append(dict(choice=choice,id=ident,page=page,frame=photo['frame'],full_capture=photo['capture'],full_capture_sha256=photo['sha256'],complete_overview_pane_RGB_equal=True))
    assert len(images)==8 and len(checks)==30 and len(transitions)==4
    assert namecounts=={2:32,17:48,85:38}
    for spec in images:assert sha(Path(spec['path']).read_bytes())==spec['sha256']
    full=Path('E:/Rota Nova translations/Generated/work/emulation_v193/lil_B221_English_v7002/frame_005950_cold_boot.png')
    images.append(dict(path=str(full),sha256=sha(full.read_bytes()),scope='Individually viewed full frame5950 resolves apparent wide-sheet first-letter clipping;the complete He is present.'))
    ROOT.mkdir(parents=True)
    view=ROOT/'fourteen_speeches_both_options_thirty_pages_headers_and_normal_returns_viewed.json'
    save(view,dict(actual_proof=str(ACTUAL),actual_proof_sha256=sha(ACTUAL.read_bytes()),later_proof=str(LATER),later_proof_sha256=sha(LATER.read_bytes()),
        viewed_images=images,all8_English_sheets_individually_returned_and_viewed=True,
        all30_complete_overview_panes_equal_original_crops=checks,ordinary_page_transitions=transitions,
        all14_complete_English_speeches_and_both_choices_viewed=True,
        all118_complete_native_body_and_current_name_holds_and_portraits_pass=True,
        all4_two_page_progressions_use_ordinary_A4760_and_A5960=True,
        Yes0_R27_No1_R33_complete_menu_masks_and_visible_highlights_pass=True,
        normal_ends0_0_and0_1_at6693_both_Amsterdam_ports6790_viewed=True,
        no_missing_leading_internal_final_letters_unintended_pages_blank_pages_or_bad_scene_transitions_observed=True,
        seven_specific_row_reasons25_ordinary_boundaries_and_R67_had_gone_reason_preserved=True,
        original_QA_diagnostics_no_warning_error_or_global_waiver=True,
        all_source_English_command_results_and_UI_words_equal=True,
        both_final_source_English_frames_viewed_all_later_differences_preserved=True,
        later_frame6790_source_Depart_menu_versus_English_port_and16001_English_food_notice_are_measured_schedule_differences=True,
        no_full_RAM_future_sequence_broad_simulation_or_complete_causal_equivalence_claim=True,
        Square_Shopkeeper_current_rendering_not_natural_label_approval=True,
        full_catalogue_UI_unvisited=True,initialized_fixture_not_natural_event_progress_or_full_route=True,
        visual_review_pending=False,new_credit=0,full_goal_complete=False))
    doc=deepcopy(read(OLD));c=contract();image=NdsImage.open(doc['current_ROM']);arm=image.read_file('/__arm9__.bin')
    block=IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks[221];stored=read(STORED)
    for row in doc['records']:
        ident=row['id'];binding=c['record_bindings'][ident];profile=profile_for(arm,block,ident)
        encoded=encode_relocatable_dialogue(bytes.fromhex(row['source_hex']),row['english'],profile)
        qa=audit_relocatable_dialogue_record(bytes.fromhex(row['source_hex']),row['english'],profile)
        observed=panels[ident]
        assert encoded.encoded.hex()==binding['compiled_hex']
        assert all(p['panel']['native_pages']==binding['native_page_count'] for p in observed)
        row.update(compiled_hex=encoded.encoded.hex(),formatted_markup=encoded.formatted_markup,
            native_profile_maximum_total_rows=binding['maximum_total_rows'],original_physical_native_rows_per_page=4,
            native_page_count=binding['native_page_count'],qa_waivers=[],qa_waiver_reason=None,
            informational_row_count_reason=binding['row_count_reason'],base_QA_report=qa,
            reviewed_ordinary_boundaries=binding['ordinary_wrap_reasons'],reviewed_short_complete_sentence_openings=[],
            reviewed_native_page_boundary=binding['page_boundary_reason'],actual_record_observed=True,
            actual_complete_body_holds=sum(len(h) for p in observed for h in p['panel']['actual_complete_page_holds']),
            actual_complete_name_holds=sum(len(p['panel']['complete_name_holds']) for p in observed),
            actual_observed_choice_paths=[p['choice'] for p in observed],
            native_plane_verified_not_actual_English_gameplay=False,current_complete_native_display_pending=False,
            speaker_label_wider_localization_review_open=row['source_selector']==85,
            formatting_reason='All logical/compiled/final-stored native pages and actual complete English black/gray/body/current-name holds pass. The fourteen source preambles,voices3/4/0,zero macros,one two-choice menu,four relatives,A000 and full normal end are preserved. Only R46/R60 use two original four-row pages,with ordinary A advancement. All seven informational row reasons,25 ordinary boundaries and the exact R67 had/gone reason retain every original QA diagnostic. Current Square Shopkeeper rendering is preservation,not a new natural-label approval. Measured later-world differences and initialized-fixture limits remain explicit. Registered release/patch/startup remain pending.')
        row['review']['formatting']=True
    doc['historical_all14_four_prose_gates_true_formatting_false']=doc.pop('all14_four_prose_gates_true_formatting_false')
    name=deepcopy(read(OLD_NAME))
    for row in name['records']:
        ident=row['actor_ID'];row['technical_current_complete_name_holds']=namecounts[ident]
        row['current_name_glyph_planes_and_actual_headers_complete']=True
        row['native_complete_name_planes_and_actual_headers_pending']=False
        if ident in [2,17]:row['review']['formatting']=True
        else:
            assert row['review']['naturalness'] is False
            row['technical_preservation_not_natural_label_or_target_Shopkeeper_approval']=True
    name.update(previous_name_review=str(OLD_NAME),previous_name_review_sha256=sha(OLD_NAME.read_bytes()),
        actual_English_proof=str(ACTUAL),actual_English_proof_sha256=sha(ACTUAL.read_bytes()),
        two_contextual_personal_name_retention_forms_approved=True,
        actor85_wider_ten_role_Shopkeeper_layer_still_pending=True,
        full_catalogue_UI_unvisited=True,no_name_asset_change_or_duplicate_credit=True)
    save(NEW_NAME,name)
    shared=dict(previous_manuscript=str(OLD),previous_manuscript_sha256=sha(OLD.read_bytes()),
        actual_English_proof=str(ACTUAL),actual_English_proof_sha256=sha(ACTUAL.read_bytes()),
        actual_English_view=str(view),actual_English_view_sha256=sha(view.read_bytes()),
        actual_source_proof=actual['source_actual_proof'],actual_source_proof_sha256=actual['source_actual_proof_sha256'],
        native_font_proof='work/analysis/lil_B221_native_pages_v6980c/all14_paragraphs16_complete_native_pages112_alignments.json',
        native_stored_proof=str(STORED),native_stored_proof_sha256=sha(STORED.read_bytes()),
        native_name_proof='work/analysis/lil_B221_name_planes_v6981/three_actors_six_getters_nine_name_component_planes36_alignments.json',
        relocated_control_proof='work/analysis/lil_B221_relocated_controls_v7000b/all14_final_dispatches_A00025_normal_seeded_ends_four_relatives_one_menu.json',
        policy_validation=str(POLICY),policy_validation_sha256=sha(POLICY.read_bytes()),
        later_scope_proof=str(LATER),later_scope_proof_sha256=sha(LATER.read_bytes()),
        speaker_name_review=str(NEW_NAME),speaker_name_review_sha256=sha(NEW_NAME.read_bytes()),
        formatting_review_pending=False,all16_speech_choice_formatting_gates_true=True,
        status='complete contextual/native/actual review;sealed references and registered release pending')
    doc.update(shared);save(NEW,doc)
    choices=deepcopy(read(OLD_CHOICE));target=compile_choices(choices['records'])
    refs=read('work/analysis/lil_B221_relocation_v6994/all16_objects21_commands_four_relatives_full1208_inverse_RESEARCH.json')['blocks'][0]['choice_commands'][0]
    for row in choices['records']:
        row.update(typed_target_object_hex=target.hex(),source_count=2,native_indices_and_original_return_values_preserved=True,
            actual_observed_choice_paths=[0,1],actual_menu_mask_holds=[4,2],current_complete_native_display_pending=False,
            formatting_reason='The final complete14-byte menu,all source/current references and both even-alignment label pointers pass. Yes/No remain original indices0/1. Nine isolated VM cases and twelve style planes are separate from actual visible labels/highlights and both unforced branches. Final stored command126 and label offsets132/136 are exact;registered integration remains pending.')
        row['historical_choice_getter_layout_branch_pending']=row.pop('native_choice_getter_layout_result_and_branch_binding_pending')
        row['native_choice_getter_layout_result_and_branch_binding_pending']=False
        row['review']['formatting']=True
    assert refs['new_offset']==126 and [r['new_offset'] for r in refs['label_references']]==[132,136]
    choices.update(shared);choices['previous_manuscript']=str(OLD_CHOICE);choices['previous_manuscript_sha256']=sha(OLD_CHOICE.read_bytes())
    choices['historical_original_indices_branch_mapping_cancel_and_native_display_pending']=choices.pop('original_indices_branch_mapping_cancel_and_native_display_pending')
    choices['original_indices_branch_mapping_cancel_and_native_display_pending']=False
    save(NEW_CHOICE,choices)
    assert all(all(r['review'].values()) for r in doc['records']+choices['records'])
    save(ROOT/'all16_five_gates_approved_registered_release_pending.json',dict(manuscript=str(NEW),manuscript_sha256=sha(NEW.read_bytes()),
        choice_manuscript=str(NEW_CHOICE),choice_manuscript_sha256=sha(NEW_CHOICE.read_bytes()),
        speaker_name_review=str(NEW_NAME),speaker_name_review_sha256=sha(NEW_NAME.read_bytes()),
        actual_view=str(view),actual_view_sha256=sha(view.read_bytes()),all16_five_gates_approved=True,
        all_source_native_actual_and_later_limits_preserved=True,new_review_credit=0,full_goal_complete=False))
    print('14 speeches/two labels approved through all five gates. Both page/choice paths and normal returns viewed;Shopkeeper layer and registered release pending.')
