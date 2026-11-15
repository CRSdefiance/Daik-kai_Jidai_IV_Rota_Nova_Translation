"""Record six returned image sheets and retain the measured B187 evidence limits."""
from pathlib import Path
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/lil_B187_actual_review_v5214')
INPUT=ROOT/'paired_all115_samples28_commands16_planes_and_final_state_analysis.json'
OUTPUT=ROOT/'all16_panels12_fullscreens_linear_return_and_measured_differences.json'
if __name__=='__main__':
    assert not OUTPUT.exists();d=read(INPUT);actual=read(d['actual_proof'])
    assert d['visual_review_pending'] and d['nontext_equal_samples']==115 and not d['nontext_difference_samples']
    assert d['fixture_return_frames']==[6694,6695]
    assert d['exact_timing_difference_counts']==dict(total=16,speech=14,control_or_end=2)
    assert d['whole_RGB_final9001_equal'] and d['all_sampled_postscene_whole_RGB_equal']
    assert not d['sampled_postscene_whole_RGB_differences_unmasked']
    assert all(d['postscene9001_native_component_equality'].values())
    assert d['postscene9001_whole1A04_actor_models_and_captain2_equal']
    assert d['PRNG_equality'] and d['postscene9001_PRNG_seeds']==[2467799992,2467799992]
    assert len(actual['actual_panels'])==16 and sum(len(r['holds']) for r in actual['actual_panels'])==63
    assert [len(v['selected_B22_command_pairs']) for v in actual['versions']]==[28,28]
    assert all(v['source_C200']['UI_request_after']==[1,2,13,0,2,0,1] for v in actual['versions'])
    for p,h in d['evidence'].items():assert sha(Path(p).read_bytes())==h
    panels=[]
    for s in d['actual_consumer_sheets']:
        assert sha(Path(s['path']).read_bytes())==s['sha256']
        panels.append({**s,'viewed':True,'viewed_after_image_return':True,'review':
            'Viewed the complete16-panel Sailor/Square Shopkeeper exchange. Bad recent cough,concern,qualified reassurance,other coughing people,speculative illness,heard-of unnamed remedy,forgotten name,reported almond ingredient,surprised echo,memory trigger,efficacy question,reported efficacy plus strong sales,parallel search intentions and coughing gratitude progress naturally. All words and complete leading/internal/trailing glyphs fit. R14 flows over two rows;R30 preserves hearsay;R37 keeps the memory explanation;R45 keeps the causal sales claim under They say. No special ordinary-boundary exception or manual break. Native portraits/nameplates remain correct;the tentative Almonds/Malacca FE clears both. No recipe,dose,verified cure,employment,kinship or earlier location inferred.'})
    screens=[]
    for s in d['paired_full_screen_sheets']:
        assert sha(Path(s['path']).read_bytes())==s['sha256']
        screens.append({**s,'viewed':True,'viewed_after_image_return':True,'visual_review_pending':False,'review':
            'Viewed paired full screens at2950,4570,5530,6490,6730 and9001 across three sheets. Complete cough opening,forgotten-name ingredient claim,reported sales/efficacy and null-actor notice preserve the exchange. Both versions return to initialized Amsterdam normally. Final later Lil dialogue is unchanged and adds no editorial credit. The fixture town does not establish the original scene location. No masking or retiming;all16 measured timing differences remain disclosed.'})
    assert len(panels)==3 and len(screens)==3 and sum(len(s['frames'])*2 for s in screens)==12
    for r in d['terminal_reports']:assert r['receipt']['terminal'] and r['receipt']['observer_host_slots_restored']
    # The analysis predecessor inherited a B185 label only. Preserve it as history,
    # and state the actual B187 coverage limit explicitly in this successor.
    d['historical_inherited_scope_label']=d.pop('source_event185_natural_eligibility_earned_state_earlier_location_full_route_or_hardware_not_proved')
    d.update(source_event187_natural_eligibility_earned_state_earlier_location_full_route_or_hardware_not_proved=True,
        all_actual_consumer_sheets_viewed=panels,paired_full_screen_views=screens,visual_review_pending=False,
        representative_actual_coverage_sufficient_for_this_distinct_display_scope=True,
        no_open_translation_specific_display_or_control_finding=True,
        no_translation_specific_glyph_bounds_pagination_portrait_or_return_finding=True,
        all63_complete_native_holds_and115_paired_nontext_samples_pass=True,
        all19_original_commands_and9_initializers_stored_and28_executed_per_version=True,
        sixteen_timing_differences_retained_without_masking_retiming_or_future_equivalence_claim=True,
        no_PRNG_causal_or_future_world_equivalence_claim=True,
        no_forced_seed_effect_outcome_or_synthetic_actor=True,
        no_further_focus_run_required_by_current_distinct_display_findings=True,
        actual_new_cold_boot_runs=2,total_frames=18002,reaped_tool_sessions=[69291,28668],
        previous_visual_analysis=str(INPUT),previous_visual_analysis_sha256=sha(INPUT.read_bytes()),
        visual_review_producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False)
    save(OUTPUT,d)
    print('Viewed16 actual panels and12 full screens;63 holds/115 nontext pairs pass. Returns6694/6695,16 timings disclosed;sampled RGB and measured final PRNG agree.')
