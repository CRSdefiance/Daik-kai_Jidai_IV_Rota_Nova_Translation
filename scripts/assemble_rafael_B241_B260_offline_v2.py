"""Carry forward byte-identical pages and bind the fresh visual refinements."""
from pathlib import Path

from scripts import assemble_rafael_B241_B260_offline_v1 as initial
from scripts.audit_story_glyph_consistency import load, save
from scripts.pack_rafael_B201_B220_review_sheets_v1 import read_image, sheet_batch
from scripts.refine_rafael_B241_B260_wraps_v4 import DELTA, DELTA_MANUSCRIPT, PLAN


ROOT, digest = initial.ROOT, initial.digest
OUT = ROOT / 'offline_display_v2'
DELTA_NATIVE = ROOT / 'ordinary_native_delta_v1/compiled_native_pages.json'
DELTA_SHEETS = ROOT / 'body_visual_delta_v1'
FINAL_MANUSCRIPT = OUT / 'formatting_manuscript.json'
FINAL_PLAN = OUT / 'automatic_plans.json'
FINAL_NATIVE = OUT / 'compiled_native_pages.json'


def pages(records):
    for row in records:
        render = row['complete_native_English_display']
        views = [render] if row['kind'] == 'system-FE' else render['pages']
        for index, page in enumerate(views, 1):
            assert digest(page['preview']) == page['preview_sha256']
            yield (row['id'], index), page


def main():
    assert not OUT.exists() and not DELTA_SHEETS.exists()
    paths = (initial.FINAL_MANUSCRIPT, initial.FINAL_PLAN, initial.FINAL_NATIVE,
             initial.OUT/'menu.json', initial.OUT/'styles.json', PLAN, DELTA, DELTA_NATIVE)
    manuscript, old_plan, old_native, menu, styles, plan, delta_plan, native = map(load, paths)
    assert old_native['runtime'] == native['runtime'] and old_native['font_sha256'] == native['font_sha256']
    assert native['all_first_internal_final_glyph_codes_pixels_input_canaries_andbounds_pass']
    assert native['complete_consumption_andpagination_exact'] and not native['actual_gameplay']
    assert native['manuscript_sha256'] == digest(DELTA_MANUSCRIPT) and native['plan_sha256'] == digest(DELTA)
    assert delta_plan['complete_plan_sha256'] == digest(PLAN)
    delta = {row['id']: row for row in native['records']}
    assert len(delta) == len(delta_plan['records']) == 16 and native['fresh_compiled_alignments'] == 64
    before = {row['id']: row for row in old_plan['records']}
    after = {row['id']: row for row in plan['records']}
    expected = {ident for ident, row in after.items() if row['encoded_hex'] != before[ident]['encoded_hex']}
    assert expected == delta.keys() and all(not ident.startswith('SC0_') for ident in expected)
    assert len(before) == len(old_native['records']) == 286 and len(after) == 284
    before.update(after)
    final_plan = [before[row['id']] for row in old_plan['records']]
    final_records = [delta.get(row['id'], row) for row in old_native['records']]
    assert all(r['compiled_hex'] == p['encoded_hex'] for r, p in zip(final_records, final_plan, strict=True))

    old_pages, final_pages = map(dict, (pages(old_native['records']), pages(final_records)))
    changed, reused = [], []
    for key, page in final_pages.items():
        ident, index = key
        row = dict(id=ident, page=index, preview=page['preview'], preview_sha256=page['preview_sha256'])
        if key in old_pages and old_pages[key]['preview_sha256'] == page['preview_sha256']:
            reused.append(row)
        else:
            changed.append((f'{ident} page {index}',
                read_image(Path(page['preview']), page['preview_sha256']), row))
    assert len(old_pages) == 298 and len(final_pages) == 294 and changed
    assert {key[0] for key in old_pages.keys() - final_pages.keys()} <= expected
    sheets = sheet_batch(DELTA_SHEETS, changed, columns=3, columns_width=468, row_height=148, max_rows=8, scale=2)
    evidence = {str(path): digest(path) for path in (*paths, Path(__file__))}
    OUT.mkdir()
    save(FINAL_MANUSCRIPT, manuscript)
    common = dict(manuscript=str(FINAL_MANUSCRIPT), manuscript_sha256=digest(FINAL_MANUSCRIPT),
                  runtime=old_native['runtime'], new_credit=0)
    save(FINAL_PLAN, {**plan, **common, 'records': final_plan, 'pages': len(final_pages), 'evidence': evidence})
    common.update(plan=str(FINAL_PLAN), plan_sha256=digest(FINAL_PLAN))
    save(FINAL_NATIVE, {**old_native, **common, 'records': final_records, 'pages': len(final_pages),
        'fresh_compiled_alignments_total_across_attempts': 1200, 'evidence': evidence})
    save(OUT/'menu.json', {**menu, **common})
    save(OUT/'styles.json', {**styles, **common, 'plan_reuse_exact_style_bodies': True, 'evidence': evidence})
    save(DELTA_SHEETS/'sheet_index.json', dict(sheets=sheets, unchanged_pages=reused, pages=len(changed),
        before=str(initial.FINAL_NATIVE), before_sha256=digest(initial.FINAL_NATIVE),
        after=str(FINAL_NATIVE), after_sha256=digest(FINAL_NATIVE), direct_review_pending=True))
    print(f'{len(changed)} refreshed pages and {len(reused)} exact preview reuses, {len(final_pages)} final pages.')


if __name__ == '__main__':
    main()
