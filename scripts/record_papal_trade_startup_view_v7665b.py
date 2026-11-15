"""Record viewed own-ROM startup sheets and correct historical town-location shorthand."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/papal_trade_startup_view_v7665b')
START=Path('work/analysis/papal_trade_startup_verification_v7664c/own_ROM_three_NewGames_town_exact_prior_comparisons.json')
if __name__=='__main__':
    assert not ROOT.exists();d=read(START);assert d['whole_RGB_frame_pairs']==40 and d['all_current_requested_andfinal_frames_equal_V7611'] and d['all_native_actor_andcaptain_controls_equal']
    assert len(d['review_sheets'])==2 and [r['measured_original_captain_ID'] for r in d['runs']]==[0,1,2,1]
    for s in d['review_sheets']:assert sha(Path(s['path']).read_bytes())==s['sha256']
    ROOT.mkdir(parents=True);save(ROOT/'two_own_ROM_startup_sheets_viewed_scope_corrected.json',dict(candidate=d['candidate'],candidate_sha256=d['candidate_sha256'],startup_proof=str(START),startup_proof_sha256=sha(START.read_bytes()),viewed=True,viewed_sheets=d['review_sheets'],all40_whole_frame_pairs_andnative_actor_captain_controls_pass=True,actual_NewGame_captains=[0,1,2],actual_inherited_town_captain=1,town_frame3200_displays_Copenhagen=True,historical_Stockholm_town_shorthand_corrected=True,Stockholm_belongs_to_separate_Hodram_opening_initialized_scene_not_this_town_capture=True,historical_town_plan_Lil_route2_label_preserved_andexplicitly_superseded=True,original_pointer_mode_mismatch_runs_andfailed_7664_7664b_comparisons_preserved=True,matching_pointer_route0_route1_successors_andunchanged_Lil_town_runs_verified_without_guard_relaxation=True,no_incidental_opening_names_lines_orcity_gameplay_editorial_credit=True,no_optional_activation_earned_progress_fullroute_orhardware_claim=True,all_runs_terminal_andreaped=True,new_credit=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
