"""Require registered integration, exact patch, regressions and viewed startup."""
from pathlib import Path
from dk4tool.patch import lil_B221_editorial_v1 as story
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read
ROOT=Path('work/analysis')

def gates():
    release=read(ROOT/'lil_B221_release_v7012/registered_release_verification.json')
    start=read(ROOT/'lil_B221_startup_v7015/cold_boot_Lil_startup_town_verification.json')
    view=read(ROOT/'lil_B221_startup_v7015/current_six_frame_visual_review.json')
    reg=read(ROOT/'lil_B221_registration_v7010/registration_receipt.json');conf=read(story.CONFIG)
    doc,menu=[read(conf[k]) for k in ['manuscript','choice_manuscript']];seal=read(doc['reference_approval'])
    assert seal['all16_five_gates_and_exact_references_approved']
    for k in ['manuscript','choice_manuscript']:assert seal[k+'_sha256']==sha(Path(conf[k]).read_bytes())
    assert len(doc['records'])==14 and len(menu['records'])==2 and all(all(r['review'].values()) for r in doc['records']+menu['records'])
    assert release['all613_manifest_batches_and114_accepted_layers_present'] and release['all18_registered_release_checks_pass']
    assert release['whole_ROM_reconstruction_byte_exact'] and release['every_other_file_font_graphic_route_ARM9_ARM7_and_component_exact_to_V6956']
    assert release['all_earlier_profiles_and_V4701_promotion_unchanged']
    assert start['all_current_requested_and_final_framebuffers_equal_V6956'] and start['paired_frame_count']==31
    assert start['all_five_postload_actor_model_and_captain_checks_equal'] and start['source_and_disposable_town_donor_unchanged']
    assert view['viewed'] and view['sha256']==start['review_sheet_sha256']==sha(Path(view['sheet']).read_bytes())
    assert reg['negative_count']==46 and reg['all_negatives_reject_before_mutation']
    assert read(ROOT/'lil_B221_retention_v7013/pin_receipt.json')['all_prior_pins_preserved']
    tests=read(ROOT/'lil_B221_regressions_v7011/terminal.json')
    assert tests['terminal'] and tests['returncode']==0 and sha(Path(tests['log']).read_bytes())==tests['log_sha256']
    assert '110 passed' in Path(tests['log']).read_text('utf8')
    for k in ['candidate','patch']:assert sha(Path(release[k]).read_bytes())==release[k+'_sha256']
    assert release['candidate_sha256']==start['candidate_sha256']==sha(Path(release['exact_patch_reconstruction']).read_bytes())==conf['reference_ROM_sha256']==sha(Path(conf['reference_ROM']).read_bytes())
    registry=read('translations/release_stack.json');manifest=read(release['manifest'])
    assert len(manifest['batches'])==613 and len(manifest['checks'])==18 and all(manifest['checks'].values())
    assert manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes())
    assert len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v4701'
    for p,h in conf['dependencies'].items():assert sha(Path(p).read_bytes())==h,p
    stage=release['stage'];assert stage['all335_other_SC2_blocks_unchanged'] and len(stage['changed_records'])==16
    assert stage['all16_speech_choice_objects_and16_native_pages_actual_complete']
    assert stage['actual_complete_body_holds']==stage['actual_complete_name_holds']==118
    assert stage['original_A000_four_relatives_menu_and_normal_end_value_words0_1_preserved']
    assert stage['personal_names_retained_shared_Shopkeeper_layer_still_open'] and stage['all_measured_source_English_scope_and_later_limits_preserved']
    actual=read(doc['actual_English_proof']);seen=read(doc['actual_English_view']);later=read(doc['later_scope_proof'])
    assert actual['actual_unique_speeches']==14 and actual['actual_complete_native_page_observations']==30
    assert actual['all30_stored_commands_executed_in_union'] and actual['all_four_actual_two_page_transitions_use_original_A_input']
    assert [v['normal_terminal_result'] for v in actual['versions']]==[[0,0],[0,1]]
    assert [(v['source_exit_frame'],v['exit_frame']) for v in actual['versions']]==[(6215,6693)]*2
    assert actual['all_jobs_terminal_and_reaped'] and not seen['visual_review_pending']
    assert later['all_original_command_result_words_agree'] and later['all_measured_differences_retained_for_later_older_record_technical_reaudit']
    assert later['no_full_RAM_every_frame_future_sequence_broad_simulation_or_complete_causal_claim']
    for case in ['newgame','town']:assert read(ROOT/'lil_B221_runs_v7014'/f'{case}_terminal.json')['terminal']
    return release
