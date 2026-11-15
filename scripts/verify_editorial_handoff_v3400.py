"""Independent48-record source/current/native andcoverage audit."""
from collections import Counter
from pathlib import Path
from dk4tool.dialogue.lil_B137_profile import profile_for,DEPENDENCIES
from dk4tool.dialogue.lil_B137_layout_v3 import encode_relocatable_dialogue,audit_relocatable_dialogue_record
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/editorial_handoff_verification_v3400');CHECKPOINT=Path('work/analysis/lil_B137_checkpoint_v3399b')
if __name__=='__main__':
    assert not ROOT.exists();rp=CHECKPOINT/'checkpoint_receipt.json';receipt=read(rp)
    for kind in ['evidence','updated_files']:
        for p,digest in receipt[kind].items():assert sha(Path(p).read_bytes())==digest,(kind,p)
    lp=Path('translations/editorial_review_current_v1.json');ledger=read(lp);before=read(CHECKPOINT/'editorial_review_current_v1.json.before');prior=read(receipt['prior_verified_handoff'])
    assert sha((CHECKPOINT/'editorial_review_current_v1.json.before').read_bytes())==prior['ledger_sha256'] and sha(Path(prior['handoff_receipt']).read_bytes())==prior['handoff_receipt_sha256']
    for p,digest in read(prior['handoff_receipt'])['updated_files'].items():
        saved=CHECKPOINT/(Path(p).name+'.before');assert sha((saved if saved.exists() else Path(p)).read_bytes())==digest
    fresh=ledger['contextual_story_natural_dialogue_pass_v1871'];oldfresh=before['contextual_story_natural_dialogue_pass_v1871'];doc=read(fresh['latest_contextual_manuscript']);validate_natural_dialogue_batch(doc);rows=doc['records'];selected={historical_key(r) for r in rows};keys={historical_key(r) for r in fresh['record_keys']};oldkeys={historical_key(r) for r in oldfresh['record_keys']};integrated={historical_key(r) for r in fresh['integrated_record_keys']};pending={historical_key(r) for r in fresh['pending_record_keys']}
    assert len(rows)==len(selected)==48 and keys-oldkeys==selected==pending and oldkeys==integrated and keys==integrated|pending and not integrated&pending
    assert (fresh['fresh_pass_records_explicitly_reread'],fresh['fresh_pass_records_integrated'],fresh['fresh_pass_records_pending_native_actual_release'])==(4880,4832,48) and len(keys)==len(fresh['record_keys'])==4880
    assert ledger['records_with_source_and_prose_pass']==ledger['records_with_source_prose_drafts']==sum(ledger['source_prose_reviewed_counts_by_file'].values())==4883 and ledger['source_prose_reviewed_counts_by_file']['/data/SC2.DK4']==3053
    assert (ledger['records_editorially_completed'],ledger['records_revised_and_integrated'],ledger['retained_wordings_editorially_completed'])==(4832,3185,1647) and Counter(r['editorial_decision'] for r in rows)=={'revise':22,'retain-wording':26}
    for k in ['completed_editorial_families','completed_editorial_record_counts_by_file','current_integrated_candidate','reviewed_but_incomplete_COMMON_IDs','unresolved_graphics_work','older_record_reaudit_after_full_editorial_goal','native_source_universe_inventory_v2701c','Proof_terminology_consistency_lead_v3286','lil_B131_B133_completion_v3342b']:assert ledger[k]==before[k],k
    image,clean=NdsImage.open(doc['current_ROM']),NdsImage.open('work/clean.nds');en,jp=[IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks for im in [image,clean]];arm=image.read_file('/__arm9__.bin');font=read(doc['native_font_proof']);cases={c['id']:c for c in font['cases']}
    assert len(cases)==48 and font['current_original_macro_alignment_calls']==384 and len(font['source_consumer_negative_controls'])==31 and len(font['source_bound_formatter_negatives'])==14 and all(c['rejected'] for c in font['source_consumer_negative_controls']+font['source_bound_formatter_negatives']) and len(font['review_sheets'])==6
    for s in font['review_sheets']:assert sha(Path(s['path']).read_bytes())==s['sha256']
    for r in rows:
        assert all(r['review'].values()) and r['source_meaning'] and r['context'] and r['localization_note'] and not any(tag in r['english'] for tag in ['{LB','{ALIGN','{PAD'])
        b=r['block'];s,c=r['source_reference'],r['current_reference'];raw,value=bytes.fromhex(r['source_hex']),bytes.fromhex(r['current_hex'])
        assert jp[b][s['offset']:s['offset']+s['bytes']]==raw and en[b][c['offset']:c['offset']+c['bytes']]==value and jp[b][s['offset']+s['bytes']]==en[b][c['offset']+c['bytes']]==0 and jp[b][s['offset']-5:s['offset']+1]==en[b][c['offset']-5:c['offset']+1]==bytes.fromhex(r['source_complete_preamble_hex'])
        p=profile_for(arm,en[b]);encoded=encode_relocatable_dialogue(raw,r['english'],p);assert encoded.encoded.hex()==r['compiled_hex']==cases[r['id']]['encoded_hex'] and encoded.encoded[0]==raw[0] and b'\0' not in encoded.encoded
        qa=audit_relocatable_dialogue_record(raw,r['english'],p);assert not [i for i in qa['issues'] if i['severity'] in ['warning','error'] and i['code'] not in r.get('qa_waivers',[])]
        if r['editorial_decision']=='retain-wording':assert r['english'].split('}',1)[1]==r['effective_predecessor_paragraph'] and r['fresh_retained_wording_justification']
        assert sha(Path(cases[r['id']]['preview']).read_bytes())==cases[r['id']]['preview_sha256']
    assert sum(bool(r.get('qa_waivers')) for r in rows)==18 and sum(r['registered_runtime_catalog_entry'] is not None for r in rows)==0
    for p,digest in DEPENDENCIES.items():assert sha(Path(p).read_bytes())==digest
    c=ledger['current_integrated_candidate'];release=read('work/analysis/lil_B135_B136_release_v3373/registered_release_verification.json');assert sha(Path(c['path']).read_bytes())==c['sha256']==release['candidate_sha256'] and sha(Path(c['patch']).read_bytes())==c['patch_sha256']==release['patch_sha256'] and Path(release['exact_patch_reconstruction']).read_bytes()==Path(c['path']).read_bytes()
    manifest,registry=read(c['manifest']),read('translations/release_stack.json');assert manifest['profile']=='all-routes-unified-v3372' and len(manifest['batches'])==522 and len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v1492' and manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes())
    assert ledger['goal_status']=='active' and not ledger['full_goal_complete'] and Path('docs/editorial_handoff_current.md').read_text(encoding='utf-8').startswith('# Current editorial handoff - V3399')
    ROOT.mkdir(parents=True);save(ROOT/'verified_handoff.json',dict(checkpoint='V3399',ledger=str(lp),ledger_sha256=sha(lp.read_bytes()),handoff_receipt=str(rp),handoff_receipt_sha256=sha(rp.read_bytes()),fresh_records=4880,fresh_integrated=4832,fresh_pending=48,source_prose=4883,new_source_prose_reviews=48,new_completed_records=0,completed_records=4832,historical_revised=3185,historical_retained=1647,proposed_revisions=22,justified_retentions=26,incomplete_COMMON=3,incomplete_route=48,all48_exact_source_current_five_gates_and_native_planes_verified=True,all48_retention_revision_findings_and_conditional_humor_thought_emote_and_wage_provenance_verified=True,prior_release_ledger_and_all_wider_scope_preserved=True,candidate=c['path'],candidate_sha256=c['sha256'],patch=c['patch'],patch_sha256=c['patch_sha256'],all_jobs_terminal=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('IndependentV3399audit passes:4880reread/4832integrated/48pending;48source/current/native/fivegates verified. Fullwidergoal active.')
