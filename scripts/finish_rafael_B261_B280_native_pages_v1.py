"""Reuse the complete B261–B277 native checks and rerender the remaining blocks."""
from pathlib import Path
import sys
from types import FunctionType

from scripts.pack_rafael_B201_B220_review_sheets_v1 import body, read_image
from scripts.write_rafael_B261_B280_contextual_v1 import ROOT, load, save, sha


MANUSCRIPT = ROOT / 'ordinary_formatting_manuscript_v4.json'
PRIOR_PLAN = ROOT / 'refined_plan_v5/automatic_plans.json'
PLAN = ROOT / 'refined_plan_v6/automatic_plans.json'
PRIOR_NATIVE = ROOT / 'native_pages_v2'
TAIL_MANUSCRIPT = ROOT / 'tail_formatting_manuscript_v1.json'
TAIL_PLAN = ROOT / 'tail_automatic_plans_v1.json'
TAIL_NATIVE = ROOT / 'tail_native_v1/compiled_native_pages.json'
NATIVE = ROOT / 'complete_native_pages_v1.json'
SHEETS = ROOT / 'body_review_sheets_v1'
TAIL_BLOCKS = [278, 279, 280]
CHANGED = 'DK4_MES_B278_R0047'


def digest(path):
    return sha(Path(path).read_bytes())


def prepare():
    assert not TAIL_MANUSCRIPT.exists() and not TAIL_PLAN.exists()
    doc, prior, plan = map(load, (MANUSCRIPT, PRIOR_PLAN, PLAN))
    assert prior['manuscript_sha256'] == plan['manuscript_sha256'] == digest(MANUSCRIPT)
    assert not plan['failures']
    assert [row['id'] for old, row in zip(prior['records'], plan['records'], strict=True) if old != row] == [CHANGED]
    rows = [row for row in doc['records'] if row['block'] in TAIL_BLOCKS]
    assert len(rows) == 11 and all(row['kind'] != 'typed-choice-label' for row in rows)
    assert all((PRIOR_NATIVE / f'B{block}_checked.json').is_file() for block in range(261, 278))
    save(TAIL_MANUSCRIPT, {**doc, 'records': rows, 'blocks': TAIL_BLOCKS,
         'physical_speech_objects': len(rows), 'typed_choice_objects': 0, 'typed_choice_commands': 0,
         'subset_of': str(MANUSCRIPT), 'subset_of_sha256': digest(MANUSCRIPT)})
    save(TAIL_PLAN, {**plan, 'records': [row for row in plan['records'] if row['block'] in TAIL_BLOCKS],
         'manuscript': str(TAIL_MANUSCRIPT), 'manuscript_sha256': digest(TAIL_MANUSCRIPT)})


def complete():
    assert not SHEETS.exists()
    doc, prior, plan, tail = map(load, (MANUSCRIPT, PRIOR_PLAN, PLAN, TAIL_NATIVE))
    assert tail['runtime'] == doc['runtime'] and tail['manuscript_sha256'] == digest(TAIL_MANUSCRIPT)
    assert tail['plan_sha256'] == digest(TAIL_PLAN) and tail['fresh_compiled_alignments'] == 44
    assert tail['all_first_internal_final_glyph_codes_pixels_input_canaries_andbounds_pass']
    assert tail['complete_consumption_andpagination_exact'] and not tail['actual_gameplay']
    checked = [PRIOR_NATIVE / f'B{block}_checked.json' for block in range(261, 278)]
    reused = []
    for path in checked:
        block = load(path)
        assert not block['actual_gameplay'] and block['new_credit'] == 0
        reused.extend(block['records'])
    assert len(reused) == 119
    records = reused + tail['records']
    for index, (row, planned) in enumerate(zip(records, plan['records'], strict=True)):
        assert row['id'] == planned['id'] and row['compiled_hex'] == planned['encoded_hex']
        assert row['logical_English'] == planned['logical_English']
        assert len(row['native_alignment']['cases']) == 4
        if index < len(reused):
            assert planned == prior['records'][index]
        display = row['complete_native_English_display']
        pages = [display] if row['kind'] == 'system-FE' else display['pages']
        assert len(pages) == planned['expected_native_pages']
        assert all(digest(page['native_plane']) == page['native_plane_sha256'] for page in pages)
    pages = sum(row['expected_native_pages'] for row in plan['records'])
    assert pages == 131
    combined = {**tail, 'records': records, 'pages': pages,
         'manuscript': str(MANUSCRIPT), 'manuscript_sha256': digest(MANUSCRIPT),
         'plan': str(PLAN), 'plan_sha256': digest(PLAN), 'fresh_compiled_alignments': 520,
         'exact_earlier_block_rows_reused': len(reused), 'fresh_tail_rows': len(tail['records']),
         'review_sheets': [], 'excluded_typed_choice_IDs_separately_pending': [
             row['id'] for row in doc['records'] if row['kind'] == 'typed-choice-label'
         ],
         'evidence': {**tail['evidence'], **{str(path): digest(path) for path in (*checked, TAIL_NATIVE, PRIOR_PLAN, PLAN)}}}
    if NATIVE.exists():
        assert load(NATIVE) == combined
    else:
        save(NATIVE, combined)
    pack = FunctionType(body.__code__, {
        **body.__globals__, 'read_image': lambda path, expected: read_image(Path(path), expected),
    })
    pack(SHEETS, NATIVE)
    print('Combined 119 unchanged native checks and 11 fresh checks into 131 reviewable pages.')


if __name__ == '__main__':
    if sys.argv[1:] == ['--prepare']:
        prepare()
    else:
        complete()
