"""Require the full registered release, exact patch and own startup before B234 credit."""
from pathlib import Path
from dk4tool.patch import lil_B234_editorial_v1 as story
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read
ROOT=Path('work/analysis')
RELEASE=ROOT/'lil_B234_release_v7612/registered_release_verification.json';START=ROOT/'lil_B234_startup_v7615/cold_boot_Lil_startup_town_verification.json';VIEW=ROOT/'lil_B234_startup_v7615/current_six_frame_visual_review.json';REG=ROOT/'lil_B234_registration_v7610/registration_receipt.json';PIN=ROOT/'lil_B234_retention_v7613/pin_receipt.json'
def gates():
    release,start,view,reg=map(read,[RELEASE,START,VIEW,REG]);conf=read(story.CONFIG);doc=read(conf['manuscript']);seal=read(doc['reference_approval'])
    assert seal['manuscript_sha256']==sha(Path(conf['manuscript']).read_bytes()) and seal['all18_five_gates_andexact_references_approved'] and len(doc['records'])==18 and all(all(r['review'].values()) for r in doc['records'])
    assert release['all626_manifest_batches_and114_accepted_layers_present'] and release['all18_registered_release_checks_pass'] and release['whole_ROM_reconstruction_byte_exact'] and release['every_other_file_font_graphic_route_ARM9_ARM7_and_component_exact_to_V7563'] and release['all_earlier_profiles_and_V4701_promotion_unchanged']
    assert start['all_current_requested_and_final_framebuffers_equal_V7563'] and start['paired_frame_count']==31 and start['all_five_postload_actor_model_and_captain_checks_equal'] and start['source_and_disposable_town_donor_unchanged'] and view['viewed'] and view['sha256']==start['review_sheet_sha256']==sha(Path(view['sheet']).read_bytes())
    assert reg['profile']=='all-routes-unified-v7611' and reg['negative_count']==110 and reg['all_negatives_reject_before_mutation'] and read(PIN)['all_prior_pins_preserved']
    tests=read(ROOT/'lil_B234_regressions_v7611/terminal.json');assert tests['terminal'] and tests['returncode']==0 and sha(Path(tests['log']).read_bytes())==tests['log_sha256'] and '110 passed' in Path(tests['log']).read_text('utf8')
    for k in ['candidate','patch']:assert sha(Path(release[k]).read_bytes())==release[k+'_sha256']
    assert release['candidate_sha256']==start['candidate_sha256']==sha(Path(release['exact_patch_reconstruction']).read_bytes())==reg['reference_ROM_sha256']==sha(Path(reg['reference_ROM']).read_bytes())
    registry=read('translations/release_stack.json');manifest=read(release['manifest'])
    assert len(manifest['batches'])==626 and len(manifest['checks'])==18 and all(manifest['checks'].values()) and len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v4701' and manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes())
    for p,h in conf['dependencies'].items():assert sha(Path(p).read_bytes())==h,p
    stage=release['stage'];assert stage['all335_other_SC2_blocks_unchanged'] and len(stage['changed_records'])==18 and all(r['block']==234 for r in stage['changed_records']) and stage['all18_objects18_pages_actual_complete'] and stage['original_A000_normal_end_residual_value_andsource_tail_inverse_preserved']
    warned=[r for r in doc['records'] if r['base_QA_report']['exact_reviewed_base_warnings']]
    assert len(warned)==1 and warned[0]['source_record_index']==33 and warned[0]['base_QA_report']['exact_reviewed_base_warnings']==[dict(severity='warning',code='weak-line-ending',message="line 1 ends with weak wrap word 'the'")] and sum(bool(r['row_count_reason']) for r in doc['records'])==8
    actual=read(doc['actual_English_proof'])
    assert (actual['actual_unique_speeches'],actual['actual_native_pages'],actual['actual_complete_body_holds'],actual['actual_complete_name_holds'])==(18,18,71,71) and actual['all18_single_original_native_pages_verified'] and actual['ASCII_dark_gray_andexact_R5_CP932_light_gray_complete_masks_andall_name_masks_verified']
    for case in ['newgame','town']:assert read(ROOT/'lil_B234_runs_v7614'/f'{case}_terminal.json')['terminal']
    binding=read(ROOT/'current_V7611_native_v7616/registered_current_native_input_binding.json')
    assert binding['candidate_sha256']==release['candidate_sha256'] and binding['all123264_payload_bytes_COMMON_directory_actual_captain_and_exact2b6_guards_pass']
    return release
