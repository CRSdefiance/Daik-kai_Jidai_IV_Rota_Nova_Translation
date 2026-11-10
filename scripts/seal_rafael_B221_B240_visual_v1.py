"""Seal the inspected native pages and exact visual refinements for Rafael B221–B240."""
from pathlib import Path

from scripts import assemble_rafael_B221_B240_offline_v1 as initial
from scripts import assemble_rafael_B221_B240_offline_v2 as final
from scripts.audit_story_glyph_consistency import load, save
from scripts.review_rafael_B221_B240_menus_v1 import REVIEW as CAPTIONS

VISUAL = final.OUT / 'visual_review.json'
NOTES = {
    'DK4_MES_B221_R0027': 'Keep the full appositive at the top of the continuation. The first page ends on Tokugawa.',
    'DK4_MES_B223_R0017': 'The final swan call remains on the third row with its original leading pause.',
    'DK4_MES_B223_R0047': 'Keep the entire suggestion to go look on the final row.',
    'DK4_MES_B224_R0005': 'The full Three Kingdoms title stays on one row.',
    'DK4_MES_B225_R0045': 'Continue the same quotation on page two. The seal stays together and its origin starts the continuation.',
    'DK4_MES_B225_R0066': 'Keep the ordinary wrap across the place name. Joining both words would leave a short opening ending in the.',
    'DK4_MES_B227_R0019': 'Both I characters render in normal width and the full runtime name remains. The question has its own row.',
    'DK4_MES_B230_R0036': 'The first row is a complete question. The checker’s weak word belongs at the end of that question.',
    'DK4_MES_B232_R0027': 'Keep the four-row wrap. Moving the entire item title to the next row would add a short second page.',
    'DK4_MES_B237_R0028': 'Use two pages to keep the two place names and the sentence intact. The direction remains a clear continuation.',
}


def index(sheets):
    return {(row['id'], row['page']): row['preview_sha256'] for sheet in sheets for row in sheet['included']}


def main():
    assert not VISUAL.exists()
    body, delta, names, captions, native, plan = map(load, (
        initial.BODY_SHEETS/'sheet_index.json', final.BODY_SHEETS/'sheet_index.json',
        initial.NAMES, CAPTIONS, final.FINAL_NATIVE, final.FINAL_PLAN))
    assert body['native_receipt_sha256'] == delta['before_sha256'] == initial.digest(initial.FINAL_NATIVE)
    assert delta['after_sha256'] == initial.digest(final.FINAL_NATIVE)
    assert body['pages'] == native['pages'] == 279 and len(body['sheets']) == 12
    assert len(delta['sheets']) == 1 and delta['pages'] == 17
    assert names['scoped_actors'] == 26 and names['distinct_strings'] == 25
    assert len(names['review_sheets']) == 3 and sum(s['strings'] for s in names['review_sheets']) == 25
    assert len(captions['menus']) == 3 and captions['visually_reviewed_captions'] == 7
    sheets = body['sheets'] + delta['sheets'] + names['review_sheets'] + [m['sheet'] for m in captions['menus']]
    assert all(initial.digest(Path(sheet['path'])) == sheet['sha256'] for sheet in sheets)
    changed = index(delta['sheets'])
    reused = index([{'included': delta['unchanged_pages']}])
    viewed = index(body['sheets'])
    assert changed.keys().isdisjoint(reused)
    assert reused == {key: viewed[key] for key in reused}
    assert len(reused) == 262 and len(viewed) == 279
    target = {}
    for row in native['records']:
        render = row['complete_native_English_display']
        pages = [render] if row['kind'] == 'system-FE' else render['pages']
        for i, page in enumerate(pages, 1):
            target[row['id'], i] = page['preview_sha256']
            assert initial.digest(Path(page['preview'])) == page['preview_sha256']
    assert changed | reused == target
    assert len(native['records']) == len(plan['records']) == 263
    assert sum(row.get('source_staged_progressive', False) for row in native['records']) == 3
    assert sum(row.get('source_staged_FE', False) for row in native['records']) == 1
    style = load(final.OUT/'styles.json')
    assert (len(style['objects']), style['native_target_slot_cases'], style['physical_alternatives']) == (4, 32, 29)
    shared = {key: native[key] for key in ('manuscript', 'manuscript_sha256', 'plan', 'plan_sha256', 'runtime')}
    save(VISUAL, {**shared, 'native': str(final.FINAL_NATIVE), 'native_sha256': initial.digest(final.FINAL_NATIVE),
        'body_pages': 279, 'fresh_final_body_pages': 17, 'exact_prior_page_images_reused': 262,
        'source_staged_FE_pages': 1, 'source_staged_progressive_pages': 3, 'source_FE_pages': 3,
        'typed_choice_captions': 7, 'reviewed_caption_style_planes': 28, 'scoped_name_count': 26,
        'distinct_scoped_name_strings': 25, 'all_final_body_caption_and_name_sheets_directly_viewed': True,
        'all_final_direct_visual_findings_resolved': True, 'individual_visual_findings': NOTES, 'sheets': sheets,
        'names': str(initial.NAMES), 'names_sha256': initial.digest(initial.NAMES), 'actual_gameplay': False,
        'stored_branch_loader_and_gameplay_checks_pending': True, 'new_credit': 0,
        'evidence': {str(path): initial.digest(path) for path in (
            initial.BODY_SHEETS/'sheet_index.json', final.BODY_SHEETS/'sheet_index.json',
            initial.NAMES, CAPTIONS, final.FINAL_NATIVE, final.OUT/'styles.json', Path(__file__))}})
    print('Sealed direct visual review of all 279 final body pages, seven captions and 25 name strings.')


if __name__ == '__main__':
    main()

