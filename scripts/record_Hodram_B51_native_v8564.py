"""Record direct native-page review without approving pending stored/actual gates."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/Hodram_B51_native_review_v8564')
OLD = Path('translations/hodram_B51_editorial_manuscript_v1.json')
DOC = Path('translations/hodram_B51_editorial_manuscript_v2.json')
PAGES = Path('work/analysis/Hodram_B51_pages_v8563/compiled_native_pages.json')
REASONS = {
    6: 'Four automatically generated native rows preserve the full lack-of-knowledge statement, explicit southern Mediterranean setting and complete leaving recommendation. The ordinary complete-word wrap between southern and Mediterranean is readable in the full warning. The first row cannot simply take the next word planned under the measured protected-break pair-phase allowance; the formatter uses the original216px available width. No words are shortened or padded to force a preferred layout.',
    10: 'One native row preserves the full hesitation and explanatory question, including all three leading periods and final question mark. No leading blank row or extra page appears.',
    14: 'Four complete native rows preserve the unspecified bad news description, idiomatic well-meant advice and direction to another sea. The complete bad news and your own good phrases remain coherent. The ordinary telling / you wrap is readable across the sentence and loses no glyph; it needs no manual prose break, narrowed viewport or QA waiver.',
    32: 'The short hesitant echo is complete on one native row, with all leading periods and the final question mark. Its original nested conditional control is separate from this offline body preview.',
    39: 'The retained private question is complete on one native row. Opening and closing parentheses and the final question mark survive; the thought remains unresolved. Retention is contextual, not an attempt to fit an old allocation.',
}

if __name__ == '__main__':
    assert not ROOT.exists() and not DOC.exists()
    old, pages = map(read, [OLD, PAGES])
    planpath = Path(pages['plan'])
    plan = read(planpath)
    assert pages['manuscript_sha256'] == plan['manuscript_sha256'] == sha(OLD.read_bytes()) and pages['plan_sha256'] == sha(planpath.read_bytes())
    sheet = pages['review_sheet']
    assert sha(Path(sheet['path']).read_bytes()) == sheet['sha256'] and len(pages['records']) == 5
    rows, infos = [], []
    for original, p, n in zip(old['records'], plan['records'], pages['records'], strict=True):
        assert original['id'] == p['id'] == n['id'] and original['english'] == n['logical_English'] == ' '.join(p['lines'])
        assert len(n['pages']) == 1 and not original['review']['formatting']
        for page in n['pages']:
            for key in ['native_plane', 'preview']:
                assert sha(Path(page[key]).read_bytes()) == page[key + '_sha256']
        for issue in p['base_QA']['issues']:
            assert issue['severity'] == 'info' and issue['code'] == 'line-break-count'
            infos.append(dict(id=original['id'], issue=issue))
        row = deepcopy(original)
        row.update(compiled_hex=p['encoded_hex'], compiled_bytes=len(bytes.fromhex(p['encoded_hex'])), formatted_markup=p['formatted_markup'],
            planned_English_markup=p['planning_record']['english'], generated_lines=p['lines'], expected_native_pages=1,
            qa_waivers=[], qa_waiver_scope=[], native_body_review_reason=REASONS[row['source_record_index']],
            native_body_review_proof=str(PAGES), native_body_review_proof_sha256=sha(PAGES.read_bytes()), compiled_native_body_review=deepcopy(n),
            all_stored_controls_actual_branch_context_headers_policy_andregistered_release_pending=True)
        assert row['english'] == original['english'] and row['source_hex'] == original['source_hex'] and row['current_hex'] == original['current_hex'] and row['review'] == original['review']
        rows.append(row)
    assert len(rows) == 5 and len(infos) == 2
    doc = deepcopy(old)
    doc.update(records=rows, predecessor_manuscript=str(OLD), predecessor_manuscript_sha256=sha(OLD.read_bytes()),
        compiled_plan=str(planpath), compiled_plan_sha256=sha(planpath.read_bytes()), native_body_pages=str(PAGES), native_body_pages_sha256=sha(PAGES.read_bytes()),
        all_five_complete_native_body_pages_directly_viewed=True, all_five_formatting_gates_still_false=True,
        two_original_line_count_infos_zero_warnings_waivers=True, status='contextual-prose-andcompiled-native-body-reviewed-stored-actual-policy-release-pending')
    save(DOC, doc)
    ROOT.mkdir(parents=True)
    save(ROOT / 'native_body_review.json', dict(manuscript=str(DOC), manuscript_sha256=sha(DOC.read_bytes()), predecessor_manuscript=str(OLD),
        predecessor_manuscript_sha256=sha(OLD.read_bytes()), directly_viewed_sheet=sheet, reviewed_body_pages=5, all_five_complete_bodies_visually_read=True,
        individual_body_reviews=[dict(id=r['id'], reason=r['native_body_review_reason'], generated_lines=r['generated_lines'], compiled_hex=r['compiled_hex']) for r in rows],
        original_infos=infos, original_warnings=[], original_QA_not_suppressed=True, no_qa_waivers=True,
        all_approved_words_source_current_references_andreview_gates_preserved=True, full216px_width_font_metrics_pagination_andguard_rules_unchanged=True,
        body_preview_not_actual_names_scene_branches_ornatural_activation=True, all_five_formatting_gates_false=True,
        new_credit=0, new_emulator_runs=0, full_goal_complete=False, evidence={str(p): sha(p.read_bytes()) for p in [OLD, PAGES, planpath, Path(__file__)]}))
    print('Five complete B51 native bodies directly viewed; two original line-count infos, zero warnings/waivers. Manuscriptv2 preserves all prose, references and gates; stored/actual/release pending.')
