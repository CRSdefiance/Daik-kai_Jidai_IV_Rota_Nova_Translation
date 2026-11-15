"""Apply hash-validated metadata, then independently verify36 pending reviews."""
import os
from collections import Counter
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.checkpoint_lil_B169_v4231 import ROOT as CHECKPOINT, DOC, FAMILY
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/editorial_handoff_verification_v4232')

if __name__ == '__main__':
    assert not ROOT.exists()
    workspace = Path.cwd().resolve()
    plan = read(CHECKPOINT/'mutation_plan.json')
    for item in plan:
        target, staged = Path(item['target']),Path(item['planned'])
        assert target.is_relative_to(workspace) and staged.is_relative_to(CHECKPOINT.resolve())
        assert sha(target.read_bytes()) == item['before_sha256']
        assert sha(staged.read_bytes()) == item['planned_sha256']
        assert staged.stat().st_size >= target.stat().st_size
    for item in plan:
        data = Path(item['planned']).read_bytes()
        with Path(item['target']).open('r+b') as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        assert sha(Path(item['target']).read_bytes()) == item['planned_sha256']
    lp = Path('translations/editorial_review_current_v1.json')
    ledger,before = read(lp),read(CHECKPOINT/(lp.name+'.before'))
    allowed = {'records_with_source_and_prose_pass','records_with_source_prose_drafts','source_prose_reviewed_counts_by_file',
        'reviewed_but_incomplete_route_record_IDs','active_source_prose_drafts','contextual_story_natural_dialogue_pass_v1871',
        'coverage_units','formatting_watchlist','unfinished_editorial_scope_v4231','lil_B169_scope_reconciliation_v4231','latest_checkpoint'}
    assert {k:v for k,v in before.items() if k not in allowed} == {k:v for k,v in ledger.items() if k not in allowed}
    assert ledger['goal_status'] == 'active' and not ledger['full_goal_complete']
    fresh,old = ledger['contextual_story_natural_dialogue_pass_v1871'],before['contextual_story_natural_dialogue_pass_v1871']
    assert fresh['integrated_record_keys'] == old['integrated_record_keys']
    assert fresh['record_keys'][:5656] == old['record_keys']
    keys = [historical_key(row) for row in fresh['record_keys']]
    assert len(keys) == len(set(keys)) == 5692
    assert (fresh['fresh_pass_records_explicitly_reread'],fresh['fresh_pass_records_integrated'],fresh['fresh_pass_records_pending_native_actual_release']) == (5692,5656,36)
    doc = read(DOC)
    rows = doc['records']
    assert len(rows) == 36 and Counter(row['editorial_decision'] for row in rows) == {'revise':19,'retain-wording':17}
    expected = [{'file_path':'/data/SC2.DK4','id':r['id']} for r in rows]
    assert fresh['pending_record_keys'] == fresh['record_keys'][5656:] == expected
    assert len(fresh['pending_contextual_families']) == 1 and fresh['pending_contextual_families'][0]['id'] == FAMILY
    assert ledger['records_with_source_and_prose_pass'] == ledger['records_with_source_prose_drafts'] == 5695
    assert ledger['source_prose_reviewed_counts_by_file']['/data/SC2.DK4'] == 3839
    assert ledger['source_prose_reviewed_counts_by_file']['/data/SC3.DK4'] == 64
    assert sum(ledger['source_prose_reviewed_counts_by_file'].values()) == 5695
    assert (ledger['records_editorially_completed'],ledger['records_revised_and_integrated'],ledger['retained_wordings_editorially_completed']) == (5656,3595,2061)
    for previous,current in zip(before['coverage_units'],ledger['coverage_units'][:-1],strict=True):
        if previous['id'] != 'all-route-scenes':
            assert current == previous
        else:
            assert current['reviewed_route_records'] == 4093 and current['completed_route_records'] == 4057
            assert {k:v for k,v in previous.items() if k not in ['reviewed_route_records','completed_route_records','next']} == {k:v for k,v in current.items() if k not in ['reviewed_route_records','completed_route_records','next']}
    assert ledger['coverage_units'][-1]['id'] == FAMILY and ledger['coverage_units'][-1]['completion_credit_added'] == 0
    source,current = [IlnkContainer.parse(NdsImage.open(path).read_file('/data/SC2.DK4')).blocks[169] for path in ['work/clean.nds',doc['current_ROM']]]
    for row in rows:
        assert all(row['review'].values()) and row['full_clean_context_precedes_comparison']
        assert row['source_meaning'] == row['fresh_source_gloss']
        for data,reference,value in [(source,row['source_reference'],row['source_hex']),(current,row['current_reference'],row['current_hex'])]:
            at = reference['offset']
            raw = bytes.fromhex(value)
            assert data[at:at+len(raw)] == raw and data[at+len(raw)] == 0
        assert row['source_selector'] in [2,6,9,20,21,76]
        if row['editorial_decision'] == 'retain-wording':
            assert row['english'].split('}',1)[1] == row['effective_predecessor_paragraph']
            assert row['fresh_retained_wording_justification']
    approval = read('work/analysis/lil_B169_native_approval_v4230/approval_receipt.json')
    assert approval['manuscripts'] == {str(DOC):sha(DOC.read_bytes())}
    assert (approval['progressive_planes'],approval['current_macro_alignment_cases'],approval['source_consumer_negatives'],approval['source_macro_negatives'],approval['formatter_negatives']) == (36,288,21,2,14)
    assert len(approval['review_sheets']) == 5 and all(s['viewed_in_full_current_turn'] and sha(Path(s['path']).read_bytes()) == s['sha256'] for s in approval['review_sheets'])
    receipt = read(CHECKPOINT/'staged_receipt.json')
    for path,digest in {**receipt['evidence'],**receipt['preserved_release_files']}.items():
        assert sha(Path(path).read_bytes()) == digest,path
    promoted = read('translations/promoted_build.json')
    assert promoted['profile'] == 'all-routes-unified-v4204'
    assert sha(Path(promoted['rom']).read_bytes()) == promoted['rom_sha256']
    scope = ledger['unfinished_editorial_scope_v4231']
    assert sha(Path(scope['path']).read_bytes()) == scope['sha256']
    assert scope['remaining_B170_B180_physical_speeches'] == 231 and scope['incomplete_route_source_prose'] == 36
    assert scope['canonical_Maria32_pending_uncredited'] and scope['wider_story_shared_town_random_help_prose_open']
    assert Path('docs/editorial_handoff_current.md').read_text(encoding='utf-8').startswith('# Current editorial handoff - V4231')
    ROOT.mkdir(parents=True)
    result = dict(checkpoint='V4231',ledger_sha256=sha(lp.read_bytes()),fresh_reread=5692,integrated=5656,pending=36,
        source_prose=5695,revised=3595,retained=2061,new_source_prose_reviews=36,new_completed_records=0,
        all_prior_completions_promoted_main_registry_builder_and_wider_scope_preserved=True,
        all36_clean_current_references_individual_glosses_retentions_and_native_approval_verified=True,
        source_consumer_negatives=21,macro_negatives=2,formatter_negatives=14,native_planes=36,macro_cases=288,
        all5_complete_native_sheets_viewed=True,actual_selected_B169_IDs=[],new_emulator_runs=0,
        remaining_B170_B180_physical_speeches=231,all_jobs_terminal=True,full_goal_active=True,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False)
    save(ROOT/'verified_handoff.json',result)
    save(CHECKPOINT/'checkpoint_receipt.json',{**receipt,'ledger_sha256':result['ledger_sha256'],
        'updated_files':{str(Path(r['target']).relative_to(workspace)):r['planned_sha256'] for r in plan}})
    print('V4231 independently verified:5692/5656/36;5695 source/prose. All36 source/current/native references and17 justified retentions pass. V4204 main unchanged;full goal active.')
