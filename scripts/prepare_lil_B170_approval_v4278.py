"""Prepare five-gate approval for all33 current native source-bound B170 speeches."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B170_approval_tools_v4278')
if __name__=='__main__':
    assert not ROOT.exists()
    tool=derive('scripts/approve_lil_B169_native_v4230.py','scripts/approve_lil_B170_native_v4278.py',{
        'all36':'all33','lil_B169_layout_v2':'lil_B170_layout_v2','lil_B169_profile':'lil_B170_profile',
        'lil_B169_native_approval_v4230':'lil_B170_native_approval_v4278',
        'lil_B169_editorial_manuscript_v3':'lil_B170_editorial_manuscript_v4',
        'lil_B169_editorial_manuscript_v4':'lil_B170_editorial_manuscript_v5',
        'lil_B169_fonts_v4229':'lil_B170_fonts_v4277',
        "len(font['cases']) == 36 and font['current_original_macro_alignment_calls'] == 288":"len(font['cases']) == 33 and font['current_original_macro_alignment_calls'] == 264",
        "len(font['negative_controls']) == 21":"len(font['negative_controls']) == 13",
        'blocks[169]':'blocks[170]',
        'Whole-exchange fluster/flattery, sea-rule legend, clue/ruin distinctions and tavern give-and-take remain complete.':'Whole-exchange collision/argument,apology/flattery,Admiral/fleet explanation,Taoist practice,qualified sympathy,resolve test,passage request and final encouragement remain complete.',
        'block=169':'block=170',"{b'FI': 5, b'FO': 2}":"{b'FI': 1, b'FO': 1}",
        "{'revise':19, 'retain-wording':17}":"{'revise':21, 'retain-wording':12}",
        "sum(bool(row.get('qa_waivers')) for row in doc['records']) == 14":"sum(bool(row.get('qa_waivers')) for row in doc['records']) == 11",
        "['native_twelve_consumer_cases']":"['native_four_consumer_cases']",'len(names) == 12':'len(names) == 4',
        'current_original_macro_alignment_calls=288':'current_original_macro_alignment_calls=264,new_current_original_macro_alignment_calls=16,reused_original_macro_alignment_calls=248',
        'progressive_planes=36':'progressive_planes=33',
        'source_FI5_FO2_and_six_selectors_preserved':'source_FI1_FO1_and_two_selectors_preserved',
        'three_source_predicates_one_later_numeric_A000_and_end_preserved':'source_pause_C200_two_resources_one_later_A000_and_both_ends_preserved',
        'revised=19,retained=17':'revised=21,retained=12',
        'current_macro_alignment_cases=288,source_consumer_negatives=21':'current_macro_alignment_cases=264,source_consumer_negatives=13',
        'narrow_row_count_notes=14':'narrow_row_count_notes=11',
        'actual_selected_B169_IDs':'actual_selected_B170_IDs',
        'B169:36 five-gate reviews approved,19 revisions/17 retentions;36 native planes/288 cases;21+2+14 rejection controls.':'B170:33 five-gate reviews approved,21 revisions/12 retentions;33 native planes/264 cases;13+2+14 rejection controls.',
    })
    ROOT.mkdir(parents=True)
    save(ROOT/'source_derivation.json',dict(tool=tool,native_planes=33,total_macro_cases=264,fresh_cases=16,exact_reused_cases=248,
        revised=21,retained=12,source_consumer_negatives=13,macro_negatives=2,formatter_negatives=14,
        new_source_prose_reviews=0,new_completed_records=0,full_goal_complete=False))
    print('B170 native approval producer prepared;all33 source/context/English decisions and five viewed sheets required.')
