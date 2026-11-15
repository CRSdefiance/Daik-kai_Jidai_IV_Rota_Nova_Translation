"""Record the seventeen viewed panels and twelve paired full screens."""
from pathlib import Path
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/lil_B189_actual_review_v5299')
INPUT=ROOT/'paired_all115_samples29_commands17_planes_and_final_state_analysis.json'
OUTPUT=ROOT/'all17_panels12_fullscreens_two_pair_return_and_measured_differences.json'
if __name__=='__main__':
    assert not OUTPUT.exists();d=read(INPUT);actual=read(d['actual_proof'])
    assert d['visual_review_pending'] and d['nontext_equal_samples']==115 and not d['nontext_difference_samples']
    assert d['fixture_return_frames']==[6937,6937] and d['exact_timing_difference_counts']==dict(total=8,speech=8,control_or_end=0)
    assert d['whole_RGB_final9001_equal'] and d['all_sampled_postscene_whole_RGB_equal'] and not d['sampled_postscene_whole_RGB_differences_unmasked']
    assert all(d['postscene9001_native_component_equality'].values()) and d['postscene9001_whole1A04_actor_models_and_captain2_equal']
    assert not d['PRNG_equality'] and d['postscene9001_PRNG_seeds']==[463267532,3723009301]
    assert len(actual['actual_panels'])==17 and sum(len(r['holds']) for r in actual['actual_panels'])==67
    assert [len(v['selected_B22_command_pairs']) for v in actual['versions']]==[29,29]
    assert all(v['source_C200']['UI_request_after']==[1,2,13,0,2,0,1] for v in actual['versions'])
    for p,h in d['evidence'].items():assert sha(Path(p).read_bytes())==h
    panels=[]
    for s in d['actual_consumer_sheets']:
        assert sha(Path(s['path']).read_bytes())==s['sha256']
        panels.append({**s,'viewed':True,'viewed_after_image_return':True,'review':
            'Viewed all17 actual panels as the complete two-pair scene. Guildmaster147/Square Shopkeeper82 discuss the recent acquisition,subjective praise,home invitation,collecting craze,scarcity and hearsay buying-up. Trader104/Port Worker113 then privately discuss the worthless-ceramics sale,unbelievable price,their own short funds and proposed approach. Four portraits/nameplates and their transition remain correct. Ten revised paragraphs and seven retentions read naturally with the comic irony intact. Two-row shorter replies and three-row market/boast/proposal paragraphs remain complete with all glyphs,punctuation,bounds and one-page consumption. The tentative Ceramics/Hamburg FE clears portrait/name. No family relationship,Chinese origin,new rank,narrator-certified valuation or second completed sale is invented.'})
    screens=[]
    for s in d['paired_full_screen_sheets']:
        assert sha(Path(s['path']).read_bytes())==s['sha256']
        screens.append({**s,'viewed':True,'viewed_after_image_return':True,'visual_review_pending':False,'review':
            'Viewed paired full screens at4330,5050,5530,6730,6970 and9001 across three sheets. Reported buying-up,the switch to the Trader,the recent worthless-ceramics sale,the impersonal forecast,normal initialized Amsterdam return and unchanged later Camille tutorial remain complete. The fixture town does not establish the original scene location;following dialogue adds no editorial credit. Eight speech timings and unequal final measured PRNG remain disclosed despite equal sampled postscene/final RGB. No masking,retiming,forced seed,causal PRNG or future-world/full-RAM equivalence claim.'})
    assert len(panels)==len(screens)==3 and sum(len(s['frames'])*2 for s in screens)==12
    for r in d['terminal_reports']:assert r['receipt']['terminal'] and r['receipt']['observer_host_slots_restored']
    d.update(all_actual_consumer_sheets_viewed=panels,paired_full_screen_views=screens,visual_review_pending=False,
        representative_actual_coverage_sufficient_for_this_distinct_display_scope=True,no_open_translation_specific_display_or_control_finding=True,
        no_translation_specific_glyph_bounds_pagination_portrait_or_return_finding=True,all67_complete_native_holds_and115_paired_nontext_samples_pass=True,
        all20_original_commands_and9_initializers_stored_and29_executed_per_version=True,four_original_speakers_and_two_pair_portrait_transition_observed=True,
        eight_speech_timing_and_unequal_final_PRNG_differences_retained_without_masking_retiming_or_equivalence_claim=True,
        no_PRNG_causal_or_future_world_equivalence_claim=True,no_forced_seed_effect_outcome_or_synthetic_actor=True,
        no_further_focus_run_required_by_current_distinct_display_findings=True,actual_new_cold_boot_runs=2,total_frames=18002,reaped_tool_sessions=[47003,51945],
        previous_visual_analysis=str(INPUT),previous_visual_analysis_sha256=sha(INPUT.read_bytes()),visual_review_producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False)
    save(OUTPUT,d)
    print('Viewed17 actual panels and12 full screens;67 holds/115 nontext pairs pass. Four-speaker transition observed;8 speech timings and unequal final PRNG disclosed.')
