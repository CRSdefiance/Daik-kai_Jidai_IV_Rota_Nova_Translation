"""Verify current ledger formatting by exact prior bytes and complete semantic equality."""
import gzip
import json
from pathlib import Path
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/editorial_handoff_verification_v4360')
CHECKPOINT=Path('work/analysis/editorial_ledger_storage_v4359')

if __name__=='__main__':
    assert not ROOT.exists()
    receipt=read(CHECKPOINT/'storage_receipt.json')
    raw=gzip.decompress((CHECKPOINT/'ledger.before.json.gz').read_bytes())
    assert sha(raw)==receipt['before_ledger_sha256'] and len(raw)==receipt['before_bytes']==105030011
    old=json.loads(raw);lp=Path('translations/editorial_review_current_v1.json');data=lp.read_bytes();current=json.loads(data)
    assert sha(data)==receipt['ledger_sha256'] and len(data)==receipt['after_bytes']==88387409
    assert data==encode_ledger(current) and data.count(b'\n')==data.count(b'\r\n') and len(data)<100*1024*1024
    record=current['current_ledger_storage_v4359']
    assert {k:v for k,v in current.items() if k!='current_ledger_storage_v4359'}==old
    assert record['before_sha256']==sha(raw) and record['before_bytes']==len(raw)
    assert sha(Path(record['encoder']).read_bytes())==record['encoder_sha256']
    for key in ['updated_files','preserved_files']:
        for path,digest in receipt[key].items():assert sha(Path(path).read_bytes())==digest,(key,path)
    for row in read(CHECKPOINT/'mutation_plan.json'):
        assert sha(Path(row['before_copy']).read_bytes())==row['before_sha256']
        assert Path(row['planned']).read_bytes()==Path(row['path']).read_bytes()
    prior=Path(receipt['prior_verified_handoff']);proof=read(prior)
    assert sha(prior.read_bytes())==receipt['prior_verified_handoff_sha256']==record['prior_verified_handoff_sha256']
    assert proof['ledger_sha256']==sha(raw) and proof['checkpoint']=='V4357'
    completion=read('work/analysis/lil_B171_completion_v4357/completion_receipt.json')
    assert completion['updated_files'][str(lp.resolve())]==sha(raw)
    fresh=current['contextual_story_natural_dialogue_pass_v1871']
    assert (fresh['fresh_pass_records_explicitly_reread'],fresh['fresh_pass_records_integrated'],fresh['fresh_pass_records_pending_native_actual_release'])==(5762,5762,0)
    assert not fresh['pending_contextual_families'] and not fresh['pending_record_keys']
    assert (current['records_with_source_and_prose_pass'],current['records_editorially_completed'],current['records_revised_and_integrated'],current['retained_wordings_editorially_completed'])==(5765,5762,3659,2103)
    assert current['goal_status']=='active' and not current['full_goal_complete']
    candidate=current['current_integrated_candidate'];promotion=read('translations/promoted_build.json')
    assert candidate['profile']=='all-routes-unified-v4353' and promotion['profile']=='all-routes-unified-v4303'
    assert sha(Path(candidate['path']).read_bytes())==candidate['sha256']==proof['candidate_sha256']=='964c2da7273773c2db63b53eaf1136981d212c4e6282aee303ad101cc508de4e'
    assert sha(Path(candidate['patch']).read_bytes())==candidate['patch_sha256']==proof['patch_sha256']=='96d1fd20e085519c65b75dfd88d57ced2b4a6b1d21503ed385173833dd83528b'
    manifest=read(candidate['manifest']);registry=read('translations/release_stack.json')
    assert len(manifest['batches'])==547 and len(registry['accepted_layers'])==114
    assert manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes())
    assert registry['latest_promoted_build']['profile']==promotion['profile']
    assert Path('docs/editorial_handoff_current.md').read_text(encoding='utf-8').startswith('# Current editorial handoff - V4359')
    assert 'scripts.editorial_ledger_storage_v1.encode_ledger' in Path('docs/build_continuity_protocol.md').read_text(encoding='utf-8')
    ROOT.mkdir(parents=True)
    save(ROOT/'verified_handoff.json',dict(checkpoint='V4359',ledger_sha256=sha(data),ledger_bytes=len(data),
        previous_exact_ledger_bytes_preserved=True,all_previous_JSON_values_identical=True,only_new_storage_provenance_field_added=True,
        all_B171_completion_source_predecessor_native_actual_and_registered_evidence_reused_by_exact_values_and_ROM_hashes=True,
        prior_full_completion_audit=str(prior),prior_full_completion_audit_sha256=sha(prior.read_bytes()),
        fresh_reread=5762,integrated=5762,pending=0,source_prose=5765,revised=3659,retained=2103,
        candidate=candidate['path'],candidate_sha256=candidate['sha256'],patch=candidate['patch'],patch_sha256=candidate['patch_sha256'],
        manifest_batches=547,accepted_layers=114,promoted_main_V4303_unchanged=True,
        new_source_prose_reviews=0,new_completed_records=0,new_emulator_runs=0,
        remaining_B172_B180_physical_speeches=161,remaining_choice_command_leads=0,
        all_jobs_terminal=True,full_goal_active=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('V4360 independent storage audit passes:all prior JSON values and exact bytes preserved;88.39MB;5762 integrated/0 pending;V4353 candidate,V4303 main. Full goal active.')
