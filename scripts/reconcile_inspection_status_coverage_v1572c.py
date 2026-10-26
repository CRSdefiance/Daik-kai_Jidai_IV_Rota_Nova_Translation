"""Reconcile two1572 source reviews into the historical draft alias and subset index."""
from pathlib import Path
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
if __name__=='__main__':
    root=Path('work/analysis/inspection_status_coverage_v1572c');assert not root.exists()
    path=Path('translations/editorial_review_current_v1.json');ledger=read(path)
    assert ledger['records_with_source_and_prose_pass']==1492 and ledger['records_with_source_prose_drafts']==1490
    assert ledger['records_editorially_completed']==1338 and len(ledger['reviewed_but_incomplete_COMMON_IDs'])==154
    source='translations/inspection_status_editorial_manuscript_v1.json'
    assert all(n in ledger['active_source_prose_drafts']['native_message_IDs'] for n in [306,307])
    ledger['records_with_source_prose_drafts']=1492
    ledger['active_source_prose_drafts']['manuscript_record_subsets_pending'][source]=[306,307]
    root.mkdir(parents=True)
    save(root/'legacy_alias_and_subset_reconciliation.json',{'source_review_producer':'scripts/author_inspection_status_v1572b.py',
        'source_review_manuscript':source,'manuscript_sha256':sha(Path(source).read_bytes()),
        'explanation':'1572b added two genuine source/prose reviews to the primary count and pending IDs but omitted the historical alias and manuscript subset index. Bring those two bookkeeping fields into agreement without adding any further reviews or completions.',
        'primary_source_prose':1492,'legacy_alias_before':1490,'legacy_alias_after':1492,'completed':1338,
        'additional_source_reviews_added':0,'additional_completion_credit':0,'full_goal_complete':False})
    ledger['inspection_status_source_counter_reconciliation']=str(root/'legacy_alias_and_subset_reconciliation.json')
    save(path,ledger);print('Historical source-draft alias and pending subset reconciled;primary1492 and completed1338 unchanged.')
