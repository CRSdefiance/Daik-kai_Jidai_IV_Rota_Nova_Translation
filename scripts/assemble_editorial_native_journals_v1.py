"""Aggregate exact completed native journals without replaying or approving visuals."""
import argparse
from pathlib import Path
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    for name in ['selection', 'template', 'out']:
        ap.add_argument('--' + name, type=Path, required=True)
    args = ap.parse_args()
    assert not args.out.exists()
    selection, template = map(load, [args.selection, args.template])
    assert selection['native_selection_complete'] and selection['remaining_records'] == 0
    manuscript = Path(selection['final_manuscript'])
    planpath = Path(selection['final_plan'])
    assert digest(manuscript) == selection['final_manuscript_sha256']
    assert digest(planpath) == selection['final_plan_sha256']
    doc, plan = map(load, [manuscript, planpath])
    assert plan['manuscript_sha256'] == digest(manuscript) and not plan['failures']
    planned = {r['id']: r for r in plan['records']}
    originals = {r['id']: r for r in doc['records'] if r['kind'] != 'typed-choice-label'}
    assert planned.keys() == originals.keys()
    assert template['all_first_internal_final_glyph_codes_pixels_input_canaries_andbounds_pass']
    assert template['complete_consumption_andpagination_exact']
    rows, runs, dependencies = [], {}, {}
    seen = set()
    for binding in selection['reused_native_records']:
        path = Path(binding['receipt'])
        assert digest(path) == binding['receipt_sha256']
        proof = load(path)
        assert proof['four_native_alignment_cases_pass']
        assert proof['all_original_native_glyph_pixels_consumption_canaries_bounds_androw_assertions_pass']
        assert not proof['actual_gameplay']
        row = proof['record']
        key = row['id']
        assert key not in seen
        seen.add(key)
        assert row['compiled_hex'] == binding['compiled_hex'] == planned[key]['encoded_hex']
        assert row['logical_English'] == originals[key]['english']
        assert all(row[k] == originals[key][k] for k in ['source_reference', 'current_reference'])
        assert len(row['native_alignment']['cases']) == 4
        rp = Path(proof['native_run_inputs'])
        assert digest(rp) == proof['native_run_inputs_sha256']
        run = runs.setdefault(str(rp), load(rp))
        assert run['runtime'] == template['runtime'] == doc['runtime']
        assert run['font_sha256'] == template['font_sha256']
        assert run['all_v1_native_assertions_preserved']
        assert run['producer_sha256'] == digest('scripts/check_editorial_compiled_pages_explicit_captain_v2.py')
        assert digest(run['macro_proof']) == run['macro_proof_sha256']
        for k in ['source_owned_target_page_adapter', 'source_owned_progressive_macro_adapter']:
            assert run[k] == template[k]
        display = row['complete_native_English_display']
        pages = display['pages'] if row['kind'] == 'progressive' else [display]
        assert len(pages) == planned[key]['expected_native_pages'] == binding['pages']
        for page in pages:
            for kind in ['preview', 'native_plane']:
                assert digest(page[kind]) == page[kind + '_sha256']
        dependencies[str(path)] = digest(path)
        rows.append(row)
    assert seen == planned.keys() and len(rows) == selection['complete_body_candidates']
    result = {**template, 'records': rows, 'pages': sum(p['expected_native_pages'] for p in planned.values()),
        'manuscript': str(manuscript), 'manuscript_sha256': digest(manuscript),
        'plan': str(planpath), 'plan_sha256': digest(planpath), 'review_sheets': [],
        'fresh_compiled_alignments': 0, 'selected_alignment_cases': 4 * len(rows),
        'aggregation_of_completed_exact_receipts_not_fresh_monolithic_run': True,
        'native_receipts': dependencies, 'native_run_inputs': {p: digest(p) for p in runs},
        'direct_visual_review_pending': True, 'actual_gameplay': False, 'new_credit': 0,
        'evidence': {str(p): digest(p) for p in [args.selection, args.template, manuscript, planpath, Path(__file__)]}}
    save(args.out, result)
    print(dict(records=len(rows), pages=result['pages'], selected_alignments=4 * len(rows), new_native_cases=0))


if __name__ == '__main__':
    main()
