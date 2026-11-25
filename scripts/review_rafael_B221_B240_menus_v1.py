"""Record direct review of the three native offline caption sheets."""
from pathlib import Path

from scripts.audit_story_glyph_consistency import load, save
from scripts.check_rafael_B221_B240_menus_v1 import OUTPUT
from scripts.write_rafael_B221_B240_contextual_v1 import OUT, digest

TWO = OUTPUT / '2_option_proofs/complete_choice_objects.json'
THREE = OUTPUT / '3_option_proofs/menu_provider_and_planes.json'
REVIEW = OUTPUT / 'direct_caption_review_v1.json'
FINDINGS = {
    (224, 64): (['Yes', 'No'], 'Both short answers are centered with complete initial and final glyphs.'),
    (233, 136): (['I do.', "I don't."], 'Both answers are legible in full, including the apostrophe and final periods.'),
    (224, 242): (['Zhao Yun', 'Guan Yu', 'Zhuge Liang'],
                 'All full names are legible, including the first Z and final g of the widest label.'),
}


def main():
    assert not REVIEW.exists()
    two, three, doc = map(load, (TWO, THREE, OUT))
    assert two['all_checks_pass'] and three['complete_caption_glyphs_centering_bounds_guards_andconsumption_pass']
    assert not two['actual_gameplay'] and not three['actual_gameplay']
    assert (two['complete_caption_style_planes'], three['complete_English_caption_style_planes']) == (16, 12)
    sheets = {(item['block'], item['source_command_offset']): item['review_sheet'] for item in two['objects']}
    sheets[224, 242], = three['review_sheets']
    decisions = []
    for (block, offset), (captions, finding) in FINDINGS.items():
        sheet = sheets[block, offset]
        assert digest(Path(sheet['path'])) == sheet['sha256']
        rows = [row for row in doc['records'] if row['kind'] == 'typed-choice-label'
                and (row['block'], row['source_command_offset']) == (block, offset)]
        assert [row['english'] for row in rows] == captions
        decisions.append(dict(block=block, source_command_offset=offset, sheet=sheet, english=captions,
            record_ids=[row['id'] for row in rows], direct_visual_finding=finding))
    save(REVIEW, dict(menus=decisions, visually_reviewed_captions=7, complete_caption_style_planes=28,
        native_provider_alignments=18, bridged_modal_returns=60, actual_gameplay=False,
        stored_integration_and_actual_controller_pending=True, new_credit=0,
        evidence={str(path): digest(path) for path in (TWO, THREE, OUT, Path(__file__))}))
    print('Recorded direct review of seven captions from three menus. Stored and in-game checks are pending.')


if __name__ == '__main__':
    main()

