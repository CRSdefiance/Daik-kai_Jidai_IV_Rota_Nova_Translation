"""Require the registered cumulative ROM,exact patch,current startup and all name evidence."""
from pathlib import Path
from dk4tool.patch import square_shopkeeper_label_release_v2 as owned
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read
BASE=Path('work/analysis')
def gates():
    release=read(BASE/'square_shopkeeper_release_v7030/registered_release_verification.json')
    start=read(BASE/'square_shopkeeper_startup_v7033/registered_current_startup_and_town_verification.json')
    view=read(BASE/'square_shopkeeper_startup_v7033/current_six_frame_visual_review.json')
    reg=read(BASE/'square_shopkeeper_registration_v7028/registration_receipt.json');conf=read(owned.CONFIG)
    assert release['all614_manifest_batches_and114_accepted_layers_present'] and release['all18_registered_release_checks_pass'] and release['whole_ROM_reconstruction_byte_exact']
    assert release['all_earlier_profiles_and_V4701_promotion_unchanged'] and release['every_other_file_font_graphic_route_ARM7_code_and_unowned_ARM9_bytes_exact_to_V7011']
    assert release['component_changes']==[owned.PATH] and release['file_changes']==[]
    assert release['stage']['all_ten_contextual_five_gates_and_native_representative_nameplates_pass'] and release['stage']['actual_changed_headers']==9
    assert start['all_current_requested_and_final_framebuffers_equal_V7011'] and start['paired_frame_count']==31 and start['all_five_actor_captain_and_current_payload_controls_pass']
    assert start['actual_target_NewGame7019_reused_by_exact_whole_ROM_hash'] and start['fresh_registered_town7032_cold_boot'] and start['unchanged_source_and_disposable_town_donor']
    assert view['viewed'] and view['sha256']==start['review_sheet_sha256']==sha(Path(view['sheet']).read_bytes())
    assert read(BASE/'square_shopkeeper_retention_v7031/pin_receipt.json')['all_prior_pins_preserved']
    atomic=read(BASE/'square_shopkeeper_atomic_v7027/atomic_validation_receipt.json')
    assert atomic['negative_count']==reg['negative_count']==61 and atomic['all_negatives_reject_before_mutation']
    tests=read(BASE/'square_shopkeeper_regressions_v7029/terminal.json')
    assert tests['terminal'] and tests['returncode']==0 and sha(Path(tests['log']).read_bytes())==tests['log_sha256'] and '110 passed' in Path(tests['log']).read_text('utf8')
    for key in ['candidate','patch']:assert sha(Path(release[key]).read_bytes())==release[key+'_sha256']
    assert release['candidate_sha256']==start['candidate_sha256']==sha(Path(release['exact_patch_reconstruction']).read_bytes())==conf['reference_ROM_sha256']
    assert Path(release['candidate']).read_bytes()==Path(conf['reference_ROM']).read_bytes()
    manifest=read(release['manifest']);registry=read('translations/release_stack.json')
    assert len(manifest['batches'])==614 and len(manifest['checks'])==18 and all(manifest['checks'].values())
    assert manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes())
    assert len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v4701'
    for path,digest in conf['dependencies'].items():assert sha(Path(path).read_bytes())==digest,path
    binding=read(BASE/'current_V7029_native_v7033/registered_current_native_input_binding.json')
    assert binding['candidate_sha256']==release['candidate_sha256'] and binding['ARM9_sha256']==release['ARM9_sha256']
    assert binding['full_current_ROM_equals_own_research_boot_ROM'] and binding['no_old_ROM_or_RAM_overlay_or_relaxed_runtime_instruction_guard']
    assert sha(Path(binding['input']).read_bytes())==binding['input_sha256']
    return release
