"""Independently verify14 pending reviews,native contracts and unchanged V3526 release."""
from collections import Counter
from copy import deepcopy
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/editorial_handoff_verification_v3552')
CHECKPOINT=Path('work/analysis/lil_B141_checkpoint_v3551')
AMEND=Path('work/analysis/lil_B141_checkpoint_wording_v3551b')
if __name__=='__main__':
    assert not ROOT.exists();receiptpath=CHECKPOINT/'checkpoint_receipt.json';receipt=read(receiptpath);amendpath=AMEND/'wording_correction_receipt.json';amend=read(amendpath)
    assert amend['original_receipt_sha256']==sha(receiptpath.read_bytes())
    for p,d in receipt['evidence'].items():assert sha(Path(p).read_bytes())==d,p
    for p,d in receipt['updated_files'].items():assert sha((AMEND/(Path(p).name+'.before')).read_bytes())==d,p
    for p,d in amend['updated_files'].items():assert sha(Path(p).read_bytes())==d,p
    lp=Path('translations/editorial_review_current_v1.json');ledger=read(lp);before=read(CHECKPOINT/'editorial_review_current_v1.json.before');prior=read(receipt['prior_verified_handoff']);assert sha((CHECKPOINT/'editorial_review_current_v1.json.before').read_bytes())==prior['ledger_sha256']
    preword=read(AMEND/'editorial_review_current_v1.json.before');expected=deepcopy(preword);expected['latest_checkpoint']=expected['latest_checkpoint'].replace(amend['old'],amend['new']);expected['lil_B141_scope_reconciliation_v3551']['summary']=expected['lil_B141_scope_reconciliation_v3551']['summary'].replace(amend['old'],amend['new']);assert ledger==expected
    assert Path('docs/editorial_handoff_current.md').read_text(encoding='utf-8').startswith('# Current editorial handoff - V3551')
    fresh=ledger['contextual_story_natural_dialogue_pass_v1871'];reviewed={historical_key(r) for r in fresh['record_keys']};integrated={historical_key(r) for r in fresh['integrated_record_keys']};pending={historical_key(r) for r in fresh['pending_record_keys']};completed={historical_key(r) for g in ledger['completed_editorial_families'] for r in g['records']}
    assert len(reviewed)==len(fresh['record_keys'])==5031 and len(integrated)==len(completed)==5017 and len(pending)==14 and integrated==completed and not integrated&pending and reviewed==integrated|pending
    assert (fresh['fresh_pass_records_explicitly_reread'],fresh['fresh_pass_records_integrated'],fresh['fresh_pass_records_pending_native_actual_release'])==(5031,5017,14)
    assert (ledger['records_with_source_and_prose_pass'],ledger['records_with_source_prose_drafts'],ledger['records_editorially_completed'],ledger['records_revised_and_integrated'],ledger['retained_wordings_editorially_completed'])==(5034,5034,5017,3268,1749)
    assert sum(ledger['source_prose_reviewed_counts_by_file'].values())==5034 and ledger['source_prose_reviewed_counts_by_file']['/data/SC2.DK4']==3178 and ledger['source_prose_reviewed_counts_by_file']['/data/SC3.DK4']==64
    assert dict(Counter(path for path,ident in completed))==ledger['completed_editorial_record_counts_by_file']
    docpath=Path('translations/lil_B141_editorial_manuscript_v6.json');doc=read(docpath);approval=read('work/analysis/lil_B141_native_approval_v3550/approval_receipt.json');assert sha(docpath.read_bytes())==approval['manuscript_sha256'] and approval['all14_five_review_gates_true']
    assert {historical_key(r) for r in doc['records']}==pending and Counter(r['editorial_decision'] for r in doc['records'])=={'revise':7,'retain-wording':7}
    source=read(doc['source_context']);image,clean=NdsImage.open(doc['current_ROM']),NdsImage.open('work/clean.nds');jp,en=[IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks[141] for im in [clean,image]]
    for r in doc['records']:
        for raw,ref,key in [(jp,r['source_reference'],'source_hex'),(en,r['current_reference'],'current_hex')]:
            at=ref['offset'];value=bytes.fromhex(r[key]);assert raw[at:at+len(value)]==value and raw[at+len(value)]==0 and raw[ref['header_offset']:ref['header_offset']+6].hex()==r['source_complete_preamble_hex']
        assert all(r['review'].values()) and r['fresh_source_gloss'] and r['whole_exchange_context'] and r['source_gloss_precedes_older_English_comparison']
        if r['editorial_decision']=='retain-wording':assert r['fresh_retained_wording_justification'] and r['english'].split('}',1)[1]==r['effective_predecessor_macro_paragraph']==r['effective_predecessor_paragraph']
        for k in ['FI','FA','FO']:assert bytes.fromhex(r['source_hex']).count(k.encode())==r['english'].count('{MACRO:'+k+'}')
    native=read(doc['native_font_proof']);assert len(native['cases'])==14 and native['current_original_macro_alignment_calls']==112 and len(native['source_consumer_negative_controls'])==17 and len(native['source_bound_formatter_negatives'])==14 and all(c['rejected'] for c in native['source_consumer_negative_controls']+native['source_bound_formatter_negatives'])
    assert len(native['review_sheets'])==2 and sum(bool(r.get('qa_waivers')) for r in doc['records'])==9
    for s in native['review_sheets']:assert sha(Path(s['path']).read_bytes())==s['sha256'] and s['review'].startswith('Viewed final')
    branches=read(doc['branch_proof']);assert len(branches['operands_requiring_adjustment_when_resizing'])==13 and len(branches['cases'])==130 and branches['all_scoped_destinations_equal_mapped_instruction_boundaries']
    controls=read(doc['control_contract']);assert len(controls['speech_dispatch_cases'])==28 and controls['source_macro_counts']=={'FI':1,'FA':0,'FO':0} and len(controls['source_630A_cases'])==10 and controls['source_630A_not_misclassified_as_actual_payment']
    assert all(c['source_owned_UI_request_words']==[1,0,13,0,0,0,1] and len(c['source_owned_UI_writes'])==9 and c['native_presentation_resource_bodies_not_executed'] for c in controls['source_C200_cases'])
    finance=read(doc['source_finance_contract']);assert finance['source_threshold_gold']==1000000 and finance['source_payment_gold']==900000 and finance['original_selected_Lil_company_money_identity']['before_funds']==34882
    assert [c['input_funds'] for c in finance['cases']]==[0,899999,900000,999999,1000000,1000001,2000000]
    for c in finance['cases']:
        v=c['input_funds'];assert c['source_predicate']['native_result'][1]==(0 if v<1000000 else 1 if v==1000000 else 2) and c['source_payment']['after_funds']==max(0,v-900000) and c['source_payment']['all_other4MiB_actor_roster_event_RNG_models_ABI_input_owner_and_output_guards_exact']
    entry=read(doc['source_entry_proof'])['selected_B141_source_event'];assert entry['event_ID']==141 and entry['action_index']==142 and entry['script_block']==141 and entry['must_be_completed']==[140]
    for k in ['completed_editorial_families','current_integrated_candidate','completed_editorial_record_counts_by_file','reviewed_but_incomplete_COMMON_IDs','unresolved_graphics_work','older_record_reaudit_after_full_editorial_goal','native_source_universe_inventory_v2701c','Proof_terminology_consistency_lead_v3286']:assert ledger[k]==before[k],k
    candidate=ledger['current_integrated_candidate'];assert candidate['profile']=='all-routes-unified-v3526' and sha(Path(candidate['path']).read_bytes())==candidate['sha256']==doc['current_ROM_sha256'] and sha(Path(candidate['patch']).read_bytes())==candidate['patch_sha256']
    registry=read('translations/release_stack.json');manifest=read(candidate['manifest']);assert len(manifest['batches'])==526 and len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v1492' and manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes())
    scope=ledger['unfinished_editorial_scope_v3551'];assert sha(Path(scope['path']).read_bytes())==scope['sha256'] and scope['B142_and_later_unreviewed'] and scope['canonical_Maria32_pending_uncredited'] and scope['Proof_terminology_consistency_open'] and scope['next_uncredited_B141_physical_speeches']==0
    assert ledger['goal_status']=='active' and not ledger['full_goal_complete']
    ROOT.mkdir(parents=True);save(ROOT/'verified_handoff.json',dict(checkpoint='V3551',ledger_sha256=sha(lp.read_bytes()),handoff_receipt=str(receiptpath),handoff_receipt_sha256=sha(receiptpath.read_bytes()),wording_correction_receipt=str(amendpath),wording_correction_receipt_sha256=sha(amendpath.read_bytes()),fresh_reread=5031,integrated=5017,pending=14,source_prose=5034,revised=3268,retained=1749,candidate=candidate['path'],candidate_sha256=candidate['sha256'],patch=candidate['patch'],patch_sha256=candidate['patch_sha256'],all14_clean_current_references_retention_macro_templates_and_native_gates_verified=True,source_threshold_million_and_payment900000_distinguished=True,no_B141_gameplay_or_earned_funding_claim=True,all_prior_completed_reviews_and_wider_scope_preserved=True,full_goal_active=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('V3551 verified:5031 reread,5017 integrated,14 pending;5034 source-prose. V3526/526 batches unchanged;all wider scope active.')
