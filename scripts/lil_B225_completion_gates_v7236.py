"""Require exact registered release,patch,current startup andown native context before credit."""
from pathlib import Path
from dk4tool.patch import lil_B225_editorial_v1 as story
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read
ROOT=Path('work/analysis')
RELEASE=ROOT/'lil_B225_release_v7231/registered_release_verification.json';START=ROOT/'lil_B225_startup_v7234/cold_boot_Lil_startup_town_verification.json';VIEW=ROOT/'lil_B225_startup_v7234/current_six_frame_visual_review.json';REG=ROOT/'lil_B225_registration_v7229/registration_receipt.json';PIN=ROOT/'lil_B225_retention_v7232/pin_receipt.json'
def gates():
    release,start,view,reg=map(read,[RELEASE,START,VIEW,REG]);conf=read(story.CONFIG);doc=read(conf['manuscript']);seal=read(doc['reference_approval'])
    assert seal['manuscript_sha256']==sha(Path(conf['manuscript']).read_bytes()) and seal['all13_five_gates_andexact_references_approved'] and len(doc['records'])==13 and all(all(r['review'].values()) for r in doc['records'])
    assert release['all618_manifest_batches_and114_accepted_layers_present'] and release['all18_registered_release_checks_pass'] and release['whole_ROM_reconstruction_byte_exact'] and release['every_other_file_font_graphic_route_ARM9_ARM7_and_component_exact_to_V7168'] and release['all_earlier_profiles_and_V4701_promotion_unchanged']
    assert start['all_current_requested_and_final_framebuffers_equal_V7168'] and start['paired_frame_count']==31 and start['all_five_postload_actor_model_and_captain_checks_equal'] and start['source_and_disposable_town_donor_unchanged'] and view['viewed'] and view['sha256']==start['review_sheet_sha256']==sha(Path(view['sheet']).read_bytes())
    assert reg['profile']=='all-routes-unified-v7230' and reg['negative_count']==182 and reg['all_negatives_reject_before_mutation'] and read(PIN)['all_prior_pins_preserved']
    tests=read(ROOT/'lil_B225_regressions_v7230/terminal.json');assert tests['terminal'] and tests['returncode']==0 and sha(Path(tests['log']).read_bytes())==tests['log_sha256'] and '110 passed' in Path(tests['log']).read_text('utf8')
    for k in ['candidate','patch']:assert sha(Path(release[k]).read_bytes())==release[k+'_sha256']
    assert release['candidate_sha256']==start['candidate_sha256']==sha(Path(release['exact_patch_reconstruction']).read_bytes())==reg['reference_ROM_sha256']==sha(Path(reg['reference_ROM']).read_bytes())
    registry=read('translations/release_stack.json');manifest=read(release['manifest']);assert len(manifest['batches'])==618 and len(manifest['checks'])==18 and all(manifest['checks'].values()) and len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v4701'
    for p,h in conf['dependencies'].items():assert sha(Path(p).read_bytes())==h,p
    stage=release['stage'];assert stage['all335_other_SC2_blocks_unchanged'] and len(stage['changed_records'])==13 and all(r['block']==225 for r in stage['changed_records']) and stage['all13_objects14_pages_actual_complete'] and stage['original630B_A000_normal_end_residual_value_and_source_tail_inverse_preserved']
    assert not sum(len(r['base_QA_report']['exact_reviewed_base_warnings']) for r in doc['records']) and sum(bool(r['row_count_reason']) for r in doc['records'])==2
    actual=read(doc['actual_English_proof']);assert (actual['actual_unique_speeches'],actual['actual_native_pages'],actual['actual_complete_body_holds'],actual['actual_complete_name_holds'])==(13,14,55,55) and actual['source_R26_both_complete_pages_andordinary_A_advance_bound']
    for case in ['newgame','town']:assert read(ROOT/'lil_B225_runs_v7233'/f'{case}_terminal.json')['terminal']
    binding=read(ROOT/'current_V7230_native_v7235/registered_current_native_input_binding.json');assert binding['candidate_sha256']==release['candidate_sha256'] and binding['all123264_payload_bytes_COMMON_directory_actual_captain_and_exact2b6_guards_pass']
    return release
