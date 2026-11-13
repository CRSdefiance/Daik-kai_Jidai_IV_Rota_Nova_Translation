"""Require the sealed batch, complete registered reconstruction and actual current startup."""
from pathlib import Path
from dk4tool.patch import lil_B214_editorial_v1 as story
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read
ROOT=Path('work/analysis');RELEASE=ROOT/'lil_B214_release_v6734/registered_release_verification.json';START=ROOT/'lil_B214_startup_v6737/cold_boot_Lil_startup_town_verification.json';VIEW=START.parent/'current_six_frame_visual_review.json';REG=ROOT/'lil_B214_registration_v6732/registration_receipt.json';PIN=ROOT/'lil_B214_retention_v6735/pin_receipt.json'
def gates():
    release,start,view,reg=map(read,[RELEASE,START,VIEW,REG]);conf=read(story.CONFIG);doc=read(conf['manuscript']);seal=read(doc['reference_approval'])
    assert seal['manuscript_sha256']==sha(Path(conf['manuscript']).read_bytes()) and seal['all17_five_gates_and_exact_references_approved'] and all(all(r['review'].values()) for r in doc['records'])
    assert release['all606_manifest_batches_and114_accepted_layers_present'] and release['all18_registered_release_checks_pass'] and release['whole_ROM_reconstruction_byte_exact'] and release['every_other_file_font_graphic_route_ARM9_ARM7_and_component_exact_to_V6686'] and release['all_earlier_profiles_and_V4701_promotion_unchanged']
    assert start['all_current_requested_and_final_framebuffers_equal_V6686'] and start['paired_frame_count']==31 and start['all_five_postload_actor_model_and_captain_checks_equal'] and start['source_and_disposable_town_donor_unchanged']
    assert view['viewed'] and view['sha256']==start['review_sheet_sha256']==sha(Path(view['sheet']).read_bytes()) and reg['negative_count']==127 and reg['all_negatives_reject_before_mutation'] and read(PIN)['all_prior_pins_preserved']
    tests=read(ROOT/'lil_B214_regressions_v6733/terminal.json');assert tests['terminal'] and tests['returncode']==0 and sha(Path(tests['log']).read_bytes())==tests['log_sha256'] and '110 passed' in Path(tests['log']).read_text('utf-8')
    for k in ['candidate','patch']:assert sha(Path(release[k]).read_bytes())==release[k+'_sha256']
    assert release['candidate_sha256']==start['candidate_sha256']==sha(Path(release['exact_patch_reconstruction']).read_bytes())==reg['reference_ROM_sha256']==sha(Path(reg['reference_ROM']).read_bytes())
    registry=read('translations/release_stack.json');manifest=read(release['manifest']);assert len(manifest['batches'])==606 and len(manifest['checks'])==18 and all(manifest['checks'].values()) and len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v4701'
    for p,h in conf['dependencies'].items():assert sha(Path(p).read_bytes())==h
    stage=release['stage'];assert stage['all335_other_SC2_blocks_unchanged'] and len(stage['changed_records'])==17 and stage['all10_preambles_one_D0_object_seven_bodies_eight_slots_and_aliases_preserved'] and stage['native17_pages_actual9_objects9_pages29_holds_offline8_explicit'] and stage['all_observed_equality_and_final_scope_limits_retained']
    for case in ['newgame','town']:assert read(ROOT/'lil_B214_runs_v6736'/f'{case}_terminal.json')['terminal']
    a,v=map(read,[doc['actual_English_proof'],doc['actual_English_view']]);assert (a['actual_unique_objects'],a['actual_native_pages'],a['complete_body_holds'],a['complete_name_holds'])==(9,9,29,29) and len(a['offline_only_object_IDs'])==8 and not a['failures'] and not v['visual_review_pending']
    assert v['both_following_B120_end9813_and_final_Sailor_Dizzy_starvation_notice_viewed'] and v['no_full_RAM_future_sequence_broad_simulation_or_complete_causal_claim']
    return release
