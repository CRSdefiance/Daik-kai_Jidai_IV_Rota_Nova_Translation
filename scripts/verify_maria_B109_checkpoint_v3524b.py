"""Independently reconcile the26 source/current reviews and pending coverage ledger."""
from collections import Counter
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/editorial_handoff_verification_v3524b')
if __name__=='__main__':
    assert not ROOT.exists();lp=Path('translations/editorial_review_current_v1.json');ledger=read(lp);receipt=read('work/analysis/maria_B109_checkpoint_v3524/checkpoint_receipt.json')
    for p,d in receipt['updated_files'].items():assert sha(Path(p).read_bytes())==d,p
    assert Path('docs/editorial_handoff_current.md').read_text(encoding='utf-8').startswith('# Current editorial handoff - V3524')
    fresh=ledger['contextual_story_natural_dialogue_pass_v1871'];key=lambda r:(r['file_path'],r['id']);reviewed={key(r) for r in fresh['record_keys']};integrated={key(r) for r in fresh['integrated_record_keys']};pending={key(r) for r in fresh['pending_record_keys']};completed={key(r) for g in ledger['completed_editorial_families'] for r in g['records']}
    assert len(reviewed)==5017 and len(integrated)==len(completed)==4991 and len(pending)==26 and integrated==completed and not integrated&pending and reviewed==integrated|pending
    assert (fresh['fresh_pass_records_explicitly_reread'],fresh['fresh_pass_records_integrated'],fresh['fresh_pass_records_pending_native_actual_release'])==(5017,4991,26)
    assert (ledger['records_with_source_and_prose_pass'],ledger['records_with_source_prose_drafts'],ledger['records_editorially_completed'],ledger['records_revised_and_integrated'],ledger['retained_wordings_editorially_completed'])==(5020,5020,4991,3252,1739)
    counts=Counter(k[0] for k in completed);assert dict(counts)==ledger['completed_editorial_record_counts_by_file']
    assert ledger['source_prose_reviewed_counts_by_file']['/data/SC3.DK4']==64 and ledger['source_prose_reviewed_counts_by_file']['/data/SC2.DK4']==3164
    path=Path('translations/maria_B109_editorial_manuscript_v10.json');doc=read(path);assert Counter(r['editorial_decision'] for r in doc['records'])=={'revise':16,'retain-wording':10}
    assert {key(r) for r in doc['records']}==pending and all(all(r['review'].values()) for r in doc['records'])
    old=NdsImage.open(doc['current_ROM']);clean=NdsImage.open('work/clean.nds');a,b=[IlnkContainer.parse(im.read_file('/data/SC3.DK4')).blocks[109] for im in [clean,old]]
    for r in doc['records']:
        for raw,ref,field in [(a,r['source_reference'],'source_hex'),(b,r['current_reference'],'current_hex')]:
            at=ref['offset'];value=bytes.fromhex(r[field]);assert raw[at:at+len(value)]==value and raw[at+len(value)]==0 and raw[ref['header_offset']:ref['header_offset']+6].hex()==r['source_complete_preamble_hex']
        assert r['fresh_source_gloss'] and r['whole_exchange_context'] and r['source_gloss_precedes_older_English_comparison']
        if r['editorial_decision']=='retain-wording':assert r['fresh_retained_wording_justification'] and r['english'].split('}',1)[1]==r['effective_predecessor_paragraph']
    actual=read(doc['representative_proof']);assert actual['complete_matching_panels']==26 and not actual['unmatched_capture_planes'] and actual['B109_content_in_B33_entry_fixture_only'] and actual['source_event109_not_selected_or_earned']
    assert ledger['goal_status']=='active' and not ledger['full_goal_complete'] and ledger['unresolved_graphics_work'] and ledger['older_record_reaudit_after_full_editorial_goal']
    root=ledger['unfinished_editorial_scope_v3524'];assert sha(Path(root['path']).read_bytes())==root['sha256'] and root['next_uncredited_physical_speeches']==14 and root['canonical_Maria32_pending_uncredited'] and root['Proof_terminology_consistency_open']
    assert ledger['current_integrated_candidate']['profile']=='all-routes-unified-v3487'
    registry=read('translations/release_stack.json');assert len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v1492'
    ROOT.mkdir(parents=True);save(ROOT/'verified_handoff.json',dict(checkpoint='V3524',ledger_sha256=sha(lp.read_bytes()),fresh_reread=5017,integrated=4991,pending=26,source_prose=5020,revised=3252,retained=1739,all26_clean_current_references_and_retention_reasons_bound=True,actual_content_B33_fixture_scope_preserved=True,full_goal_active=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('V3524 independently reconciled:5017 reread,4991 integrated,26 pending;exact references,retentions and wider scope pass.')
