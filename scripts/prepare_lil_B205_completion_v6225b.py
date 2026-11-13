"""Prepare exactly-once17-record completion with a complete inverse of all earlier ledger history."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B205_completion_tools_v6225')
GATES='''def gates():
    release,start,view,reg,actual,transitions=map(read,[RELEASE,START,VIEW,REG,ACTUAL,TRANSITIONS])
    assert release['all594_manifest_batches_and114_accepted_layers_present'] and release['all18_registered_release_checks_pass'] and release['whole_ROM_reconstruction_byte_exact'] and release['every_other_file_font_graphic_route_ARM9_ARM7_and_component_exact_to_V6160']
    assert start['all_current_requested_and_final_framebuffers_equal_V6160'] and start['paired_frame_count']==31 and start['all_five_postload_actor_model_and_captain_checks_equal'] and start['source_and_disposable_town_donor_unchanged']
    assert view['viewed'] and view['sha256']==start['review_sheet_sha256']==sha(Path(view['sheet']).read_bytes())
    assert reg['negative_count']==78 and reg['all_negatives_reject_before_mutation'] and read(PIN)['all_prior_pins_preserved']
    assert (actual['actual_unique_speech_panels'],actual['complete_matching_observations'],actual['complete_matching_holds'])==(17,17,63) and not actual['failures'] and not actual['offline_only_display_IDs']
    assert actual['all34_commands25_source_plus9_initializers_and_seven_FE_objects_observed'] and actual['original_command_paths_results_and_complete_end_preserved']
    assert transitions['no_open_translation_specific_display_control_or_return_finding'] and not transitions['visual_review_pending'] and len(transitions['viewed_sheets'])==5
    state=read(transitions['measured_state_proof']);assert sha(Path(transitions['measured_state_proof']).read_bytes())==transitions['measured_state_proof_sha256']
    assert state['source_exit_frame']==state['English_exit_frame']==7175 and state['later_whole_RGB_equal_samples']==98 and not state['later_source_English_RGB_differences']
    assert all(state['native_final_component_equality'].values()) and state['whole_actor_and_captain_equal'] and state['final_PRNG_equal'] and state['no_whole_state_or_future_sequence_equivalence_claim']
    assert not actual['source_English_command_timing_differences'] and not actual['source_English_command_RNG_differences'] and state['generated_Rainbow_Parrot_notice_same_frame_whole_RGB_equal_at7150']
    tests=read('work/analysis/lil_B205_regressions_v6220/terminal.json');assert tests['terminal'] and tests['returncode']==0 and sha(Path(tests['log']).read_bytes())==tests['log_sha256'] and '110 passed' in Path(tests['log']).read_text('utf-8')
    for key in ['candidate','patch']:assert sha(Path(release[key]).read_bytes())==release[key+'_sha256']
    assert release['candidate_sha256']==start['candidate_sha256']==sha(Path(release['exact_patch_reconstruction']).read_bytes())==sha(Path('out/lil_B205_reference_v6203_RESEARCH_ONLY.nds').read_bytes())
    registry=read('translations/release_stack.json');manifest=read(release['manifest']);assert len(manifest['batches'])==594 and len(manifest['checks'])==18 and all(manifest['checks'].values()) and len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v4701'
    return release
'''
if __name__=='__main__':
    assert not ROOT.exists();old=Path('scripts/complete_lil_B204_v6165b.py').read_text(encoding='utf-8');a=old.index('def gates():');b=old.index('\ndef restore',a);family=next(l for l in old.splitlines() if l.startswith('FAMILY='))
    tool=derive('scripts/complete_lil_B204_v6165b.py','scripts/complete_lil_B205_v6225.py',{
        old[a:b]:GATES,family:"FAMILY='Lil-B205-parrot-five-mimicry-echoes-two-sounds-catch-and-victory-joke17'",
        'B204':'B205','B205':'B206','lil_B204_completion_text_v6165':'lil_B205_completion_text_v6225','completion_v6165':'completion_v6225','verification_v6166':'verification_v6226','V6165':'V6225','V6160':'V6220',
        'manuscript_v8':'manuscript_v7','release_v6161':'release_v6221','startup_v6163':'startup_v6223','actual_v6146/all20_actual_English_panels_complete_native_holds_two_source_scopes_and_return':'actual_v6211/all17_actual_English_panels_complete_native_holds_source_comparison_and_return','actual_review_v6147/viewed20_panels_four_letters_complete_return_and_honest_scope':'actual_review_v6212/viewed17_panels_five_echoes_two_sounds_complete_return_and_honest_scope','verification_v6134':'verification_v6198','registration_v6151':'registration_v6217','retention_v6164':'retention_v6224','regressions_v6160':'regressions_v6220',
        'blocks[204]':'blocks[205]','blocks=[204]':'blocks=[205]','block=204':'block=205','block=205':'block=206','event204':'event205','source204':'source205',
        '[-20:]':'[-17:]','==20':'==17','added_once=20':'added_once=17','records=20':'records=17','completed_objects=20':'completed_objects=17','speeches=20':'speeches=17','observations=20':'observations=17','credit_added=20':'credit_added=17','records=20':'records=17','all20':'all17','exactly20':'exactly17','20 disjoint':'17 disjoint','20 reviews':'17 reviews','and20 ':'and17 ',
        "{'revise':12,'retain-wording':8}":"{'revise':8,'retain-wording':9}",'revised=12,retained=8':'revised=8,retained=9','revised_count=12,retained_count=8,fresh_revisions=12,fresh_retentions=8':'revised_count=8,retained_count=9,fresh_revisions=8,fresh_retentions=9','new_revisions=12,justified_retentions=8':'new_revisions=8,justified_retentions=9',
        '6350':'6370','6370':'6387','6373':'6390','3981':'3989','2389':'2398','4464':'4484','4484':'4501','4770':'4787','593':'594','holds=77':'holds=63',
        'goal_turn_new_frames=34403':'goal_turn_new_frames=47404','goal_turn_new_emulator_runs=3':'goal_turn_new_emulator_runs=4','new_English_content_fixture_runs=1':'new_English_content_fixture_runs=1,new_Japanese_content_fixture_runs=1','reused_prior_Japanese_frames=13001,current_same_code_prefix_from8420_frame_menu_run=True':'new_Japanese_frames=13001,no_separate_older_cross_build_baseline=True','reused_prior_source_frames=13001':'reused_prior_source_frames=0',
        'unfinished_editorial_scope_v6133':'unfinished_editorial_scope_v6197','all26_source_commands_and9_initializers_observed':'all25_source_commands_and9_initializers_observed','all26_commands20_preambles6_leaves_and_original_results_preserved':'all25_commands17_preambles8_leaves_and_original_results_preserved',
        'no_B204_actor_macro_letter_count_effect_or_end_assumptions_inherited':'no_B205_actor_macro_echo_sound_count_effect_or_end_assumptions_inherited',
        'startup31_frames_and_five_actor_controls_match_V6110':'startup31_frames_and_five_actor_controls_match_V6160','measured_timing_RNG_later_RGB_and_state_differences_retained':'measured_equal_timing_RNG98_later_RGB_and_bounded_state_scope_preserved',
        'Stage,audit,apply and verify20':'Stage,audit,apply and verify17','source_prose_and_completed_records=True':'source_prose_and_completed_records=True',
    })
    pin=derive('scripts/pin_lil_B204_v6164.py','scripts/pin_lil_B205_v6224.py',{'B204':'B205','retention_v6164':'retention_v6224','release_v6161':'release_v6221','V6160':'V6220'})
    binding=derive('scripts/bind_current_V6160_native_v6168.py','scripts/bind_current_V6220_native_v6228.py',{'V6160':'V6220','native_v6168':'native_v6228','verification_v6166':'verification_v6226','lil_B204_release_v6161':'lil_B205_release_v6221','lil_B204_runs_v6162':'lil_B205_runs_v6222','not_B205_or_any_later_event_activation':'not_B206_or_any_later_event_activation'})
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_completion_retention_and_future_context_tools.json',dict(completion=tool,retention=pin,current_native_binding=binding,all_history_inverse_and_exactly_once_disjoint_key_guards_preserved=True,completed_before=6370,completed_after=6387,source_prose_after=6390,revised_after=3989,retained_after=2398,source_objects=17,new_emulator_jobs=4,new_frames=47404,no_shared_mutation_yet=True,full_goal_complete=False));print('B205 completion/pinning/next-native-context tools prepared. No credit before all release/startup gates;full goal/history remain intact.')
