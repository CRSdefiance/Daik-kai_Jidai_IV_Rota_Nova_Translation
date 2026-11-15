"""Record all17 viewed actual panels and16 full paired screens with measured limits."""
from pathlib import Path
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/lil_B190_actual_review_v5341b')
INPUT=ROOT/'paired_all115_samples_conditional_commands17_planes_and_final_state_analysis.json'
OUTPUT=ROOT/'all17_panels_16_fullscreens_conditional_return_and_measured_differences.json'
if __name__=='__main__':
    assert not OUTPUT.exists();d=read(INPUT);actual=read(d['actual_proof'])
    assert d['fixture_return_frames']==[6934,6937] and d['exact_timing_difference_counts']==dict(total=9,speech=7,control_or_end=2)
    assert d['nontext_equal_samples']==115 and not d['nontext_difference_samples']
    assert [(r['frame'],r['whole_frame_difference_bbox']) for r in d['sampled_postscene_whole_RGB_differences_unmasked']]==[(7690,[225,371,239,376]),(7870,[225,371,239,376])]
    assert d['whole_RGB_final9001_equal'] and not d['all_sampled_postscene_whole_RGB_equal']
    assert d['PRNG_equality'] and d['postscene9001_PRNG_seeds']==[2467799992,2467799992]
    assert all(d['postscene9001_native_component_equality'].values()) and d['postscene9001_whole1A04_actor_models_and_captain2_equal']
    path=d['observed_random_path_difference'];assert path['same_control_path']
    assert path['original_effects_by_case']=={'clean_Japanese':[52],'reviewed_English':[52]}
    assert path['clean']==path['English'] and [(r['source_offset'],r['fixture_offset'],r['roll'],r['result']) for r in path['clean']]==[(8,56,875,2)]
    assert len(actual['actual_panels'])==17 and sum(len(r['holds']) for r in actual['actual_panels'])==67
    assert [len(v['selected_B22_command_pairs']) for v in actual['versions']]==[34,34]
    assert all(v['selected_B22_command_pairs'][-1]['result_words']==[0,2] and v['source_C200'][0]['result_words']==[3,2] for v in actual['versions'])
    for p,h in d['evidence'].items():assert sha(Path(p).read_bytes())==h
    panels=[]
    for s in d['actual_consumer_sheets']:
        assert sha(Path(s['path']).read_bytes())==s['sha256']
        panels.append({**s,'viewed_after_image_return':True,'review':'Viewed all17 actual Sailor/Port Worker panels as one exchange:opening gossip,residence owner,unknown-cause illness,common-knowledge dismissal,later-development question,reported store-bought one-go cure,surprise,explicit skepticism,apparent-truth reply and panacea reputation,personal wish and proposed shopping. All English leading/internal/final glyphs and punctuation are complete. The substantial one/two-row paragraphs preserve meanings without manual breaks. Correct portraits/nameplates remain;tentative Medicine/Havana FE clears both. No purchase,use,recovery,rank,kinship or earlier location is invented.'})
    screens=[]
    for i,s in enumerate(d['paired_full_screen_sheets'],1):
        assert sha(Path(s['path']).read_bytes())==s['sha256']
        review=('Viewed full Japanese/English paired screens for the mansion owner,reported retail cure,explicit doubt,impersonal notice,normal initialized Amsterdam return and later unchanged Camille tutorial. Havana names the forecast only. Later dialogue adds no editorial credit.' if i<=3 else 'Viewed both complete later indicator-difference pairs at7690/7870. Differences are confined to the original A-button indicator lower shadow x225..238/y371..375. All other pixels agree;no masking or retiming.')
        screens.append({**s,'viewed_after_image_return':True,'visual_review_pending':False,'review':review})
    assert len(panels)==3 and len(screens)==4 and sum(len(s['frames'])*2 for s in screens)==16
    for r in d['terminal_reports']:assert r['receipt']['terminal'] and r['receipt']['observer_host_slots_restored']
    carry=Path('work/analysis/lil_B190_carried_result_v5340b/all15_C200_and15_end_prior_result_cases.json')
    proof=read(carry);assert len(proof['cases'])==15 and proof['original_interpreter_preserves_caller_second_result_word']
    d.update(all_actual_consumer_sheets_viewed=panels,paired_full_screen_views=screens,visual_review_pending=False,
        representative_actual_coverage_sufficient_for_this_distinct_display_scope=True,
        no_translation_specific_glyph_bounds_pagination_portrait_or_return_finding=True,
        all67_complete_native_holds_and115_paired_nontext_samples_pass=True,
        all29_original_commands_and9_initializers_stored_actual_conditional_execution34_commands_per_version=True,
        both_unforced_native_roll875_result2_select_source52_effect=True,
        original_carried_result2_C200_3_2_and_end_0_2_preserved=True,
        nine_timing_and_two_original_indicator_shadow_differences_retained_without_masking_or_retiming=True,
        measured_final_PRNG_equality_not_future_world_or_full_RAM_equivalence=True,
        no_forced_seed_effect_outcome_or_synthetic_actor=True,no_further_focus_run_required_by_current_distinct_display_findings=True,
        carried_result_proof=str(carry),carried_result_proof_sha256=sha(carry.read_bytes()),
        actual_new_cold_boot_runs=2,total_frames=18002,reaped_tool_sessions=[28865,55853],
        previous_visual_analysis=str(INPUT),previous_visual_analysis_sha256=sha(INPUT.read_bytes()),
        visual_review_producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False)
    save(OUTPUT,d)
    print('Viewed17 panels/16 fullscreens;67 holds/115 nontext pairs pass. Roll875/result2/effect52;returns6934/6937. Nine timings/two indicator shadows disclosed;final measured PRNG agrees.')
