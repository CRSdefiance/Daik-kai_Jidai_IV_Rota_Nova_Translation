"""Align the expanded batch's identity/visual references without changing coverage orreview decisions."""
import gzip
import os
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from scripts.editorial_ledger_storage_v1 import encode_ledger
from dk4tool.patch.grand_race_menu_release import sha

if __name__=='__main__':
    ledger=Path('translations/editorial_review_current_v1.json');root=Path('work/analysis/Rafael255_storage_reference_alignment_20261105')
    assert not root.exists();before=ledger.read_bytes();prior=load(ledger)
    checkpoint=Path('work/analysis/Rafael255_storage_checkpoint_20261105/verified_mutations.json')
    assert sha(before)==load(checkpoint)['ledger_sha256'] and prior['records_editorially_completed']==11845
    key='Rafael_SC0_B101_B120_clean_20261105';old=prior[key];batch=dict(old)
    identity=Path(old['scoped_identity']);visual=Path('work/analysis/Rafael255_reconstruction_inputs_v1_20261105/visual_andinventory_approval.json')
    drafts=Path('work/analysis/Rafael_B101_B120_clean_20261105/14_style_meanings_andindependent_drafts_v1.json')
    batch.update(scoped_identity_sha256=sha(identity.read_bytes()),complete_direct_visual_approval=str(visual),
        complete_direct_visual_approval_sha256=sha(visual.read_bytes()),independent_source_style_drafts=14,
        style_drafts=str(drafts),style_drafts_sha256=sha(drafts.read_bytes()))
    assert batch['new_credit']==0 and batch['contextual_comparisons']==255 and batch['all_fifth_formatting_gates_pending']
    updated={**prior,key:batch};assert all(updated[k]==v for k,v in prior.items() if k!=key)
    encoded=encode_ledger(updated);root.mkdir();(root/'ledger.before.json.gz').write_bytes(gzip.compress(before,compresslevel=1,mtime=0))
    assert gzip.decompress((root/'ledger.before.json.gz').read_bytes())==before
    save(root/'mutation_plan.json',dict(previous_checkpoint=str(checkpoint),previous_checkpoint_sha256=sha(checkpoint.read_bytes()),
        ledger_before_sha256=sha(before),ledger_after_sha256=sha(encoded),batch_key=key,
        changed_fields={k:dict(before=old.get(k),after=v) for k,v in batch.items() if old.get(k)!=v},
        all_other_keys_counts_review_decisions_source_keys_andrelease_identities_preserved=True,new_credit=0))
    assert ledger.read_bytes()==before
    staged=ledger.with_name('editorial_review_current_v1.pending_Rafael255_reference_alignment.json');assert not staged.exists()
    staged.write_bytes(encoded);os.replace(staged,ledger);assert sha(ledger.read_bytes())==sha(encoded)
    save(root/'verified_mutations.json',dict(ledger_sha256=sha(encoded),completed=11845,
        all_other_keys_preserved=True,source_identity_andcomplete255_visual_references_hash_exact=True,new_credit=0,full_goal_complete=False))
    doc=Path('docs/editorial_Rafael255_storage_checkpoint_20261105.md')
    previous=doc.read_bytes();(root/'checkpoint_document.before.md').write_bytes(previous)
    with doc.open('a',encoding='utf-8',newline='\n') as output:
        output.write('\nCoverage reference alignment: `work/analysis/Rafael255_storage_reference_alignment_20261105/verified_mutations.json` is the latest ledger hash. It corrects the expanded identity digest and points the complete visual reference to the255-object composite; counts and all review decisions are unchanged.\n')
    print('Aligned six expanded identity/style/visual reference fields;255 reviews and11845 integrated unchanged.')
