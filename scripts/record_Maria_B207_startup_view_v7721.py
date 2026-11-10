"""Record three viewed own-ROM startup sheets; retain exact captain/town/unlock scope."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/maria_B207_startup_view_v7721')
START=Path('work/analysis/maria_B207_startup_verification_v7720/own_ROM_four_NewGames_town_exact_V7660_controls_andfour_strict_inputs.json')
if __name__=='__main__':
    assert not ROOT.exists();d=read(START);assert d['whole_RGB_frame_pairs']==47 and d['actual_frames']==33405 and d['all_current_requested_andfinal_frames_equal_V7660'] and d['all_native_actor_andcaptain_controls_equal']
    assert len(d['review_sheets'])==3 and [r['measured_original_captain_ID'] for r in d['runs']]==[0,1,2,3,1]
    for s in d['review_sheets']:assert sha(Path(s['path']).read_bytes())==s['sha256']
    ROOT.mkdir(parents=True);save(ROOT/'three_own_ROM_startup_sheets_viewed.json',dict(candidate=d['candidate'],candidate_sha256=d['candidate_sha256'],startup_proof=str(START),startup_proof_sha256=sha(START.read_bytes()),viewed=True,viewed_sheets=d['review_sheets'],all47_whole_frame_pairs_native_actor_captain_controls_pass=True,actual_NewGame_captains=[0,1,2,3],actual_inherited_town_captain=1,town_frame3200_displays_Copenhagen=True,Maria_exact_system_only_unlock_earned_false=True,source_anddisposable_town_donors_unchanged=True,no_incidental_opening_names_lines_orcity_gameplay_editorial_credit=True,no_optional_activation_earned_progress_fullroute_orhardware_claim=True,all_five_jobs_terminal_andreaped=True,new_credit=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('Three V7717 startup sheets viewed:47 matching frames,allfour NewGames andCopenhagen town1. Strict own inputs anddisclosed Maria unlock/donor scope retained.')
