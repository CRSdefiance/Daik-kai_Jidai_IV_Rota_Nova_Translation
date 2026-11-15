"""Independently verify the completed26-object release,coverage ledger and scope."""
from collections import Counter
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/editorial_handoff_verification_v3531')
CHECKPOINT=Path('work/analysis/maria_B109_completion_v3530')
if __name__=='__main__':
    assert not ROOT.exists();receiptpath=CHECKPOINT/'completion_receipt.json';receipt=read(receiptpath)
    for group in ['evidence','updated_files']:
        for p,d in receipt[group].items():assert sha(Path(p).read_bytes())==d,(group,p)
    lp=Path('translations/editorial_review_current_v1.json');ledger=read(lp);before=read(CHECKPOINT/'editorial_review_current_v1.json.before');prior=read(receipt['prior_verified_handoff']);assert sha((CHECKPOINT/'editorial_review_current_v1.json.before').read_bytes())==prior['ledger_sha256']
    assert Path('docs/editorial_handoff_current.md').read_text(encoding='utf-8').startswith('# Current editorial handoff - V3530')
    key=historical_key;fresh=ledger['contextual_story_natural_dialogue_pass_v1871'];reviewed={key(r) for r in fresh['record_keys']};integrated={key(r) for r in fresh['integrated_record_keys']};allrows=[r for g in ledger['completed_editorial_families'] for r in g['records']];completed={key(r) for r in allrows}
    assert len(allrows)==len(reviewed)==len(integrated)==len(completed)==5017 and reviewed==integrated==completed
    assert not fresh['pending_record_keys'] and not fresh['pending_contextual_families'] and (fresh['fresh_pass_records_explicitly_reread'],fresh['fresh_pass_records_integrated'],fresh['fresh_pass_records_pending_native_actual_release'])==(5017,5017,0)
    assert (ledger['records_with_source_and_prose_pass'],ledger['records_with_source_prose_drafts'],ledger['records_editorially_completed'],ledger['records_revised_and_integrated'],ledger['retained_wordings_editorially_completed'])==(5020,5020,5017,3268,1749)
    assert Counter(r['historical_editorial_decision'] for r in allrows)=={'revise':3268,'retain':1749}
    assert dict(Counter(key(r)[0] for r in allrows))==ledger['completed_editorial_record_counts_by_file']
    assert ledger['source_prose_reviewed_counts_by_file']==before['source_prose_reviewed_counts_by_file'] and ledger['source_prose_reviewed_counts_by_file']['/data/SC3.DK4']==64
    assert ledger['completed_editorial_families'][:-1]==before['completed_editorial_families']
    family=ledger['completed_editorial_families'][-1];final=read(family['final_review']);assert family['id']=='Maria-B109-resolve-and-loyalty26' and family['records']==final['records'] and Counter(r['editorial_decision'] for r in final['records'])=={'revise':16,'retain-wording':10}
    releasepath=Path('work/analysis/maria_B109_release_v3527/registered_release_verification.json');release=read(releasepath);candidate=ledger['current_integrated_candidate'];rom=NdsImage.open(candidate['path']);block=IlnkContainer.parse(rom.read_file('/data/SC3.DK4')).blocks[109];jp=IlnkContainer.parse(NdsImage.open('work/clean.nds').read_file('/data/SC3.DK4')).blocks[109]
    assert sha(Path(candidate['path']).read_bytes())==candidate['sha256']==release['candidate_sha256']==final['candidate_sha256']
    assert sha(Path(candidate['patch']).read_bytes())==candidate['patch_sha256']==release['patch_sha256'] and release['whole_ROM_reconstruction_byte_exact']
    manifest=read(candidate['manifest']);registry=read('translations/release_stack.json');assert manifest['profile']==candidate['profile']=='all-routes-unified-v3526' and len(manifest['batches'])==526 and all(manifest['checks'].values()) and manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes())
    assert len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v1492'
    assert block[:4]==b'CS\1\1' and block[8:18]==jp[8:18]==bytes.fromhex('00450000008084468380') and len(block)==1752
    previous=NdsImage.open('out/all_routes_combined_v3487_candidate.nds');assert [p for _,p,v in previous.iter_files() if rom.read_file(p)!=v]==['/data/SC3.DK4'] and all(rom.read_file(p)==v for p,v in previous.iter_components())
    a,b=[IlnkContainer.parse(im.read_file('/data/SC3.DK4')).blocks for im in [previous,rom]];assert [n for n,(x,y) in enumerate(zip(a,b,strict=True)) if x!=y]==[109]
    for r in final['records']:
        assert all(r['review'].values()) and r['fresh_source_gloss'] and r['whole_exchange_context'] and r['source_gloss_precedes_older_English_comparison']
        at=r['source_reference']['offset'];value=bytes.fromhex(r['source_hex']);assert jp[at:at+len(value)]==value and jp[at+len(value)]==0
        ref=r['integrated_reference'];at=ref['offset'];value=bytes.fromhex(r['integrated_hex']);assert block[at:at+len(value)]==value and block[at+len(value)]==0 and r['current_hex']==r['integrated_hex']
        assert block[ref['header_offset']:ref['header_offset']+6].hex()==r['source_complete_preamble_hex']
        old=r['historical_source_prose_predecessor_fields'];at=old['current_reference']['offset'];value=bytes.fromhex(old['current_hex']);assert a[109][at:at+len(value)]==value and a[109][at+len(value)]==0
        if r['editorial_decision']=='retain-wording':assert r['fresh_retained_wording_justification'] and r['english'].split('}',1)[1]==r['effective_predecessor_paragraph']
    doc=read(final['manuscript']);actual=read(doc['representative_proof']);assert actual['complete_matching_panels']==actual['complete_matching_holds']==26 and not actual['unmatched_capture_planes'] and actual['source_event109_not_selected_or_earned'] and actual['B109_content_in_B33_entry_fixture_only']
    startup=read('work/analysis/maria_B109_startup_v3529/cold_boot_Lil_startup_town_verification.json');view=read('work/analysis/maria_B109_startup_v3529/current_six_frame_visual_review.json');assert startup['paired_frame_count']==31 and startup['all_current_requested_and_final_framebuffers_equal_V3487'] and view['viewed'] and view['sha256']==sha(Path(view['sheet']).read_bytes())
    for k in ['reviewed_but_incomplete_COMMON_IDs','unresolved_graphics_work','older_record_reaudit_after_full_editorial_goal','native_source_universe_inventory_v2701c','Proof_terminology_consistency_lead_v3286']:assert ledger[k]==before[k]
    scope=ledger['unfinished_editorial_scope_v3530'];assert sha(Path(scope['path']).read_bytes())==scope['sha256'] and scope['next_uncredited_physical_speeches']==14 and scope['canonical_Maria32_pending_uncredited'] and scope['Proof_terminology_consistency_open']
    assert ledger['goal_status']=='active' and not ledger['full_goal_complete']
    ROOT.mkdir(parents=True);save(ROOT/'verified_handoff.json',dict(checkpoint='V3530',ledger_sha256=sha(lp.read_bytes()),handoff_receipt=str(receiptpath),handoff_receipt_sha256=sha(receiptpath.read_bytes()),fresh_reread=5017,integrated=5017,pending=0,source_prose=5020,revised=3268,retained=1749,candidate=candidate['path'],candidate_sha256=candidate['sha256'],patch=candidate['patch'],patch_sha256=candidate['patch_sha256'],manifest_batches=526,accepted_layers=114,source_control_repair_and_all26_integrated_references_verified=True,actual_content_B33_fixture_scope_preserved=True,full_goal_active=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('V3530 independently verified:5017 reread/integrated,5020 source-prose;V3526/526 batches/exact patch;full wider goal active.')
