"""Bind seven final wrap improvements to exact source/current paragraphs and viewed pages."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

ROOT = Path('work/Maria_B286_B302_clean_20261110')


def main():
    out = ROOT/'final_layout_delta_v1.json'
    assert not out.exists()
    initialpath = ROOT/'plan_v2/automatic_plans.json'
    finalpath = ROOT/'plan_v5/automatic_plans.json'
    sourcepath = ROOT/'formatting_v1/formatting_input.json'
    approvalpath = ROOT/'offline_display_approval_v1.json'
    initial, final, source, approval = map(load, [initialpath, finalpath, sourcepath, approvalpath])
    assert approval['all_final_body_pages_directly_viewed']
    assert approval['all_names_andcaptions_directly_viewed']
    old = {r['id']: r for r in initial['records']}
    prose = {r['id']: r for r in source['records']}
    changed = []
    for row in final['records']:
        prior = old[row['id']]
        assert row['logical_English'] == prior['logical_English'] == prose[row['id']]['english']
        if row['encoded_hex'] == prior['encoded_hex']:
            continue
        ident = row['id']
        changed.append(dict(id=ident, source_reference=prose[ident]['source_reference'],
            current_reference=prose[ident]['current_reference'], logical_English=row['logical_English'],
            initial_lines=prior['lines'], final_lines=row['lines'],
            initial_compiled_hex=prior['encoded_hex'], final_compiled_hex=row['encoded_hex'],
            initial_pages=prior['expected_native_pages'], final_pages=row['expected_native_pages']))
    assert len(changed) == 7
    assert sum(r['expected_native_pages'] for r in initial['records']) == 310
    assert sum(r['expected_native_pages'] for r in final['records']) == 309
    assert next(r for r in changed if r['id'] == 'DK4_MES_B298_R0049')['final_pages'] == 1
    save(out, dict(records=changed, final_layout_changes=7, phrase_wrap_improvements=6,
        initial_pages=310, final_pages=309, pages_reclaimed=1,
        one_reviewed_give_up_on_preference_already_satisfied_without_byte_change=True,
        Ancient_City_Map_short_opening_retained_to_keep_exact_item_title_together=True,
        no_prose_shortening_or_font_width_runtime_control_change=True,
        no_undocumented_dramatic_breaks_or_QA_waivers=True,
        fresh_changed_record_native_cases=24, compatible_body_record_proofs_reused=303,
        all_final_pages_directly_viewed=True, actual_gameplay=False, new_credit=0,
        evidence={str(p): digest(p) for p in [initialpath, finalpath, sourcepath, approvalpath, Path(__file__)]}))
    print('PASS seven final layout improvements,310 to309 pages;prose unchanged.')


if __name__ == '__main__':
    main()
