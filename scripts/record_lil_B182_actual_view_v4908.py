"""Seal all eight actual panels and every measured full-screen difference."""
from pathlib import Path
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/lil_B182_actual_review_v4907')
INPUT=ROOT/'paired_all115_samples_conditional_commands8_planes_and_final_state_analysis.json'
OUTPUT=ROOT/'all8_panels_48_fullscreens_conditional_return_and_measured_differences.json'
if __name__=='__main__':
    assert not OUTPUT.exists();d=read(INPUT)
    assert d['visual_review_pending'] and d['nontext_equal_samples']==115 and not d['nontext_difference_samples']
    assert d['fixture_return_frames']==[4776,4775]
    assert d['exact_timing_difference_counts']==dict(total=13,speech=7,control_or_end=6)
    assert d['whole_RGB_final9001_equal'] and not d['all_sampled_postscene_whole_RGB_equal']
    diffs=d['sampled_postscene_whole_RGB_differences_unmasked'];assert len(diffs)==18
    assert all(r['whole_frame_difference_bbox']==[224,360,240,376] for r in diffs)
    assert all(d['postscene9001_native_component_equality'].values()) and d['postscene9001_whole1A04_actor_models_and_captain2_equal']
    assert not d['PRNG_equality'] and d['postscene9001_PRNG_seeds']==[3723009301,403514907]
    path=d['observed_random_path_difference'];assert path['same_control_path']
    assert path['original_effects_by_case']=={'clean_Japanese':[532],'reviewed_English':[532]}
    assert path['clean']==path['English'][:0]+path['clean']  # The distinct fixture offsets remain recorded below.
    for row in [*path['clean'],*path['English']]:
        assert (row['source_offset'],row['before_seed'],row['after_seed'],row['roll'],row['result'])==(512,2411727400,3133977409,52,0)
    for p,h in d['evidence'].items():assert sha(Path(p).read_bytes())==h
    panels=[]
    for s in d['actual_consumer_sheets']:
        assert sha(Path(s['path']).read_bytes())==s['sha256']
        panels.append({**s,'viewed':True,'review':
            'Viewed all8 actual panels on two sheets. Two distinct generic Lady portraits and labels match the clean scene. The invitation to gossip,reported forthcoming engagement to the duke\'s son,reported extravagant ring cost,admiration for the duke,anticipated princess appearance and imitation lead naturally into competitive urgency and the admission that the stone is unknown. Six revisions and two justified wording retentions work as one exchange. The complete one-line prospective Gems/London FE clears portrait/name. Complete first/internal/final glyphs,punctuation,bounds and one-page consumption pass. No guessed stone,currency,personal names,marriage date,completed wedding or earlier London location.'})
    screens=[]
    for index,s in enumerate(d['paired_full_screen_sheets'],1):
        assert sha(Path(s['path']).read_bytes())==s['sha256']
        review=('Viewed the complete paired screens for the gossip,the comic admission,the impersonal forecast,normal initialized Amsterdam town return and following tutorial. London is the forecast location only;the fixture town does not establish the original conversation location.' if index<=3 else
            'Viewed every complete paired difference screen. The difference is the original animated A-button indicator within x224-240/y360-376. All other pixels agree in each measured frame. The following tutorial and its names/text are preserved without adding editorial credit. Nothing is masked,retimed or edited to force equality.')
        screens.append({**s,'viewed':True,'visual_review_pending':False,'review':review})
    assert len(panels)==2 and len(screens)==12 and sum(len(s['frames'])*2 for s in screens)==48
    for r in d['terminal_reports']:assert r['receipt']['terminal'] and r['receipt']['observer_host_slots_restored']
    d.update(all_actual_consumer_sheets_viewed=panels,paired_full_screen_views=screens,visual_review_pending=False,
        representative_actual_coverage_sufficient_for_this_distinct_display_scope=True,
        no_translation_specific_glyph_bounds_pagination_portrait_or_return_finding=True,
        measured_timing_RGB_and_final_RNG_differences_retained_without_equivalence_claim=True,
        no_forced_seed_effect_outcome_or_synthetic_actor=True,no_PRNG_causal_trace_or_future_world_equivalence_claim=True,
        no_further_focus_run_required_by_current_distinct_display_findings=True,
        actual_new_cold_boot_runs=2,total_frames=18002,reaped_tool_sessions=[55613,45687],
        previous_visual_analysis=str(INPUT),previous_visual_analysis_sha256=sha(INPUT.read_bytes()),
        visual_review_producer_sha256=sha(Path(__file__).read_bytes()))
    save(OUTPUT,d)
    print('Viewed8 actual panels,2 sheets and48 full screens. Both unforced rolls52 select source effect532;returns4776/4775.18 later RGB differences are original A indicators. Final RGB,five state groups and whole actor agree;unequal final RNG seeds retained.')
