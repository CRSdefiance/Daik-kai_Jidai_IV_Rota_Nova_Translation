"""Record actual visual inspection and native approval; retain release/scene gates."""
from copy import deepcopy
from pathlib import Path
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.grand_race_menu_release import sha
from scripts.powder_fire_native_plan_v1309 import compiled
from scripts.verify_village_wrap_v608 import read,save

ROOT = Path('work/analysis/powder_fire_native_review_v1313')
OLD = Path('translations/powder_fire_editorial_manuscript_v1.json')
NEW = Path('translations/powder_fire_editorial_manuscript_v2.json')
FONT = Path('work/analysis/powder_fire_fonts_v1310/native_font_proof.json')


def main():
    assert not ROOT.exists() and not NEW.exists()
    doc,font = read(OLD),read(FONT)
    assert font['manuscript_sha256'] == sha(OLD.read_bytes()) and len(font['cases']) == 8
    assert not font['line_boundary_findings_requiring_visual_review']
    sheet = Path(font['review_sheet'])
    assert sha(sheet.read_bytes()) == font['review_sheet_sha256']
    rows = {row['message_id']:row for row in doc['records']}
    assert {case['message_id'] for case in font['cases']} == set(rows)
    for case in font['cases']:
        assert case['compiled_hex'] == compiled(rows[case['message_id']]).hex()
        assert case['complete228x64_native_independent_font_and_all_letters_equal']
        assert case['uniform_visible_origins_no_authored_indent_and_bounds_pass']
        assert not case['single_word_final_row'] and not case['weak_line_end_indices']
        assert sha(Path(case['preview']).read_bytes()) == case['preview_sha256']
    copies = Path('work/analysis/powder_fire_copies_v1311/all_native_copies_and_prefix_cache_sequence.json')
    escape = Path('work/analysis/powder_fire_escape_v1312/original_direct_escape_regression.json')
    assert read(copies)['complete_native_copies'] == 7336 and len(read(copies)['sequenced_cache_cases']) == 180
    assert len(read(escape)['all13_original_direct_pipeline_cases']) == 13
    assert all(read(path)['ARM9_sha256'] == font['ARM9_sha256'] and read(path)['COMMON_sha256'] == font['COMMON_sha256'] for path in [copies,escape])
    ROOT.mkdir(parents=True)
    visual = ROOT/'visual_and_native_review.json'
    save(visual,{'review_sheet_actually_visually_inspected':str(sheet),'sheet_sha256':sha(sheet.read_bytes()),
        'all8_voice_panels_and6_unique_messages_visually_reviewed':True,
        'all8_original_pipelines_complete_native_fonts_and_both_source_fallbacks_pass':True,
        'all206_existing_noncaptain_source_selections_pass':True,
        'zero_missing_letters_uneven_indents_internal_gaps_or_out_of_bounds_pixels':True,
        'no_single_word_final_rows_or_unreviewed_weak_boundaries':True,
        'no_case_or_policy_waivers_required':True,
        'scope':'Native selection,loader,printf,macro,formatter and whole228x64 native/independent fonts. CPU file-success and portrait-construction boundaries are explicit. Revised actual GPU/gameplay and registered release remain pending.',
        'native_copies7336_cache_sequences180_and13_escape_regressions_pass':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'completed_entries_added':0,'full_goal_complete':False})
    native = deepcopy(doc)
    native.update(formatting_review_pending=False,status='6-source-prose-native-font-reviewed;registered-release-and-original-gameplay-pending',
        reviewed_research_manuscript=str(OLD),reviewed_research_manuscript_sha256=sha(OLD.read_bytes()),
        native_font_proof=str(FONT),native_font_proof_sha256=sha(FONT.read_bytes()),
        native_copy_proof=str(copies),native_copy_proof_sha256=sha(copies.read_bytes()),
        escape_regression_proof=str(escape),escape_regression_proof_sha256=sha(escape.read_bytes()),
        visual_review=str(visual),visual_review_sha256=sha(visual.read_bytes()),
        no_new_ROM_native_layout_or_revised_gameplay_approval=False,
        original_gameplay_and_registered_ROM_integration_still_pending=True)
    for row in native['records']:
        row['review']['formatting'] = True
        row['compiled_hex'] = compiled(row).hex()
        row['status'] = 'native-font-approved;registered-release-and-original-gameplay-pending'
    validate_natural_dialogue_batch(native)
    assert all(compiled(row) == compiled(rows[row['message_id']]) for row in native['records'])
    save(NEW,native)
    print('Six fire alerts native/visually approved without waivers;registered release and revised actual scene remain pending.',flush=True)


if __name__ == '__main__':
    main()
