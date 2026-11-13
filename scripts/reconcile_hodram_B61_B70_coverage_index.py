"""Repair the nested search index for already credited records; add no new credit."""
from collections import Counter
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save

LEDGER=Path('translations/editorial_review_current_v1.json')
ROOT=Path('work/analysis/Hodram_B71_B80_editorial_20261101')
KEY='Hodram_B61_B70_nested_index_reconciliation_20261101'

if __name__=='__main__':
    before=LEDGER.read_bytes();ledger=load(LEDGER);assert KEY not in ledger
    assert ledger['records_editorially_completed']==7543
    ident='Hodram_SC1B61_B70_complete_contextual_release_20261101'
    family=next(row for row in ledger['completed_editorial_families'] if row['id']==ident)
    coverage=next(row for row in ledger['coverage_units'] if row['id']==ident)
    final_path=Path(family['final_review']);final=load(final_path)
    release_path=Path(coverage['release_verification']);release=load(release_path)
    assert sha(release_path.read_bytes())==coverage['release_verification_sha256']
    assert not release['own_registered_startup_pending'] and release['clean_input_patch_byte_exact']
    assert len(final['records'])==coverage['completion_credit_added']==224
    assert {r['id'] for r in final['records']}==set(family['record_IDs'])==set(coverage['record_IDs'])
    assert all(all(r['review'][gate] for gate in ['source','context','localization','naturalness','formatting']) for r in final['records'])
    context=ledger['contextual_story_natural_dialogue_pass_v1871']
    keys=[dict(file_path=r['file_path'],id=r['id']) for r in final['records']]
    index={(r['file_path'],r['id']) for r in context['record_keys']}
    integrated={(r['file_path'],r['id']) for r in context['integrated_record_keys']}
    assert len(index)==len(integrated)==context['fresh_pass_records_integrated']==7319
    assert context['fresh_pass_records_explicitly_reread']==7319
    assert not index & {(r['file_path'],r['id']) for r in keys}
    assert index==integrated
    backup=ROOT/'ledger_before_nested_index_reconciliation.json';assert not backup.exists()
    backup.write_bytes(before)
    context['record_keys'].extend(keys);context['integrated_record_keys'].extend(keys)
    context['record_IDs'].extend(r['id'] for r in keys)
    context['fresh_pass_records_integrated']+=224
    context['fresh_pass_records_explicitly_reread']+=224
    assert len(context['record_keys'])==len(context['integrated_record_keys'])==7543
    counts=Counter(r['file_path'] for r in context['record_keys'])
    assert counts['/data/SC1.DK4']==463
    ledger[KEY]=dict(already_credited_family=ident,missing_nested_keys_added=224,
        previous_nested_count=7319,reconciled_nested_count=7543,global_completed_count_unchanged=7543,
        final_review=str(final_path),final_review_sha256=sha(final_path.read_bytes()),
        release_verification=str(release_path),release_verification_sha256=sha(release_path.read_bytes()),
        previous_ledger=str(backup),previous_ledger_sha256=sha(before),
        completed_by_file=dict(counts),new_credit=0)
    assert ledger['records_revised_and_integrated']==4670 and ledger['retained_wordings_editorially_completed']==2873
    assert ledger['records_with_source_and_prose_pass']==ledger['records_with_source_prose_drafts']==7546
    assert LEDGER.read_bytes()==before;save(LEDGER,ledger)
    save(ROOT/'nested_index_reconciliation.json',ledger[KEY])
    print('Nested index reconciled to7543 existing completions,SC1=463. No new credit or change to global totals.')
