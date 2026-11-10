"""Bind the final body, signature, style, and caption proofs to one manuscript."""
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save
from scripts.write_rafael_B241_B260_contextual_v1 import OUT as PROSE, ROOT


OUT = ROOT / 'offline_display_v1'
MANUSCRIPT = ROOT / 'ordinary_formatting_manuscript_v1.json'
STAGING = ROOT / 'source_staged_layouts_v1.json'
PLAN = ROOT / 'ordinary_plans_v3/automatic_plans.json'
NATIVE = ROOT / 'ordinary_native_v1/compiled_native_pages.json'
STAGED = ROOT / 'staged_native_v1/compiled_staged.json'
STYLES = ROOT / 'compiled_style_v1/compiled_style_objects.json'
CAPTIONS = ROOT / 'native_menus_v1/complete_choice_objects.json'
NAMES = ROOT / 'retained_name_planes_v1/native_name_planes.json'
FRANCISCA = ROOT / 'Francisca_name_field_v1/native/native_name_fields_verification.json'
BODY_SHEETS = ROOT / 'body_visual_v1'
FINAL_MANUSCRIPT = OUT / 'formatting_manuscript.json'
FINAL_PLAN = OUT / 'automatic_plans.json'
FINAL_NATIVE = OUT / 'compiled_native_pages.json'


def digest(path):
    return sha(Path(path).read_bytes())


def main():
    assert not OUT.exists()
    paths = (PROSE, MANUSCRIPT, STAGING, PLAN, NATIVE, STAGED, STYLES, CAPTIONS, NAMES, FRANCISCA)
    original, manuscript, staging, plan, native, staged, styles, captions, names, francisca = map(load, paths)
    runtime = original['runtime']
    assert all(doc['runtime'] == runtime for doc in (manuscript, staging, native, staged, styles, names))
    assert native['manuscript_sha256'] == styles['manuscript_sha256'] == plan['manuscript_sha256'] == digest(MANUSCRIPT)
    assert native['plan_sha256'] == styles['plan_sha256'] == digest(PLAN) and not plan['failures']
    assert all(not proof['actual_gameplay'] for proof in (native, staged, captions, francisca))
    assert native['all_first_internal_final_glyph_codes_pixels_input_canaries_andbounds_pass']
    assert native['complete_consumption_andpagination_exact'] and native['FE_actual_glyph_row_membership_checked']
    assert native['fresh_compiled_alignments'] == 4 * 284
    assert staged['complete_native_glyphs_pages_bounds_and_canaries_pass'] and staged['source_staged_placements_exact']
    assert staged['font_sha256'] == native['font_sha256']
    assert (len(styles['objects']), styles['native_target_slot_cases'], styles['physical_alternatives']) == (2, 16, 14)
    assert styles['source_alias_equivalence_exact']
    assert names['scoped_actors'] == 19 and names['all_retained_progressive_names_ASCII_complete_andfit_native216px']
    assert francisca['original_progressive_andfull_name_getters_pass']
    assert all(r['text'] == 'Francisca' for r in francisca['versions'][1]['names']['rows'])

    records = {row['id']: row for row in native['records'] + staged['records']}
    plans = {row['id']: row for row in plan['records'] + staged['plans']}
    rows = {row['id']: row for row in manuscript['records'] + staging['records']}
    assert len(records) == len(plans) == 286 and len(rows) == len(original['records']) == 292
    for authored in original['records']:
        ident = authored['id']
        row = rows[ident]
        assert row['editorial_logical_English'] == authored['english']
        assert all(row[key] == authored[key] for key in ('source_hex', 'source_reference', 'current_reference', 'review'))
        if ident not in plans:
            assert row['kind'] == 'typed-choice-label'
            continue
        result, planned = records[ident], plans[ident]
        assert result['compiled_hex'] == planned['encoded_hex'] and result['logical_English'] == row['english']
        assert all(row[key] == result[key] for key in ('source_reference', 'current_reference', 'kind'))
        assert not any(i['severity'] in ('error', 'warning') for i in planned['base_QA']['issues'])
        assert len(result['native_alignment']['cases']) == 4
        for key in ('source_staged_progressive', 'source_staging_reason'):
            if key in result:
                row[key] = result[key]
    ordered = [row['id'] for row in original['records']]
    spoken = [ident for ident in ordered if ident in records]
    page_count = sum(plans[ident]['expected_native_pages'] for ident in spoken)
    assert page_count == native['pages'] + 2

    # All three current and proposed caption sheets were directly inspected.
    assert captions['all_checks_pass'] and captions['physical_caption_records'] == 6
    menus, sheets = [], []
    for item in captions['objects']:
        receipt, compiled = Path(item['receipt']), Path(item['compiled_path'])
        assert digest(receipt) == item['receipt_sha256'] and digest(compiled) == item['compiled_sha256']
        proof = load(receipt)
        assert proof['runtime'] == runtime and proof['complete_caption_glyphs_centering_bounds_guards_andconsumption_pass']
        assert proof['native_choice_object_hex'] == compiled.read_bytes().hex()
        assert proof['native_choice_object_hex'].startswith('0021')
        sheet = proof['review_sheet']
        assert digest(sheet['path']) == sheet['sha256']
        sheets.append(sheet)
        menus.append(dict(block=item['block'], source_command_offset=item['source_command_offset'],
            record_IDs=item['record_ids'], target_object_hex=proof['native_choice_object_hex'], source_word=0x2100,
            versions=proof['versions'], native_receipt=str(receipt), native_receipt_sha256=digest(receipt)))
    assert len(menus) == 3
    assert sorted(ident for menu in menus for ident in menu['record_IDs']) == sorted(set(rows) - set(records))

    evidence = {str(path): digest(path) for path in (*paths, Path(__file__))}
    OUT.mkdir()
    save(FINAL_MANUSCRIPT, {**manuscript, 'records': [rows[ident] for ident in ordered],
        'physical_speech_objects': 286, 'ordinary_speech_objects': 272, 'pending_staged_merge': [],
        'source_staged_FE_panels': 0, 'source_staged_progressive_letters': 2, 'evidence': evidence})
    common = dict(manuscript=str(FINAL_MANUSCRIPT), manuscript_sha256=digest(FINAL_MANUSCRIPT),
                  runtime=runtime, new_credit=0)
    save(FINAL_PLAN, {**plan, **common, 'records': [plans[ident] for ident in spoken], 'pages': page_count,
                      'evidence': evidence})
    common.update(plan=str(FINAL_PLAN), plan_sha256=digest(FINAL_PLAN))
    save(FINAL_NATIVE, {**native, **common, 'records': [records[ident] for ident in spoken], 'pages': page_count,
        'selected_compiled_alignments': 4*len(records), 'review_sheets': [],
        'direct_visual_review_pending': True, 'evidence': evidence})
    save(OUT/'menu.json', {**common, 'menus': menus, 'offline_visual_approved': True, 'direct_view_pending': False,
        'caption_visual_sheets': sheets, 'typed_labels': 6, 'caption_planes': 24, 'evidence': evidence})
    save(OUT/'styles.json', {**styles, **common, 'evidence': evidence})
    print(f'Assembled {page_count} verified body previews and the reviewed name and caption proofs.')


if __name__ == '__main__':
    main()
