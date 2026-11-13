"""Record returned-image review and exact practical coverage; retain offline distinctions."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B196_actual_review_v5630')
INPUT=Path('work/analysis/lil_B196_actual_review_v5629b/three_paths_final_state_and_full_screen_analysis.json')
if __name__=='__main__':
    assert not ROOT.exists();d=read(INPUT);actual=read(d['actual_proof'])
    assert sha(Path(d['actual_proof']).read_bytes())==d['actual_proof_sha256']
    assert not actual['failures'] and not actual['paired_nontext_region_differences']
    assert len(actual['actual_panels'])==13 and len(actual['all_actual_speech_observations'])==24 and len(actual['actual_menu_cases'])==13
    assert len(actual['offline_only_display_IDs'])==11 and 'DK4_MES_B196_R0074' in actual['offline_only_display_IDs']
    assert not actual['command_timing_differences'] and not actual['later_whole_RGB_differences']
    assert [(v['path'],v['fixture_exit_frame']) for v in actual['versions']]==[(p,f) for p,f in [('first_buy',4299),('all_pass',5255),('deepest_buy',5258)] for _ in range(2)]
    for pair in d['paired_final_state_measurements']:
        assert all(pair['five_native_component_equality'].values()) and pair['whole1A04_actor_and_captain2_equal'] and pair['PRNG_equal']
    assert [p['PRNG_seeds'] for p in d['paired_final_state_measurements']]==[[81408564]*2,[2691520228]*2,[591843373]*2]
    for p,h in d['evidence'].items():assert sha(Path(p).read_bytes())==h
    sheets=[]
    for s in d['actual_consumer_menu_sheets']:
        assert sha(Path(s['path']).read_bytes())==s['sha256']
        sheets.append({**s,'viewed':True,'viewed_after_image_return':True,'review':'Viewed thirteen distinct speech panels and thirteen menu observations. The opening/cackle,silent ellipsis,all six offer amounts,unexpected greed,pleading,post-sale regret,elliptical value judgment and future sell-elsewhere intention remain complete. Lil FE FI clears portrait/name and reads Lil: Charm +1! Buy is index0 and Pass index1 in all six menus. Complete current native label masks and visibly correct selections match returns;ordinary highlight blink phase also matches Japanese. No clipped first/internal/final glyph,overflow,blank page or premature manual break finding in the observed panels.'})
    full=[]
    for s in d['full_screen_sheets']:
        assert sha(Path(s['path']).read_bytes())==s['sha256']
        full.append({**s,'viewed':True,'viewed_after_image_return':True,'review':'Viewed complete paired Japanese/English screens for first-buy Charm notice and actual item presentation/acquisition notice,final refusal/future sale and deepest-buy regret. Sampled normal postscene Sea View continues in the paired fixtures. Vezas\' Scales is visibly presented by the existing item UI;this does not license adding its name to otherwise unnamed seller dialogue or add item-name/widget fidelity credit. Source event196 was relocated to B22 after nine original initializers;natural eligibility,earned affordability,unvisited companion asides and a full playthrough remain unclaimed.'})
    extra=Path('E:/Rota Nova translations/Generated/work/emulation_v193/lil_B196_display_v5627_first_buy_reviewed_English/frame_012970_cold_boot.png')
    assert extra.is_file();extra_view=dict(path=str(extra),sha256=sha(extra.read_bytes()),viewed=True,viewed_after_image_return=True,review='Viewed first-buy fixture normal postscene Sea View at12970;no stuck modal or dialogue remains. Not a full sailing test.')
    assert len(sheets)==5 and len(full)==3
    for v in actual['versions']:
        report=read(v['capture_report']);run=Path('work/analysis/lil_B196_display_run_v5627_'+v['path']+'_'+v['case'])
        terminal=read(run/'terminal.json');assert terminal['terminal'] and terminal['observer_host_slots_restored']
        assert report['cold_boot'] and not report['savestate_loaded'] and report['frames']==13001
    ROOT.mkdir(parents=True)
    evidence={**d['evidence'],str(INPUT):sha(INPUT.read_bytes()),str(extra):sha(extra.read_bytes()),str(Path(__file__)):sha(Path(__file__).read_bytes())}
    save(ROOT/'viewed13_panels13_menus_three_paths_and_measured_state_scope.json',dict(
        actual_proof=d['actual_proof'],actual_proof_sha256=d['actual_proof_sha256'],previous_visual_analysis=str(INPUT),previous_visual_analysis_sha256=sha(INPUT.read_bytes()),
        all_actual_consumer_menu_sheets_viewed=sheets,paired_full_screen_views=full,first_buy_postscene_view=extra_view,
        actual_unique_speech_panels=13,actual_speech_observations=24,actual_menu_cases=13,complete_native_speech_holds=actual['complete_native_holds'],
        offline_only_display_IDs=actual['offline_only_display_IDs'],eleven_other_speeches_native_offline_not_gameplay=True,
        all_six_original_menus_and_first_buy_deepest_buy_and_all_pass_endings_observed=True,
        original119_source_commands_and9_init_commands_stored_without_omission_or_flattening=True,
        original_predicates_RNG_funds_unforced_and_frontend_ordinary_gamepad_only=True,
        no_difference_in_paired_command_timings_or_sampled_postscene_RGB=True,
        paired_final_state_measurements=d['paired_final_state_measurements'],
        five_native_groups_whole1A04_actor_captain2_and_PRNG_equal_within_each_pair=True,
        first_audit_excluded_settled_age31_to35_frames_and_blink_phase_was_not_a_ROM_defect=True,
        corrected_audit_preserves_complete_native_foregrounds_visible_correct_selection_and_paired_backgrounds=True,
        first_state_review_stopped_on_save_helper_default_argument_successor_serializes_native_bytes_explicitly=True,
        preserved_first_audit='work/analysis/lil_B196_actual_v5628/three_paired_paths_native_panels_menus_and_separate_endings.json',
        preserved_first_review='scripts/review_lil_B196_actual_v5629.py',
        no_open_translation_specific_display_menu_control_or_return_finding=True,
        representative_actual_coverage_sufficient_for_this_distinct_display_scope=True,
        no_further_focus_run_required_by_current_distinct_display_findings=True,
        item_picture_and_acquisition_notice_observed_without_complete_item_inventory_semantic_audit=True,
        actual_event196_natural_selection_outer_eligibility_earned_affordability_unvisited_paths_not_claimed=True,
        no_causal_future_world_full_RAM_full_playthrough_or_hardware_claim=True,
        actual_new_cold_boot_runs=6,total_frames=78006,reaped_tool_sessions=[35487,22688,78215,4908,28838,51389],
        visual_review_pending=False,all_ROMs_translations_producers_failures_and_evidence_preserved=True,
        evidence=evidence,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('Viewed5 speech/menu sheets,3 paired full-screen sheets and first-buy return;13 distinct panels/13 menu cases/three endings pass.11 other speeches remain offline-only.6 cold boots/78006 frames;all sessions reaped.')
