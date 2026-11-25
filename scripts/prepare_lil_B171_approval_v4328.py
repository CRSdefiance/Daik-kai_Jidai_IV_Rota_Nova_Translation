"""Prepare full native approval after all five B171 sheets were viewed."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT = Path('work/analysis/lil_B171_approval_tools_v4328')

if __name__ == '__main__':
    assert not ROOT.exists()
    tool = derive('scripts/approve_lil_B169_native_v4230.py', 'scripts/approve_lil_B171_native_v4328.py', {
        'all36': 'all37', 'lil_B169_layout_v2': 'lil_B171_layout_v1', 'lil_B169_profile': 'lil_B171_profile',
        'lil_B169_native_approval_v4230': 'lil_B171_native_approval_v4328',
        'lil_B169_editorial': 'lil_B171_editorial', 'lil_B169_fonts_v4229': 'lil_B171_fonts_v4327',
        "len(font['cases']) == 36 and font['current_original_macro_alignment_calls'] == 288": "len(font['cases']) == 37 and font['current_original_macro_alignment_calls'] == 296",
        "len(font['negative_controls']) == 21": "len(font['negative_controls']) == 15",
        'blocks[169]': 'blocks[171]', 'block=169': 'block=171',
        'Whole-exchange fluster/flattery, sea-rule legend, clue/ruin distinctions and tavern give-and-take remain complete.': 'Whole-exchange faint/formal introduction,self-blame,travel prohibition,expulsion,siblinglike bond,humble requests,dream uncertainty,Yifa perception and arts explanation,renewed practice and work-first comic turn remain complete. Ordinary complete-sentence wraps retain every word;no named phrase or source identity is split.',
        "{b'FI': 5, b'FO': 2}": "{b'FI': 1}",
        "{'revise':19, 'retain-wording':17}": "{'revise':24, 'retain-wording':13}",
        "sum(bool(row.get('qa_waivers')) for row in doc['records']) == 14": "sum(bool(row.get('qa_waivers')) for row in doc['records']) == 16",
        "[('FI','Lil'),('FO','Argot Co.')]": "[('FI','Lil')]",
        "['native_twelve_consumer_cases']": "['native_six_consumer_cases']", 'len(names) == 12': 'len(names) == 6',
        'current_original_macro_alignment_calls=288': 'current_original_macro_alignment_calls=296,new_current_original_macro_alignment_calls=296,reused_original_macro_alignment_calls=0',
        'progressive_planes=36': 'progressive_planes=37',
        'source_FI5_FO2_and_six_selectors_preserved': 'source_FI1_and_three_selectors_preserved',
        'three_source_predicates_one_later_numeric_A000_and_end_preserved': 'source_four_presentations_one_resource_C200_and_both_ends_preserved',
        'no_A000_recruitment_label_or_earned_flag_claim': 'no_source_A000_or2000_pause_or_earned_event_claim',
        'revised=19,retained=17': 'revised=24,retained=13',
        'current_macro_alignment_cases=288,source_consumer_negatives=21,source_macro_negatives=2': 'current_macro_alignment_cases=296,source_consumer_negatives=15,source_macro_negatives=1',
        'narrow_row_count_notes=14': 'narrow_row_count_notes=16',
        'actual_selected_B169_IDs': 'actual_selected_B171_IDs',
        'B169:36 five-gate reviews approved,19 revisions/17 retentions;36 native planes/288 cases;21+2+14 rejection controls.': 'B171:37 five-gate reviews approved,24 revisions/13 retentions;37 native planes/296 cases;15+1+14 rejection controls.',
    })
    ROOT.mkdir(parents=True)
    save(ROOT / 'source_derivation.json', dict(tool=tool, native_planes=37, total_macro_cases=296, fresh_cases=296, exact_reused_cases=0,
        revised=24, retained=13, source_consumer_negatives=15, macro_negatives=1, formatter_negatives=14,
        all_five_native_sheets_viewed=True, new_source_prose_reviews=0, new_completed_records=0, full_goal_complete=False))
