"""Bind observed tutorial page findings and reuse only exact unchanged native pages."""
import argparse
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save

ROOT = Path('work/analysis/Rafael_early_tutorial_B42_B43_formatting_20261104')
DOC = ROOT / 'formatting_input.json'
INITIAL = ROOT / 'initial_plans_v1/automatic_plans.json'
NATIVE = Path('work/analysis/Rafael_early_tutorial_B42_B43_native_20261104/initial_v1/compiled_native_pages.json')
FINDINGS = {
    'DK4_MES_B42_R0019': ('Keep an eye', 'The initial page strands you have left on the next page. Start the complete closing sentence on page two.'),
    'DK4_MES_B43_R0030': ('and helps everyone', 'The initial page separates helps from everyone tire less quickly. Keep the complete second benefit on page two.'),
}


def prepare():
    output = ROOT / 'page_clause_preferences_v2.json'
    assert not output.exists()
    doc, plans, native = map(load, [DOC, INITIAL, NATIVE])
    assert len(native['records']) == 40 and native['pages'] == 42
    assert native['all_first_internal_final_glyph_codes_pixels_input_canaries_andbounds_pass']
    rows = {r['id']: r for r in doc['records']}
    by_id = {r['id']: r for r in plans['records']}
    preferences = {}
    for ident, (clause, reason) in FINDINGS.items():
        row = rows[ident]
        preferences[ident] = dict(bindings={k: sha(row[k].encode('utf-8')) for k in ['source_hex', 'current_hex', 'english']},
            page_clause=clause, reason=reason, initial_lines=by_id[ident]['lines'])
    sheets = [dict(**s, directly_viewed=True) for s in native['review_sheets']]
    assert len(sheets) == 5 and sum(s['pages'] for s in sheets) == 42
    assert all(sha(Path(s['path']).read_bytes()) == s['sha256'] for s in sheets)
    save(output, dict(records=preferences, manuscript=str(DOC), manuscript_sha256=sha(DOC.read_bytes()),
        initial_plan=str(INITIAL), initial_plan_sha256=sha(INITIAL.read_bytes()),
        initial_native=str(NATIVE), initial_native_sha256=sha(NATIVE.read_bytes()), directly_viewed_sheets=sheets,
        all42_initial_pages_directly_viewed=True, prose_unchanged=True, no_authored_breaks_orgeometry_changes=True,
        normal_ASCII_First_andcomplete_Rafael_name_viewed=True, FE_Deck_View_three_rows_viewed=True,
        actual_gameplay=False, new_credit=0, guide_photos=False))
    print('Two observed page-boundary findings bound; all 42 initial native pages viewed.')


def subset():
    root = ROOT / 'changed_native_inputs_v2'
    assert not root.exists()
    final = ROOT / 'page_clauses_v2/automatic_plans.json'
    doc, plans, initial = map(load, [DOC, final, INITIAL])
    old = {r['id']: r for r in initial['records']}
    changed = {r['id'] for r in plans['records'] if r['encoded_hex'] != old[r['id']]['encoded_hex']}
    assert changed == set(FINDINGS) and not plans['failures']
    assert all(not any(i['severity'] in ['warning', 'error'] for i in r['base_QA']['issues']) for r in plans['records'])
    selected = deepcopy(doc)
    selected['records'] = [r for r in doc['records'] if r['id'] in changed]
    selected.update(physical_speech_objects=2, ordinary_speech_objects=2,
        subset_of=str(DOC), subset_of_sha256=sha(DOC.read_bytes()))
    root.mkdir()
    manuscript = root / 'two_changed_records.json'
    save(manuscript, selected)
    tested = deepcopy(plans)
    tested['records'] = [r for r in plans['records'] if r['id'] in changed]
    tested.update(manuscript=str(manuscript), manuscript_sha256=sha(manuscript.read_bytes()),
        full_plan=str(final), full_plan_sha256=sha(final.read_bytes()))
    save(root / 'two_changed_plans.json', tested)
    print('Only two changed records need fresh native page checks; 38 exact proofs retained.')


def approve():
    output = ROOT / 'speech_display_approved_v2'
    assert not output.exists()
    final = ROOT / 'page_clauses_v2/automatic_plans.json'
    replacement = Path('work/analysis/Rafael_early_tutorial_B42_B43_native_20261104/page_clauses_v2/compiled_native_pages.json')
    preferences = ROOT / 'page_clause_preferences_v2.json'
    doc, plans, initial, old, fresh, viewed = map(load, [DOC, final, INITIAL, NATIVE, replacement, preferences])
    assert fresh['runtime'] == old['runtime'] and fresh['font_sha256'] == old['font_sha256']
    for receipt in [old, fresh]:
        assert receipt['all_first_internal_final_glyph_codes_pixels_input_canaries_andbounds_pass']
        assert receipt['complete_consumption_andpagination_exact']
    old_plans = {r['id']: r for r in initial['records']}
    changed = {r['id'] for r in plans['records'] if r['encoded_hex'] != old_plans[r['id']]['encoded_hex']}
    assert changed == set(FINDINGS) == {r['id'] for r in fresh['records']}
    native = {r['id']: r for r in old['records']}
    native.update({r['id']: r for r in fresh['records']})
    prose = {r['id']: r for r in doc['records']}
    pages = 0
    for plan in plans['records']:
        row = native[plan['id']]
        assert row['logical_English'] == plan['logical_English'] == prose[row['id']]['english']
        assert row['compiled_hex'] == plan['encoded_hex']
        for field in ['source_reference', 'current_reference']:
            assert row[field] == prose[row['id']][field]
        assert len(row['native_alignment']['cases']) == 4
        assert all(c['output_hex'] == row['expanded_native_hex'] for c in row['native_alignment']['cases'])
        rendered = row['complete_native_English_display']
        samples = [rendered] if row['kind'] == 'system-FE' else rendered['pages']
        if row['kind'] == 'system-FE':
            assert rendered['planned_native_row_comparison']['complete_glyph_row_membership_exact']
        assert len(samples) == plan['expected_native_pages']
        for sample in samples:
            for path_key, hash_key in [('native_plane', 'native_plane_sha256'), ('preview', 'preview_sha256')]:
                assert sha(Path(sample[path_key]).read_bytes()) == sample[hash_key]
        pages += len(samples)
    assert pages == 42 and len(native) == 40
    sheets = viewed['directly_viewed_sheets'] + [dict(**s, directly_viewed=True) for s in fresh['review_sheets']]
    assert len(fresh['review_sheets']) == 2 and fresh['pages'] == 4
    assert all(sha(Path(s['path']).read_bytes()) == s['sha256'] for s in sheets)
    output.mkdir()
    final_plan = deepcopy(plans)
    final_plan.update(actual_layout_corrections=sorted(changed), no_prose_changed=True, direct_visual_review_pending=False)
    plan_path = output / 'all40_compiled_plans.json'
    save(plan_path, final_plan)
    result = deepcopy(old)
    result.update(records=[native[r['id']] for r in doc['records']], plan=str(plan_path), plan_sha256=sha(plan_path.read_bytes()),
        pages=42, review_sheets=sheets, direct_visual_review_pending=False,
        all42_final_pages_directly_viewed=True, exact_unchanged_complete_record_proofs_reused=38,
        fresh_changed_record_proofs=2, fresh_changed_alignments=8, actual_layout_corrections=sorted(changed),
        evidence={str(p): sha(p.read_bytes()) for p in [DOC, INITIAL, final, NATIVE, replacement, preferences, Path(__file__)]})
    native_path = output / 'all40_native_pages.json'
    save(native_path, result)
    save(output / 'visual_approval.json', dict(native=str(native_path), native_sha256=sha(native_path.read_bytes()),
        pages=42, all_final_pages_directly_viewed_or_exact_plane_reuse=True, directly_viewed_sheets=sheets,
        layout_corrections=sorted(changed), prose_shortening=False, authored_breaks=False, QA_waivers=False,
        normal_ASCII_First_andcomplete_Rafael_name_viewed=True, FE_Deck_View_three_rows_viewed=True,
        stored_script_names_andrepresentative_gameplay_pending=True, actual_gameplay=False, new_credit=0, guide_photos=False))
    print('All 40 speeches/42 final pages approved offline; two page-boundary fixes; no prose changes or QA waivers.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('stage', choices=['prepare', 'subset', 'approve'])
    globals()[parser.parse_args().stage]()
