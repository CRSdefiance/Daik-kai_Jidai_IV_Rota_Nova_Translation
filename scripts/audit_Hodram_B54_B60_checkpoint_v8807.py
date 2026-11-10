"""Independently reconstruct checkpoint inverse and verify pending82 evidence."""
import sys
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/Hodram_B54_B60_checkpoint_v8806')
KEY='Hodram_SC1B54_B60_82_contextual_prose_native_display_pending_storage_actual_release_v8806'
SCOPE='unfinished_editorial_scope_v8806'

if __name__=='__main__':
    mode=sys.argv[1];assert mode in ['stage','verify']
    m=read(ROOT/'stage_manifest.json');old=read(ROOT/'ledger_before.json');new=read(ROOT/'ledger_staged.json')
    assert sha((ROOT/'ledger_before.json').read_bytes())==m['ledger_before_sha256'] and sha((ROOT/'ledger_staged.json').read_bytes())==m['ledger_staged_sha256']
    assert set(new)-set(old)=={KEY,SCOPE} and not set(old)-set(new)
    assert new['goal_status']==old['goal_status']=='active' and not new['full_goal_complete']
    assert [new[k] for k in ['records_editorially_completed','records_with_source_and_prose_pass','records_revised_and_integrated','retained_wordings_editorially_completed']]==[old[k] for k in ['records_editorially_completed','records_with_source_and_prose_pass','records_revised_and_integrated','retained_wordings_editorially_completed']]
    assert new['records_editorially_completed']==7237 and new['records_revised_and_integrated']==4492 and new['retained_wordings_editorially_completed']==2745
    assert new['current_integrated_candidate']==old['current_integrated_candidate']
    inverse=deepcopy(new);del inverse[KEY];del inverse[SCOPE];inverse['latest_checkpoint']=old['latest_checkpoint']
    assert len(inverse['research_checkpoints'])==len(old['research_checkpoints'])+1
    assert inverse['research_checkpoints'][:-1]==old['research_checkpoints'];inverse['research_checkpoints']=old['research_checkpoints']
    assert inverse==old
    scope_old=read(ROOT/'scope_before.json');scope_new=read(new[SCOPE]['path'])
    assert sha((ROOT/'scope_before.json').read_bytes())==m['scope_before_sha256'] and sha(Path(new[SCOPE]['path']).read_bytes())==new[SCOPE]['sha256']
    assert scope_new.pop(KEY)==new[KEY] and scope_new==scope_old
    for r in m['documents']:
        before=Path(r['before']).read_bytes();staged=Path(r['staged']).read_bytes()
        assert sha(before)==r['before_sha256'] and sha(staged)==r['staged_sha256']
        assert staged[r['prefix_bytes']:]==before and b'V8806' in staged[:r['prefix_bytes']]
    p=new[KEY];doc=read(p['manuscript']);view=read(p['native_view']);pages=read(view['native_pages']);plan=read(view['plan'])
    assert p['new_credit']==p['new_emulator_runs']==0 and not p['new_ROM']
    assert len(p['records'])==len(doc['records'])==len(view['records'])==len(pages['records'])==len(plan['records'])==82
    assert p['revisions']==doc['revised']==46 and p['retentions']==doc['retained']==36
    completed={historical_key(r) for f in old['completed_editorial_families'] for r in f['records']}
    pending={historical_key(r) for r in p['records']};assert len(pending)==82 and len(completed)==7237 and not pending&completed
    total=0
    for a,b,c,d in zip(doc['records'],view['records'],pages['records'],plan['records'],strict=True):
        assert a['id']==b['id']==c['id']==d['id']
        assert a['source_reference']==b['source_reference']==c['source_reference'] and a['current_reference']==b['current_reference']==c['current_reference']
        assert a['english']==b['logical_English']==c['logical_English']==d['logical_English']
        assert b['compiled_hex']==c['compiled_hex']==d['encoded_hex']
        assert all(a['review'][g] for g in ['source','context','localization','naturalness']) and not a['review']['formatting']
        assert not any(i['severity'] in ['error','warning'] for i in d['base_QA']['issues'])
        assert (a['decision']=='retention')==(a['english']==a['prior_macro_normalized_comparison'])
        assert a['localization_note'] and (a['retention_reason'] if a['decision']=='retention' else a['finding'])
        display=c['complete_native_English_display'];total+=display['pages'] if a['kind']=='system-FE' else len(display['pages'])
    assert total==pages['complete_native_English_pages']==85 and len(view['viewed_sheets'])==11 and view['all_generated_word_boundaries_reviewed']==79
    assert view['Geronimo_Alonso_shared_de_field_fullname_consumers_anddeployment_still_open']
    for path,digest in {**m['protected_files'],**m['evidence']}.items():assert sha(Path(path).read_bytes())==digest
    for r in view['viewed_sheets']:assert sha(Path(r['path']).read_bytes())==r['sha256']
    report=dict(pass_=True,stage_manifest_sha256=sha((ROOT/'stage_manifest.json').read_bytes()),
        whole_prior_ledger_inverse_andall_old_scope_values_exact=True,all_old_document_bytes_preserved=True,
        source_positions=82,prose_revisions=46,justified_retentions=36,native_pages=85,viewed_sheets=11,
        all_counts_andcompleted_families_unchanged=True,current_candidate_andclean_patch_registry_builder_canonical_clean_inputs_unchanged=True,
        zero_new_credit_no_ROM_ornew_gameplay=True,full_goal_complete=False,goal_status='active',
        auditor=str(Path(__file__)),auditor_sha256=sha(Path(__file__).read_bytes()))
    report['pass']=report.pop('pass_')
    if mode=='stage':
        assert sha(Path('translations/editorial_review_current_v1.json').read_bytes())==m['ledger_before_sha256']
        for r in m['documents']:assert sha(Path(r['path']).read_bytes())==r['before_sha256']
        save(ROOT/'independent_staged_audit.json',report)
        print('Independent audit passes:full ledger/scope inverses;all prior document bytes;82 uncredited decisions/85 pages;release artifacts exact.')
    else:
        assert sha(Path('translations/editorial_review_current_v1.json').read_bytes())==m['ledger_staged_sha256']
        for r in m['documents']:assert sha(Path(r['path']).read_bytes())==r['staged_sha256']
        assert sha(Path('docs/editorial_Hodram_B54_B60_v8806.md').read_bytes())==m['checkpoint_doc_sha256']
        report.update(ledger_sha256=m['ledger_staged_sha256'],candidate_sha256=old['current_integrated_candidate']['sha256'],completed=7237,credited_source_prose_anddrafts=7240,
            native_view=str(p['native_view']),next_scope=KEY,formatting_stored_actual_andregisteredintegration_pending=True)
        save(ROOT/'verified_handoff_v8807.json',report)
        print('Verified V8806 handoff:current V8778 unchanged;82 prose/native-reviewed pending integration;7,237 completed;full goal active.')
