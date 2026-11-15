"""Seal nine viewed tea panels,twenty full screens and disclosed timing differences."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B184_actual_review_v5071')
INPUT=ROOT/'paired_all115_samples21_commands9_planes_and_final_state_analysis.json'
OUTPUT=ROOT/'all2_actual_sheets9_planes_fullscreens_return_and_final_state.json'

if __name__=='__main__':
    assert not OUTPUT.exists();d=read(INPUT)
    assert d['visual_review_pending'] and d['nontext_equal_samples']==115 and not d['nontext_difference_samples']
    assert d['fixture_return_frames']==[5014,5015] and d['exact_timing_difference_counts']==dict(total=8,speech=6,control_or_end=2)
    assert d['sampled_postscene_first_frame']==5050 and not d['all_sampled_postscene_whole_RGB_equal']
    assert d['whole_RGB_final9001_equal'] and len(d['sampled_postscene_whole_RGB_differences_unmasked'])==4
    assert [(r['frame'],r['whole_frame_difference_bbox']) for r in d['sampled_postscene_whole_RGB_differences_unmasked']]==[
        (6970,[224,360,240,376]),(7150,[224,360,240,376]),(7690,[224,360,240,376]),(7870,[224,360,240,376])]
    assert all(d['postscene9001_native_component_equality'].values()) and d['postscene9001_whole1A04_actor_models_and_captain2_equal']
    assert d['PRNG_equality'] and d['postscene9001_PRNG_seeds']==[403514907,403514907]
    assert d['all_content_jobs_terminal'] and d['actual21_of21_stored_fixture_commands_selected']
    for p,h in d['evidence'].items():assert sha(Path(p).read_bytes())==h
    panels=[]
    for s in d['actual_consumer_sheets']:
        assert sha(Path(s['path']).read_bytes())==s['sha256']
        panels.append({**s,'viewed':True,'review':
            'Viewed all9 actual panels on2 sheets as one exchange. Woman165 and Man164 retain distinct original portraits and complete couple nameplates. Personal pleasure,delayed-popularity observation,dry agreement,polite household errand,willing reply,relaxed calm and gentle hyperbole progress naturally. R14 has two safe rows,catch on sooner intact and every word unchanged from approved prose. R22 keeps the complete buy-tomorrow question together on row2. The closing null-actor FE clears portrait/name and preserves tentative Tea/Sofala notice. All leading/internal/final glyphs,punctuation,guards,bounds and one-page consumption match independent native planes. Five individual retentions work in context. No marriage,age,kinship,city shortage,cargo depletion,price,profit,earned boom,medical effect or prior household location is invented.'})
    screens=[]
    for s in d['paired_full_screen_sheets']:
        assert sha(Path(s['path']).read_bytes())==s['sha256']
        screens.append({**s,'viewed':True,'visual_review_pending':False,'review':
            'Viewed all20 paired full screens.3370 shows the revised two-row observation;3850 the complete household request;4090 the willing reply;4810 the impersonal prospective Tea/Sofala notice.5050 shows normal return to initialized Amsterdam town/Port;9001 shows matching later sailing instructions. Four later original A-indicator differences at6970/7150/7690/7870 are confined to x224..239/y360..375. They are preserved without masking or retiming;all115 upper/portrait/name samples agree. Eight command timings and returns5014/5015 differ. Five measured native groups,whole1A04 actor/captain2,final RGB and PRNG403514907 agree. No causal PRNG,future-world or full-RAM equivalence claim. Subsequent dialogue adds no editorial credit. Source event184 was not naturally selected;no earned fashion,earlier household location,full route or hardware claim.'})
    assert len(panels)==2 and len(screens)==5 and sum(len(s['frames'])*2 for s in screens)==20
    actual=read(d['actual_proof'])
    for v in actual['versions']:
        assert v['source_C200']['UI_request_after']==[1,2,13,0,2,0,1] and v['source_C200']['UI_pending_after']==1
    d.update(all2_actual_sheets_viewed=panels,paired_full_screen_views=screens,visual_review_pending=False,
        representative_actual_coverage_sufficient_for_this_distinct_display_scope=True,no_open_translation_specific_display_or_control_finding=True,
        no_source_command_omission_flattening_or_forced_actor=True,no_additional_focus_run_without_concrete_risk=True,
        no_PRNG_causal_or_future_world_equivalence_claim=True,actual_new_cold_boot_runs=2,total_frames=18002,
        actual_C200_request_words=[1,2,13,0,2,0,1],actual_C200_pending=1,
        isolated_C200_zero_resource_fields_not_imposed_on_actual_effect_body=True,
        later_four_original_A_indicator_differences_reviewed_without_masking_or_retiming=True,
        previous_visual_analysis=str(INPUT),previous_visual_analysis_sha256=sha(INPUT.read_bytes()),
        reaped_tool_sessions=[dict(case='clean_Japanese',session_id=3993,exit_code=0),dict(case='reviewed_English',session_id=7174,exit_code=0)],
        visual_review_producer_sha256=sha(Path(__file__).read_bytes()))
    save(OUTPUT,d)
    print('Viewed9 panels/2 sheets/20 full screens. All21 commands and normal return pass. Eight timing/four later A-indicator differences retained;final RGB,native groups,actors and measured RNG agree. No further display/control risk.')
