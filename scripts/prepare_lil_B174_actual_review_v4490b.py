"""Bind the viewed original A-indicator to its measured exact framebuffer rectangle."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B174_actual_review_tools_v4490b')
if __name__=='__main__':
    assert not ROOT.exists()
    tool=derive('scripts/review_lil_B174_actual_v4490.py','scripts/review_lil_B174_actual_v4490b.py',{
        'lil_B174_actual_review_v4490':'lil_B174_actual_review_v4490b',
        'notice_difference is not None and 196<=notice_difference[0]<notice_difference[2]<=216 and 360<=notice_difference[1]<notice_difference[3]<=384':
            'notice_difference==(224,360,240,376)',
    })
    ROOT.mkdir(parents=True);save(ROOT/'source_derivation.json',dict(tool=tool,
        initial_wrong_indicator_rectangle_assertion_preserved=True,
        measured_exact_notice_pair_RGB_difference_rectangle=[224,360,240,376],
        original_A_button_indicator_visually_identified_in_both_current_full_screens=True,
        complete_notice_text_plane_equal=True,no_ROM_prose_capture_orobserver_change=True,full_goal_complete=False))
    print('Prepared exact measured16x16 A-indicator comparison; whole notice text and all nontext checks remain unchanged.')
