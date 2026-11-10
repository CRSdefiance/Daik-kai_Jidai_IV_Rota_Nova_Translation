"""Assemble B221–B240 offline proofs and produce complete readable body sheets."""
from pathlib import Path

from scripts.audit_story_glyph_consistency import load, save
from scripts.pack_rafael_B201_B220_review_sheets_v1 import body
from scripts.plan_rafael_B221_B240_v1 import FORMATTING, ROOT, STAGED
from scripts.review_rafael_B221_B240_menus_v1 import REVIEW as CAPTIONS, THREE, TWO
from scripts.write_rafael_B221_B240_contextual_v1 import OUT as PROSE, digest

OUT = ROOT / 'offline_display_v1'
PLAN = ROOT / 'ordinary_plans_v5/automatic_plans.json'
NATIVE = ROOT / 'ordinary_native_v1/compiled_native_pages.json'
STYLES = ROOT / 'compiled_style_v1/compiled_style_objects.json'
NAMES = ROOT / 'scoped_name_planes_v1/native_name_planes.json'
STAGED_NATIVE = ROOT / 'staged_native_v1/compiled_staged.json'
STAGED_DELTA = ROOT / 'staged_native_delta_v1/compiled_staged.json'
BODY_SHEETS = ROOT / 'body_visual_v1'
FINAL_PLAN = OUT / 'automatic_plans.json'
FINAL_NATIVE = OUT / 'compiled_native_pages.json'
FINAL_MANUSCRIPT = OUT / 'formatting_manuscript.json'


def main():
    assert not OUT.exists() and not BODY_SHEETS.exists()
    paths = (PROSE, FORMATTING, STAGED, PLAN, NATIVE, STAGED_NATIVE, STAGED_DELTA, STYLES, NAMES,
             CAPTIONS, TWO, THREE)
    original, manuscript, staging, plan, native, staged, delta, styles, names, captions, two, three = map(load, paths)
    runtime = original['runtime']
    assert all(doc['runtime'] == runtime for doc in (manuscript, staging, native, staged, delta, styles, names, three))
    assert native['manuscript_sha256'] == plan['manuscript_sha256'] == styles['manuscript_sha256'] == digest(FORMATTING)
    assert native['plan_sha256'] == styles['plan_sha256'] == digest(PLAN) and not plan['failures']
    assert all(not proof['actual_gameplay'] for proof in (native, staged, delta, captions))
    assert native['all_first_internal_final_glyph_codes_pixels_input_canaries_andbounds_pass']
    assert native['complete_consumption_andpagination_exact'] and native['FE_actual_glyph_row_membership_checked']
    assert native['fresh_compiled_alignments'] == 1036
    for proof in (staged, delta):
        assert proof['complete_native_glyphs_pages_bounds_and_canaries_pass'] and proof['source_staged_placements_exact']
        assert proof['font_sha256'] == native['font_sha256']
    assert (len(styles['objects']), styles['native_target_slot_cases'], styles['physical_alternatives']) == (4, 32, 29)
    assert styles['source_alias_equivalence_exact']
    assert names['all_scoped_progressive_names_ASCII_complete_andfit_native216px']
    assert (names['scoped_actors'], names['distinct_strings']) == (26, 25)
    assert captions['visually_reviewed_captions'] == 7 and captions['complete_caption_style_planes'] == 28

    replacements = {r['id'] for r in delta['records']}
    assert replacements == {'DK4_MES_B226_R0068', 'DK4_MES_B235_R0048'}
    records = {row['id']: row for row in native['records'] + staged['records'] + delta['records']}
    plans = {row['id']: row for row in plan['records'] + staged['plans'] + delta['plans']}
    rows = {row['id']: row for row in manuscript['records'] + staging['records']}
    assert len(records) == len(plans) == 263 and len(rows) == len(original['records']) == 270
    for authored in original['records']:
        ident = authored['id']
        row = rows[ident]
        assert row['editorial_logical_English'] == authored['english']
        assert all(row[key] == authored[key] for key in ('source_hex', 'source_reference', 'current_reference', 'review'))
        if ident not in plans:
            assert row['kind'] == 'typed-choice-label'
            continue
        result = records[ident]
        planned = plans[ident]
        assert result['compiled_hex'] == planned['encoded_hex'] and result['logical_English'] == row['english']
        assert all(row[key] == result[key] for key in ('source_reference', 'current_reference', 'kind'))
        assert not any(i['severity'] in ('error','warning') for i in planned['base_QA']['issues'])
        assert len(result['native_alignment']['cases']) == 4
        for key in ('source_staged_FE', 'source_staged_progressive', 'source_staging_reason'):
            if key in result:
                row[key] = result[key]
    ordered = [row['id'] for row in original['records']]
    spoken = [ident for ident in ordered if ident in records]
    page_count = sum(plans[ident]['expected_native_pages'] for ident in spoken)
    assert page_count == 279

    menus = []
    for item in two['objects']:
        receipt = Path(item['receipt'])
        compiled = Path(item['compiled_path'])
        assert digest(receipt) == item['receipt_sha256'] and digest(compiled) == item['compiled_sha256']
        proof = load(receipt)
        assert proof['runtime'] == runtime and proof['complete_caption_glyphs_centering_bounds_guards_andconsumption_pass']
        assert proof['native_choice_object_hex'] == compiled.read_bytes().hex()
        menus.append(dict(block=item['block'], source_command_offset=item['source_command_offset'],
            record_IDs=item['record_ids'], target_object_hex=proof['native_choice_object_hex'], source_word=0x2100,
            versions=proof['versions'], native_receipt=str(receipt), native_receipt_sha256=digest(receipt)))
    assert len(three['menus']) == 1 and three['complete_caption_glyphs_centering_bounds_guards_andconsumption_pass']
    menus.append({**three['menus'][0], 'source_word': 0x2200, 'native_receipt': str(THREE),
                  'native_receipt_sha256': digest(THREE)})
    assert sorted(ident for menu in menus for ident in menu['record_IDs']) == sorted(set(rows) - set(records))

    evidence = {str(path): digest(path) for path in (*paths, Path(__file__))}
    OUT.mkdir()
    final_manuscript = {**manuscript, 'records': [rows[ident] for ident in ordered],
        'physical_speech_objects': 263, 'ordinary_speech_objects': 234, 'pending_staged_merge': [],
        'source_staged_FE_panels': 1, 'source_staged_progressive_letters': 3, 'evidence': evidence}
    save(FINAL_MANUSCRIPT, final_manuscript)
    common = dict(manuscript=str(FINAL_MANUSCRIPT), manuscript_sha256=digest(FINAL_MANUSCRIPT),
                  runtime=runtime, new_credit=0)
    save(FINAL_PLAN, {**plan, **common, 'records': [plans[ident] for ident in spoken], 'pages': page_count,
                      'evidence': evidence})
    common.update(plan=str(FINAL_PLAN), plan_sha256=digest(FINAL_PLAN))
    save(FINAL_NATIVE, {**native, **common, 'records': [records[ident] for ident in spoken], 'pages': page_count,
        'selected_compiled_alignments': 4*len(records), 'fresh_compiled_alignments_total_across_attempts': 1060,
        'review_sheets': [], 'direct_visual_review_pending': True, 'evidence': evidence})
    save(OUT/'menu.json', {**common, 'menus': menus, 'offline_visual_approved': True, 'direct_view_pending': False,
        'caption_visual_receipt': str(CAPTIONS), 'caption_visual_receipt_sha256': digest(CAPTIONS),
        'typed_labels': 7, 'caption_planes': 28})
    save(OUT/'styles.json', {**styles, **common, 'evidence': evidence})
    body(BODY_SHEETS, FINAL_NATIVE)
    print('Assembled 279 verified body previews, 25 scoped name strings, seven captions and four native style commands.')


if __name__ == '__main__':
    main()

