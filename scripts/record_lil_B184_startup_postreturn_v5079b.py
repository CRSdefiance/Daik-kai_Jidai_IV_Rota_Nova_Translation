"""Record visual approval after the displayed six-frame image has returned."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B184_startup_v5079')
if __name__=='__main__':
    output=ROOT/'current_six_frame_postreturn_visual_review.json';assert not output.exists()
    earlier=ROOT/'current_six_frame_visual_review.json';proof=ROOT/'cold_boot_Lil_startup_town_verification.json'
    d=read(earlier);p=read(proof)
    assert p['paired_frame_count']==31 and p['all_current_requested_and_final_framebuffers_equal_V5030']
    assert d['sha256']==p['review_sheet_sha256']==sha(Path(d['sheet']).read_bytes())
    d.update(previous_early_view_receipt=str(earlier),previous_early_view_receipt_sha256=sha(earlier.read_bytes()),
        previous_receipt_ordering_note='The earlier receipt ran in the same tool call that emitted the image,before the model received that image. Preserve it as an ordering diagnostic;this successor follows actual inspection after tool return.',
        inspected_after_image_tool_return=True,
        visual_review='Viewed the full six-frame sheet after image return:captain selection2000,Amsterdam setup2400,Lil opening4000,Copenhagen town11900,Figurehead13700 and Bow Gun17401. Portrait/name,text,leading/final glyphs,menus and established graphics are complete in these samples. All31 whole frame pairs/five actor controls remain exact to V5030;no new display finding. Inherited town battery does not establish earned progression;B184 natural event is not selected.',
        proof=str(proof),proof_sha256=sha(proof.read_bytes()),producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False)
    save(output,d)
