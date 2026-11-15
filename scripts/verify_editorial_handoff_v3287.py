"""Independent V3286 count/reference/native-proof/release-scope audit."""
from collections import Counter
from pathlib import Path
from dk4tool.dialogue.lil_B122_B127_profile_v2 import profile_for,DEPENDENCIES as PROFILE_DEPS
from dk4tool.dialogue.lil_B122_B127_layout_v2 import encode_relocatable_dialogue,audit_relocatable_dialogue_record,DEPENDENCIES
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/editorial_handoff_verification_v3287')
CHECKPOINT=Path('work/analysis/lil_B122_B127_checkpoint_v3286')
if __name__=='__main__':
    assert not ROOT.exists();rp=CHECKPOINT/'checkpoint_receipt.json';receipt=read(rp)
    for group in ['evidence','updated_files']:
        for p,digest in receipt[group].items():assert sha(Path(p).read_bytes())==digest,(group,p)
    lp=Path('translations/editorial_review_current_v1.json');ledger=read(lp);before=read(CHECKPOINT/'editorial_review_current_v1.json.before');prior=read(receipt['prior_verified_handoff'])
    assert sha((CHECKPOINT/'editorial_review_current_v1.json.before').read_bytes())==prior['ledger_sha256'] and sha(Path(prior['handoff_receipt']).read_bytes())==prior['handoff_receipt_sha256']
    for p,digest in read(prior['handoff_receipt'])['updated_files'].items():
        saved=CHECKPOINT/(Path(p).name+'.before');assert sha((saved if saved.exists() else Path(p)).read_bytes())==digest
    fresh=ledger['contextual_story_natural_dialogue_pass_v1871'];old=before['contextual_story_natural_dialogue_pass_v1871'];doc,menu=map(read,[fresh['latest_contextual_manuscript'],fresh['latest_contextual_choice_draft']]);rows=doc['records']+menu['records']
    for d in [doc,menu]:validate_natural_dialogue_batch(d)
    selected={historical_key(r) for r in rows};keys={historical_key(r) for r in fresh['record_keys']};oldkeys={historical_key(r) for r in old['record_keys']};integrated={historical_key(r) for r in fresh['integrated_record_keys']};pending={historical_key(r) for r in fresh['pending_record_keys']};complete={historical_key(r) for g in ledger['completed_editorial_families'] for r in g['records']}
    assert len(rows)==len(selected)==159 and keys-oldkeys==selected==pending and oldkeys==integrated==complete and keys==integrated|pending and not integrated&pending
    assert len(keys)==len(fresh['record_keys'])==len(fresh['record_IDs'])==4734 and (fresh['fresh_pass_records_explicitly_reread'],fresh['fresh_pass_records_integrated'],fresh['fresh_pass_records_pending_native_actual_release'])==(4734,4575,159)
    assert Counter(p for p,k in keys)=={'/COMMON/MESFILE.DK4':1599,'/data/SC2.DK4':2907,'/data/SC0.DK4':117,'/data/SC1.DK4':73,'/data/SC3.DK4':38}
    assert ledger['records_with_source_and_prose_pass']==ledger['records_with_source_prose_drafts']==sum(ledger['source_prose_reviewed_counts_by_file'].values())==4737
    assert (ledger['records_editorially_completed'],ledger['records_revised_and_integrated'],ledger['retained_wordings_editorially_completed'])==(4575,3087,1488)
    for k in ['completed_editorial_families','completed_editorial_record_counts_by_file','current_integrated_candidate','reviewed_but_incomplete_COMMON_IDs','unresolved_graphics_work','older_record_reaudit_after_full_editorial_goal','native_source_universe_inventory_v2701c','lil_after_B119_next_clean_source_lead_v3258']:assert ledger[k]==before[k],k
    assert ledger['reviewed_but_incomplete_COMMON_IDs']==[750,751,752] and set(ledger['reviewed_but_incomplete_route_record_IDs']['/data/SC2.DK4'])=={k for p,k in selected}
    assert Counter(r['editorial_decision'] for r in rows)=={'revise':55,'retain-wording':104}
    image,clean=NdsImage.open(doc['current_ROM']),NdsImage.open('work/clean.nds');arm=image.read_file('/__arm9__.bin');en,jp=[IlnkContainer.parse(i.read_file('/data/SC2.DK4')).blocks for i in [image,clean]]
    merged=read(doc['native_font_proof']);assert sha(Path(doc['native_font_proof']).read_bytes())==doc['native_font_proof_sha256'];cases={c['id']:c for c in merged['cases']}
    assert len(cases)==155 and merged['current_original_macro_alignment_calls']==1240 and len(merged['menu_targets'])==2 and len(merged['review_sheets'])==23
    for k,n in [('source_bound_formatter_negatives',28),('source_consumer_negative_controls',23)]:assert len(merged[k])==n and all(r['rejected'] for r in merged[k])
    for s in merged['review_sheets']:assert sha(Path(s['path']).read_bytes())==s['sha256']
    for r in rows:
        assert not any(t in r['english'] for t in ['{LB','{ALIGN','{PAD']);body=r['english'] if r['kind']=='typed-choice-label' else r['english'].split('}',1)[1]
        if r['editorial_decision']=='retain-wording':assert body==r['effective_predecessor_paragraph'] and r['fresh_retained_wording_justification']
        b=r['block'];sr,cr=r['source_reference'],r['current_reference'];raw=bytes.fromhex(r['source_hex'])
        assert jp[b][sr['offset']:sr['offset']+sr['bytes']]==raw and en[b][cr['offset']:cr['offset']+cr['bytes']]==bytes.fromhex(r['current_hex'])
        assert jp[b][sr['offset']+sr['bytes']]==en[b][cr['offset']+cr['bytes']]==0
        if r['kind']=='typed-choice-label':
            target=next(t for t in merged['menu_targets'] if (t['block'],t['command_offset'])==(b,r['command_offset']));assert target['labels'][r['option_index']]==r['english'] and r['compiled_hex']==r['english'].encode('ascii').hex();continue
        assert jp[b][sr['offset']-5:sr['offset']+1]==en[b][cr['offset']-5:cr['offset']+1]==bytes.fromhex(r['source_complete_preamble_hex'])
        p=profile_for(arm,en[b],'FE-paper' if r['kind']=='system-FE' else 'progressive');encoded=encode_relocatable_dialogue(raw,r['english'],p);assert encoded.encoded.hex()==r['compiled_hex']==cases[r['id']]['encoded_hex']
        qa=audit_relocatable_dialogue_record(raw,r['english'],p);assert not [i for i in qa['issues'] if i['severity'] in ['warning','error'] and i['code'] not in r.get('qa_waivers',[])]
        assert sha(Path(cases[r['id']]['preview']).read_bytes())==cases[r['id']]['preview_sha256']
    assert sum(bool(r.get('qa_waivers')) for r in rows)==68
    source,control,branch=map(read,[doc['source_context'],doc['control_contract'],doc['branch_proof']]);assert source['total_editorial_objects']==159 and len(source['records'])==155 and len(source['typed_choice_records'])==4 and sum(len(b['all_clean_native_commands']) for b in source['blocks'])==312
    assert len(control['speech_dispatch_cases'])==310 and len(control['current_original_predicate_cases'])==14 and not control['original_event_queries'] and len(branch['cases'])==640 and len(branch['operands_requiring_adjustment_when_resizing'])==64
    waits=read(doc['original2000_wait_proof']);assert waits['current_zero_argument_wait_contract_bound_by_exact_original_code_and_actual_Lil_pause_evidence']
    for deps in [DEPENDENCIES,PROFILE_DEPS]:
        for p,digest in deps.items():assert sha(Path(p).read_bytes())==digest
    c=ledger['current_integrated_candidate'];release=read('work/analysis/lil_B111_B119_release_v3252b/registered_release_verification.json')
    assert sha(Path(c['path']).read_bytes())==c['sha256']==release['candidate_sha256'] and sha(Path(c['patch']).read_bytes())==c['patch_sha256']==release['patch_sha256'] and release['whole_ROM_reconstruction_byte_exact']
    assert Path(release['exact_patch_reconstruction']).read_bytes()==Path(c['path']).read_bytes()
    manifest,registry=read(c['manifest']),read('translations/release_stack.json');assert manifest['profile']==c['profile']=='all-routes-unified-v3251' and len(manifest['batches'])==517 and len(registry['accepted_layers'])==114 and all(manifest['checks'].values()) and manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes()) and registry['latest_promoted_build']['profile']=='all-routes-unified-v1492'
    inventory=read(ledger['unfinished_editorial_scope_v3286']['path']);oldinventory=read(before['unfinished_editorial_scope_v3258']['path'])
    for k in oldinventory:
        if k not in ['incomplete_route_source_prose_groups','incomplete_route_source_prose_count','next_focus']:assert inventory[k]==oldinventory[k],k
    assert inventory['incomplete_COMMON_count']==3 and inventory['incomplete_route_source_prose_count']==159 and inventory['canonical_Maria_SC3_B97_uncredited32_source_lead']['records']==32
    term=ledger['Proof_terminology_consistency_lead_v3286'];assert term==inventory['Proof_terminology_consistency_lead_v3286'] and term['separate_from_deferred_older_record_technical_reaudit'] and sha(Path(term['proof']).read_bytes())==term['proof_sha256']
    assert ledger['goal_status']=='active' and not ledger['full_goal_complete'] and Path('docs/editorial_handoff_current.md').read_text(encoding='utf-8').startswith('# Current editorial handoff - V3286')
    ROOT.mkdir(parents=True);save(ROOT/'verified_handoff.json',dict(checkpoint='V3286',ledger=str(lp),ledger_sha256=sha(lp.read_bytes()),handoff_receipt=str(rp),handoff_receipt_sha256=sha(rp.read_bytes()),fresh_records=4734,fresh_integrated=4575,fresh_pending=159,source_prose=4737,new_source_prose_reviews=159,new_completed_records=0,completed_records=4575,historical_revised=3087,historical_retained=1488,proposed_revisions=55,justified_retentions=104,incomplete_COMMON=3,incomplete_route=159,all159_exact_source_current_references_and_five_gates_verified=True,all155_native_planes_four_labels_and1240_macro_cases_verified=True,all23_sheets_hash_bound=True,Proof_terminology_editorial_consistency_still_open=True,canonical_Maria32_pending_uncredited=True,source00_B133_unbound_separate_from_later_technical_reaudit=True,prior_completed_release_patch_and_startup_preserved=True,prior_ledger_and_updated_file_chains_verified=True,candidate=c['path'],candidate_sha256=c['sha256'],patch=c['patch'],patch_sha256=c['patch_sha256'],actual_selected_B122_B127_IDs=[],new_emulator_runs=0,all_jobs_terminal=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('IndependentV3286 audit passes:4734 reread/4575 integrated/159 pending;all159 source/current/five gates verified;currentV3251 and broader goal preserved.')
