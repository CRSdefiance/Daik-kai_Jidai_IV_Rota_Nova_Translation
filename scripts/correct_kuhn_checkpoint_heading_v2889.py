"""Correct one inherited heading; preserve every review, count and release byte."""
from pathlib import Path
from copy import deepcopy
from shutil import copy2
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/lil_Kuhn_Alliance_heading_v2889')
AUDIT=Path('work/analysis/editorial_handoff_verification_v2888/verified_handoff.json')
OLD='## V2887:90 Kuhn alliance reviews completed in V2883'
NEW='## V2887:82 Kuhn alliance reviews completed in V2883'
if __name__=='__main__':
    assert not ROOT.exists();audit=read(AUDIT);prior=Path(audit['handoff_receipt']);receipt=read(prior)
    for p,d in receipt['updated_files'].items():assert sha(Path(p).read_bytes())==d,p
    ledger=Path(audit['ledger']);assert sha(ledger.read_bytes())==audit['ledger_sha256']
    docs=[Path(p) for p in receipt['updated_files'] if Path(p).parent==Path('docs')]
    assert len(docs)==5 and all(p.read_text(encoding='utf-8').count(OLD)==1 for p in docs)
    ROOT.mkdir(parents=True)
    for p in [ledger,*docs]:copy2(p,ROOT/(p.name+'.before'))
    for p in docs:
        original=p.read_bytes();changed=original.replace(OLD.encode(),NEW.encode(),1)
        assert changed!=original;p.write_bytes(changed)
        assert p.read_bytes()==(ROOT/(p.name+'.before')).read_bytes().replace(OLD.encode(),NEW.encode(),1)
    assert sha(ledger.read_bytes())==audit['ledger_sha256']
    proof=ROOT/'heading_only_correction.json'
    save(proof,dict(prior_verified_handoff=str(AUDIT),prior_verified_handoff_sha256=sha(AUDIT.read_bytes()),prior_completion_receipt=str(prior),prior_completion_receipt_sha256=sha(prior.read_bytes()),old_heading=OLD,new_heading=NEW,before_files=receipt['updated_files'],after_files={str(p):sha(p.read_bytes()) for p in [ledger,*docs]},only_five_heading_literals_changed=True,ledger_all_records_counts_and_current_candidate_byte_identical=True,source_prose_or_completion_credit_added=0,no_ROM_registry_builder_or_manifest_change=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    combined=deepcopy(receipt);combined.update(updated_files={str(p):sha(p.read_bytes()) for p in [ledger,*docs]},baseline_completion_root='work/analysis/lil_Kuhn_Alliance_completion_v2887',metadata_correction=str(proof),metadata_correction_sha256=sha(proof.read_bytes()),this_operation_adds_source_prose_orcompletion_credit=0)
    combined['evidence'].update({str(prior):sha(prior.read_bytes()),str(AUDIT):sha(AUDIT.read_bytes()),str(proof):sha(proof.read_bytes()),str(Path(__file__)):sha(Path(__file__).read_bytes())})
    final_receipt=ROOT/'completion_receipt.json';save(final_receipt,combined)
    verified=deepcopy(audit);verified.update(handoff_receipt=str(final_receipt),handoff_receipt_sha256=sha(final_receipt.read_bytes()),metadata_correction=str(proof),metadata_correction_sha256=sha(proof.read_bytes()),original_verification=str(AUDIT),original_verification_sha256=sha(AUDIT.read_bytes()),no_new_native_or_gameplay_reexecution=True,this_operation_adds_credit=0,producer_sha256=sha(Path(__file__).read_bytes()))
    for p,d in combined['updated_files'].items():assert sha(Path(p).read_bytes())==d
    save(ROOT/'verified_handoff.json',verified)
    print('Corrected five V2887 headings from90 to82. Ledger/reviews/counts/ROM/patch unchanged; original receipts and backups preserved.')
