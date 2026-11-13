"""Record the viewed six-frame current3300 headless gameplay sheet."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
if __name__=='__main__':
    root=Path('work/analysis/lil_B122_B127_startup_v3303');proof=root/'cold_boot_Lil_startup_town_verification.json';out=root/'current_six_frame_visual_review.json';assert not out.exists();d=read(proof);sheet=Path(d['review_sheet']);assert sha(sheet.read_bytes())==d['review_sheet_sha256'] and d['paired_frame_count']==31
    save(out,dict(viewed=True,sheet=str(sheet),sha256=sha(sheet.read_bytes()),candidate=d['candidate'],candidate_sha256=d['candidate_sha256'],review='Viewed current3300 captain-name confirmation,opening transition,Lil opening speech,Copenhagen town menu andtwo Refit help panels. Complete text/framebuffer shapes agree with scoped31-frame V3251 comparison;no startup stall ornew visible text/layout regression in these samples.',actual_scope='Two targeted headless cold boots:4001 NewGame/17401 town frames. Inherited five-ship town battery is not earned progression;no selected B122-B127 scene,full-route orhardware claim.',verification=str(proof),verification_sha256=sha(proof.read_bytes()),producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
