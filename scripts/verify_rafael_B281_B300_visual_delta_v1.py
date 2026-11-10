"""Verify fresh layout bytes and carry forward unchanged native page evidence."""
from pathlib import Path
import sys
from types import FunctionType

from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import body, digest, read_image
from scripts.plan_rafael_B281_B300_v1 import FORMATTING, ROOT
from scripts.refine_rafael_B281_B300_visual_v1 import FIRST_NATIVE


ORIGINAL = ROOT / 'FE_plan_v1/automatic_plans.json'
PLAN = ROOT / 'visual_plan_v4/automatic_plans.json'
DELTA = ROOT / 'visual_delta_inputs_v1'
DELTA_MANUSCRIPT = DELTA / 'manuscript.json'
DELTA_PLAN = DELTA / 'automatic_plans.json'
FRESH = ROOT / 'visual_delta_native_v1/compiled_native_pages.json'
SHEETS = ROOT / 'visual_delta_sheets_v1'
FINAL = ROOT / 'final_native_pages_v1.json'


def inputs():
    manuscript, old, plan = map(load, (FORMATTING, ORIGINAL, PLAN))
    assert old['manuscript_sha256'] == plan['manuscript_sha256'] == digest(FORMATTING)
    assert not plan['failures'] and not any(
        issue['severity'] in ('error', 'warning') for row in plan['records'] for issue in row['base_QA']['issues']
    )
    delta = {}
    for a, b in zip(old['records'], plan['records'], strict=True):
        assert a['id'] == b['id'] and a['logical_English'] == b['logical_English']
        if a['encoded_hex'] != b['encoded_hex']:
            delta[b['id']] = b
        else:
            assert a['expected_native_pages'] == b['expected_native_pages']
    return manuscript, plan, delta


def prepare():
    manuscript, plan, delta = inputs()
    assert not DELTA.exists() and delta
    rows = [row for row in manuscript['records'] if row['id'] in delta]
    assert len(rows) == len(delta) and all(row['kind'] != 'typed-choice-label' for row in rows)
    DELTA.mkdir()
    save(DELTA_MANUSCRIPT, {
        **manuscript, 'records': rows, 'blocks': sorted({row['block'] for row in rows}),
        'physical_speech_objects': len(rows),
        'typed_choice_objects': 0, 'typed_choice_commands': 0,
        'subset_of': str(FORMATTING), 'subset_of_sha256': digest(FORMATTING),
    })
    save(DELTA_PLAN, {**plan, 'records': list(delta.values()), 'manuscript': str(DELTA_MANUSCRIPT),
                     'manuscript_sha256': digest(DELTA_MANUSCRIPT)})
    print(f'Ready for {len(rows)} fresh native checks.')


def combine():
    assert not FINAL.exists() and not SHEETS.exists()
    manuscript, plan, delta = inputs()
    original, fresh = map(load, (FIRST_NATIVE, FRESH))
    assert manuscript['runtime'] == original['runtime'] == fresh['runtime']
    assert original['plan_sha256'] == digest(ORIGINAL)
    assert fresh['plan_sha256'] == digest(DELTA_PLAN)
    assert fresh['manuscript_sha256'] == digest(DELTA_MANUSCRIPT)
    for receipt in (original, fresh):
        assert receipt['all_first_internal_final_glyph_codes_pixels_input_canaries_andbounds_pass']
        assert receipt['complete_consumption_andpagination_exact'] and not receipt['actual_gameplay']
    new = {row['id']: row for row in fresh['records']}
    assert new.keys() == delta.keys()
    records = []
    for old, planned in zip(original['records'], plan['records'], strict=True):
        assert old['id'] == planned['id']
        row = new.get(old['id'], old)
        assert row['compiled_hex'] == planned['encoded_hex']
        assert row['logical_English'] == planned['logical_English']
        assert len(row['native_alignment']['cases']) == 4
        display = row['complete_native_English_display']
        pages = [display] if row['kind'] == 'system-FE' else display['pages']
        assert len(pages) == planned['expected_native_pages']
        assert all(digest(page['native_plane']) == page['native_plane_sha256'] for page in pages)
        records.append(row)
    total = sum(row['expected_native_pages'] for row in plan['records'])
    assert fresh['fresh_compiled_alignments'] == 4 * len(new)
    save(FINAL, {
        **original, 'records': records, 'pages': total, 'plan': str(PLAN), 'plan_sha256': digest(PLAN),
        'fresh_compiled_alignments': original['fresh_compiled_alignments'] + fresh['fresh_compiled_alignments'],
        'fresh_visual_delta_records': len(new), 'reused_unchanged_visual_records': len(records) - len(new),
        'review_sheets': [],
        'evidence': {**original['evidence'], **fresh['evidence'],
                     **{str(path): digest(path) for path in (FIRST_NATIVE, FRESH, PLAN, Path(__file__))}},
    })
    pack = FunctionType(body.__code__, {
        **body.__globals__, 'read_image': lambda path, expected: read_image(Path(path), expected),
    })
    pack(SHEETS, FRESH)
    print(f'Verified {len(records)} final records and {total} pages, with {len(new)} fresh renders.')


if __name__ == '__main__':
    if sys.argv[1:] == ['--prepare']:
        prepare()
    else:
        combine()
