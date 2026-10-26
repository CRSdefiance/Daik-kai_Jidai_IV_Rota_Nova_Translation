"""Record the viewed six-frame current startup/town sheet without new coverage claims."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
if __name__=='__main__':
    proof=Path('work/analysis/lil_B168_startup_v4207/cold_boot_Lil_startup_town_verification.json');d=read(proof);out=proof.parent/'current_six_frame_visual_review.json';assert not out.exists()
    assert d['paired_frame_count']==31 and d['all_current_requested_and_final_framebuffers_equal_V4160'] and sha(Path(d['review_sheet']).read_bytes())==d['review_sheet_sha256']
    save(out,dict(viewed=True,sheet=d['review_sheet'],sha256=d['review_sheet_sha256'],current_candidate=d['candidate'],candidate_sha256=d['candidate_sha256'],six_selected_character_selection_Lil_opening_town_and_Refit_frames_viewed=True,no_new_display_finding=True,source_B168_not_selected=True,inherited_town_battery_not_earned_progress=True,proof=str(proof),proof_sha256=sha(proof.read_bytes()),producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
