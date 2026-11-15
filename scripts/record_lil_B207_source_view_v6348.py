"""Record the returned source images,all13 speeches and actual town return without scope inflation."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B207_source_view_v6348')
SOURCE=Path('work/analysis/lil_B207_source_actual_v6347/all13_source_speeches_all24_commands_and_complete_return.json')
if __name__=='__main__':
    assert not ROOT.exists();d=read(SOURCE);assert d['source_distinct_speech_observations']==13 and d['total_speech_observations']==13 and d['all15_source_commands_and9_original_initializers_observed'] and d['all_jobs_terminal_and_reaped'] and not d['unvisited_source_indices'] and d['exit_frame']==5976
    views=[]
    for r in d['review_sheets']+d['transition_sheets']:
        assert sha(Path(r['path']).read_bytes())==r['sha256'];views.append({**r,'viewed':True,'viewed_after_image_return':True})
    assert len(views)==4 and d['transition_sheets'][0]['frames']==[3010,6070,11001]
    assert not any(r['block']==120 and r['word']==0 for r in d['following_native_commands'])
    ROOT.mkdir(parents=True);save(ROOT/'all13_source_speeches_nameplates_and_town_return_viewed.json',dict(source_actual_proof=str(SOURCE),source_actual_proof_sha256=sha(SOURCE.read_bytes()),viewed_sheets=views,
        source_review='Viewed the complete13-speech Japanese exchange on three full bottom-screen sheets. Emilio eagerly asks for a weapon and wants to become stronger too;Lil jokes about food,explicitly says she is kidding,and asks its name. The Minotaur axe request leads to an uncertain old-island clue and her qualified search offer. His two celebrations are checked by her repeated if-I-feel-like-it condition and separate undecided-gift warning,ending in his disappointedえー. Native selectors2/14 match Lil Argot and Emilio Ferog portraits/nameplates. The displayed Emilio surname is complete and readable;its stored first F is full-width and remains a concrete encoding/metrics review lead,not yet a reason to rewrite the source name. No new age,family,rank,weapon restriction or location is inferred from portraits or staging.',
        return_review='The whole-screen transition sheet shows the source scene at3010 and a normal Amsterdam port return at6070 after B207 content exit5976. Frame11001 is following B120 sailing-lesson dialogue with black upper screen and Lil\'s readable name/text. B120 is still active;its complete end or unobstructed sailing was not observed in this11001-frame run. This is sufficient evidence of the B207-to-town return,not a full route,natural event207 activation or complete later transition proof.',
        actual_source_speeches=13,actual_source_commands=15,original_B22_initializers=9,actual_menu_cases=0,source_exit_frame=5976,complete_B207_end_observed=True,actual_town_return_frame=6070,following_B120_active_at_final_frame=True,following_B120_complete_end_not_observed=True,
        original_roster_funds_conditions_RNG_and_effect_results_unforced=True,no_natural_event207_original_location_earned_progress_full_quest_effect_route_or_hardware_claim=True,
        current_name_data_unchanged_mixed_width_F_review_still_pending=True,no_new_English_display_or_registered_release_approval=True,all_jobs_terminal_and_reaped=True,visual_review_pending=False,new_review_credit=0,new_ROMs=0,new_emulator_runs=0,evidence={**d['evidence'],str(SOURCE):sha(SOURCE.read_bytes()),str(Path(__file__)):sha(Path(__file__).read_bytes())},full_goal_complete=False));print('All13 source speeches/four sheets and normal town return viewed. Final11001 remains B120 dialogue;no full later-route or name-byte-change claim.')
