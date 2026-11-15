"""Reconcile reusable actual display rules with focused current native tests."""
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.prepare_lil_B111_B119_research_v3240b import ROM,PARENT,PLAN
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B111_B119_sampling_v3245')
DOC=Path('translations/lil_B111_B119_editorial_manuscript_v5.json')
CONTROL=Path('work/analysis/lil_B111_B119_relocated_controls_v3243d/all150_dispatch12_style_commands2484_getters16_predicate_query_pairs.json')
REFERENCE=Path('work/analysis/lil_B111_B119_reference_census_v3242/all305_commands64_relative_sites_and_shipped_entry_census.json')
PADDING=Path('work/analysis/lil_B111_B119_research_v3240b/research_image_receipt.json')
HISTORY=Path('work/analysis/lil_Seville_sampling_v2721b/representative_rule_reconciliation.json')
START=Path('work/analysis/lil_Shrines_Temples_startup_v3207/cold_boot_Lil_startup_town_verification.json')
FE=Path('work/analysis/lil_B111_B119_FE_v3235/current_FE_macro_font_and_typed_paper_proof.json')
COPY=Path('work/analysis/lil_B111_B119_relocated_copy_v3244/moved_return0_and_unowned_copy_proof.json')

if __name__=='__main__':
    assert not ROOT.exists()
    doc,control,reference,padding,history,start,plan,fe,copy=map(read,[DOC,CONTROL,REFERENCE,PADDING,HISTORY,START,PLAN,FE,COPY])
    parent,image,historical=[NdsImage.open(p) for p in [PARENT,ROM,history['candidate']]]
    assert sha(PARENT.read_bytes())==doc['current_ROM_sha256']==start['candidate_sha256']
    assert sha(ROM.read_bytes())==reference['research_ROM_sha256']==control['research_ROM_sha256']==padding['research_ROM_sha256']==copy['research_ROM_sha256']
    assert image.read_file('/__arm9__.bin')==parent.read_file('/__arm9__.bin')==historical.read_file('/__arm9__.bin')
    for path in ['/COMMON/MESFILE.DK4','/data/EV2.DK4','/GRP/KANJI.FNT']:
        assert image.read_file(path)==parent.read_file(path)==historical.read_file(path)
    current_blocks,old_blocks=[IlnkContainer.parse(i.read_file('/data/SC2.DK4')).blocks for i in [parent,historical]]
    for n in [22,74]:assert current_blocks[n]==old_blocks[n]
    for k in ['all4_historical_progressive_holds_freshly_match_current_full_ink_gray_blank_masks','historical_B74_whole_source_block_equal_current','original_presenter_return_choice_VM_and_text_render_spans_historical_current_exact','no_open_translation_specific_display_or_control_finding']:assert history[k],k
    assert start['all_current_requested_and_final_framebuffers_equal_V3144'] and start['current_Lil_captain2_and_B22_payload_verified']
    assert padding['all150_final_targets_complete_native_planes_equal_reviewed_planes'] and padding['current_final_padded_macro_alignment_cases']==600
    for k in ['all150_final_stored_paragraphs_reach_expected_original_consumer_and_exact_macro_text','all2484_pointer_cases_and_all_source_alias_groups_preserved','all15_predicate_and_one_query_current_relocated_results_and_source_operands_equal','original_query_r0_r1_r2_and_mapped_incidental_r3_cursor_exact']:assert control[k],k
    assert len(control['relocated_predicate_pairs'])==16 and len(control['original_event_queries'])==1 and control['original_event_queries'][0]['event']==319
    assert fe['all1_one_native_page_consumes_complete_target'] and fe['all1_complete_native_independent_planes_all_glyphs_and_canaries_equal']
    assert fe['historical_calibration']['current_calibration_matches_complete_historical_ink_and_blank_mask']
    assert copy['all32_unowned_copy_speeches_byte_exact_and_unreachable_from_ordinary_Lil_entry'] and len(copy['original_VM_return_cases'])==2
    assert all(not b['choice_commands'] for b in plan['blocks'])
    historical_review=Path('work/analysis/lil_Seville_reference_approval_v2722/representative_sheet_review.json')
    current_review=Path('work/analysis/lil_Shrines_Temples_completion_v3208/current_six_frame_visual_review.json')
    for path in [historical_review,current_review]:
        r=read(path);assert r['viewed'] and sha(Path(r['sheet']).read_bytes())==r['sha256']
    evidence={str(p):sha(p.read_bytes()) for p in [DOC,CONTROL,REFERENCE,PADDING,HISTORY,START,PLAN,FE,COPY,historical_review,current_review,Path(doc['appended_copy_classification']),Path('docs/editorial_testing_scope_v1870.md'),Path(__file__)]}
    ROOT.mkdir(parents=True)
    save(ROOT/'relocated_predicates_and_representative_rule_reconciliation.json',dict(candidate=str(PARENT),candidate_sha256=sha(PARENT.read_bytes()),research_ROM=str(ROM),research_ROM_sha256=sha(ROM.read_bytes()),ARM9_sha256=sha(image.read_file('/__arm9__.bin')),evidence=evidence,relocated_predicate_pairs=control['relocated_predicate_pairs'],original_event_queries=control['original_event_queries'],historical_complete_ink_gray_blank_masks_reused_without_new_RGB_execution=True,historical_B74_and_current_B22_whole_blocks_exact=True,current_ARM9_COMMON_EV2_font_and_shared_consumer_bytes_exact=True,prior_current_Lil_and_town_startup31frames_inherited_not_new_runs=True,prior_current_startup=str(START),historical_representative_proof=str(HISTORY),historical_FE_geometry_calibrated_one_current_unlabeled_gold_notice_verified=True,source_4100_voice_selection_distinct_from_player_choices=True,current4100_actual5_prefixes_all34_bodies_all48_aliases_and_all207_catalog_styles_bound=True,all15_predicates_and_event319_query_preserve_native_operands_results_and_mapped_cursor=True,moved_return0_two_native_VM_modes_and_complete_graph_preserve_unowned32_copy=True,canonical_Maria_SC3_B97_32_targets_remain_pending_uncredited=True,inherited_three_access_travel_funds_fixtures_and_five_ship_town_battery_not_earned=True,no_new_fixture_or_event_roster_RNG_health_outcome_mutation=True,
        policy_resolution='The user authorizes reusable source-bound display rules and focused native checks instead of visiting every conditional line. Historical actual progressive holds and FE tutorial remain representative by exact ARM9,COMMON,EV2,font andB74/B22 bytes. All150 current paragraph planes/1200logical-compiled macro cases/600final stored-target cases pass. Six4100objects preserve actualD0,D1,D6,D7,DC selectors,34body planes and48aliases through12whole commands and2484current-relocated catalog pointer cases without assigning roles. No player-choice object occurs. The distinct event319 query receives equal source operands/results/r0-r2 and exactly mapped incidentalr3 cursor; source code overwritesr2/r3 before use. All305physicalcommands/64spans/320native skipcases/inverse bytes,336loaders/two parent modes/three entrycensuses pass. The moved original B115return0 passes both originalVMmodes andconservative fullprefix graph;its1886byte unownedcopy remains exact andcanonicalMaria32 queued without Lil company dispatch. These are offline native tests and inherited scoped actual gameplay evidence. No remaining translation-specific display/control finding requires individual visits under the user policy. All newscene rewards,rescues,donations,gifts,trends andprogress remain unearned. Fresh registered cumulative build,exact cleanpatch andcurrentstartup remain mandatory. Wider editorial scope,graphics separation andlater older-record technical re-audit remain open.',
        no_open_translation_specific_display_or_control_finding=True,individual_selected_B111_B119_visits_not_required_for_reusable_rules=True,actual_selected_B111_B119_IDs=[],new_individual_nameplate_observations=[],new_emulator_runs=0,registered_release_and_current_startup_still_pending=True,full_goal_complete=False))
    print('Representative actual shared display rules reconciled withall150native targets/variable4100/event319/movedreturn0 focusedtests. No newselected gameplay;registeredrelease/startup pending.')
