"""Record the returned fifteen-panel and twelve-fullscreen cooking review."""
from pathlib import Path
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/lil_B193_actual_review_v5473')
INPUT=ROOT/'paired_all115_samples27_commands15_planes_and_final_state_analysis.json'
OUTPUT=ROOT/'all15_panels12_fullscreens_three_Ladies_return_and_measured_differences.json'
if __name__=='__main__':
    assert not OUTPUT.exists();d=read(INPUT);actual=read(d['actual_proof'])
    assert d['visual_review_pending'] and d['nontext_equal_samples']==115 and not d['nontext_difference_samples']
    assert d['fixture_return_frames']==[6457,6457] and d['exact_timing_difference_counts']==dict(total=10,speech=10,control_or_end=0)
    assert d['whole_RGB_final9001_equal'] and d['all_sampled_postscene_whole_RGB_equal'] and not d['sampled_postscene_whole_RGB_differences_unmasked']
    assert all(d['postscene9001_native_component_equality'].values()) and d['postscene9001_whole1A04_actor_models_and_captain2_equal']
    assert d['PRNG_equality'] and d['postscene9001_PRNG_seeds']==[463267532,463267532]
    assert len(actual['actual_panels'])==15 and sum(len(r['holds']) for r in actual['actual_panels'])==59
    assert [len(v['selected_B22_command_pairs']) for v in actual['versions']]==[27,27]
    assert all(v['source_C200']['UI_request_after']==[1,2,13,0,2,0,1] for v in actual['versions'])
    for p,h in d['evidence'].items():assert sha(Path(p).read_bytes())==h
    panels=[]
    for s in d['actual_consumer_sheets']:
        assert sha(Path(s['path']).read_bytes())==s['sha256']
        panels.append({**s,'viewed':True,'viewed_after_image_return':True,'review':
            'Viewed all15 panels as the whole three-Lady cooking exchange. The three distinct portraits bind source selectorsA6/A7/A8;Lady names remain correct. The lone question mark is complete. R25 displays all four required rows through local ingredients,including reported classification. R37 keeps relief and tentative first-person tonight plan;R44 offers immediate cooking instruction;R55 retains explicit friendship. Every first/internal/final glyph and punctuation fits. The prospective chilies/Seoul FE clears portrait and name. No manual break,font,width,guard,phase or pagination exception.'})
    screens=[]
    for s in d['paired_full_screen_sheets']:
        assert sha(Path(s['path']).read_bytes())==s['sha256']
        screens.append({**s,'viewed':True,'viewed_after_image_return':True,'visual_review_pending':False,'review':
            'Viewed full paired source/English meal praise,four-row ingredient explanation,cooking offer and prospective notice. Normal Amsterdam town return and unchanged later Camille tutorial remain complete. All sampled postscene whole RGB agrees,without masking or retiming. The B22 fixture town does not establish original location;later dialogue adds no credit. Ten source/English speech timings still differ. Final equal PRNG is a measured result,not causal,future-world or full-RAM equivalence.'})
    assert len(panels)==len(screens)==3 and sum(len(s['frames'])*2 for s in screens)==12
    for r in d['terminal_reports']:assert r['receipt']['terminal'] and r['receipt']['observer_host_slots_restored']
    d.update(all_actual_consumer_sheets_viewed=panels,paired_full_screen_views=screens,visual_review_pending=False,
        representative_actual_coverage_sufficient_for_this_distinct_display_scope=True,no_open_translation_specific_display_or_control_finding=True,
        no_translation_specific_glyph_bounds_pagination_portrait_or_return_finding=True,all59_complete_native_holds_and115_paired_nontext_samples_pass=True,
        all18_original_commands_and9_initializers_stored_and27_executed_per_version=True,
        ten_speech_timing_differences_retained_without_masking_retiming_or_equivalence_claim=True,
        three_distinct_original_Lady_portraits_and_four_row_explanation_cooking_offer_and_friendship_observed=True,
        no_PRNG_causal_or_future_world_equivalence_claim=True,no_forced_seed_effect_outcome_or_synthetic_actor=True,
        no_further_focus_run_required_by_current_distinct_display_findings=True,actual_new_cold_boot_runs=2,total_frames=18002,reaped_tool_sessions=[41974,91056],
        previous_visual_analysis=str(INPUT),previous_visual_analysis_sha256=sha(INPUT.read_bytes()),visual_review_producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False)
    save(OUTPUT,d);print('Viewed15 panels/12 full screens;59 holds/115 nontext pairs pass. Ten speech timings differ;postscene/final RGB and measured final PRNG agree.')
