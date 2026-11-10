"""Independent pre-apply/post-apply lossless ledger and release audit."""
from pathlib import Path
from copy import deepcopy
import argparse
import json

from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/shop657_checkpoint_v4771')

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--applied',action='store_true');args=parser.parse_args()
    plan=read(ROOT/'metadata_plan.json');files=plan['files'];assert len(files)==9
    for row in files:
        staged=Path(row['staged']).read_bytes();assert sha(staged)==row['after_sha256']
        p=Path(row['target'])
        if args.applied:assert p.read_bytes()==staged
        elif row['existed']:assert p.read_bytes()==Path(row['before']).read_bytes() and sha(p.read_bytes())==row['before_sha256']
        else:assert not p.exists()
        if row['existed'] and p.suffix=='.md':
            old=Path(row['before']).read_text(encoding='utf-8');new=staged.decode('utf-8').replace('\r\n','\n')
            assert old in new or new.endswith(old.split('\n',1)[1].lstrip('\n'))
    row=next(r for r in files if Path(r['target'])==Path('translations/editorial_review_current_v1.json'))
    before=json.loads(Path(row['before']).read_bytes());after=json.loads(Path(row['staged']).read_bytes())
    inverse=deepcopy(after)
    inverse['current_integrated_candidate']=inverse.pop('previous_current_integrated_candidate_before_shop657_v4771')
    inverse['latest_checkpoint']=inverse.pop('previous_latest_checkpoint_before_shop657_v4771')
    inverse.pop(plan['ledger_key']);inverse.pop('editorial_localization_and_layout_standard_v4771')
    assert inverse==before
    for field in ['records_editorially_completed','records_with_source_and_prose_pass',
                  'records_revised_and_integrated','retained_wordings_editorially_completed',
                  'completed_editorial_record_counts_by_file','source_prose_reviewed_counts_by_file']:
        assert before[field]==after[field]
    assert after['full_goal_complete'] is False and after[plan['ledger_key']]['added_editorial_credit']==0
    for p in after[plan['ledger_key']]['B180_passing_proofs']:assert Path(p).exists()
    release=read('work/analysis/shop657_release_v4767/registered_release_verification.json')
    actual=read('work/analysis/shop657_actual_verification_v4770/ordinary_actual_and_startup_verification.json')
    current=after['current_integrated_candidate'];manifest=read(current['manifest']);stack=read('translations/release_stack.json')
    assert current['sha256']==release['candidate_sha256']==manifest['candidate_sha256']==actual['candidate_sha256']==sha(Path(current['path']).read_bytes())
    assert current['patch_sha256']==sha(Path(release['patch']).read_bytes())
    assert manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes())
    assert len(manifest['batches'])==561 and len(stack['accepted_layers'])==114 and all(manifest['checks'].values())
    assert stack['latest_promoted_build']['profile']=='all-routes-unified-v4701'
    assert release['exact_clean_input_reconstruction'] and release['expected_whole_ROM_equal']
    assert len(actual['actual_holds'])==4 and actual['total_new_emulator_frames']==20003
    assert after[plan['ledger_key']]['all8_actual_screens_and6_native_tiles_viewed'] is True
    final=next(r for r in files if Path(r['target'])==Path('translations/shop657_layout_final_review_v1.json'))
    f=json.loads(Path(final['staged']).read_bytes());r=f['records'][0]
    assert r['integrated_hex']==r['proposed_compiled_hex'] and r['actual_evidence']['hold_frame']==8000
    assert f['added_editorial_credit']==0 and f['actual_new_gameplay_pending'] is False
    receipt=ROOT/('post_apply_audit.json' if args.applied else 'pre_apply_audit.json')
    assert not receipt.exists()
    save(receipt,dict(all9_metadata_targets_exact=True,all_original_root_and_nested_ledger_history_preserved=True,
        all_coverage_counters_preserved=True,registered_candidate_manifest_patch_actual_and_source_bindings_exact=True,
        full_editorial_objective_preserved=True,all114_accepted_layers_and_promoted_main_unchanged=True,
        staged_not_applied=not args.applied,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('Lossless ledger,9 metadata targets,561 cumulative entries,exact patch and completed actual657 checks pass; '+('applied.' if args.applied else 'staged only.'))
