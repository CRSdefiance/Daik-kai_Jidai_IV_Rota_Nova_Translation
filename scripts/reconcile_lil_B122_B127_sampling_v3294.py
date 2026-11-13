"""Bind scoped actual shared rules and focused final native tests."""
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.prepare_lil_B122_B127_research_v3289b import ROM,PARENT,PLAN
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B122_B127_sampling_v3294')
DOC=Path('translations/lil_B122_B127_editorial_manuscript_v5.json')
CONTROL=Path('work/analysis/lil_B122_B127_relocated_controls_v3292/all155_relocated_dispatches_and14_predicate_pairs.json')
REFERENCE=Path('work/analysis/lil_B122_B127_reference_census_v3291/all312_commands64_relative_sites_and_shipped_entry_census.json')
PADDING=Path('work/analysis/lil_B122_B127_research_v3289b/research_image_receipt.json')
HISTORY=Path('work/analysis/lil_Seville_sampling_v2721b/representative_rule_reconciliation.json')
START=Path('work/analysis/lil_B111_B119_startup_v3254/cold_boot_Lil_startup_town_verification.json')
FE=Path('work/analysis/lil_B122_B127_FE_v3284/current_FE_macro_font_and_typed_paper_proof.json')
WAIT=Path('work/analysis/lil_B122_original2000_waits_v3265/original2000_actual_rule_and_current_source_binding.json')
RETURN=Path('work/analysis/lil_trade_branch_return_v3293/original_choice_control_paths_and_both_VM_return_modes.json')
if __name__=='__main__':
    assert not ROOT.exists();doc,control,reference,padding,history,start,plan,fe,wait,branch=map(read,[DOC,CONTROL,REFERENCE,PADDING,HISTORY,START,PLAN,FE,WAIT,RETURN])
    parent,image,historical=[NdsImage.open(p) for p in [PARENT,ROM,history['candidate']]]
    assert sha(PARENT.read_bytes())==doc['current_ROM_sha256']==start['candidate_sha256']==wait['candidate_sha256']
    assert sha(ROM.read_bytes())==reference['research_ROM_sha256']==control['research_ROM_sha256']==padding['research_ROM_sha256']==branch['research_ROM_sha256']
    assert image.read_file('/__arm9__.bin')==parent.read_file('/__arm9__.bin')==historical.read_file('/__arm9__.bin')
    for path in ['/COMMON/MESFILE.DK4','/data/EV2.DK4','/GRP/KANJI.FNT']:assert image.read_file(path)==parent.read_file(path)==historical.read_file(path)
    current_blocks,old_blocks=[IlnkContainer.parse(i.read_file('/data/SC2.DK4')).blocks for i in [parent,historical]]
    for n in [22,74]:assert current_blocks[n]==old_blocks[n]
    for k in ['all4_historical_progressive_holds_freshly_match_current_full_ink_gray_blank_masks','historical_B74_whole_source_block_equal_current','original_presenter_return_choice_VM_and_text_render_spans_historical_current_exact','no_open_translation_specific_display_or_control_finding']:assert history[k]
    assert start['all_current_requested_and_final_framebuffers_equal_V3204'] and start['paired_frame_count']==31 and start['current_Lil_captain2_and_B22_payload_verified']
    assert padding['all155_final_targets_complete_native_planes_equal_reviewed_planes'] and padding['current_final_padded_macro_alignment_cases']==620
    assert padding['all2_final2100_objects_four_labels_and6_selection_cancel_cases_bound'] and padding['both_original_pause_resume_words_and20_decoder_cases_bound']
    assert control['all155_final_stored_paragraphs_reach_expected_original_consumer_and_exact_macro_text'] and control['all10_FE_preserve_original_null_actor_before_dynamic_fallback'] and control['all14_predicate_current_relocated_results_and_source_operands_equal'] and len(control['relocated_predicate_pairs'])==14 and not control['original_event_queries']
    assert fe['all10_one_native_page_consumes_complete_target'] and fe['all10_complete_native_independent_planes_all_glyphs_and_canaries_equal'] and fe['historical_calibration']['current_calibration_matches_complete_historical_ink_and_blank_mask']
    assert wait['current_zero_argument_wait_contract_bound_by_exact_original_code_and_actual_Lil_pause_evidence'] and wait['all3_historical_pause_captures_viewed'] and wait['current_and_historical_B22_whole_block_exact']
    assert branch['selection0_skips_already_know_return_and_reaches_tutorial'] and branch['selection1_enters_already_know_branch_and_return0'] and len(branch['original_VM_return_cases'])==12 and len(branch['conditional_native_paths'])==6
    historical_review=Path('work/analysis/lil_Seville_reference_approval_v2722/representative_sheet_review.json');current_review=Path('work/analysis/lil_B111_B119_completion_v3255/current_six_frame_visual_review.json')
    for path in [historical_review,current_review]:
        r=read(path);assert r['viewed'] and sha(Path(r['sheet']).read_bytes())==r['sha256']
    evidence={str(p):sha(p.read_bytes()) for p in [DOC,CONTROL,REFERENCE,PADDING,HISTORY,START,PLAN,FE,WAIT,RETURN,historical_review,current_review,Path('docs/editorial_testing_scope_v1870.md'),Path(__file__)]}
    ROOT.mkdir(parents=True);save(ROOT/'representative_rules_and_focused_current_native_reconciliation.json',dict(candidate=str(PARENT),candidate_sha256=sha(PARENT.read_bytes()),research_ROM=str(ROM),research_ROM_sha256=sha(ROM.read_bytes()),ARM9_sha256=sha(image.read_file('/__arm9__.bin')),evidence=evidence,historical_complete_ink_gray_blank_masks_reused_without_new_RGB_execution=True,historical_B74_and_current_B22_whole_blocks_exact=True,current_ARM9_COMMON_EV2_font_and_shared_consumer_bytes_exact=True,prior_current_Lil_and_town_startup31frames_inherited_not_new_runs=True,prior_current_startup=str(START),historical_representative_proof=str(HISTORY),historical_FE_geometry_calibrated_ten_current_unlabeled_panels_verified=True,original_source2000_pause_and_normal_A_rule_reused_under_exact_code_B22_and_asset_binding=True,final20_pause_decoder_cases_explicit_UI_body_unexecuted=True,both_mapped_pause_resumption_boundaries_exact=True,two2100_menus_source_order_indices_geometry_complete_planes_and_selection_cancel_bound=True,trade_tutorial_and_already_know_branch_native_paths_and_both_return_modes_bound=True,all14_predicates_preserve_source_operands_results_and_unowned_RAM=True,inherited_three_access_fixtures_and_five_ship_town_battery_remain_unearned=True,no_new_event_roster_RNG_health_outcome_fixture=True,
        policy_resolution='Under the user testing scope, exact shared consumer/runtime/COMMON/EV2/font/B74/B22 bindings transfer actual progressive/menu/FE rules. Current complete155 speech planes,1240 logical/compiled macro cases,620 final stored-target cases,155 relocated dispatches and14 predicate pairs pass. Two2100 menus preserve four labels,0/1/cancel,original geometry andcomplete ink/blank planes;final whole-object getters andsix VMreturns match. Two2000 source controls intentionally pause illustrations for normalA: three historical actual Lil captures viewed, exact current code/B22/assets bound,20 final decoder cases explicitly bridge the unexecuted54E44UIbody,and both mapped resume boundaries are exact. This does not transfer arbitrary historical prose or claim newB122 gameplay. B126 choice0 native conditions skip the already-know branch and reach tutorial;choice1 enters that branch andreturn0. Six source/current/target paths and12 original VMreturns preserve this;no naive linear graph discards the tutorial. All312commands/64spans/320skipcases/inverse bytes,336wholeloaders/two parent modes/threeentrycensuses pass. These are offline current native checks and inherited scoped gameplay evidence. No translation-specific distinct display/control risk remains that requires every conditional scene to be visited. No earned death/recovery,recruitment,gift,statgain,profit orprogress. Fresh registered build/exact cleanpatch/current startup remain required. Wider prose,Proof terminology consistency,separate graphics andlater technical re-audit stay open.',
        no_open_translation_specific_display_or_control_finding=True,individual_selected_B122_B127_visits_not_required_for_reusable_rules=True,actual_selected_B122_B127_IDs=[],new_individual_nameplate_observations=[],new_emulator_runs=0,registered_release_and_current_startup_still_pending=True,full_goal_complete=False))
    print('Actual shared display/pause rules and current155speech/four-label/predicate/conditional-return focused proofs reconciled. No selected new gameplay;registered release/startup pending.')
