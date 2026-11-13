"""Finish the exact saved checkpoint plan through verified sibling-file replacements.

The first writer created the new standalone report and backups, then Windows
rejected opening the compressed handoff for direct writing. Its other five
documents and ledger remain byte-exact at the saved before hashes. Do not rerun
the original checkpoint or discard its plan; finish only these planned bytes.
"""
import gzip,os
from pathlib import Path
from scripts import checkpoint_maria270_research_v1 as producer
from scripts.audit_story_glyph_consistency import load,save
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from dk4tool.patch.grand_race_menu_release import sha

def main():
    captured=[]
    producer.checkpoint=lambda **kwargs:captured.append(kwargs)
    producer.main();assert len(captured)==1;k=captured[0]
    root=Path(k['mutation']);plan=load(root/'mutation_plan.json')
    assert not (root/'verified_mutations.json').exists()
    for p,h in k['protected'].items():assert digest(p)==h
    ledger_path=Path('translations/editorial_review_current_v1.json')
    before=gzip.decompress((root/'ledger.before.json.gz').read_bytes())
    assert sha(before)==plan['ledger_before_sha256']==digest(ledger_path)
    prior=load(ledger_path);ledger=dict(prior)
    assert prior['records_editorially_completed']==k['completed']==19462
    assert k['batch_updates']['new_credit']==0 and not prior['full_goal_complete']
    ledger[k['batch_key']]={**prior[k['batch_key']],**k['batch_updates']}
    for key,value in k['additional_updates'].items():
        assert key in prior and prior[key].get('new_credit',0)==value['new_credit']==0
        ledger[key]={**prior[key],**value}
    ledger['latest_checkpoint']=k['summary']
    assert all(ledger[key]==value for key,value in prior.items()
        if key not in [k['batch_key'],'latest_checkpoint',*k['additional_updates']])
    encoded=encode_ledger(ledger);assert sha(encoded)==plan['ledger_after_sha256']
    updates={Path(k['document']):k['document_text'].encode('utf-8')}
    prefix=('# Current editorial checkpoint - 2026-11-09\n\n'+k['summary']+'\n\nContinue from ['+
        Path(k['document']).stem+']('+Path(k['document']).name+'). Reuse the completed checks; earlier entries below are historical.\n\n').encode('utf-8')
    for index,row in enumerate(plan['documentation']):
        p=Path(row['path'])
        if row['before_sha256'] is not None:
            original=(root/f'{index}.before').read_bytes();assert sha(original)==row['before_sha256']
            updates[p]=prefix+original
        assert sha(updates[p])==row['after_sha256']
        assert (digest(p) if p.exists() else None) in [row['before_sha256'],row['after_sha256']]
    # Every replacement is validated before any existing destination is changed.
    for row in plan['documentation']:
        p=Path(row['path'])
        if digest(p)==row['after_sha256']:continue
        staged=p.with_name(p.name+'.Maria270_recovery_v1.pending')
        assert not staged.exists()
        with staged.open('xb') as f:f.write(updates[p])
        assert digest(staged)==row['after_sha256'] and digest(p)==row['before_sha256']
        os.replace(staged,p);assert digest(p)==row['after_sha256']
    staged=ledger_path.with_name(ledger_path.name+'.Maria270_recovery_v1.pending')
    assert not staged.exists() and digest(ledger_path)==plan['ledger_before_sha256']
    with staged.open('xb') as f:f.write(encoded)
    assert digest(staged)==plan['ledger_after_sha256'];os.replace(staged,ledger_path)
    for p,h in k['protected'].items():assert digest(p)==h
    assert digest(ledger_path)==plan['ledger_after_sha256']
    save(root/'verified_mutations.json',dict(ledger_sha256=digest(ledger_path),completed=19462,
        all_other_keys_preserved=True,protected_release_identities_unchanged=True,new_credit=0,full_goal_complete=False,
        recovered_exact_original_plan=True,direct_document_open_failed_before_ledger_mutation=True,
        recovery_producer=str(Path(__file__)),recovery_producer_sha256=digest(__file__)))
    print('Recovered exact saved checkpoint plan;all six document hashes andledger match;zero credit;releases unchanged.')

if __name__=='__main__':main()
