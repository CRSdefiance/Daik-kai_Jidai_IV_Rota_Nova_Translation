"""Clear explicitly named stale status flags after verified once-only registration."""
import argparse
import gzip
import os
from copy import deepcopy
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--batch',required=True)
    for name in ['release','out']:p.add_argument('--'+name,type=Path,required=True)
    p.add_argument('--flags',nargs='+',required=True);args=p.parse_args()
    assert not args.out.exists() and len(args.flags)==len(set(args.flags))
    release=load(args.release);ledgerpath=Path('translations/editorial_review_current_v1.json')
    before=ledgerpath.read_bytes();prior=load(ledgerpath);batch=prior[args.batch]
    assert not prior['full_goal_complete'] and release['exact_all_integrated_references_bound']
    assert release['clean_input_patch_byte_exact'] and not release['own_registered_startup_pending']
    assert digest(release['candidate'])==release['candidate_sha256']==prior['current_integrated_candidate']['sha256']
    assert digest('translations/release_stack.json')==release['registry_sha256']
    assert batch['new_credit']==batch['completion_credit_added']==release['new_contextual_records']>0
    assert batch['registered_release_verification_sha256']==digest(args.release)
    bindings=load(release['exact_record_bindings'])['records']
    assert digest(release['exact_record_bindings'])==release['exact_record_bindings_sha256']
    assert len(bindings)==batch['new_credit'] and all(all(r['review'].values()) for r in bindings)
    assert batch['all_five_registered_review_gates_pass'] and batch['final_cumulative_integration_complete']
    assert all(flag.endswith('_pending') and batch[flag] is True for flag in args.flags)
    ledger=deepcopy(prior)
    for flag in args.flags:ledger[args.batch][flag]=False
    assert {k:v for k,v in ledger.items() if k!=args.batch}=={k:v for k,v in prior.items() if k!=args.batch}
    assert {k:v for k,v in ledger[args.batch].items() if k not in args.flags}=={k:v for k,v in batch.items() if k not in args.flags}
    args.out.mkdir(parents=True)
    backup=args.out/'ledger_before.json.gz';backup.write_bytes(gzip.compress(before,compresslevel=1,mtime=0));assert gzip.decompress(backup.read_bytes())==before
    encoded=encode_ledger(ledger);pending=ledgerpath.with_name('editorial_review_current.'+args.out.name+'.pending.json')
    assert not pending.exists();pending.write_bytes(encoded);assert ledgerpath.read_bytes()==before
    os.replace(pending,ledgerpath);assert ledgerpath.read_bytes()==encoded
    save(args.out/'verification.json',dict(batch=args.batch,cleared_flags=args.flags,ledger_before_sha256=__import__('hashlib').sha256(before).hexdigest(),ledger_after_sha256=digest(ledgerpath),
        existing_credit_preserved=batch['new_credit'],all_counts_other_keys_andunrelated_batches_exact=True,
        registered_release=str(args.release),registered_release_sha256=digest(args.release),new_credit=0,full_goal_complete=False))
    print('Cleared stale registered status flags; all credit and unrelated ledger data preserved.')


if __name__=='__main__':main()
