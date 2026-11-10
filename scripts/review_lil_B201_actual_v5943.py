"""Record viewed source pairs and measure exported final state without simulation claims."""
from pathlib import Path
import inspect
from collections import Counter
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_market_gameplay_v753 import state
from scripts.verify_shipyard_gameplay_v760 import models
from scripts.verify_tavern_gameplay_v767 import persistent_objects
from scripts.verify_followup_gameplay_v778 import tasks
from scripts.verify_ceremony_prayer_gameplay_v814 import calendar
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B201_actual_review_v5943')
ACTUAL=Path('work/analysis/lil_B201_actual_v5942/two_paths_all24_complete_panels_two_options_and_source_comparisons.json')
if __name__=='__main__':
    assert not ROOT.exists();d=read(ACTUAL)
    assert not d['failures'] and not d['paired_nontext_region_differences'] and not d['command_result_differences']
    assert d['actual_unique_speech_panels']==24 and d['actual_English_speech_observations']==37 and d['complete_native_holds']==144 and not d['offline_only_display_IDs']
    assert all(h['shared_source_speech_hold'] and all(h['paired_region_equality'].values()) for r in d['all_actual_speech_observations'] for h in r['holds'])
    assert [sum(h['selected_highlight_matches_return_when_visible'] for h in r['holds']) for r in d['actual_menu_cases']]==[4,2]
    versions={(v['path'],v['case']):v for v in d['versions']};measured=[];durations=[];evidence={**d['evidence'],str(ACTUAL):sha(ACTUAL.read_bytes()),str(Path(__file__)):sha(Path(__file__).read_bytes())}
    for path in ['buy','decline']:
        values=[];left,right=[versions[path,c] for c in ['clean_Japanese','reviewed_English']]
        for v in [left,right]:
            snap=v['final_readonly_RAM_snapshot'];raw=Path(snap['path']).read_bytes();assert sha(raw)==snap['sha256'] and len(raw)==4194304
            arm=NdsImage.open(v['research_ROM']).read_file('/__arm9__.bin');cpu,get=get_machine(arm,raw);actor,captain=get(0xCB184),get(0x7F244)
            assert captain==2 and 0x02000000<=actor<=0x02400000-0x1A04
            components={fn.__name__:fn(arm,raw) for fn in [state,models,persistent_objects,tasks,calendar]};components['tasks']=dict(bytes=len(components['tasks']),sha256=sha(components['tasks']))
            values.append(dict(case=v['case'],snapshot=snap,components=components,whole_actor_hex=bytes(cpu.mem_read(actor,0x1A04)).hex(),captain_ID=captain,seed=int.from_bytes(raw[0x168EB8:0x168EBC],'little')));evidence[snap['path']]=snap['sha256']
        measured.append(dict(path=path,final_frame=13001,native=values,five_native_component_equality={k:values[0]['components'][k]==values[1]['components'][k] for k in values[0]['components']},whole_actor_and_captain_equal=values[0]['whole_actor_hex']==values[1]['whole_actor_hex'],PRNG_seeds=[v['seed'] for v in values],PRNG_equal=values[0]['seed']==values[1]['seed'],source_English_exit_frames=[left['fixture_exit_frame'],right['fixture_exit_frame']]))
        for a,b in zip(left['selected_B22_command_pairs'],right['selected_B22_command_pairs'],strict=True):
            assert (a.get('original_source_offset'),a['word'],a['result_words'])==(b.get('original_source_offset'),b['word'],b['result_words'])
            da,db=a['returned']-a['start'],b['returned']-b['start']
            if da!=db:durations.append(dict(path=path,source_offset=a.get('original_source_offset'),word=a['word'],source_duration=da,English_duration=db,delta=db-da))
    views=[]
    for s in d['review_sheets']+d['transition_sheets']:
        assert sha(Path(s['path']).read_bytes())==s['sha256'];views.append({**s,'viewed':True,'viewed_after_image_return':True,'original_detail':True})
    assert len(views)==6
    for p,h in d['evidence'].items():assert sha(Path(p).read_bytes())==h
    bounds=Counter(tuple(r['whole_RGB_bbox']) for r in d['later_whole_RGB_differences'])
    ROOT.mkdir(parents=True);save(ROOT/'viewed24_panels_both_options_returns_and_measured_state_scope.json',dict(
        actual_proof=str(ACTUAL),actual_proof_sha256=sha(ACTUAL.read_bytes()),viewed_sheets=views,
        visual_review='Viewed all24 complete English speech panels, both full-screen source/English menu and return sheets. Lil doubts the worn rope and asks for it free;Carlo challenges300000 and bargains through30000/200000/50000/150000/75000 to100000. Purchase includes arrangements,deck delivery and separate Charm/Wits notices;refusal keeps the usable-rope rationale,trader complaint,apology and Spirit notice. Trader is a contextual role,not an invented personal name or kinship. All144 native-plane holds preserve first/internal/final glyphs and equal source upper,portrait,name and item regions. Buy and Pass labels are centered,complete,and visibly highlight options0/1. No clipping,overflow,unintended page,blank text page or authored premature line break found. Existing Tireless Hawser/Equipment/Sail Handle widget remains outside new title/effect fidelity credit. Both paths return to town;the buy path later shows B120 sailing dialogue with black upper screen and refusal reaches Sea View in both source and English. These later scenes add no new editorial credit.',
        actual_unique_speech_panels=24,actual_speech_observations=37,actual_menu_cases=2,complete_native_speech_holds=144,complete_visibly_selected_menu_holds=[4,2],offline_only_display_IDs=[],
        all_original_command_paths_words_and_results_equal=True,all44_original_commands_and9_initializers_observed_over_each_two_path_union=True,
        all144_complete_native_holds_match_same_frame_source_upper_portrait_name_and_picture_regions=True,
        original_funds_roster_conditions_RNG_and_effect_results_unforced_and_ordinary_gamepad_only=True,
        paired_command_timing_differences=d['command_timing_differences'],command_duration_changes=durations,within_scene_RNG_differences=d['command_RNG_differences'],
        postscene_RGB_differences=d['later_whole_RGB_differences'],postscene_difference_bounds=[dict(bounds=list(k),samples=v) for k,v in bounds.items()],
        paired_final_state_measurements=measured,original_native_getters={fn.__name__:inspect.getsource(fn) for fn in [state,models,persistent_objects,tasks,calendar]},
        native_getters_applied_to_exported_copies_only=True,no_new_emulator_boot_or_forced_state=True,
        no_pixels_masked_retimed_or_edited=True,no_causal_explanation_of_timing_RNG_or_world_differences_certified=True,
        broad_postscene_full_RAM_future_world_equivalence_unproven=True,
        original_source_payment100000_saturates35000_to0_not_earned_affordability_or_outer_eligibility_proof=True,
        actual_event201_natural_selection_original_location_full_item_effect_semantics_full_playthrough_hardware_not_claimed=True,
        no_open_translation_specific_display_menu_control_or_return_finding=True,representative_actual_coverage_sufficient_for_this_distinct_display_scope=True,
        no_further_focus_run_required_by_current_distinct_display_findings=True,
        new_successful_English_runs=2,new_successful_English_frames=26002,reused_prior_source_runs=2,reused_prior_source_frames=26002,total_successful_frames=52004,
        terminal_reaped_English_tool_sessions=[29410,91880],all_failed_producers_and_intermediate_outputs_preserved=True,
        visual_review_pending=False,new_editorial_credit=0,evidence=evidence,full_goal_complete=False))
    print([(r['path'],r['five_native_component_equality'],r['whole_actor_and_captain_equal'],r['PRNG_seeds'],r['source_English_exit_frames']) for r in measured]);print('Six sheets viewed;24 panels/37 observations/144 complete holds/two options accepted within disclosed display/control/return scope.')
