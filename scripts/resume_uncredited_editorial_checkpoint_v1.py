"""Commit an exact backed-up uncredited checkpoint after a transient Windows rename refusal."""
import argparse,gzip,json,os,time
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from dk4tool.patch.grand_race_menu_release import sha

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--mutation',type=Path,required=True)
    parser.add_argument('--pending',type=Path,required=True)
    parser.add_argument('--allow-key',action='append',required=True)
    args=parser.parse_args();dest=Path('translations/editorial_review_current_v1.json')
    verified=args.mutation/'verified_mutations.json';assert not verified.exists()
    plan=load(args.mutation/'mutation_plan.json');before=gzip.decompress((args.mutation/'ledger.before.json.gz').read_bytes())
    assert sha(before)==plan['ledger_before_sha256']==sha(dest.read_bytes())
    pending=args.pending.read_bytes();assert sha(pending)==plan['ledger_after_sha256']
    old,new=map(json.loads,[before,pending]);allowed=set(args.allow_key)|{'latest_checkpoint'}
    assert all(new[k]==v for k,v in old.items() if k not in allowed)
    assert set(new)-set(old)<=allowed and not (set(old)-set(new))
    for key in allowed-{'latest_checkpoint'}:
        assert key in new and new[key]['new_credit']==0
        if key in old:assert old[key].get('new_credit',0)==0
    assert (old['records_editorially_completed'],new['records_editorially_completed'])==(11418,11418)
    assert not new['full_goal_complete'] and plan['new_credit']==0
    assert new['current_integrated_candidate']==old['current_integrated_candidate']
    for entry in plan['documentation']:assert sha(Path(entry['path']).read_bytes())==entry['after_sha256']
    for path,digest in plan['protected'].items():assert sha(Path(path).read_bytes())==digest
    refused=[]
    for attempt in range(5):
        assert sha(dest.read_bytes())==plan['ledger_before_sha256'] and sha(args.pending.read_bytes())==plan['ledger_after_sha256']
        try:os.replace(args.pending,dest)
        except PermissionError as error:
            refused.append(str(error))
            if attempt==4:raise
            time.sleep(.25)
        else:break
    assert sha(dest.read_bytes())==plan['ledger_after_sha256']
    for path,digest in plan['protected'].items():assert sha(Path(path).read_bytes())==digest
    save(verified,dict(ledger_sha256=plan['ledger_after_sha256'],completed=11418,
        all_other_keys_preserved=True,protected_release_identities_unchanged=True,new_credit=0,full_goal_complete=False,
        exact_prepared_transaction_resumed_without_regenerating_or_double_crediting=True,
        original_Windows_rename_refusal_preserved_in_producer_history=True,retry_refusals=refused,
        producer_sha256=sha(Path(__file__).read_bytes())))
    print('Committed exact pending uncredited checkpoint;11418 integrated unchanged;all unrelated keys andprotected identities exact.')
