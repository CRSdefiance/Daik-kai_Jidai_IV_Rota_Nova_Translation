"""Record the returned eleven-panel and36-fullscreen visual review."""
from pathlib import Path
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/lil_B188_actual_review_v5258')
INPUT=ROOT/'paired_all115_samples23_commands11_planes_and_final_state_analysis.json'
OUTPUT=ROOT/'all11_panels36_fullscreens_linear_return_and_measured_differences.json'
DIFFERENCES=[(6250,[225,371,239,376]),(6430,[225,371,239,376]),(7450,[224,360,240,376]),(7630,[224,360,240,376]),
    (7690,[224,360,240,376]),(7870,[224,360,240,376]),(7930,[224,360,240,376]),(8110,[224,360,240,376]),
    (8410,[224,360,240,376]),(8590,[224,360,240,376]),(8770,[224,360,240,376]),(8950,[224,360,240,376])]
if __name__=='__main__':
    assert not OUTPUT.exists();d=read(INPUT);actual=read(d['actual_proof'])
    assert d['visual_review_pending'] and d['nontext_equal_samples']==115 and not d['nontext_difference_samples']
    assert d['fixture_return_frames']==[5495,5497] and d['exact_timing_difference_counts']==dict(total=11,speech=9,control_or_end=2)
    assert d['whole_RGB_final9001_equal'] and not d['all_sampled_postscene_whole_RGB_equal']
    assert [(r['frame'],r['whole_frame_difference_bbox']) for r in d['sampled_postscene_whole_RGB_differences_unmasked']]==DIFFERENCES
    assert all(d['postscene9001_native_component_equality'].values()) and d['postscene9001_whole1A04_actor_models_and_captain2_equal']
    assert not d['PRNG_equality'] and d['postscene9001_PRNG_seeds']==[403514907,1520957695]
    assert len(actual['actual_panels'])==11 and sum(len(r['holds']) for r in actual['actual_panels'])==43
    assert [len(v['selected_B22_command_pairs']) for v in actual['versions']]==[23,23]
    assert all(v['source_C200']['UI_request_after']==[1,2,13,0,2,0,1] for v in actual['versions'])
    for p,h in d['evidence'].items():assert sha(Path(p).read_bytes())==h
    panels=[]
    for s in d['actual_consumer_sheets']:
        assert sha(Path(s['path']).read_bytes())==s['sha256']
        panels.append({**s,'viewed':True,'viewed_after_image_return':True,'review':
            'Viewed all11 actual Daimyo/Guildmaster panels as one exchange. Praise,conjecture,firm agreement,personal discovery,unfamiliar-name question,giyaman/glass explanation,echo,first-person collection decision,sweeping gathering order and compliance remain distinct. The native roles support the formal my lord address without an invented new title. R22 keeps a coherent realization/complement split over two rows;R38 puts the decision and command on separate complete rows. All leading/internal/trailing glyphs and punctuation fit. Both portraits/nameplates remain correct;the tentative Glass/Osaka FE clears them. No source control,manual break,font,width,guard,phase or pagination exception.'})
    screens=[]
    for index,s in enumerate(d['paired_full_screen_sheets'],1):
        assert sha(Path(s['path']).read_bytes())==s['sha256']
        review=('Viewed paired Japanese/English praise,R22 realization,R38 collection order,impersonal notice,normal Amsterdam return and final unchanged Camille tutorial. The fixture town does not establish the original scene location;later dialogue adds no review credit.' if index<=3 else
            'Viewed complete paired difference screens. Only the original A-button indicator differs:two lower-shadow rectangles x225..238/y371..375 and ten full-indicator rectangles x224..239/y360..375. Every pixel outside the measured rectangles agrees. Text,portraits,names and transitions remain complete. No masking,retiming,forced RNG or causal/future-world equivalence claim.')
        screens.append({**s,'viewed':True,'viewed_after_image_return':True,'visual_review_pending':False,'review':review})
    assert len(panels)==2 and len(screens)==9 and sum(len(s['frames'])*2 for s in screens)==36
    for r in d['terminal_reports']:assert r['receipt']['terminal'] and r['receipt']['observer_host_slots_restored']
    d.update(all_actual_consumer_sheets_viewed=panels,paired_full_screen_views=screens,visual_review_pending=False,
        representative_actual_coverage_sufficient_for_this_distinct_display_scope=True,no_open_translation_specific_display_or_control_finding=True,
        no_translation_specific_glyph_bounds_pagination_portrait_or_return_finding=True,all43_complete_native_holds_and115_paired_nontext_samples_pass=True,
        all14_original_commands_and9_initializers_stored_and23_executed_per_version=True,
        eleven_timing_twelve_original_indicator_and_unequal_PRNG_differences_retained_without_masking_retiming_or_equivalence_claim=True,
        no_PRNG_causal_or_future_world_equivalence_claim=True,no_forced_seed_effect_outcome_or_synthetic_actor=True,
        no_further_focus_run_required_by_current_distinct_display_findings=True,actual_new_cold_boot_runs=2,total_frames=18002,reaped_tool_sessions=[3329,99190],
        previous_visual_analysis=str(INPUT),previous_visual_analysis_sha256=sha(INPUT.read_bytes()),visual_review_producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False)
    save(OUTPUT,d)
    print('Viewed11 actual panels and36 full screens;43 holds/115 nontext pairs pass. Eleven timings,twelve original indicator differences and unequal final PRNG retained.')
