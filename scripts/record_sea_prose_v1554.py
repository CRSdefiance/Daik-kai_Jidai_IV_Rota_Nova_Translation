"""Record eight source/prose reviews; native layout and gameplay stay open."""
from copy import deepcopy
from pathlib import Path
from scripts.verify_village_wrap_v608 import read, save
from dk4tool.patch.grand_race_menu_release import sha

ROOT = Path('work/analysis/sea_responses_review_v1554')
DOC = Path('translations/sea_responses_editorial_manuscript_v1.json')

if __name__ == '__main__':
    assert not ROOT.exists()
    doc = read(DOC)
    assert len(doc['records']) == 8 and (doc['revised'], doc['retained']) == (5, 3) and doc['formatting_review_pending']
    assert all(all(r['review'][k] for k in ['source', 'context', 'localization', 'naturalness']) and not r['review']['formatting'] for r in doc['records'])
    p = Path('translations/editorial_review_current_v1.json')
    ledger = read(p)
    before = deepcopy(ledger)
    assert (ledger['records_editorially_completed'], ledger['records_with_source_and_prose_pass'], len(ledger['reviewed_but_incomplete_COMMON_IDs'])) == (1338, 1482, 144)
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
    drafts['note'] = 'Eight creature/ghost inspection reactions have source/context/prose review;five revisions,three justified retentions. Native layout/visuals/release/original inspection remain open,plus earlier144 entries and broader prose.'
    ledger['coverage_units'].append({'id': 'Shared-sea-inspection-fear-awe8-source-prose', 'native_message_IDs': ids,
        'manuscript': str(DOC), 'source_context': doc['source_context'], 'status': 'source-context-prose-reviewed;native-formatting-release-gameplay-pending',
        'completed_entries_added': 0, 'full_goal_complete': False})
    ledger['formatting_watchlist']['sea_inspection_fear_awe8'] = {'native_message_IDs': ids, 'manuscript': str(DOC),
        'source_context': doc['source_context'], 'exact_original_parent': '02053DB8', 'exact_original_table': '021186E0',
        'original_logical_role': 7, 'false_war_reference_2209_prose_corrected_not_yet_integrated': True,
        'native_font_visual_registered_release_and_original_inspection_pending': True}
    summary = ('V1554 source/context/prose-reviews8 original creature/ghost inspection responses2209-2216:5 proposed revisions3 retentions. '
        'Remove the invented war reference2209,restore complete comprehension/first-sighting clauses2210/2211,avoid an invented habitat claim2212,and use a natural fear admission2215. '
        'Retain natural monster recognition2213,challenge question2214 and contemplative sea-mystery exclamation2216 with explicit reasons. Original class34-38 taxonomy, '
        'special-target6F66C/6F674/role7/53D44/table021186E0 and207 actor choices are mapped;no species,arguments,macros or outcomes added. '
        'Counts1338 complete(1000 revised338 retained),1490 source/prose,152 reviewed-incomplete COMMON. Native layout/visual/copy/cache/registered release/actual inspection remain pending. '
        'V1542 experimental,V1492 promoted;broader shared/routes/raw prose,separate graphics/all18 plaques and later older-record re-audit remain open;goal active.')
    ledger['latest_checkpoint'] = summary
    ledger['research_checkpoints'].append({'id': 'V1554-sea-inspection8-source-prose', 'proof': str(ROOT / 'source_review_receipt.json'),
        'manuscript': str(DOC), 'source_prose_reviews_added': 8, 'completed_entries_added': 0, 'full_goal_complete': False})
    for k in ['records_editorially_completed', 'records_revised_and_integrated', 'retained_wordings_editorially_completed',
              'current_integrated_candidate', 'current_native_relocation_reference', 'source_pins', 'unresolved_graphics_work', 'older_record_reaudit_after_full_editorial_goal']:
        assert ledger[k] == before[k], k
    save(p, ledger)
    Path('docs/sea_responses_v1554_source_review.md').write_text('# V1554 eight sea inspection prose reviews\n\n' + summary +
        '\n\nSource-reviewed manuscript: `' + str(DOC) + '`. All prose is one unwrapped paragraph. The isolated activation pilot is research,not an earned/naturally spawned encounter. '
        'No new formatting or gameplay completion credit is granted here.\n', encoding='utf-8')
    for name in ['translation_progress.md', 'known_issues.md', 'todo.md', 'editorial_review_goal.md']:
        with (Path('docs') / name).open('a', encoding='utf-8', newline='\n') as f:
            f.write('\n\n## V1554 sea inspection8 source/prose\n\n' + summary + '\n\nSee [source review](sea_responses_v1554_source_review.md).\n')
    save(ROOT / 'source_review_receipt.json', {'manuscript': str(DOC), 'manuscript_sha256': sha(DOC.read_bytes()),
        'completed': 1338, 'source_prose': 1490, 'reviewed_incomplete_COMMON': 152,
        'source_prose_reviews_added': 8, 'completed_entries_added': 0, 'producer_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print('Sea inspection8 source/prose recorded:1490 reviewed,1338 complete,152 COMMON pending;formatting/integration/gameplay remain open.')
