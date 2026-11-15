"""Seal eight viewed fur panels,26 full screens and measured differences."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B185_actual_review_v5117b')
INPUT=ROOT/'paired_all115_samples20_commands8_planes_and_final_state_analysis.json'
OUTPUT=ROOT/'all2_actual_sheets8_planes_fullscreens_return_and_final_state.json'
if __name__=='__main__':
    assert not OUTPUT.exists();d=read(INPUT)
    assert d['visual_review_pending'] and d['nontext_equal_samples']==115 and not d['nontext_difference_samples']
    assert d['fixture_return_frames']==[4777,4775] and d['exact_timing_difference_counts']==dict(total=8,speech=6,control_or_end=2)
    assert d['sampled_postscene_first_frame']==4810 and not d['all_sampled_postscene_whole_RGB_equal']
    assert d['whole_RGB_final9001_equal'] and len(d['sampled_postscene_whole_RGB_differences_unmasked'])==7
    assert [(r['frame'],r['whole_frame_difference_bbox']) for r in d['sampled_postscene_whole_RGB_differences_unmasked']]==[
        (5530,[225,371,239,376]),(5710,[225,371,239,376]),(6310,[224,360,240,376]),(6730,[224,360,240,376]),
        (6910,[224,360,240,376]),(7450,[224,360,240,376]),(7630,[224,360,240,376])]
    assert all(d['postscene9001_native_component_equality'].values()) and d['postscene9001_whole1A04_actor_models_and_captain2_equal']
    assert not d['PRNG_equality'] and d['postscene9001_PRNG_seeds']==[463267532,790984746]
    assert d['all_content_jobs_terminal'] and d['actual20_of20_stored_fixture_commands_selected']
    for p,h in d['evidence'].items():assert sha(Path(p).read_bytes())==h
    panels=[]
    for s in d['actual_consumer_sheets']:
        assert sha(Path(s['path']).read_bytes())==s['sha256']
        panels.append({**s,'viewed':True,'review':
            'Viewed all8 actual panels on2 sheets as a complete exchange. Woman165 and Man164 retain distinct original portraits and complete couple nameplates. The cold complaint,recollection,fur-coat wish,freezing hyperbole,reported sales/rising prices,hearsay reply,wish for warmth and continuing coat desire flow naturally. Four retained casual turns work in context. R16 has two safe rows with all words intact;this cold and prices are going up remain coherent. R26 retains the cold-weather concession and condition. The final null-actor FE clears portrait/name and keeps Furs/Stockholm prospective. All leading/internal/final glyphs,punctuation,guards,bounds and one-page consumption match complete independent native planes. No marriage,age,kinship,date,temperature,price amount,shortage,profit guarantee,purchase,medical effect,earned boom or previous conversation location is invented.'})
    screens=[]
    for s in d['paired_full_screen_sheets']:
        assert sha(Path(s['path']).read_bytes())==s['sha256']
        screens.append({**s,'viewed':True,'visual_review_pending':False,'review':
            'Viewed all26 paired full screens after their image tool calls returned.3370 shows the coat wish and hyperbole;3610 the full reported sales/prices in two rows;4330 the restored concession;4570 the tentative Furs/Stockholm notice;4810 normal return to initialized Amsterdam town/Port;9001 the matching later Camille question. Seven later original A-indicator differences at5530/5710/6310/6730/6910/7450/7630 stay inside x224..239/y360..375,the first two affecting only its lower shadow. All115 paired upper/portrait/name samples agree without masking or retiming. Eight command timings,returns4777/4775 and PRNG463267532/790984746 differ and remain disclosed. Final RGB,five measured native groups and whole1A04 actor/captain2 agree. No causal PRNG,future-world or full-RAM equality claim. Later dialogue adds no credit. Source event185 was not naturally selected;no earned fashion,earlier conversation location,full route or hardware claim.'})
    assert len(panels)==2 and len(screens)==7 and sum(len(s['frames'])*2 for s in screens)==26
    actual=read(d['actual_proof'])
    assert sum(len(r['holds']) for r in actual['actual_panels'])==31
    for v in actual['versions']:assert v['source_C200']['UI_request_after']==[1,2,13,0,2,0,1] and v['source_C200']['UI_pending_after']==1
    d.update(all2_actual_sheets_viewed=panels,paired_full_screen_views=screens,visual_review_pending=False,
        representative_actual_coverage_sufficient_for_this_distinct_display_scope=True,no_open_translation_specific_display_or_control_finding=True,
        no_source_command_omission_flattening_or_forced_actor=True,no_additional_focus_run_without_concrete_risk=True,
        no_PRNG_causal_or_future_world_equivalence_claim=True,actual_new_cold_boot_runs=2,total_frames=18002,
        actual_C200_request_words=[1,2,13,0,2,0,1],actual_C200_pending=1,
        isolated_C200_zero_resource_fields_not_imposed_on_actual_effect_body=True,
        later_seven_original_A_indicator_differences_reviewed_without_masking_or_retiming=True,
        previous_visual_analysis=str(INPUT),previous_visual_analysis_sha256=sha(INPUT.read_bytes()),
        reaped_tool_sessions=[dict(case='clean_Japanese',session_id=99162,exit_code=0),dict(case='reviewed_English',session_id=36571,exit_code=0)],
        original_actor_getter_0xCB184_restored_in_exported_copy_analysis=True,stopped_0xCB185_analysis_producer_and_derivation_guard_preserved=True,
        visual_review_producer_sha256=sha(Path(__file__).read_bytes()))
    save(OUTPUT,d)
    print('Viewed8 panels/2 sheets/26 full screens. All20 commands and normal return pass. Eight timings,seven later A-indicator differences and unequal measured RNG retained;final RGB,native groups and whole actors agree.')
