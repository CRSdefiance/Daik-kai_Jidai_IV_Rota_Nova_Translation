"""Record eight source/prose reviews without granting formatting or completion credit."""
from copy import deepcopy
from pathlib import Path
from scripts.verify_village_wrap_v608 import read, save
from dk4tool.patch.grand_race_menu_release import sha

ROOT = Path('work/analysis/declaration_responses_review_v1533')
DOC = Path('translations/declaration_responses_editorial_manuscript_v1.json')

if __name__ == '__main__':
    assert not ROOT.exists()
    doc = read(DOC)
    assert len(doc['records']) == 8 and doc['revised'] == 8 and doc['formatting_review_pending']
    assert all(all(r['review'][k] for k in ['source', 'context', 'localization', 'naturalness']) and not r['review']['formatting'] for r in doc['records'])
    p = Path('translations/editorial_review_current_v1.json')
    ledger = read(p)
    before = deepcopy(ledger)
    assert (ledger['records_editorially_completed'], ledger['records_with_source_and_prose_pass'], len(ledger['reviewed_but_incomplete_COMMON_IDs'])) == (1330, 1474, 144)
    ids = [r['message_id'] for r in doc['records']]
    done = {n for f in ledger['completed_editorial_families'] for n in f.get('native_message_IDs', [])}
    assert not set(ids) & (done | set(ledger['reviewed_but_incomplete_COMMON_IDs']))
    ROOT.mkdir(parents=True)
    save(ROOT / 'coverage_before_source_review.json', before)
    ledger['records_with_source_and_prose_pass'] += 8
    ledger['records_with_source_prose_drafts'] += 8
    ledger['source_prose_reviewed_counts_by_file']['/COMMON/MESFILE.DK4'] += 8
    ledger['reviewed_but_incomplete_COMMON_IDs'] = sorted([*ledger['reviewed_but_incomplete_COMMON_IDs'], *ids])
    drafts = ledger['active_source_prose_drafts']
    drafts['native_message_IDs'] = sorted(set(drafts['native_message_IDs']) | set(ids))
    drafts['manuscripts'].append(str(DOC))
    drafts['manuscript_record_subsets_pending'][str(DOC)] = ids
    drafts['note'] = 'Eight war responses have source/context/prose review but native wrapping/fonts/visuals/release/original revised scene remain pending. Earlier144 entries and broader shared/routes/raw prose remain open.'
    ledger['coverage_units'].append({'id': 'Shared-NPC-declaration-responses8-source-prose', 'native_message_IDs': ids,
        'manuscript': str(DOC), 'source_context': doc['source_context'], 'status': 'source-context-prose-reviewed;native-formatting-release-gameplay-pending',
        'completed_entries_added': 0, 'full_goal_complete': False})
    ledger['formatting_watchlist']['NPC_declaration_responses8'] = {'native_message_IDs': ids, 'manuscript': str(DOC),
        'source_context': doc['source_context'], 'exact_original_parent': '02053F40', 'exact_original_table': '021184E0',
        'fullwidth_I_2206_2207_requires_postmacro_native_proof': True, 'native_font_visual_registered_release_and_revised_original_event_pending': True}
    summary = ('V1533 source/context/prose-reviews eight original NPC declaration responses2201-2208,all proposed revisions. '
        'Restore interception2202,non-losing resolve2203,the complete personal boast2205,and direct retaliatory promise2208; '
        'preserve the explicit hostile threat2206 and frightened plea2207 with ordinary ASCII I pending native proof. '
        'Original6F024/table021184E0/6F02C/53F0C/direct actor path and actual James Clifford28/voice4/2205 are mapped. '
        'V1530 DMA-as-UI-constructor label is corrected explicitly byV1531;source bytes and actual event remain exact. '
        '186-byte encoded table fits188 owned bytes with unchanged172-byte gate/123040 staged bytes. Native runtime/font/visual/copy/cache/release/gameplay gates remain pending. '
        'Counts1330 complete(992 revised338 retained),1482 source/prose,152 reviewed-incomplete COMMON. V1520 experimental,V1492 promoted; '
        'broader shared/routes/raw prose,separate graphics/all18 plaques and later older-record re-audit remain open;goal active.')
    ledger['latest_checkpoint'] = summary
    ledger['research_checkpoints'].append({'id': 'V1533-NPC-declaration8-source-prose', 'proof': str(ROOT / 'source_review_receipt.json'),
        'manuscript': str(DOC), 'source_prose_reviews_added': 8, 'completed_entries_added': 0, 'full_goal_complete': False})
    for k in ['records_editorially_completed', 'records_revised_and_integrated', 'retained_wordings_editorially_completed',
              'current_integrated_candidate', 'current_native_relocation_reference', 'source_pins', 'unresolved_graphics_work',
              'older_record_reaudit_after_full_editorial_goal']:
        assert ledger[k] == before[k], k
    save(p, ledger)
    Path('docs/declaration_responses_v1533_source_review.md').write_text('# V1533 eight declaration-response prose reviews\n\n' + summary +
        '\n\nSource-reviewed manuscript: `' + str(DOC) + '`. All words are one unwrapped paragraph without authored indent or line breaks. '
        'The separate fear/sea table2209-2216 is not part of this batch;2209 remains an unreviewed context lead.\n', encoding='utf-8')
    for name in ['translation_progress.md', 'known_issues.md', 'todo.md', 'editorial_review_goal.md']:
        with (Path('docs') / name).open('a', encoding='utf-8', newline='\n') as f:
            f.write('\n\n## V1533 NPC declaration8 source/prose review\n\n' + summary + '\n\nSee [source review](declaration_responses_v1533_source_review.md).\n')
    save(ROOT / 'source_review_receipt.json', {'manuscript': str(DOC), 'manuscript_sha256': sha(DOC.read_bytes()),
        'completed': 1330, 'source_prose': 1482, 'reviewed_incomplete_COMMON': 152,
        'source_prose_reviews_added': 8, 'completed_entries_added': 0, 'producer_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print('War8 source/prose recorded:1482 reviewed,1330 complete,152 COMMON entries pending;formatting/integration/gameplay still open.')
