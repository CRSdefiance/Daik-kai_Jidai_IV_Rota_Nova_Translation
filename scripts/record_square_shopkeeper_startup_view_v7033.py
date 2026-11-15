"""Record the viewed registered current startup/town sheet with exact source-run provenance."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
if __name__=='__main__':
    proof=Path('work/analysis/square_shopkeeper_startup_v7033/registered_current_startup_and_town_verification.json');d=read(proof);out=proof.parent/'current_six_frame_visual_review.json'
    assert not out.exists() and d['paired_frame_count']==31 and d['all_current_requested_and_final_framebuffers_equal_V7011']
    assert sha(Path(d['review_sheet']).read_bytes())==d['review_sheet_sha256']
    save(out,dict(viewed=True,sheet=d['review_sheet'],sha256=d['review_sheet_sha256'],candidate=d['candidate'],candidate_sha256=d['candidate_sha256'],
        six_selection_opening_town_and_Refit_frames_viewed=True,no_new_display_finding=True,newgame_reused_from_exact_target7019=True,
        town_is_fresh_registered_cold_boot_with_inherited_battery=True,no_B189_B221_activation_full_route_or_hardware_claim=True,
        proof=str(proof),proof_sha256=sha(proof.read_bytes()),producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
