"""Record source/native progress without advancing release or completion counts."""

import ast
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.review_market_stock_v755 import CURRENT, IDS, MANUSCRIPT, ROOT
from scripts.verify_village_wrap_v608 import read, save


def main():
    doc = read(MANUSCRIPT)
    native = read(ROOT / 'native_context.json')
    matrix = read(ROOT / 'native_layout_matrix_DRAFT.json')
    findings = read(ROOT / 'layout_findings_DRAFT.json')
    dispatch = read(ROOT / 'experimental_dispatch.json')
    owner = read(ROOT / 'experimental_filter_ownership.json')
    assert [r['message_id'] for r in doc['records']] == list(IDS)
    assert len(native['all36_original_decision_fragments_each_clean_and_current']) == 36
    assert matrix['count'] == len(matrix['all_cases']) == 31013
    assert matrix['layout_findings_count'] == findings['count'] == 9065
    assert matrix['static_compile_failures'] == []
    assert len(matrix['sampled_complete_font_planes']) == 44
    assert all(r['review']['formatting'] is False for r in doc['records'])
    assert len(owner['all180_inherited_complete_output_controls']) == 180
    assert dispatch['all18340_dispatch_cases_differ_only_in767_770_direct_parent']
    assert all(not any(row['defects']) for row in matrix['all_cases'] if row['id'] >= 771)
    # Only unused imports were cleaned after the terminal layout run. Preserve
    # and bind its exact producer snapshot; both executed function bodies match.
    producer = Path('scripts/probe_market_stock_layout_v755.py')
    snapshot = ROOT / 'producer_snapshot_before_cleanup' / producer.name
    def functions(p):
        return [ast.dump(n, include_attributes=False) for n in ast.parse(p.read_text(encoding='utf-8')).body
                if isinstance(n, ast.FunctionDef)]
    assert functions(producer) == functions(snapshot)
    pins = {
        str(CURRENT): 'a44acfb6431fd2ec48e1ae5b5899ddbf1744bcac8a68e1ca6c5ec1fbc14fd246',
        'work/clean.nds': 'f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d',
        'out/raphael_natural_v2_accepted_base.nds': '3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe',
        'E:/Rota Nova translations/Saves/hodram-istanbul-golden-cutlass-blue-oak-v474.dsv': 'd991cb3bcdf74eed7aeb58c9a75957766b7c820d002423fd2b55cc8493cf8132',
        'E:/Rota Nova translations/Saves/Test fixtures/V751 disposable Istanbul donor.dsv': 'd991cb3bcdf74eed7aeb58c9a75957766b7c820d002423fd2b55cc8493cf8132',
    }
    for p, digest in pins.items():
        assert sha(Path(p).read_bytes()) == digest, p
    manifest = read(CURRENT.with_suffix('.manifest.json'))
    assert sha(Path('translations/release_stack.json').read_bytes()) == manifest['release_stack_sha256']
    config = read('translations/category_dialogue_editorial_release_v1.json')
    for p, digest in config['dependencies'].items():
        assert sha(Path(p).read_bytes()) == digest, p
    assert sha(Path(config['manuscript']).read_bytes()) == config['manuscript_sha256']
    ledger_path = Path('translations/editorial_review_current_v1.json')
    ledger = read(ledger_path)
    assert ledger['records_editorially_completed'] == 103 and ledger['records_revised_and_integrated'] == 69
    assert ledger['retained_wordings_editorially_completed'] == 34
    ledger['records_with_source_and_prose_pass'] = 120
    ledger['records_with_source_prose_drafts'] = 120
    ledger['active_source_prose_drafts'] = {
        'native_message_IDs': list(IDS), 'manuscripts': [str(MANUSCRIPT)],
        'context_proof': str(ROOT / 'native_context.json'),
        'formatting_findings': str(ROOT / 'layout_findings_DRAFT.json'),
        'status': 'source-context-prose-reviewed-formatting-integration-gameplay-pending',
        'revised_drafts': 15, 'retained_wording_drafts': 2,
        'note': 'No entries from this17-message packet count complete. The full shared/routes inventory remains open.'}
    ledger['latest_checkpoint'] = ('V755 research reviews Market767-783;36 source/current selection fragments and31013 native layouts. '
        '9065 dynamic tail/line-ending findings need resolution. Latest integrated ROM remains V754; completed count103 unchanged.')
    ledger['coverage_units'][0]['next'] = ('Resolve the full Market767-783 packet layout findings, integrate through a new registered profile, '
        'verify native copies/reconstruction and targeted gameplay. Continue750-752,754-761,784 onward, wider shared prose, Lil and every route.')
    for value in ledger.values():
        if isinstance(value, list):
            for row in value:
                if isinstance(row, dict) and row.get('id') == 'COMMON-730-compact-category-arguments':
                    row.update({'status': 'historical-finding-resolved-in-V754',
                        'detail': 'Resolved by the V754 full-name original730-only lookup, with full argument/font and compact-menu/gameplay evidence. Retained as history; no longer open work.'})
    save(ledger_path, ledger)
    reports = ['native_context.json', 'clean_and_current_neighbors.json', 'native_layout_matrix_DRAFT.json',
               'layout_findings_DRAFT.json', 'experimental_dispatch.json', 'experimental_filter_ownership.json']
    proof = {'status': 'source-prose-native-research-only-not-integrated',
        'reviewed_source_and_prose_draft_IDs': list(IDS), 'completed_entry_count_unchanged': 103,
        'latest_integrated_ROM': str(CURRENT), 'latest_integrated_ROM_sha256': pins[str(CURRENT)],
        'manuscript': str(MANUSCRIPT), 'manuscript_sha256': sha(MANUSCRIPT.read_bytes()),
        'reports': {str(ROOT / p): sha((ROOT / p).read_bytes()) for p in reports},
        'layout_producer_snapshot': str(snapshot), 'layout_producer_snapshot_sha256': sha(snapshot.read_bytes()),
        'current_layout_function_bodies_identical_after_import_cleanup': True,
        'current_source_producer_sha256': sha(Path('scripts/review_market_stock_v755.py').read_bytes()),
        'current_owner_verifier_sha256': sha(Path('scripts/verify_market_filter_owners_v755.py').read_bytes()),
        'all44_native_draft_font_planes_visually_inspected_across3_sheets': True,
        'unchanged_protected_files': pins, 'release_stack_matches_V754_manifest': True,
        'V754_dependency_pins_unchanged': True, 'new_gameplay_or_ROM_or_patch_not_claimed': True,
        'editorial_ledger_sha256': sha(ledger_path.read_bytes()), 'full_goal_complete': False}
    save(ROOT / 'draft_checkpoint_proof.json', proof)
    paragraph = ('\n\n## V755 research: Market stock and letters\n\n'
        'Seventeen clean-source drafts767-783 restore stock/gratitude/favor distinctions, introduction versus recommendation, '
        'letter upgrades and small-town versus any-town eligibility. Two existing wordings779/780 are retained. '
        'Thirty-six original selection/argument fragments pass on both clean and current code. Product-name callbacks are '
        'explicit tagged stubs; the skipped support call1096F8 is not classified as item addition. Full reward eligibility/effects remain unverified. '
        'The supplied single-product selector needs its original stack+28 value; the corrected fixture supplies it.\n\n'
        'All31013 native printf/wrap cases preserve complete words, guards and four-row bounds. All13 static drafts pass balanced compilation. '
        'The four dynamic drafts still yield9065 short final rows,9025 of which also have a weak line ending. '
        'Forty-four complete native font planes match independent glyph rasters; all three contact sheets were visually inspected. '
        'The experimental exact767-770 dispatcher fits the existing36-byte extent by replacing a redundant870-873 check. '
        'All18340 parent/ID selections differ only in those four direct calls; all main/autoload/overlay owners and180 inherited complete outputs pass. '
        'That candidate dispatcher exists only in research emulation, with no ROM emitted.\n\n'
        'Resolve the dynamic formatter findings without omitting source meaning or hiding final words, then integrate the entire17-entry packet, '
        'verify copies and clean patch reconstruction, and exercise original Market transactions/rewards in targeted gameplay. '
        'No new ROM or patch: V754 remains latest. Completed103/revised69/retained34 are unchanged;120 source/prose passes include17 pending drafts. '
        'Registry, V754 pinned dependencies, canonical, clean ROM and both protected saves are hash-verified unchanged. '
        'Remaining750-752,754-761,784 onward, wider shared prose, Lil/all routes and separate graphics audit stay open. '
        'Proof: `work/analysis/market_stock_v755/draft_checkpoint_proof.json`.\n')
    for p in ('docs/translation_progress.md', 'docs/todo.md', 'docs/known_issues.md'):
        path = Path(p)
        text = path.read_text(encoding='utf-8')
        if '## V755 research: Market stock and letters' not in text:
            path.write_text(text + paragraph, encoding='utf-8')
    print('V755 draft research recorded;17 pending,103 complete; no new release or goal completion.', flush=True)


if __name__ == '__main__':
    main()
