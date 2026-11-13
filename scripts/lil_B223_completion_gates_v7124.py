"""Require registered release, exact patch, startup, regressions and disjoint source scope."""
from pathlib import Path
from dk4tool.patch import lil_B223_editorial_v3 as story
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read
ROOT=Path('work/analysis')
RELEASE=ROOT/'lil_B223_release_v7119/registered_release_verification.json';START=ROOT/'lil_B223_startup_v7122/cold_boot_Lil_startup_town_verification.json';VIEW=ROOT/'lil_B223_startup_v7122/current_six_frame_visual_review.json';REG=ROOT/'lil_B223_registration_v7117/registration_receipt.json';PIN=ROOT/'lil_B223_retention_v7120/pin_receipt.json'
def gates():
    release,start,view,reg=map(read,[RELEASE,START,VIEW,REG]);conf=read(story.CONFIG);doc=read(conf['manuscript']);seal=read(doc['reference_approval'])
    assert seal['manuscript_sha256']==sha(Path(conf['manuscript']).read_bytes()) and seal['all17_five_gates_and_exact_references_approved'] and len(doc['records'])==17 and all(all(r['review'].values()) for r in doc['records'])
    assert release['all616_manifest_batches_and114_accepted_layers_present'] and release['all18_registered_release_checks_pass'] and release['whole_ROM_reconstruction_byte_exact'] and release['every_other_file_font_graphic_route_ARM9_ARM7_and_component_exact_to_V7067'] and release['all_earlier_profiles_and_V4701_promotion_unchanged']
    assert start['all_current_requested_and_final_framebuffers_equal_V7067'] and start['paired_frame_count']==31 and start['all_five_postload_actor_model_and_captain_checks_equal'] and start['source_and_disposable_town_donor_unchanged'] and view['viewed'] and view['sha256']==start['review_sheet_sha256']==sha(Path(view['sheet']).read_bytes())
    assert reg['negative_count']==133 and reg['all_negatives_reject_before_mutation'] and read(PIN)['all_prior_pins_preserved']
    tests=read(ROOT/'lil_B223_regressions_v7118/terminal.json');assert tests['terminal'] and tests['returncode']==0 and sha(Path(tests['log']).read_bytes())==tests['log_sha256'] and '110 passed' in Path(tests['log']).read_text('utf8')
    for k in ['candidate','patch']:assert sha(Path(release[k]).read_bytes())==release[k+'_sha256']
    assert release['candidate_sha256']==start['candidate_sha256']==sha(Path(release['exact_patch_reconstruction']).read_bytes())==reg['reference_ROM_sha256']==sha(Path(reg['reference_ROM']).read_bytes())
    registry=read('translations/release_stack.json');manifest=read(release['manifest']);assert len(manifest['batches'])==616 and len(manifest['checks'])==18 and all(manifest['checks'].values()) and len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v4701'
    for p,h in conf['dependencies'].items():assert sha(Path(p).read_bytes())==h,p
    stage=release['stage'];assert stage['all335_other_SC2_blocks_unchanged'] and len(stage['changed_records'])==17 and all(r['block']==223 for r in stage['changed_records']) and stage['native19_pages_actual9_objects11_pages37_holds_offline8_explicit'] and stage['all_measured_later_differences_and_final_scope_limits_retained']
    assert sum(len(r['base_QA_report']['exact_reviewed_base_warnings']) for r in doc['records'])==2 and sum(bool(r['row_count_reason']) for r in doc['records'])==6
    actual=read(doc['actual_English_proof']);assert (actual['actual_unique_objects'],actual['actual_native_pages'],actual['complete_body_holds'],actual['complete_name_holds'])==(9,11,37,37) and len(actual['offline_only_object_IDs'])==8 and actual['captain_IDs']==[0,2]
    for case in ['newgame','town']:assert read(ROOT/'lil_B223_runs_v7121'/f'{case}_terminal.json')['terminal']
    binding=read(ROOT/'current_V7118_native_v7123/registered_current_native_input_binding.json');assert binding['candidate_sha256']==release['candidate_sha256'] and binding['all123264_payload_bytes_COMMON_directory_actual_captain_and_exact2b6_guards_pass']
    return release
