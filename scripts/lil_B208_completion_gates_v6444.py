"""Require actual B208 release, native display, measured differences and startup evidence."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read
ROOT=Path('work/analysis')
RELEASE=ROOT/'lil_B208_release_v6440/registered_release_verification.json'
START=ROOT/'lil_B208_startup_v6443/cold_boot_Lil_startup_town_verification.json'
VIEW=START.parent/'current_six_frame_visual_review.json'
REG=ROOT/'lil_B208_registration_v6438/registration_receipt.json'
PIN=ROOT/'lil_B208_retention_v6441/pin_receipt.json'
ACTUAL=ROOT/'lil_B208_actual_v6431/all24_English_panels_complete_native_holds38_commands_and_source_comparison.json'
TRANSITIONS=ROOT/'lil_B208_actual_review_v6433/viewed24_panels95_holds_thought_FE_and_honest_broader_later_scope.json'
def gates():
    release,start,view,reg,actual,transitions=map(read,[RELEASE,START,VIEW,REG,ACTUAL,TRANSITIONS])
    assert release['all599_manifest_batches_and114_accepted_layers_present'] and release['all18_registered_release_checks_pass'] and release['whole_ROM_reconstruction_byte_exact'] and release['every_other_file_font_graphic_route_ARM9_ARM7_and_component_exact_to_V6380']
    assert start['all_current_requested_and_final_framebuffers_equal_V6380'] and start['paired_frame_count']==31 and start['all_five_postload_actor_model_and_captain_checks_equal'] and start['source_and_disposable_town_donor_unchanged']
    assert view['viewed'] and view['sha256']==start['review_sheet_sha256']==sha(Path(view['sheet']).read_bytes())
    assert reg['negative_count']==89 and reg['all_negatives_reject_before_mutation'] and read(PIN)['all_prior_pins_preserved']
    assert (actual['actual_unique_speech_panels'],actual['actual_English_speech_observations'],actual['complete_native_text_and_nameplate_holds'])==(24,24,95)
    assert not any(actual[k] for k in ['failures','paired_nontext_region_differences','command_result_differences','command_UI_word_differences','offline_only_display_IDs'])
    assert actual['source_and_English_all38_commands29_source_plus9_initializers_observed'] and actual['all_command_paths_and_results_preserved'] and actual['all_jobs_terminal_and_reaped']
    assert transitions['no_open_translation_specific_display_control_or_return_finding'] and not transitions['visual_review_pending'] and len(transitions['viewed_sheets'])==6
    assert [len(actual[k]) for k in ['command_timing_differences','command_RNG_differences','later_whole_RGB_differences']]==[16,18,44]
    state=read(transitions['postscene_native_state_proof']);assert sha(Path(transitions['postscene_native_state_proof']).read_bytes())==transitions['postscene_native_state_proof_sha256']
    assert state['five_native_component_equality']==dict(state=True,models=False,persistent_objects=False,tasks=True,calendar=False)
    assert not state['whole_actor_and_captain_equal'] and not state['final_PRNG_equal'] and state['final_PRNG_seeds']==[4024327688,3039668243]
    assert len(state['command_duration_changes'])==8 and not state['prompt_bounded_later_differences'] and len(state['broader_later_differences'])==44
    assert transitions['all16_timing18_RNG44_broader_RGB_eight_duration_and_different_final_state_witnesses_retained'] and transitions['broad_postscene_full_RAM_future_world_equivalence_unproven'] and transitions['natural_event208_original_location_earned_progress_full_effect_semantics_routes_and_hardware_unclaimed'] and transitions['final16001_both_sailing_viewed']
    assert [transitions[k] for k in ['source_exit_frame','English_exit_frame','normal_port_return_frame','following_B120_end_frame']]==[8616,8616,8710,13414]
    assert transitions['all91_progressive_name_holds_and4_portraitless_named_FE_notice_holds_complete'] and transitions['private_thought_parentheses_and_separate_Cristina_Charm_plus1_FE_notice_preserved']
    tests=read(ROOT/'lil_B208_regressions_v6439/terminal.json');assert tests['terminal'] and tests['returncode']==0 and sha(Path(tests['log']).read_bytes())==tests['log_sha256'] and '110 passed' in Path(tests['log']).read_text('utf-8')
    for key in ['candidate','patch']:assert sha(Path(release[key]).read_bytes())==release[key+'_sha256']
    assert release['candidate_sha256']==start['candidate_sha256']==sha(Path(release['exact_patch_reconstruction']).read_bytes())==sha(Path('out/lil_B208_reference_v6424_RESEARCH_ONLY.nds').read_bytes())
    registry=read('translations/release_stack.json');manifest=read(release['manifest']);assert len(manifest['batches'])==599 and len(manifest['checks'])==18 and all(manifest['checks'].values()) and len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v4701'
    return release
