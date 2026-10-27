"""Approve the15 native layouts after source/font/copy and visual review."""
from copy import deepcopy
from pathlib import Path
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/duel_special_review_v1222')
OUT = Path('translations/duel_special_editorial_manuscript_v2.json')


def main():
    assert not ROOT.exists() and not OUT.exists()
    original = Path('translations/duel_special_editorial_manuscript_v1.json')
    doc = deepcopy(read(original))
    paths = {
        'native_font_proof': 'work/analysis/duel_special_native_v1219b/native_font_scope_verification.json',
        'native_copy_proof': 'work/analysis/duel_special_copies_v1220/all_native_copies_and_prefix_cache_sequence.json',
        'escape_regression_proof': 'work/analysis/duel_special_escape_v1221/original_direct_pipeline.json',
        'dispatch_proof': 'work/analysis/duel_special_dispatch_v1217/owned_dispatch_proof.json'}
    fonts, copies, escape, dispatch = (read(paths[k]) for k in paths)
    assert len(fonts['cases']) == 51 and len(fonts['excluded_cases']) == 49
    assert copies['complete_native_copies'] == 7336 and len(copies['sequenced_cache_cases']) == 180
    assert len(escape['all13_direct_pipeline_cases']) == 13 and dispatch['exact_front_dispatch_cases'] == 131324
    assert fonts['ARM9_sha256'] == copies['ARM9_sha256'] == escape['ARM9_sha256']
    assert fonts['COMMON_sha256'] == copies['COMMON_sha256'] == escape['COMMON_sha256']
    sheet = Path(fonts['review_sheet'])
    assert sha(sheet.read_bytes()) == fonts['review_sheet_sha256']
    ROOT.mkdir(parents=True)
    visual = ROOT/'visual_review.json'
    save(visual, {
        'sheet': str(sheet), 'sheet_sha256': sha(sheet.read_bytes()),
        'all15_special_call_previews_visually_inspected': True,
        'complete_first_last_letters_and_native144x36_crop_bounds_accepted': True,
        'uniform_left_margins_no_authored_alignment_gaps_or_manual_breaks': True,
        'no_split_words_or_weak_function_word_line_ends_observed': True,
        'short_exclamation_rows_are_complete_deliberate_utterances': True,
        'single_line_centering_and_multiline_top_origin_follow_original_static_widget': True,
        'V1219_failed_escape_control_used_prose_without_source_guard': True,
        'V1219b_checks_actual_guarded_escape_bytes_without_renderer_changes': True,
        'native_CPU_boundaries_are_not_an_original_emulator_special_activation': True,
        'actual_gameplay_still_pending': True, 'producer_sha256': sha(Path(__file__).read_bytes())})
    for row in doc['records']:
        case = next(c for c in fonts['cases'] if c['message_ID'] == row['message_id'])
        row['review']['formatting'] = True
        row.update(formatted_lines=case['lines'], status='source-prose-native-format-approved;original-gameplay-pending')
    doc.update(formatting_review_pending=False, status='native-approved;registered-integration-and-gameplay-pending',
               supersedes_manuscript=str(original), supersedes_manuscript_sha256=sha(original.read_bytes()),
               target_COMMON_sha256=fonts['COMMON_sha256'], target_ARM9_sha256=fonts['ARM9_sha256'],
               visual_review=str(visual), visual_review_sha256=sha(visual.read_bytes()))
    for key, p in paths.items():
        doc[key] = p
        doc[key+'_sha256'] = sha(Path(p).read_bytes())
    validate_natural_dialogue_batch(doc)
    save(OUT, doc)
    ledger_path = Path('translations/editorial_review_current_v1.json')
    ledger = read(ledger_path)
    assert ledger['records_editorially_completed'] == 1245 and ledger['records_with_source_and_prose_pass'] == 1298
    drafts = ledger['active_source_prose_drafts']
    key = str(original)
    assert key in drafts['manuscripts']
    drafts['manuscripts'] = [str(OUT) if s == key else s for s in drafts['manuscripts']]
    subset = drafts['manuscript_record_subsets_pending'].pop(key)
    drafts['manuscript_record_subsets_pending'][str(OUT)] = subset
    ledger['duel_special_prose_v1216'].update(manuscript=str(OUT), **paths,
        visual_review=str(visual), native_formatting_pass=True,
        actual_gameplay_pending=True, completed_entries=0)
    save(ledger_path, ledger)
    print('15 native formatting gates approved;1245 complete/1298 source-prose unchanged;actual gameplay open.')


if __name__ == '__main__':
    main()
