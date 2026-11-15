"""Record the six current framebuffers viewed after the fresh cold boots."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
if __name__=='__main__':
    root=Path('work/analysis/lil_B138_startup_v3453');p=root/'current_six_frame_visual_review.json';assert not p.exists()
    proof=read(root/'cold_boot_Lil_startup_town_verification.json');sheet=Path(proof['review_sheet']);assert sha(sheet.read_bytes())==proof['review_sheet_sha256']
    save(p,dict(sheet=str(sheet),sha256=sha(sheet.read_bytes()),viewed=True,candidate=proof['candidate'],candidate_sha256=proof['candidate_sha256'],
        observations=['Lil character selection and confirmation are legible with the expected portrait and name fields.','The opening city transition and the established Lil trade-permit speech retain the expected portrait, nameplate, panel and complete visible text.','The Copenhagen town menu and Refit figurehead and bow-gun help panels remain legible, with intact menus, icons and controls.'],
        frames_viewed={'newgame':[2000,2400,4000],'town':[11900,13700,17401]},all31_whole_framebuffer_pairs_equal_V3416=proof['paired_frame_count']==31 and proof['all_current_requested_and_final_framebuffers_equal_V3416'],
        actual_selected_B138_IDs=[],targeted_headless_actual_framebuffers_not_B138_scene_or_full_playthrough=True,hardware_device_verification=False,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
