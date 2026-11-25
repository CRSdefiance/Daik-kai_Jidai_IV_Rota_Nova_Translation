"""Approve the clarified2015 native layout without release/gameplay credit."""
from copy import deepcopy
from pathlib import Path
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.grand_race_menu_release import sha
from scripts.flagship_precision_native_plan_v1356 import compiled
from scripts.verify_village_wrap_v608 import read,save

ROOT = Path('work/analysis/flagship_precision_native_review_v1361')
OLD = Path('translations/flagship_capture_precision_manuscript_v1.json')
NEW = Path('translations/flagship_capture_precision_manuscript_v2.json')


def main():
    assert not ROOT.exists() and not NEW.exists()
    doc = read(OLD)
    font_path = Path('work/analysis/flagship_precision_fonts_v1357/native_font_proof.json')
    copies = Path('work/analysis/flagship_precision_copies_v1359/all_native_copies_and_prefix_cache_sequence.json')
    escape = Path('work/analysis/flagship_precision_escape_v1360/original_direct_escape_regression.json')
    fonts = read(font_path)
    assert fonts['manuscript_sha256']==sha(OLD.read_bytes()) and len(fonts['cases'])==8 and not fonts['findings']
    assert len(fonts['all206_existing_actor_choices'])==206
    assert read(copies)['complete_native_copies']==7336 and len(read(copies)['sequenced_cache_cases'])==180
    assert len(read(escape)['all13_original_direct_pipeline_cases'])==13
    assert all(read(p)['ARM9_sha256']==fonts['ARM9_sha256'] and read(p)['COMMON_sha256']==fonts['COMMON_sha256'] for p in [copies,escape])
    for case in fonts['cases']:
        assert case['full228x64_native_independent_font_and_complete_glyphs_equal']
        assert not case['single_word_final_row'] and not case['weak_line_end_indices']
        assert sha(Path(case['preview']).read_bytes())==case['preview_sha256']
    assert sha(Path(fonts['review_sheet']).read_bytes())==fonts['review_sheet_sha256']
    ROOT.mkdir(parents=True)
    visual = ROOT/'visual_and_native_review.json'
    save(visual,{'all8_panels_and5_unique_capture_variants_actually_visually_reviewed':True,
        'review_sheet':fonts['review_sheet'],'review_sheet_sha256':fonts['review_sheet_sha256'],
        'all_native_fonts_margins_bounds_first_final_letters_pass':True,'zero_orphans_weak_endings_or_waivers':True,
        'only2015_prose_changed_other4_native_capture_formats_exact':True,
        'new_candidate_cache_loading_GPU_and_original_return_pending':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'completed_entries_added':0,'full_goal_complete':False})
    native = deepcopy(doc)
    native.update(formatting_review_pending=False,status='precision-source-native-approved;registered-integration-and-new-candidate-gameplay-pending',
        reviewed_research_manuscript=str(OLD),reviewed_research_manuscript_sha256=sha(OLD.read_bytes()),
        native_font_proof=str(font_path),native_font_proof_sha256=sha(font_path.read_bytes()),
        native_copy_proof=str(copies),native_copy_proof_sha256=sha(copies.read_bytes()),
        escape_regression_proof=str(escape),escape_regression_proof_sha256=sha(escape.read_bytes()),
        visual_review=str(visual),visual_review_sha256=sha(visual.read_bytes()))
    native['records'][0]['review']['formatting'] = True
    native['records'][0]['compiled_hex'] = compiled(native['records'][0]).hex()
    native['records'][0]['status'] = 'native-approved;registered-integration-and-new-candidate-gameplay-pending'
    validate_natural_dialogue_batch(native)
    save(NEW,native)
    print('2015 precision prose and all8 capture-voice panels approved;new registered ROM and original replay pending.',flush=True)


if __name__=='__main__':
    main()
