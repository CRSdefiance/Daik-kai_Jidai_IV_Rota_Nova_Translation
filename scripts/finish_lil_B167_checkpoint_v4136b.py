"""Finish a partially written documentation checkpoint without reapplying ledger credit."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.checkpoint_lil_B167_v4136 import ROOT,PRIOR,APPROVAL,SUMMARY
from scripts.verify_village_wrap_v608 import read,save
if __name__=='__main__':
    assert ROOT.exists() and not (ROOT/'checkpoint_receipt.json').exists()
    lp=Path('translations/editorial_review_current_v1.json');ledger=read(lp);fresh=ledger['contextual_story_natural_dialogue_pass_v1871']
    assert (fresh['fresh_pass_records_explicitly_reread'],fresh['fresh_pass_records_integrated'],fresh['fresh_pass_records_pending_native_actual_release'])==(5602,5573,29)
    ledger_hash=sha(lp.read_bytes());inv=ROOT/'unfinished_editorial_scope_inventory.json'
    docs=[Path('docs')/n for n in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']]
    section='## V4136: 29 B167 contextual/native reviews; integration pending\n\n'+SUMMARY+'\n\nApproval: '+APPROVAL.as_posix()+'. Unfinished scope: '+inv.as_posix()+'.\n\n'
    states=[]
    for i,p in enumerate(docs):
        before=ROOT/(p.name+'.before');old=before.read_bytes();first,rest=before.read_text(encoding='utf-8').split('\n',1)
        expected=(('# Current editorial handoff - V4136' if i==0 else first)+'\n\n'+section+rest).encode('utf-8')
        observed=p.read_bytes();assert observed in [old,expected],str(p)
        states.append(dict(path=str(p),before_sha256=sha(old),observed_sha256=sha(observed),expected_sha256=sha(expected),already_complete=observed==expected))
        if observed!=expected:
            tmp=p.with_name(p.name+'.v4136b.tmp');assert not tmp.exists();tmp.write_bytes(expected);tmp.replace(p)
        assert p.read_bytes()==expected
    assert sha(lp.read_bytes())==ledger_hash
    stable=[Path('translations/release_stack.json'),Path('translations/promoted_build.json'),Path('scripts/build_integrated_release.py')]
    save(ROOT/'partial_write_recovery_v4136b.json',dict(original_failure='OSError Errno22 opening docs/todo.md; ledger and first three docs had completed; remaining docs unchanged.',observed_states=states,ledger_credited_once_and_not_rewritten=True,producer_sha256=sha(Path(__file__).read_bytes()),original_producer_sha256=sha(Path('scripts/checkpoint_lil_B167_v4136.py').read_bytes())))
    save(ROOT/'checkpoint_receipt.json',dict(checkpoint='V4136',evidence=ledger['lil_B167_scope_reconciliation_v4136']['evidence'],updated_files={str(p):sha(p.read_bytes()) for p in [lp,*docs]},preserved_release_files={str(p):sha(p.read_bytes()) for p in stable},prior_verified_handoff=str(PRIOR),partial_write_recovery=str(ROOT/'partial_write_recovery_v4136b.json'),partial_write_recovery_sha256=sha((ROOT/'partial_write_recovery_v4136b.json').read_bytes()),new_source_prose_reviews=29,new_completed_records=0,proposed_revisions=16,justified_retentions=13,fresh_reread=5602,fresh_integrated=5573,fresh_pending=29,source_prose=5605,completed=5573,historical_revised=3551,historical_retained=2022,new_emulator_runs=0,all_jobs_terminal=True,full_goal_complete=False))
    print('V4136 documentation finished from exact backups; ledger remains credited once. Independent audit required.')
