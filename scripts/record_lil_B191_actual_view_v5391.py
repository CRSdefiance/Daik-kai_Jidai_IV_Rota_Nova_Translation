"""Record all13 viewed panels and20 fullscreens,including the actual no-effect path."""
from pathlib import Path
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/lil_B191_actual_review_v5390')
INPUT=ROOT/'paired_all115_samples_conditional_commands13_planes_and_final_state_analysis.json'
OUTPUT=ROOT/'all13_panels_20_fullscreens_no_effect_path_return_and_measured_differences.json'
if __name__=='__main__':
    assert not OUTPUT.exists();d=read(INPUT);actual=read(d['actual_proof'])
    assert d['fixture_return_frames']==[5977,5975] and d['exact_timing_difference_counts']==dict(total=12,speech=10,control_or_end=2)
    assert d['nontext_equal_samples']==115 and not d['nontext_difference_samples']
    assert [(r['frame'],r['whole_frame_difference_bbox']) for r in d['sampled_postscene_whole_RGB_differences_unmasked']]==[
        (6730,[225,371,239,376]),(6910,[225,371,239,376]),(7690,[224,360,240,376]),(7870,[224,360,240,376])]
    assert d['whole_RGB_final9001_equal'] and not d['all_sampled_postscene_whole_RGB_equal']
    assert not d['PRNG_equality'] and d['postscene9001_PRNG_seeds']==[759362961,1803218166]
    assert all(d['postscene9001_native_component_equality'].values()) and d['postscene9001_whole1A04_actor_models_and_captain2_equal']
    path=d['observed_random_path_difference'];assert path['same_control_path'] and path['clean']==path['English']
    assert path['original_effects_by_case']=={'clean_Japanese':[],'reviewed_English':[]}
    assert [(r['source_offset'],r['fixture_offset'],r['roll'],r['result'],r['threshold']) for r in path['clean']]==[(8,56,875,2,500),(76,124,988,2,500)]
    assert len(actual['actual_panels'])==13 and sum(len(r['holds']) for r in actual['actual_panels'])==51
    assert [len(v['selected_B22_command_pairs']) for v in actual['versions']]==[34,34]
    assert all(not v['source_A000'] and v['source_C200'][0]['result_words']==[3,2] and v['selected_B22_command_pairs'][-1]['result_words']==[0,2] for v in actual['versions'])
    for p,h in d['evidence'].items():assert sha(Path(p).read_bytes())==h
    panels=[]
    for s in d['actual_consumer_sheets']:
        assert sha(Path(s['path']).read_bytes())==s['sha256']
        panels.append({**s,'viewed_after_image_return':True,'review':'Viewed all13 Shopkeeper/Sailor panels as one exchange:admired color,competing-shop buyout warning,hesitation,urgent challenge,sellout doubt,popularity/depletion claim,repeated You think?/assurances,reluctant delegation and cajoling profit condition. R64 keeps the full question together in two substantial rows with every word intact. R88 removes unsupported Dad and avoids joint ownership while retaining the familiar appeal and source-explicit profit pitch. Correct portraits/nameplates and complete leading/internal/trailing glyphs,punctuation,bounds and single-page text remain. The tentative Dyes/Calicut FE clears portrait/name;it does not establish earlier location or earned fashion.'})
    screens=[]
    for i,s in enumerate(d['paired_full_screen_sheets'],1):
        assert sha(Path(s['path']).read_bytes())==s['sha256']
        review=('Viewed full Japanese/English pairs for the restored buyout warning,two-row R64 question,kinship-free R88 condition,impersonal notice,normal initialized Amsterdam return and later unchanged Camille tutorial. Calicut belongs to the forecast only;later dialogue adds no credit.' if i<=3 else 'Viewed all four complete later indicator-difference pairs. Frames6730/6910 differ only in the original A-button lower shadow x225..238/y371..375;7690/7870 differ within the full indicator x224..239/y360..375. No pixel masking,retiming or forced outcome.')
        screens.append({**s,'viewed_after_image_return':True,'visual_review_pending':False,'review':review})
    assert len(panels)==3 and len(screens)==5 and sum(len(s['frames'])*2 for s in screens)==20
    for r in d['terminal_reports']:assert r['receipt']['terminal'] and r['receipt']['observer_host_slots_restored']
    carry=Path('work/analysis/lil_B191_carried_result_v5392/all15_C200_and15_end_prior_result_cases.json');proof=read(carry)
    assert len(proof['cases'])==15 and proof['original_interpreter_preserves_caller_second_result_word']
    d.update(all_actual_consumer_sheets_viewed=panels,paired_full_screen_views=screens,visual_review_pending=False,
        representative_actual_coverage_sufficient_for_this_distinct_display_scope=True,
        no_translation_specific_glyph_bounds_pagination_portrait_or_return_finding=True,
        all51_complete_native_holds_and115_paired_nontext_samples_pass=True,
        all38_original_commands_and9_initializers_stored_actual_conditional_execution34_commands_per_version=True,
        both_actual_rolls875_988_at8_76_return2_skip700_at28_and_apply_no_source_A000=True,
        four_source_effect_alternatives_native_structural_only_not_actually_executed=True,
        original_carried_result2_C200_3_2_and_end_0_2_preserved=True,
        twelve_timing_four_indicator_and_unequal_final_PRNG_differences_retained_without_masking_retiming_or_equivalence_claim=True,
        no_forced_seed_effect_outcome_or_synthetic_actor=True,no_further_focus_run_required_by_current_distinct_display_findings=True,
        carried_result_proof=str(carry),carried_result_proof_sha256=sha(carry.read_bytes()),
        actual_new_cold_boot_runs=2,total_frames=18002,reaped_tool_sessions=[43428,74591],
        previous_visual_analysis=str(INPUT),previous_visual_analysis_sha256=sha(INPUT.read_bytes()),
        visual_review_producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False)
    save(OUTPUT,d)
    print('Viewed13 panels/20fullscreens;51holds/115nontext pairs pass. Rolls875/988 select original no-effect path;returns5977/5975. Twelve timings,four indicators and unequal final PRNG disclosed.')
