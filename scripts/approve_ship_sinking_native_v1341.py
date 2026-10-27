"""Approve complete native layout/font review; keep release/gameplay gates open."""
from copy import deepcopy
from pathlib import Path
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.grand_race_menu_release import sha
from scripts.ship_sinking_native_plan_v1330 import compiled
from scripts.verify_village_wrap_v608 import read,save

ROOT = Path('work/analysis/ship_sinking_native_review_v1341')
OLD = Path('translations/ship_sinking_editorial_manuscript_v3.json')
NEW = Path('translations/ship_sinking_editorial_manuscript_v4.json')
FONT = Path('work/analysis/ship_sinking_fonts_v1338/native_font_proof.json')


def main():
    assert not ROOT.exists() and not NEW.exists()
    doc,font = read(OLD),read(FONT)
    assert font['manuscript_sha256']==sha(OLD.read_bytes()) and len(font['cases'])==416 and not font['findings']
    rows = {r['message_id']:r for r in doc['records']}
    assert len(rows)==16 and len(font['sheets_for_required_visual_review'])==8
    for sheet in font['sheets_for_required_visual_review']:
        assert sha(Path(sheet['path']).read_bytes())==sheet['sha256']
    for case in font['cases']:
        assert case['compiled_hex']==compiled(rows[case['message_id']]).hex()
        assert case['complete228x64_native_and_independent_font_equal']
        assert case['uniform_visible_margin_complete_first_and_final_letters_and_bounds']
        assert not case['single_word_final_row'] and not case['weak_line_end_indices']
        if case['preview']:
            assert sha(Path(case['preview']).read_bytes())==case['preview_sha256']
    copies = Path('work/analysis/ship_sinking_copies_v1339/all_native_copies_and_prefix_cache_sequence.json')
    escape = Path('work/analysis/ship_sinking_escape_v1340/original_direct_escape_regression.json')
    assert read(copies)['complete_native_copies']==7336 and len(read(copies)['sequenced_cache_cases'])==180
    assert len(read(escape)['all13_original_direct_pipeline_cases'])==13
    assert all(read(p)['ARM9_sha256']==font['ARM9_sha256'] and read(p)['COMMON_sha256']==font['COMMON_sha256'] for p in [copies,escape])
    ROOT.mkdir(parents=True)
    visual = ROOT/'visual_and_native_review.json'
    save(visual,{'all8_native_sheets_and128_rendered_panels_actually_visually_reviewed':font['sheets_for_required_visual_review'],
        'all16_prose_templates_and8_voice_alternatives_reviewed':True,
        'all416_native_name_expansion_font_planes_equal':True,
        'zero_missing_letters_uneven_indents_internal_gaps_bounds_or_wrap_findings':True,
        'all128_PNG_previews_presented_in_the_reviewed_sheets':True,
        'no_layout_or_policy_waivers':True,
        'captured_ship_editor18_byte_bound_and_macro_like_names_verified':True,
        'scope':'Native selection,loader,printf,macro/literal handling,formatter and complete228x64 fonts. CPU file-success,UI construction and counterfactual role assignments are explicit boundaries. Actual sinking events,GPU display,dismissal and transitions remain pending.',
        'native7336_copies180_sequences13_escape_regressions_pass':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'completed_entries_added':0,'full_goal_complete':False})
    native = deepcopy(doc)
    native.update(formatting_review_pending=False,status='16-source-prose-native-font-reviewed;registered-release-and-original-gameplay-pending',
        reviewed_research_manuscript=str(OLD),reviewed_research_manuscript_sha256=sha(OLD.read_bytes()),
        native_font_proof=str(FONT),native_font_proof_sha256=sha(FONT.read_bytes()),
        native_copy_proof=str(copies),native_copy_proof_sha256=sha(copies.read_bytes()),
        escape_regression_proof=str(escape),escape_regression_proof_sha256=sha(escape.read_bytes()),
        visual_review=str(visual),visual_review_sha256=sha(visual.read_bytes()),
        no_native_formatting_release_gameplay_or_completion_approval=False,
        original_gameplay_and_registered_ROM_integration_still_pending=True)
    for row in native['records']:
        row['review']['formatting'] = True
        row['compiled_hex'] = compiled(row).hex()
        row['status'] = 'native-font-approved;registered-release-and-original-gameplay-pending'
    validate_natural_dialogue_batch(native)
    assert all(compiled(row)==compiled(rows[row['message_id']]) for row in native['records'])
    save(NEW,native)
    print('All16 sinking notices native/visually approved without waivers;registered release and original gameplay remain pending.',flush=True)


if __name__=='__main__':
    main()
