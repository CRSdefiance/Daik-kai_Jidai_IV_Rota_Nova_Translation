"""Refresh only the four latest path/hash pairs in the unfinished539 ledger entry."""
import gzip,os
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from scripts.editorial_ledger_storage_v1 import encode_ledger
from dk4tool.patch.grand_race_menu_release import sha

if __name__=='__main__':
    root=Path('work/analysis/Rafael_B61_B80_checked_20261104/checkpoint_reference_hash_repair_v1')
    ledger=Path('translations/editorial_review_current_v1.json');assert not root.exists()
    before=ledger.read_bytes();doc=load(ledger);key='Rafael_SC0_B61_B80_clean_20261104'
    entry=dict(doc[key]);changes=[]
    for name in ['final_formatting_input','final_body_plan','final_native_body','body_display_approval']:
        path=Path(entry[name]);digest=sha(path.read_bytes());prior=entry[name+'_sha256']
        assert digest!=prior
        entry[name+'_sha256']=digest;changes.append(dict(field=name,path=str(path),previous_sha256=prior,sha256=digest))
    assert entry['new_credit']==0 and doc['records_editorially_completed']==10774
    result={**doc,key:entry};assert all(result[k]==v for k,v in doc.items() if k!=key)
    encoded=encode_ledger(result);root.mkdir(parents=True)
    (root/'ledger.before.json.gz').write_bytes(gzip.compress(before,compresslevel=1,mtime=0))
    target=ledger.with_name('editorial_review_current.Rafael539_hash_repair.pending.json');assert not target.exists()
    target.write_bytes(encoded);assert load(target)==result and ledger.read_bytes()==before
    os.replace(target,ledger)
    save(root/'verification.json',dict(previous_ledger_sha256=sha(before),current_ledger_sha256=sha(ledger.read_bytes()),
        changed_entry=key,changes=changes,all_other_entries_andall_prose_credit_andrelease_state_unchanged=True,
        new_credit=0,producer_sha256=sha(Path(__file__).read_bytes())))
    print('Four latest path/hash pairs corrected;all other ledger content and10774 completions unchanged.')
