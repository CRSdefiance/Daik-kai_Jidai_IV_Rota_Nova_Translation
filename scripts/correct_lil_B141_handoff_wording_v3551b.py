"""Correct one opcode-description typo; preserve the original checkpoint and all counts."""
from copy import deepcopy
from pathlib import Path
from shutil import copy2
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
if __name__=='__main__':
    root=Path('work/analysis/lil_B141_checkpoint_wording_v3551b');assert not root.exists();receiptpath=Path('work/analysis/lil_B141_checkpoint_v3551/checkpoint_receipt.json');receipt=read(receiptpath)
    for p,d in receipt['updated_files'].items():assert sha(Path(p).read_bytes())==d
    old='while A0000080-style ownership is not inferred from prose:the exact payment command00a0ffffbdff0191 deducts900,000.'
    new='while the distinct exact A000 payment command00a0ffffbdff0191 deducts900,000. Its ownership is established from the native code and guarded execution.'
    lp=Path('translations/editorial_review_current_v1.json');ledger=read(lp);before=deepcopy(ledger);docs=[Path('docs')/n for n in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']];root.mkdir(parents=True)
    for p in [lp,*docs]:copy2(p,root/(p.name+'.before'))
    for key in ['latest_checkpoint']:
        assert ledger[key].count(old)==1;ledger[key]=ledger[key].replace(old,new)
    s=ledger['lil_B141_scope_reconciliation_v3551']['summary'];assert s.count(old)==1;ledger['lil_B141_scope_reconciliation_v3551']['summary']=s.replace(old,new)
    expected=deepcopy(before);expected['latest_checkpoint']=ledger['latest_checkpoint'];expected['lil_B141_scope_reconciliation_v3551']['summary']=ledger['lil_B141_scope_reconciliation_v3551']['summary'];assert ledger==expected;save(lp,ledger)
    for p in docs:
        t=p.read_text(encoding='utf-8');assert t.count(old)==1;p.write_text(t.replace(old,new),encoding='utf-8',newline='\n')
    save(root/'wording_correction_receipt.json',dict(checkpoint='V3551',original_receipt=str(receiptpath),original_receipt_sha256=sha(receiptpath.read_bytes()),before_ledger_sha256=sha((root/(lp.name+'.before')).read_bytes()),after_ledger_sha256=sha(lp.read_bytes()),old=old,new=new,only_two_ledger_summary_strings_and_five_document_paragraphs_changed=True,all_record_counts_reviews_pending_scope_ROM_registry_and_proofs_unchanged=True,updated_files={str(p):sha(p.read_bytes()) for p in [lp,*docs]},producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
