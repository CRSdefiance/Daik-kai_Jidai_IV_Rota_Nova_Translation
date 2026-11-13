"""Publish only the exact completion bytes already verified before a Windows rename failure."""
import gzip,os
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/maria270_release_v1')
def main():
    checkpoint=ROOT/'completion_checkpoint.json';assert not checkpoint.exists()
    plan=load(ROOT/'completion_mutation_plan.json');release=load(ROOT/'registered_release_verification.json')
    ledger=Path('translations/editorial_review_current_v1.json');pending=Path(plan['pending'])
    assert pending.resolve()==ledger.with_name('editorial_review_current.Maria270_completion_v1.pending.json').resolve()
    assert plan['new_credit']==270 and plan['family']=='Maria_SC3_B37_B49_contextual_integrated_20261109'
    assert digest(ledger)==plan['ledger_before_sha256'] and digest(pending)==plan['ledger_after_sha256']
    assert sha(gzip.decompress((ROOT/'ledger_before_completion.json.gz').read_bytes()))==plan['ledger_before_sha256']
    intended=load(pending);prior=load(ledger)
    assert prior['records_editorially_completed']==19462 and intended['records_editorially_completed']==19732
    assert intended['records_revised_and_integrated']==11871 and intended['retained_wordings_editorially_completed']==7861
    assert intended['records_with_source_and_prose_pass']==intended['records_with_source_prose_drafts']==19735
    assert intended['current_integrated_candidate']['sha256']==release['candidate_sha256']==digest(release['candidate'])
    assert digest('translations/release_stack.json')==release['registry_sha256']
    context='contextual_story_natural_dialogue_pass_v1871';batch='Maria_SC3_B37_B49_display_20261109'
    assert intended[batch]['completion_credit_added']==intended[batch]['new_credit']==270
    for field in ['record_keys','integrated_record_keys','record_IDs','reconciled_families']:
        assert intended[context][field][:len(prior[context][field])]==prior[context][field]
    assert intended['completed_editorial_families'][:-1]==prior['completed_editorial_families']
    assert intended['coverage_units'][:-1]==prior['coverage_units']
    assert intended['Maria_SC3_B37_B50_clean_20261109']==prior['Maria_SC3_B37_B50_clean_20261109']
    final=load('translations/maria270_integrated_final_review_v1.json')
    assert final['records_count']==270 and all(all(r['review'].values()) for r in final['records'])
    assert final['target_ROM_sha256']==release['candidate_sha256'] and not intended['full_goal_complete']
    for p,h in final['evidence'].items():assert digest(p)==h
    os.replace(pending,ledger)
    assert digest(ledger)==plan['ledger_after_sha256']
    save(checkpoint,dict(family=plan['family'],new_credit=270,counts=dict(completed=19732,revised=11871,retained=7861),
        source_prose_draft_historical_counts=19735,ledger_before_sha256=plan['ledger_before_sha256'],
        ledger_after_sha256=plan['ledger_after_sha256'],all_unrelated_keys_andearlier_record_prefixes_exact=True,
        main_unchanged=True,full_goal_complete=False,guide_photos=False,recovered_exact_saved_completion_plan=True,
        recovery_producer=str(Path(__file__)),recovery_producer_sha256=digest(__file__)))
    print('Published the exact saved270-credit plan once;all prior prefixes andB50 preserved;19,732 integrated.')
if __name__=='__main__':main()
