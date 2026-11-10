"""Require cumulative ancestry, exact reconstruction and current terminal startup before credit."""
from pathlib import Path
from dk4tool.patch import lil_B216_editorial_v1 as story
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read
ROOT=Path('work/analysis')
def gates():
    release=read(ROOT/'lil_B216_release_v6822/registered_release_verification.json');start=read(ROOT/'lil_B216_startup_v6825/cold_boot_Lil_startup_town_verification.json');view=read(ROOT/'lil_B216_startup_v6825/current_six_frame_visual_review.json');reg=read(ROOT/'lil_B216_registration_v6820/registration_receipt.json');conf=read(story.CONFIG);doc=read(conf['manuscript']);seal=read(doc['reference_approval'])
    assert seal['manuscript_sha256']==sha(Path(conf['manuscript']).read_bytes()) and seal['all11_five_gates_and_exact_references_approved'] and len(doc['records'])==11 and all(all(r['review'].values()) for r in doc['records'])
    assert release['all608_manifest_batches_and114_accepted_layers_present'] and release['all18_registered_release_checks_pass'] and release['whole_ROM_reconstruction_byte_exact'] and release['every_other_file_font_graphic_route_ARM9_ARM7_and_component_exact_to_V6775'] and release['all_earlier_profiles_and_V4701_promotion_unchanged']
    assert start['all_current_requested_and_final_framebuffers_equal_V6775'] and start['paired_frame_count']==31 and start['all_five_postload_actor_model_and_captain_checks_equal'] and start['source_and_disposable_town_donor_unchanged'] and view['viewed'] and view['sha256']==start['review_sheet_sha256']==sha(Path(view['sheet']).read_bytes())
    assert reg['negative_count']==17 and reg['all_negatives_reject_before_mutation'] and read(ROOT/'lil_B216_retention_v6823/pin_receipt.json')['all_prior_pins_preserved']
    tests=read(ROOT/'lil_B216_regressions_v6821/terminal.json');assert tests['terminal'] and tests['returncode']==0 and sha(Path(tests['log']).read_bytes())==tests['log_sha256'] and '110 passed' in Path(tests['log']).read_text('utf8')
    for k in ['candidate','patch']:assert sha(Path(release[k]).read_bytes())==release[k+'_sha256']
    assert release['candidate_sha256']==start['candidate_sha256']==sha(Path(release['exact_patch_reconstruction']).read_bytes())==reg['reference_ROM_sha256']==sha(Path(reg['reference_ROM']).read_bytes());registry=read('translations/release_stack.json');manifest=read(release['manifest']);assert len(manifest['batches'])==608 and len(manifest['checks'])==18 and all(manifest['checks'].values()) and len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v4701'
    for p,h in conf['dependencies'].items():assert sha(Path(p).read_bytes())==h
    stage=release['stage'];assert stage['all335_other_SC2_blocks_unchanged'] and len(stage['changed_records'])==11 and stage['all11_objects11_pages_ten_actual_one_offline_alternative'] and stage['actual_complete_body_holds']==stage['actual_complete_name_holds']==39 and stage['three_name_retentions_two_wider_role_leads_unchanged']
    for case in ['newgame','town']:assert read(ROOT/'lil_B216_runs_v6824'/f'{case}_terminal.json')['terminal']
    return release
