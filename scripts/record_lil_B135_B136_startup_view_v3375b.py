"""Record the viewed V3372 actual opening/town framebuffer sheet."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
if __name__=='__main__':
    root=Path('work/analysis/lil_B135_B136_startup_v3375');proof=root/'cold_boot_Lil_startup_town_verification.json';out=root/'current_six_frame_visual_review.json';assert not out.exists();d=read(proof);sheet=Path(d['review_sheet']);assert sha(sheet.read_bytes())==d['review_sheet_sha256'] and d['paired_frame_count']==31
    save(out,dict(viewed=True,sheet=str(sheet),sha256=sha(sheet.read_bytes()),candidate=d['candidate'],candidate_sha256=d['candidate_sha256'],review='Viewed V3372 captain-name confirmation, opening transition, Lil opening speech, Copenhagen town menu and two Refit help panels. Complete framebuffers match31 V3338 captures; no new visible text/layout regression or startup stall in these samples.',actual_scope='Two targeted headless cold boots:4001 New Game/17401 town frames. The inherited five-ship town battery remains unearned. No selected B135/B136 scene, new individual nameplate, full-route or hardware verification.',verification=str(proof),verification_sha256=sha(proof.read_bytes()),producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
