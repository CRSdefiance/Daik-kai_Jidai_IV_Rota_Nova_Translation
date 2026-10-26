"""Audit exact source/current records, native approval and incremental coverage."""
from collections import Counter
from pathlib import Path
from dk4tool.dialogue.lil_B139_B140_profile import profile_for,DEPENDENCIES
from dk4tool.dialogue.lil_B139_B140_layout_v2 import encode_relocatable_dialogue,audit_relocatable_dialogue_record
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/editorial_handoff_verification_v3477');CHECKPOINT=Path('work/analysis/lil_B139_B140_checkpoint_v3476')
if __name__=='__main__':
    assert not ROOT.exists();rp=CHECKPOINT/'checkpoint_receipt.json';receipt=read(rp)
    for kind in ['evidence','updated_files']:
        for p,digest in receipt[kind].items():assert sha(Path(p).read_bytes())==digest,(kind,p)
    lp=Path('translations/editorial_review_current_v1.json');ledger=read(lp);before=read(CHECKPOINT/'editorial_review_current_v1.json.before');prior=read(receipt['prior_verified_handoff'])
    assert sha((CHECKPOINT/'editorial_review_current_v1.json.before').read_bytes())==prior['ledger_sha256'] and sha(Path(prior['handoff_receipt']).read_bytes())==prior['handoff_receipt_sha256']
    for p,digest in read(prior['handoff_receipt'])['updated_files'].items():
        saved=CHECKPOINT/(Path(p).name+'.before');assert sha((saved if saved.exists() else Path(p)).read_bytes())==digest
    allowed={'records_with_source_and_prose_pass','records_with_source_prose_drafts','source_prose_reviewed_counts_by_file','reviewed_but_incomplete_route_record_IDs','active_source_prose_drafts','contextual_story_natural_dialogue_pass_v1871','coverage_units','formatting_watchlist','latest_checkpoint'}
    assert set(ledger)-set(before)=={'unfinished_editorial_scope_v3476','lil_B139_B140_scope_reconciliation_v3476'}
    for k in before:
        if k not in allowed:assert before[k]==ledger[k],k
    fresh=ledger['contextual_story_natural_dialogue_pass_v1871'];oldfresh=before['contextual_story_natural_dialogue_pass_v1871'];doc=read(fresh['latest_contextual_manuscript']);validate_natural_dialogue_batch(doc);rows=doc['records'];selected={historical_key(r) for r in rows};keys={historical_key(r) for r in fresh['record_keys']};oldkeys={historical_key(r) for r in oldfresh['record_keys']};integrated={historical_key(r) for r in fresh['integrated_record_keys']};pending={historical_key(r) for r in fresh['pending_record_keys']}
    assert len(rows)==len(selected)==67 and keys-oldkeys==selected==pending and oldkeys==integrated and keys==integrated|pending and not integrated&pending
    assert (fresh['fresh_pass_records_explicitly_reread'],fresh['fresh_pass_records_integrated'],fresh['fresh_pass_records_pending_native_actual_release'])==(4991,4924,67) and len(keys)==len(fresh['record_keys'])==4991
    assert ledger['records_with_source_and_prose_pass']==ledger['records_with_source_prose_drafts']==sum(ledger['source_prose_reviewed_counts_by_file'].values())==4994 and ledger['source_prose_reviewed_counts_by_file']['/data/SC2.DK4']==3164
    assert (ledger['records_editorially_completed'],ledger['records_revised_and_integrated'],ledger['retained_wordings_editorially_completed'])==(4924,3223,1701) and Counter(r['editorial_decision'] for r in rows)=={'revise':29,'retain-wording':38}
    image,clean=NdsImage.open(doc['current_ROM']),NdsImage.open('work/clean.nds');en,jp=[IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks for im in [image,clean]];arm=image.read_file('/__arm9__.bin');font=read(doc['native_font_proof']);cases={c['id']:c for c in font['cases']}
    assert len(cases)==67 and font['current_original_macro_alignment_calls']==536 and len(font['source_consumer_negative_controls'])==23 and len(font['source_bound_formatter_negatives'])==14 and all(c['rejected'] for c in font['source_consumer_negative_controls']+font['source_bound_formatter_negatives']) and len(font['review_sheets'])==9
    for s in font['review_sheets']:assert sha(Path(s['path']).read_bytes())==s['sha256']
    for r in rows:
        assert all(r['review'].values()) and r['source_meaning'] and r['context'] and r['localization_note'] and not any(tag in r['english'] for tag in ['{LB','{ALIGN','{PAD'])
        b=r['block'];s,c=r['source_reference'],r['current_reference'];raw,value=bytes.fromhex(r['source_hex']),bytes.fromhex(r['current_hex'])
        assert jp[b][s['offset']:s['offset']+s['bytes']]==raw and en[b][c['offset']:c['offset']+c['bytes']]==value and jp[b][s['offset']+s['bytes']]==en[b][c['offset']+c['bytes']]==0 and jp[b][s['offset']-5:s['offset']+1]==en[b][c['offset']-5:c['offset']+1]==bytes.fromhex(r['source_complete_preamble_hex'])
        p=profile_for(arm,en[b]);encoded=encode_relocatable_dialogue(raw,r['english'],p);assert encoded.encoded.hex()==r['compiled_hex']==cases[r['id']]['encoded_hex'] and encoded.encoded[0]==raw[0] and b'\0' not in encoded.encoded
        qa=audit_relocatable_dialogue_record(raw,r['english'],p);assert not [i for i in qa['issues'] if i['severity'] in ['warning','error'] and i['code'] not in r.get('qa_waivers',[])]
        if r['editorial_decision']=='retain-wording':assert r['english'].split('}',1)[1]==r['effective_predecessor_paragraph'] and r['fresh_retained_wording_justification']
        assert sha(Path(cases[r['id']]['preview']).read_bytes())==cases[r['id']]['preview_sha256']
    assert sum(bool(r.get('qa_waivers')) for r in rows)==27 and sum(r['registered_runtime_catalog_entry'] is not None for r in rows)==1
    for p,digest in DEPENDENCIES.items():assert sha(Path(p).read_bytes())==digest
    control=read(doc['control_contract']);assert len(control['speech_dispatch_cases'])==134 and len(control['current_original_predicate_cases'])==13 and len(control['original_event_queries'])==1 and control['original_event_queries'][0]['event']==129 and len(control['source_C200_cases'])==1 and control['source_macro_counts']=={'FI':7,'FA':0,'FO':0}
    for ident,prefix,count in [('DK4_MES_B140_R0071',2,3),('DK4_MES_B140_R0130',2,6),('DK4_MES_B140_R0274',9,6)]:
        case=cases[ident];assert bytes.fromhex(case['encoded_hex'])==bytes([prefix])+b'.'*count and [(e['code'],e['x'],e['y']) for e in case['complete_glyph_events'] if e['code']!=32]==[(46,6*n,0) for n in range(count)]
    physical=read('work/analysis/lil_after_B119_clean_scope_v3257c/complete_clean_next_exchange_inventory.json');oldrows=[r for b in physical['blocks'] for r in b['records']];assert len(oldrows)==533 and not {historical_key(r) for r in oldrows}-keys
    for file,count in before['source_prose_reviewed_counts_by_file'].items():assert ledger['source_prose_reviewed_counts_by_file'][file]==count+(67 if file=='/data/SC2.DK4' else 0)
    unit=next(u for u in ledger['coverage_units'] if u['id']=='all-route-scenes');assert (unit['reviewed_route_records'],unit['completed_route_records'])==(3392,3325)
    c=ledger['current_integrated_candidate'];release=read('work/analysis/lil_B138_release_v3451/registered_release_verification.json');assert sha(Path(c['path']).read_bytes())==c['sha256']==release['candidate_sha256'] and sha(Path(c['patch']).read_bytes())==c['patch_sha256']==release['patch_sha256'] and Path(release['exact_patch_reconstruction']).read_bytes()==Path(c['path']).read_bytes()
    manifest,registry=read(c['manifest']),read('translations/release_stack.json');assert manifest['profile']=='all-routes-unified-v3450' and len(manifest['batches'])==524 and len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v1492' and manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes())
    assert ledger['goal_status']=='active' and not ledger['full_goal_complete'] and Path('docs/editorial_handoff_current.md').read_text(encoding='utf-8').startswith('# Current editorial handoff - V3476')
    ROOT.mkdir(parents=True);save(ROOT/'verified_handoff.json',dict(checkpoint='V3476',ledger=str(lp),ledger_sha256=sha(lp.read_bytes()),handoff_receipt=str(rp),handoff_receipt_sha256=sha(rp.read_bytes()),fresh_records=4991,fresh_integrated=4924,fresh_pending=67,source_prose=4994,new_source_prose_reviews=67,new_completed_records=0,completed_records=4924,historical_revised=3223,historical_retained=1701,proposed_revisions=29,justified_retentions=38,incomplete_COMMON=3,incomplete_route=67,all67_exact_source_current_five_gates_and_native_planes_verified=True,all_prior533_physical_leads_reviewed_not_full_Lil_completion=True,prior_release_ledger_and_all_wider_scope_preserved=True,candidate=c['path'],candidate_sha256=c['sha256'],patch=c['patch'],patch_sha256=c['patch_sha256'],all_jobs_terminal=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('Independent V3476 audit passes:4991 reread/4924 integrated/67 pending;all67 exact source/current/native/five gates verified. Full wider goal active.')
