"""Seal direct visual review of final dialogue pages, names and captions."""
from pathlib import Path

from scripts import assemble_rafael_B241_B260_offline_v1 as initial
from scripts import assemble_rafael_B241_B260_offline_v2 as final
from scripts.audit_story_glyph_consistency import load, save


VISUAL = final.OUT / 'visual_review.json'
NOTES = {
    'DK4_MES_B241_R0025': 'Three lines keep the armadillo reference together.',
    'DK4_MES_B242_R0051': 'Opened the original preview individually. The a at the start of row two is complete.',
    'DK4_MES_B243_R0037': 'Four rows keep the entire Mediterranean reference on one page.',
    'DK4_MES_B245_R0030': 'Two pages preserve the article with its noun and begin the continuation with the whole verb phrase.',
    'DK4_MES_B247_R0044': 'Retain the continuation with its full closing verb phrase. Four-row wraps strand an article.',
    'DK4_MES_B248_R0046': 'Jam’s full qualification and short tag now fit on one page.',
    'DK4_MES_B249_R0038': 'The page turn separates the Skye and Lewis rumors.',
    'DK4_MES_B251_R0119': 'One page keeps the secondhand report and the swindler’s trick together.',
    'DK4_MES_B252_R0116': 'The barkeep’s decision begins the continuation and the governor’s office stays on one row.',
    'DK4_MES_B253_R0050': 'Four rows keep the description and invitation on one page.',
    'DK4_MES_B256_R0036': 'Opened the original preview individually. The a at the start of row two is complete.',
    'DK4_MES_B259_R0013': 'Opened the original preview individually. Oh, really? appears in full.',
    'DK4_MES_B260_R0058': 'Retain two pages so the question begins at the page turn.',
}


def index(rows):
    return {(row['id'], row['page']): row['preview_sha256'] for row in rows}


def main():
    assert not VISUAL.exists()
    files = (initial.BODY_SHEETS/'sheet_index.json', final.DELTA_SHEETS/'sheet_index.json',
             initial.NAMES, initial.FRANCISCA, final.FINAL_NATIVE, final.FINAL_PLAN, final.OUT/'menu.json')
    body, delta, names, francisca, native, plan, menu = map(load, files)
    assert body['native_receipt_sha256'] == delta['before_sha256'] == final.digest(initial.FINAL_NATIVE)
    assert delta['after_sha256'] == final.digest(final.FINAL_NATIVE)
    assert (body['pages'], len(body['sheets']), delta['pages'], len(delta['sheets'])) == (298, 13, 20, 1)
    viewed = index(row for sheet in body['sheets'] for row in sheet['included'])
    changed = index(row for sheet in delta['sheets'] for row in sheet['included'])
    reused = index(delta['unchanged_pages'])
    assert len(viewed) == 298 and len(reused) == 274 and changed.keys().isdisjoint(reused)
    assert reused == {key: viewed[key] for key in reused}
    assert changed | reused == {key: page['preview_sha256'] for key, page in final.pages(native['records'])}
    assert native['pages'] == plan['pages'] == 294 and len(native['records']) == len(plan['records']) == 286
    assert sum(bool(row.get('source_staged_progressive')) for row in native['records']) == 2
    assert names['scoped_actors'] == names['distinct_strings'] == 19
    assert sum(s['strings'] for s in names['review_sheets']) == 19
    assert menu['typed_labels'] == 6 and menu['caption_planes'] == 24 and menu['offline_visual_approved']
    sheets = (body['sheets'] + delta['sheets'] + names['review_sheets']
              + [francisca['review_sheet']] + menu['caption_visual_sheets'])
    assert all(final.digest(s['path']) == s['sha256'] for s in sheets)
    shared = {key: native[key] for key in ('manuscript', 'manuscript_sha256', 'plan', 'plan_sha256', 'runtime')}
    save(VISUAL, {**shared, 'native': str(final.FINAL_NATIVE), 'native_sha256': final.digest(final.FINAL_NATIVE),
        'body_pages': 294, 'fresh_final_body_pages': 20, 'exact_prior_page_images_reused': 274,
        'source_staged_FE_pages': 0, 'source_staged_progressive_pages': 2, 'source_FE_pages': 7,
        'typed_choice_captions': 6, 'reviewed_caption_style_planes': 24, 'scoped_name_count': 20,
        'distinct_scoped_name_strings': 20, 'all_final_body_caption_and_name_sheets_directly_viewed': True,
        'individual_visual_findings': NOTES, 'sheets': sheets,
        'names': str(initial.NAMES), 'names_sha256': final.digest(initial.NAMES),
        'proposed_Francisca_name': str(initial.FRANCISCA),
        'proposed_Francisca_name_sha256': final.digest(initial.FRANCISCA),
        'actual_gameplay': False, 'stored_branch_loader_and_gameplay_checks_pending': True, 'new_credit': 0,
        'evidence': {str(path): final.digest(path) for path in (*files, Path(__file__))}})
    print('Sealed direct visual review of 294 body pages, six captions and twenty scoped public names.')


if __name__ == '__main__':
    main()
