"""Record viewed pages, contextual names and all observed late-world differences."""
from copy import deepcopy
from pathlib import Path
from PIL import Image
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B223_English_review_v7109')
ACTUAL=Path('work/analysis/lil_B223_English_actual_v7108b/nine_English_objects_complete_pages_controls_return_and_later_scope.json')
OLD_NAMES=Path('translations/lil_B223_speaker_name_review_v1.json')
NEW_NAMES=Path('translations/lil_B223_speaker_name_review_v2.json')
if __name__=='__main__':
    assert not ROOT.exists() and not NEW_NAMES.exists()
    a=read(ACTUAL);source=read(a['source_actual_proof'])
    assert (a['actual_unique_objects'],a['actual_progressive_objects'],a['actual_automatic_style_objects'],a['actual_native_pages'],a['complete_body_holds'],a['complete_name_holds'])==(9,8,1,11,37,37)
    assert not a['failures'] and not a['incomplete_progressive_holds'] and not a['command_result_differences'] and not a['command_UI_word_differences'] and not a['source_command_offsets_not_observed_in_English']
    assert len(a['command_pairs'])==27 and len(a['offline_only_object_IDs'])==8 and a['offline_only_speech_IDs']==['DK4_MES_B223_R0067','DK4_MES_B223_R0070']
    assert a['actual_predicate_type2_Boolean_values']==[0] and a['normal_end_result']==[0,0] and (a['source_exit_frame'],a['English_exit_frame'],a['normal_English_port_sample_frame'])==(5253,5496,5590)
    assert len(a['semantic_upper_scene_portrait_pairs'])==9 and all(p['upper_scene_portrait_equal'] and p['portrait_only_equal'] for p in a['semantic_upper_scene_portrait_pairs'])
    assert [(p['id'],p['last_complete_previous_frame'],p['first_complete_next_frame'],p['original_A_inputs_in_interval'][0]['start']) for p in a['page_transitions']]==[('DK4_MES_B223_R0031',3550,3610,3560),('DK4_MES_B223_R0040',4510,4570,4520)]
    sheets=a['review_sheets']+[a['transition_sheet'],a['later_pair_sheet']]
    assert len(sheets)==4
    for s in sheets:assert sha(Path(s['path']).read_bytes())==s['sha256']
    # Every enlarged body pane in the two viewed sheets is exactly its saved whole frame.
    pages=[(p['id'],page) for p in a['actual_panels'] for page in p['pages']]
    for i,(_,page) in enumerate(pages):
        p=page['selected_complete_capture'];assert sha(Path(p['capture']).read_bytes())==p['sha256']
        sheet=Image.open(a['review_sheets'][i//6]['path']).convert('RGB');x,y=i%3*520+4,(i%6)//3*416+24
        expected=Image.open(p['capture']).convert('RGB').crop((0,192,256,384)).resize((512,384),Image.Resampling.NEAREST)
        assert sheet.crop((x,y,x+512,y+384)).tobytes()==expected.tobytes()
    assert a['captain_IDs']==[0,2] and not a['captain_IDs_equal'] and not a['whole_actor_and_captain_equal']
    assert a['final_PRNG_seeds']==[646626623,1613831355] and not any(a['five_native_component_equality'].values())
    assert [len(a[k]) for k in ['command_timing_differences','command_RNG_differences','command_duration_changes','upper_same_frame_region_differences','scene_same_frame_RGB_differences','later_same_frame_RGB_differences']]==[14,14,5,8,44,175]
    assert not a['unreturned_following_dialogues_at_capture_end'] and len(source['unreturned_following_dialogues_at_capture_end'])==1
    old=read(OLD_NAMES);names=deepcopy(old)
    for r in names['records']:
        actor=r['actor_ID'];assert actor in [2,13,21]
        observed=actor in [2,21];panels=[p for p in a['actual_panels'] if p['source_selector']==actor]
        assert bool(panels)==observed and all(all(p['complete_name_holds']) for p in panels)
        r.update(actual_English_headers_to_recheck=False,actual_English_header_observed=observed,actual_English_complete_header_holds=sum(len(p['complete_name_holds']) for p in panels),actual_English_header_offline_only=not observed)
        r['formatting_reason']+=' English scene: complete original header glyphs and blank guards match independently on every held page.' if observed else ' Cesare is unvisited in both actual fixtures; complete source-owned progressive/full getters and the style11 name plane remain offline evidence.'
    names.update(previous_review=str(OLD_NAMES),previous_review_sha256=sha(OLD_NAMES.read_bytes()),actual_English_proof=str(ACTUAL),actual_English_proof_sha256=sha(ACTUAL.read_bytes()),actual_English_Ian_and_Lil_headers_complete=True,Cesare_conditional_header_unvisited=True,full_catalogue_UI_unvisited=True,new_name_or_dialogue_credit=0,full_goal_complete=False)
    ROOT.mkdir(parents=True);save(NEW_NAMES,names)
    later=dict(actual_proof=str(ACTUAL),actual_proof_sha256=sha(ACTUAL.read_bytes()),source_actual_proof=a['source_actual_proof'],source_actual_proof_sha256=a['source_actual_proof_sha256'],final_native_values=a['final_native_values'],five_native_component_equality=a['five_native_component_equality'],captain_IDs=a['captain_IDs'],final_PRNG_seeds=a['final_PRNG_seeds'],source_English_scene_exits=[5253,5496],command_timing_differences=a['command_timing_differences'],command_RNG_differences=a['command_RNG_differences'],command_duration_changes=a['command_duration_changes'],all_later_same_frame_RGB_differences=a['later_same_frame_RGB_differences'],source_following_commands=a['source_following_commands'],English_following_commands=a['following_commands'],source_open_following_dialogues=source['unreturned_following_dialogues_at_capture_end'],English_open_following_dialogues=a['unreturned_following_dialogues_at_capture_end'],source_SC0_B44_open_English_only_SC2_B120_observed=True,final_source_Claudio_scene_and_English_sea_view_viewed=True,no_boot_replay_or_original_getter_change=True,no_RAM_role_roster_condition_RNG_result_or_input_timing_forced=True,no_full_RAM_future_sequence_broad_simulation_or_complete_causal_claim=True,all_measured_differences_retained_for_later_older_record_technical_reaudit=True,new_credit=0,full_goal_complete=False)
    save(ROOT/'all_measured_later_values_and_cross_route_limits.json',later)
    save(ROOT/'eleven_English_pages37_body37_name_holds_signature_and_limits_viewed.json',dict(actual_proof=str(ACTUAL),actual_proof_sha256=sha(ACTUAL.read_bytes()),viewed_sheets=sheets,all_four_sheets_individually_returned_and_viewed=True,all11_sheet_panes_pixel_equal_whole_frame_crops=True,all11_pages37_body37_name_holds_complete=True,full_Ian_Dukov_signature_and_two_original_A_page_advances_viewed=True,no_missing_clipped_duplicate_or_extra_blank_page_observed=True,actual_eight_speeches_one_style4_notice_two_conditional_speeches_six_styles_offline=True,all_nine_semantic_scene_and_portrait_pairs_equal=True,all27_observed_original_results_UI_words_and_normal_return_equal=True,later_captain0_2_and_all_world_differences_retained=True,Cesare_actual_header_and_full_catalogue_UI_unvisited=True,actor151_Sailor_Retainer_and_full207_name_review_open=True,speaker_name_review=str(NEW_NAMES),speaker_name_review_sha256=sha(NEW_NAMES.read_bytes()),visual_review_pending=False,new_credit=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('Viewed11 English pages/37 body37 headers,full Ian signature,two native A advances and all late-world differences. Lil/Ian actual;Cesare offline. Zero new credits.')
