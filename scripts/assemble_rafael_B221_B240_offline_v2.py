"""Select final native proofs and reuse only byte-identical reviewed page images."""
from pathlib import Path

from scripts.audit_story_glyph_consistency import load, save
from scripts import assemble_rafael_B221_B240_offline_v1 as prior
from scripts.pack_rafael_B201_B220_review_sheets_v1 import read_image, sheet_batch
from scripts.source_locked_derivation_v5118 import checked_text

ROOT = prior.ROOT
OUT = ROOT / 'offline_display_v2'
BODY_SHEETS = ROOT / 'body_visual_delta_v1'
NATIVE_DELTA = ROOT / 'ordinary_native_delta_v1/compiled_native_pages.json'
STYLES = ROOT / 'compiled_style_v2/compiled_style_objects.json'
FINAL_PLAN = OUT / 'automatic_plans.json'
FINAL_NATIVE = OUT / 'compiled_native_pages.json'
FINAL_MANUSCRIPT = OUT / 'formatting_manuscript.json'


def pack_delta(out, receipt):
    initial, final = map(load, (prior.FINAL_NATIVE, receipt))
    def page_map(doc):
        result = {}
        for row in doc['records']:
            display = row['complete_native_English_display']
            pages = [display] if row['kind'] == 'system-FE' else display['pages']
            for index, page in enumerate(pages, 1):
                result[row['id'], index] = page
        return result

    baseline, target = map(page_map, (initial, final))
    assert list(baseline) == list(target) and len(target) == 279
    changed, reused = [], []
    for (ident, index), page in target.items():
        old = baseline[ident, index]
        path = Path(page['preview'])
        assert prior.digest(path) == page['preview_sha256']
        assert prior.digest(Path(old['preview'])) == old['preview_sha256']
        row = dict(id=ident, page=index, preview=str(path), preview_sha256=page['preview_sha256'])
        if old['preview_sha256'] == page['preview_sha256']:
            reused.append(row)
        else:
            image = read_image(path, page['preview_sha256'])
            changed.append((f'{ident} page {index}', image, row))
    assert 0 < len(changed) <= 18
    sheets = sheet_batch(out, changed, columns=3, columns_width=468, row_height=148, max_rows=8, scale=2)
    save(out/'sheet_index.json', dict(sheets=sheets, pages=len(changed), unchanged_pages=reused,
        before=str(prior.FINAL_NATIVE), before_sha256=prior.digest(prior.FINAL_NATIVE),
        after=str(receipt), after_sha256=prior.digest(receipt), direct_review_pending=True))


source = checked_text(Path(prior.__file__).read_text(encoding='utf-8'), {
    "OUT = ROOT / 'offline_display_v1'": "OUT = ROOT / 'offline_display_v2'",
    "PLAN = ROOT / 'ordinary_plans_v5/automatic_plans.json'": "PLAN = ROOT / 'ordinary_plans_v7/automatic_plans.json'",
    "STYLES = ROOT / 'compiled_style_v1/compiled_style_objects.json'":
        "STYLES = ROOT / 'compiled_style_v2/compiled_style_objects.json'",
    "BODY_SHEETS = ROOT / 'body_visual_v1'": "BODY_SHEETS = ROOT / 'body_visual_delta_v1'",
    "CAPTIONS, TWO, THREE)\n    original,": "CAPTIONS, TWO, THREE, NATIVE_DELTA)\n    original,",
    'styles, names, captions, two, three = map(load, paths)':
        'styles, names, captions, two, three, native_delta = map(load, paths)',
    "assert native['plan_sha256'] == styles['plan_sha256'] == digest(PLAN) and not plan['failures']":
        """assert styles['plan_sha256'] == digest(PLAN) and not plan['failures']
    assert native['plan_sha256'] == digest(prior.PLAN) and native_delta['runtime'] == runtime
    assert native_delta['all_first_internal_final_glyph_codes_pixels_input_canaries_andbounds_pass']
    assert native_delta['complete_consumption_andpagination_exact'] and not native_delta['actual_gameplay']
    assert (len(native_delta['records']), native_delta['pages'], native_delta['fresh_compiled_alignments']) == (17, 18, 68)
    old_styles = load(prior.STYLES)
    old_objects = {(row['block'], row['source_command_offset']): row['target_object_hex'] for row in old_styles['objects']}
    changed = {(row['block'], row['source_command_offset']) for row in styles['objects']
               if row['target_object_hex'] != old_objects[row['block'], row['source_command_offset']]}
    assert changed == {(221, 702)}""",
    "native['records'] + staged['records'] + delta['records']":
        "native['records'] + native_delta['records'] + staged['records'] + delta['records']",
    "1060,": "1128,",
    "    body(BODY_SHEETS, FINAL_NATIVE)": "    pack_delta(BODY_SHEETS, FINAL_NATIVE)",
})
if __name__ == '__main__':
    exec(compile(source, __file__ + '::exact-final-page-and-style-selection', 'exec'), globals())

