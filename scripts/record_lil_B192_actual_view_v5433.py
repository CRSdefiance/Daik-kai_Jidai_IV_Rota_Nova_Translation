"""Record actual inspection after all returned native/paired images were viewed."""
from pathlib import Path
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/lil_B192_actual_review_v5432')
INPUT=ROOT/'paired_all115_samples20_commands8_planes_and_final_state_analysis.json'
OUTPUT=ROOT/'all8_panels26_fullscreens_linear_return_and_measured_differences.json'
DIFFERENCES=[(5530,[225,371,239,376]),(5710,[225,371,239,376]),(6310,[224,360,240,376]),
    (6730,[224,360,240,376]),(6910,[224,360,240,376]),(7450,[224,360,240,376]),(7630,[224,360,240,376])]
if __name__=='__main__':
    assert not OUTPUT.exists();d=read(INPUT);actual=read(d['actual_proof'])
    assert d['visual_review_pending'] and d['nontext_equal_samples']==115 and not d['nontext_difference_samples']
    assert d['fixture_return_frames']==[4775,4777] and d['exact_timing_difference_counts']==dict(total=9,speech=7,control_or_end=2)
    assert d['whole_RGB_final9001_equal'] and not d['all_sampled_postscene_whole_RGB_equal']
    assert [(r['frame'],r['whole_frame_difference_bbox']) for r in d['sampled_postscene_whole_RGB_differences_unmasked']]==DIFFERENCES
    assert all(d['postscene9001_native_component_equality'].values()) and d['postscene9001_whole1A04_actor_models_and_captain2_equal']
    assert not d['PRNG_equality'] and d['postscene9001_PRNG_seeds']==[790984746,3723009301]
    assert len(actual['actual_panels'])==8 and sum(len(r['holds']) for r in actual['actual_panels'])==31
    assert [len(v['selected_B22_command_pairs']) for v in actual['versions']]==[20,20]
    assert all(v['source_C200']['UI_request_after']==[1,2,13,0,2,0,1] for v in actual['versions'])
    for p,h in d['evidence'].items():assert sha(Path(p).read_bytes())==h
    panels=[]
    for s in d['actual_consumer_sheets']:
        assert sha(Path(s['path']).read_bytes())==s['sha256']
        panels.append({**s,'viewed':True,'viewed_after_image_return':True,'review':
            'Viewed all8 Sailor/Port Worker panels as the complete experience-question reversal,lack-of-chance admission,popularity hyperbole,stammered curiosity,offer,invitation and hesitant assent. R16 uses three substantial rows with the full qualified claim;R23 uses two substantial rows and a coherent continuation. R20 and R26 retain visible hesitation. All first/internal/final glyphs and punctuation fit. Correct portraits/nameplates persist;the prospective Tobacco/Istanbul FE clears them. No age,rank,kinship,health claim,smoking equipment or completed act is invented. No manual break,font,width,guard,phase or pagination change.'})
    screens=[]
    for index,s in enumerate(d['paired_full_screen_sheets'],1):
        assert sha(Path(s['path']).read_bytes())==s['sha256']
        review=('Viewed paired Japanese/English hyperbole,hesitant curiosity,offer,impersonal forecast,normal Amsterdam town return and unchanged later Camille tutorial. The fixture town does not establish the source scene location;later dialogue adds no credit.' if index<=3 else
            'Viewed full paired difference screens. Differences are confined to the measured original A-button indicator:two lower-shadow and five full-indicator rectangles. All pixels outside those rectangles agree. Text,portraits,nameplates and transitions remain complete. No masking,retiming,forced RNG,causal PRNG or future-world equivalence claim.')
        screens.append({**s,'viewed':True,'viewed_after_image_return':True,'visual_review_pending':False,'review':review})
    assert len(panels)==2 and len(screens)==7 and sum(len(s['frames'])*2 for s in screens)==26
    for r in d['terminal_reports']:assert r['receipt']['terminal'] and r['receipt']['observer_host_slots_restored']
    d.update(all_actual_consumer_sheets_viewed=panels,paired_full_screen_views=screens,visual_review_pending=False,
        representative_actual_coverage_sufficient_for_this_distinct_display_scope=True,no_open_translation_specific_display_or_control_finding=True,
        no_translation_specific_glyph_bounds_pagination_portrait_or_return_finding=True,all31_complete_native_holds_and115_paired_nontext_samples_pass=True,
        all11_original_commands_and9_initializers_stored_and20_executed_per_version=True,
        nine_timing_seven_original_indicator_and_unequal_PRNG_differences_retained_without_masking_retiming_or_equivalence_claim=True,
        no_PRNG_causal_or_future_world_equivalence_claim=True,no_forced_seed_effect_outcome_or_synthetic_actor=True,
        no_further_focus_run_required_by_current_distinct_display_findings=True,actual_new_cold_boot_runs=2,total_frames=18002,reaped_tool_sessions=[55377,31351],
        previous_visual_analysis=str(INPUT),previous_visual_analysis_sha256=sha(INPUT.read_bytes()),visual_review_producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False)
    save(OUTPUT,d)
    print('Viewed8 actual panels/26 full screens;31 holds/115 nontext pairs pass. Nine timings,seven original indicators and unequal PRNG disclosed.')
