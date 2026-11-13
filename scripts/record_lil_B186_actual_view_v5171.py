"""Record the viewed twelve actual panels and twenty paired full screens."""
from pathlib import Path
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/lil_B186_actual_review_v5170')
INPUT=ROOT/'paired_all115_samples_conditional_commands12_planes_and_final_state_analysis.json'
OUTPUT=ROOT/'all12_panels_20_fullscreens_conditional_return_and_measured_differences.json'
if __name__=='__main__':
    assert not OUTPUT.exists();d=read(INPUT);actual=read(d['actual_proof'])
    assert d['visual_review_pending'] and d['nontext_equal_samples']==115 and not d['nontext_difference_samples']
    assert d['fixture_return_frames']==[5735,5737]
    assert d['exact_timing_difference_counts']==dict(total=10,speech=4,control_or_end=6)
    assert d['whole_RGB_final9001_equal'] and not d['all_sampled_postscene_whole_RGB_equal']
    differences=d['sampled_postscene_whole_RGB_differences_unmasked']
    assert [(r['frame'],r['whole_frame_difference_bbox']) for r in differences]==[
        (6490,[225,371,239,376]),(6670,[225,371,239,376]),(7450,[224,360,240,376]),(7630,[224,360,240,376])]
    assert all(d['postscene9001_native_component_equality'].values())
    assert d['postscene9001_whole1A04_actor_models_and_captain2_equal']
    assert not d['PRNG_equality'] and d['postscene9001_PRNG_seeds']==[1803218166,2467799992]
    path=d['observed_random_path_difference'];assert path['same_control_path']
    assert path['original_effects_by_case']=={'clean_Japanese':[560],'reviewed_English':[560]}
    assert len(path['clean'])==len(path['English'])==1
    assert [(r['source_offset'],r['fixture_offset'],r['before_seed'],r['after_seed'],r['roll'],r['result']) for r in [path['clean'][0],path['English'][0]]]==[
        (540,588,2966797024,3543204249,297,0),(540,526,3543204249,4021320798,592,0)]
    assert len(actual['actual_panels'])==12 and sum(len(r['holds']) for r in actual['actual_panels'])==47
    assert [len(v['selected_B22_command_pairs']) for v in actual['versions']]==[27,27]
    for p,h in d['evidence'].items():assert sha(Path(p).read_bytes())==h
    panels=[]
    for s in d['actual_consumer_sheets']:
        assert sha(Path(s['path']).read_bytes())==s['sha256']
        panels.append({**s,'viewed_after_image_return':True,'review':
            'Viewed all12 actual panels as one Owner/Cook exchange. The missing-sweetness realization,questioning echo,light-flavor judgment,drawn-out sweet repetition,hesitant doubt,self-authority response,practical question,job retort,two perfunctory yeah-yeah replies,confident prediction and stylized laugh retain the comic progression. R13 now uses three flowing complete native rows with all words unchanged;the exact two ordinary soft wraps use the validated space. Both portraits and nameplates remain correct. Closing tentative Sweets/Alexandria FE clears portrait/name and remains complete. All leading/internal/final glyphs,punctuation,bounds and one-page consumption are intact. No recipe,ingredient,kinship,nobility or earlier conversation location is invented.'})
    screens=[]
    for index,s in enumerate(d['paired_full_screen_sheets'],1):
        assert sha(Path(s['path']).read_bytes())==s['sha256']
        review=('Viewed the full paired Japanese/English screens for the realization,revised three-row R13,perfunctory Cook reply,impersonal forecast,normal initialized Amsterdam return and later unchanged Camille tutorial. Alexandria is the forecast location only;the fixture town does not establish where the original scene occurs.' if index<=3 else
            'Viewed all complete paired difference screens. The original A-button indicator differs within x224..239/y360..375;the first two differences cover only its lower shadow at x225..238/y371..375. Every pixel outside the measured rectangle agrees. No masking,retiming or forced equality. Later dialogue adds no editorial credit.')
        screens.append({**s,'viewed_after_image_return':True,'visual_review_pending':False,'review':review})
    assert len(panels)==2 and len(screens)==5 and sum(len(s['frames'])*2 for s in screens)==20
    for r in d['terminal_reports']:assert r['receipt']['terminal'] and r['receipt']['observer_host_slots_restored']
    d.update(all_actual_consumer_sheets_viewed=panels,paired_full_screen_views=screens,visual_review_pending=False,
        representative_actual_coverage_sufficient_for_this_distinct_display_scope=True,
        no_translation_specific_glyph_bounds_pagination_portrait_or_return_finding=True,
        all47_complete_native_holds_and115_paired_nontext_samples_pass=True,
        all24_original_commands_and9_initializers_stored_actual_conditional_execution27_commands_per_version=True,
        both_unforced_native_draws_below700_select_same_source560_effect=True,
        different_measured_draws_and_final_RNG_seeds_retained_without_causal_or_future_equivalence_claim=True,
        ten_timing_and_four_original_indicator_differences_retained_without_masking_or_retiming=True,
        no_forced_seed_effect_outcome_or_synthetic_actor=True,no_further_focus_run_required_by_current_distinct_display_findings=True,
        actual_new_cold_boot_runs=2,total_frames=18002,reaped_tool_sessions=[17715,18367],
        previous_visual_analysis=str(INPUT),previous_visual_analysis_sha256=sha(INPUT.read_bytes()),
        visual_review_producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False)
    save(OUTPUT,d)
    print('Viewed12 actual panels and20 full screens;47 native holds/115 nontext pairs pass. Unforced rolls297/592 select effect560;returns5735/5737. Four original indicator differences and unequal final RNG remain disclosed.')
