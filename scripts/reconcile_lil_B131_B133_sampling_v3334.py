"""Bind actual shared display evidence and the new source00/menu contracts."""
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.prepare_lil_B131_B133_research_v3330b import ROM,PARENT,PLAN
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B131_B133_sampling_v3334')
DOC=Path('translations/lil_B131_B133_editorial_manuscript_v4.json')
CONTROL=Path('work/analysis/lil_B131_B133_relocated_controls_v3333b/all61_relocated_dispatches_source00_and5_predicate_pairs.json')
CENSUS=Path('work/analysis/lil_B131_B133_reference_census_v3332/all112_commands24_relative_sites_and_shipped_entry_census.json')
PADDING=Path('work/analysis/lil_B131_B133_research_v3330b/research_image_receipt.json')
HISTORY=Path('work/analysis/lil_Seville_sampling_v2721b/representative_rule_reconciliation.json')
START=Path('work/analysis/lil_B122_B127_startup_v3303/cold_boot_Lil_startup_town_verification.json')
FE=Path('work/analysis/lil_B131_B133_FE_v3325/current_FE_macro_font_and_typed_paper_proof.json')
TYPED=Path('work/analysis/lil_B131_B133_typed_speech_v3323/all366_whole4000_commands_and108_source00_cases.json')
OLDVIEW=Path('work/analysis/lil_Seville_reference_approval_v2722/representative_sheet_review.json')
VIEW=Path('work/analysis/lil_B122_B127_startup_v3303/current_six_frame_visual_review.json')
if __name__=='__main__':
    assert not ROOT.exists()
    doc,control,census,padding,history,start,plan,fe,typed=map(read,[DOC,CONTROL,CENSUS,PADDING,HISTORY,START,PLAN,FE,TYPED])
    parent,image,historical=[NdsImage.open(p) for p in [PARENT,ROM,history['candidate']]]
    assert sha(PARENT.read_bytes())==doc['current_ROM_sha256']==start['candidate_sha256']
    assert sha(ROM.read_bytes())==census['research_ROM_sha256']==control['research_ROM_sha256']==padding['research_ROM_sha256']
    for path in ['/__arm9__.bin','/COMMON/MESFILE.DK4','/data/EV2.DK4','/GRP/KANJI.FNT']:
        assert image.read_file(path)==parent.read_file(path)==historical.read_file(path)
    current_blocks,old_blocks=[IlnkContainer.parse(i.read_file('/data/SC2.DK4')).blocks for i in [parent,historical]]
    for n in [22,74]:assert current_blocks[n]==old_blocks[n]
    for k in ['all4_historical_progressive_holds_freshly_match_current_full_ink_gray_blank_masks','historical_B74_whole_source_block_equal_current','original_presenter_return_choice_VM_and_text_render_spans_historical_current_exact','no_open_translation_specific_display_or_control_finding']:assert history[k]
    assert start['all_current_requested_and_final_framebuffers_equal_V3251'] and start['paired_frame_count']==31 and start['current_Lil_captain2_and_B22_payload_verified']
    assert padding['all61_final_targets_complete_native_planes_equal_reviewed_planes'] and padding['current_final_padded_macro_alignment_cases']==244
    assert padding['all1_final2100_object_two_labels_and3_selection_cancel_cases_bound'] and padding['no_source2000_pause_commands'] and padding['all18_final_source00_speech_prefixes_and_nonempty_bodies_preserved']
    for k in ['all61_final_stored_paragraphs_reach_expected_original_consumer_and_exact_macro_text','all1_FE_preserves_original_null_actor_before_dynamic_fallback','all5_predicate_current_relocated_results_and_source_operands_equal','all18_final_source00_speeches_are_static_Rafael0_without_role_assignment']:assert control[k]
    assert len(control['relocated_predicate_pairs'])==5 and not control['original_event_queries']
    assert len(typed['cases'])==366 and typed['all108_source00_cases_forward_nonempty_body_after_selector_to_original_display']
    assert census['all112_clean_current_target_commands_and24_relative_sites_reexecuted'] and census['original_block_index_loader_and_parent_contract_verified_for336_blocks_two_modes']
    assert len(fe['cases'])==1
    for path in [OLDVIEW,VIEW]:
        r=read(path);assert r['viewed'] and sha(Path(r['sheet']).read_bytes())==r['sha256']
    evidence={str(p):sha(p.read_bytes()) for p in [DOC,CONTROL,CENSUS,PADDING,HISTORY,START,PLAN,FE,TYPED,OLDVIEW,VIEW,Path('docs/editorial_testing_scope_v1870.md'),Path(__file__)]}
    ROOT.mkdir(parents=True)
    save(ROOT/'representative_rules_and_focused_current_native_reconciliation.json',dict(candidate=str(PARENT),candidate_sha256=sha(PARENT.read_bytes()),research_ROM=str(ROM),research_ROM_sha256=sha(ROM.read_bytes()),ARM9_sha256=sha(image.read_file('/__arm9__.bin')),evidence=evidence,
        historical_complete_ink_gray_blank_masks_reused_without_new_RGB_execution=True,historical_B74_and_current_B22_whole_blocks_exact=True,current_ARM9_COMMON_EV2_font_and_shared_consumer_bytes_exact=True,prior_current_Lil_and_town_startup31frames_inherited_not_new_runs=True,prior_current_startup=str(START),historical_representative_proof=str(HISTORY),
        one2100_menu_source_order_indices_geometry_complete_planes_and_selection_cancel_bound=True,source00_full_typed_body_and_static_Rafael_Lil_context_macros_bound=True,all5_predicates_preserve_source_operands_results_and_unowned_RAM=True,no_source2000_pauses_or_dynamic4100_objects=True,
        policy_resolution='Exact runtime,COMMON,EV2,font,B74/B22 bytes transfer actual progressive/menu/FE display rules under the user testing scope. Current61 whole native planes,488 logical/compiled and244 final stored-target macro cases,61 relocated dispatches,five predicate pairs,112 commands,24 spans,120 relocated skips,inverse restoration,whole loaders/two parent modes andthree entry censuses pass. Eighteen actor00 speeches are real static Rafael,while runtime FI/FO still use Lil captain2;366 whole4000 cases including108 actor00 cases confirm nonempty bodies after selectors. The shared encoder remains strict and only the exact source-bound new profile permits one leading00,with embedded/trailing/duplicate NUL rejected. A17-cell acceptance lost20 leading-H pixels;the faithful18-cell successor passes the complete108px menu plane and0/1/cancel VM checks. UI input/display boundaries in parser tests are disclosed;complete native planes are separate. No distinct unresolved new translation display/control risk requires individually visiting these conditional scenes. No selected B131/B133 gameplay,earned map,share exchange,contract orprogress is claimed. Fresh registered release,exact clean patch andstartup remain required. Wider editorial scope,Proof consistency,graphics andlater technical re-audit remain open.',
        no_open_translation_specific_display_or_control_finding=True,individual_selected_B131_B133_visits_not_required_for_reusable_rules=True,actual_selected_B131_B133_IDs=[],new_individual_nameplate_observations=[],new_emulator_runs=0,registered_release_and_current_startup_still_pending=True,full_goal_complete=False))
    print('Shared actual rules and focused61-speech/two-label/source00 proofs reconciled;registered release/startup pending.')
