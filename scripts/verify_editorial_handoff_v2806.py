"""Independent119-review source/native/coverage audit; zero release credit."""
from pathlib import Path
from copy import deepcopy
from collections import Counter
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.dialogue.lil_india_polder_profile import profile_for
from dk4tool.dialogue.lil_india_polder_layout_v3 import encode_relocatable_dialogue,audit_relocatable_dialogue_record,DEPENDENCIES
from dk4tool.patch.grand_race_menu_release import sha
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/editorial_handoff_verification_v2806')
BASELINE=Path('work/analysis/lil_India_Polder_checkpoint_v2805b')
CHECKPOINT=Path('work/analysis/lil_India_Polder_checkpoint_v2805c')
if __name__=='__main__':
    assert not ROOT.exists();rp=CHECKPOINT/'checkpoint_receipt.json';receipt=read(rp)
    for group in ['evidence','updated_files']:
        for p,digest in receipt[group].items():assert sha(Path(p).read_bytes())==digest,(group,p)
    correction=read(receipt['metadata_correction']);original_receipt=read(correction['prior_receipt'])
    assert sha(Path(correction['prior_receipt']).read_bytes())==correction['prior_receipt_sha256']
    assert correction['this_operation_adds_source_prose_orcompletion_credit']==0
    for p,digest in correction['before_files'].items():assert sha((CHECKPOINT/(Path(p).name+'.before')).read_bytes())==digest
    for p in original_receipt['updated_files']:
        if Path(p).parent==Path('docs'):
            saved=(CHECKPOINT/(Path(p).name+'.before')).read_bytes()
            assert saved.replace(correction['old_title'].encode(),correction['new_title'].encode(),1)==Path(p).read_bytes()
    lp=Path('translations/editorial_review_current_v1.json');ledger=read(lp);before=read(BASELINE/'editorial_review_current_v1.json.before')
    previous=read('work/analysis/editorial_handoff_verification_v2788/verified_handoff.json');assert sha((BASELINE/'editorial_review_current_v1.json.before').read_bytes())==previous['ledger_sha256']
    for p,digest in read(previous['handoff_receipt'])['updated_files'].items():
        saved=BASELINE/(Path(p).name+'.before');assert sha((saved if saved.exists() else Path(p)).read_bytes())==digest
    def normalize_labels(item):
        item=deepcopy(item);f=item['contextual_story_natural_dialogue_pass_v1871'];family=f['latest_pending_contextual_family']
        item['active_source_prose_drafts'].pop('status')
        for group in f['pending_contextual_families']:group.pop('pending')
        item['lil_India_Polder_source_prose_native_v2805'].pop('pending')
        for unit in item['coverage_units']:
            if unit['id']==family:unit.pop('pending')
            if unit['id']=='all-route-scenes':unit.pop('next')
        return item
    assert normalize_labels(ledger)==normalize_labels(read(CHECKPOINT/'editorial_review_current_v1.json.before'))
    fresh,oldfresh=ledger['contextual_story_natural_dialogue_pass_v1871'],before['contextual_story_natural_dialogue_pass_v1871'];doc=read(fresh['latest_contextual_manuscript']);rows=doc['records']
    selected={historical_key(r) for r in rows};keys={historical_key(r) for r in fresh['record_keys']};oldkeys={historical_key(r) for r in oldfresh['record_keys']}
    integrated={historical_key(r) for r in fresh['integrated_record_keys']};pending={historical_key(r) for r in fresh['pending_record_keys']};complete={historical_key(r) for g in ledger['completed_editorial_families'] for r in g['records']}
    assert len(selected)==len(rows)==119 and keys-oldkeys==selected==pending and oldkeys==integrated==complete
    assert not integrated&pending and keys==integrated|pending and len(keys)==len(fresh['record_keys'])==len(fresh['record_IDs'])==2581
    assert (fresh['fresh_pass_records_explicitly_reread'],fresh['fresh_pass_records_integrated'],fresh['fresh_pass_records_pending_native_actual_release'])==(2581,2462,119)
    assert Counter(p for p,k in keys)=={'/COMMON/MESFILE.DK4':1599,'/data/SC2.DK4':754,'/data/SC0.DK4':117,'/data/SC1.DK4':73,'/data/SC3.DK4':38}
    assert ledger['records_with_source_and_prose_pass']==ledger['records_with_source_prose_drafts']==sum(ledger['source_prose_reviewed_counts_by_file'].values())==2584
    assert (ledger['records_editorially_completed'],ledger['records_revised_and_integrated'],ledger['retained_wordings_editorially_completed'])==(2462,1724,738)
    for k in ['completed_editorial_families','completed_editorial_record_counts_by_file','current_integrated_candidate','reviewed_but_incomplete_COMMON_IDs','unresolved_graphics_work','older_record_reaudit_after_full_editorial_goal','native_source_universe_inventory_v2701c']:assert ledger[k]==before[k],k
    assert ledger['reviewed_but_incomplete_COMMON_IDs']==[750,751,752] and set(ledger['reviewed_but_incomplete_route_record_IDs']['/data/SC2.DK4'])=={k for p,k in selected}
    assert Counter(r['editorial_decision'] for r in rows)=={'revise':84,'retain-wording':35}
    assert all(all(r['review'].values()) and r['source_meaning'] and r['context'] and r['localization_note'] for r in rows)
    assert all(not any(tag in r['english'] for tag in ['{LB','{ALIGN','{PAD']) for r in rows)
    for r in rows:
        if r['editorial_decision']=='retain-wording':
            old=' '.join(r['current_English'].split())
            for macro in ['FI','FA','FO']:old=old.replace(macro,'{MACRO:'+macro+'}')
            assert r['english'].split('}',1)[1]==old and r['fresh_retained_wording_justification']
    source,control,branch,font=map(read,[doc['source_context'],doc['control_contract'],doc['branch_proof'],doc['native_font_proof']])
    assert source['total_editorial_objects']==source['progressive_speeches']==119 and source['system_FE_panels']==source['typed_choice_labels']==0
    assert [b['block'] for b in source['blocks']]==[37,38,39,40,129,130] and [len(b['records']) for b in source['blocks']]==[13,43,15,14,27,7]
    assert sum(len(b['all_clean_native_commands']) for b in source['blocks'])==193 and len(branch['cases'])==400 and len(branch['operands_requiring_adjustment_when_resizing'])==40
    assert all(c['target_is_independently_mapped_native_boundary'] and c['source_block_owner_input_result_guards_and_ABI_exact'] for c in branch['cases'])
    assert control['all119_complete_preambles_and238_historical_dispatch_contexts_pass'] and len(control['dispatch_cases'])==238 and len(control['current_original_predicate_cases'])==10
    assert control['ordinary_native_actor_selectors']=={str(k):k for k in [2,9,16,21,92,151,171]}
    assert [(q['block'],q['event']) for q in control['original_event_queries']]==[(37,129),(38,48),(38,48),(129,130),(130,26)]
    assert all(p['all_unowned4MiB_actor_models_ABI_input_owner_and_output_canaries_exact'] and p['sole_scratch_restore_recovers_all4MiB_exact'] and p['no_predicate_or_event_flag_forced'] for p in control['current_original_predicate_cases'])
    assert font['all119_progressive_full_QA_and_complete_native_fonts_pass'] and len(font['cases'])==len(font['all119_full_QA_reports'])==119 and font['current_original_macro_alignment_calls']==952
    assert (font['newly_executed_font_cases'],font['reused_unchanged_font_cases'],font['newly_executed_current_macro_alignment_cases'],font['reused_current_macro_alignment_cases'])==(3,116,24,928)
    assert sha(Path(font['reused_proof']).read_bytes())==font['reused_proof_sha256']
    assert len(font['negative_controls'])==7 and all(n['rejected'] for n in font['negative_controls']) and len(font['review_sheets'])==15
    for s in font['review_sheets']:assert sha(Path(s['path']).read_bytes())==s['sha256']
    approval=read('work/analysis/lil_India_Polder_font_approval_v2804/approval_receipt.json')
    assert approval['manuscript_sha256']==sha(Path(fresh['latest_contextual_manuscript']).read_bytes()) and approval['all119_five_per_record_review_gates_true'] and approval['all15_review_sheets_viewed']
    assert len(approval['source_bound_formatter_negatives'])==14 and len(approval['source_English_control_macro_invariants'])==119
    assert sum(bool(r.get('qa_waivers')) for r in rows)==39 and all(r.get('qa_waivers') in [None,['line-break-count']] for r in rows)
    for p,digest in DEPENDENCIES.items():assert sha(Path(p).read_bytes())==digest
    candidate=ledger['current_integrated_candidate'];image=NdsImage.open(candidate['path']);clean=NdsImage.open('work/clean.nds');arm=image.read_file('/__arm9__.bin');en,jp=[IlnkContainer.parse(i.read_file('/data/SC2.DK4')).blocks for i in [image,clean]]
    assert sha(image.read_file('/data/SC2.DK4'))==source['current_SC2_sha256'] and sha(clean.read_file('/data/SC2.DK4'))==source['source_SC2_sha256'];cases={c['id']:c for c in font['cases']}
    for r in rows:
        b=r['block'];sr,cr=r['source_reference'],r['current_reference']
        assert jp[b][sr['offset']:sr['offset']+sr['bytes']]==bytes.fromhex(r['source_hex']) and en[b][cr['offset']:cr['offset']+cr['bytes']]==bytes.fromhex(r['current_hex'])
        assert jp[b][sr['offset']-5:sr['offset']+1]==en[b][cr['offset']-5:cr['offset']+1]==bytes.fromhex('0040ffff00'+r['source_presentation_prefix_hex'])
        p=profile_for(arm,en[b]);encoded=encode_relocatable_dialogue(bytes.fromhex(r['source_hex']),r['english'],p);assert encoded.encoded.hex()==r['compiled_hex']==cases[r['id']]['encoded_hex']
        qa=audit_relocatable_dialogue_record(bytes.fromhex(r['source_hex']),r['english'],p);assert not [i for i in qa['issues'] if i['severity'] in ['warning','error'] and i['code'] not in r.get('qa_waivers',[])]
    release=read('work/analysis/lil_Mediterranean_Africa_release_v2784/registered_release_verification.json');manifest=read(candidate['manifest']);registry=read('translations/release_stack.json')
    assert sha(Path(candidate['path']).read_bytes())==candidate['sha256']==release['candidate_sha256'] and sha(Path(candidate['patch']).read_bytes())==candidate['patch_sha256']==release['patch_sha256']
    assert sha(Path(candidate['manifest']).read_bytes())==release['manifest_sha256'] and manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes())
    assert release['whole_ROM_reconstruction_byte_exact'] and sha(Path(release['exact_patch_reconstruction']).read_bytes())==candidate['sha256']
    assert manifest['profile']=='all-routes-unified-v2783' and len(manifest['batches'])==499 and len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v1492'
    assert sha(Path('scripts/build_integrated_release.py').read_bytes())==read('work/analysis/lil_Mediterranean_Africa_registration_v2782/registration_receipt.json')['builder_sha256']
    assert control['actual_selected_India_Polder_IDs']==doc['actual_selected_India_Polder_IDs']==[] and control['new_emulator_runs']==doc['new_emulator_runs']==0
    inventory=read(ledger['unfinished_editorial_scope_v2805']['path']);assert inventory['incomplete_COMMON_count']==3 and inventory['incomplete_route_source_prose_count']==119
    unit=next(u for u in ledger['coverage_units'] if u['id']=='all-route-scenes');assert (unit['reviewed_route_records'],unit['completed_route_records'])==(982,863)
    assert ledger['raw_source_coverage_revisit']['status']=='open-before-whole-goal-completion' and ledger['next_named_target_reports_source_lead_v2664']['completion_credit_added']==0
    text=Path('docs/editorial_handoff_current.md').read_text(encoding='utf8');assert text.startswith('# Current editorial handoff - V2805') and correction['new_title'] in text and '2581 reread /2462 integrated-reconciled /119 pending' in text
    assert ledger['goal_status']=='active' and not ledger['full_goal_complete']
    ROOT.mkdir(parents=True);save(ROOT/'verified_handoff.json',dict(checkpoint='V2805',ledger=str(lp),ledger_sha256=sha(lp.read_bytes()),handoff_receipt=str(rp),handoff_receipt_sha256=sha(rp.read_bytes()),fresh_records=2581,fresh_integrated=2462,fresh_pending=119,source_prose=2584,new_source_prose_reviews=119,new_completed_records=0,proposed_revisions=84,justified_retentions=35,completed_records=2462,historical_revised=1724,historical_retained=738,incomplete_COMMON=3,incomplete_route=119,source193commands119preambles_40sites400cases_238dispatch10predicates_bound=True,current119planes952macro_cases_fullQA_and14formatter_rejections_bound=True,all15_final_sheets_viewed_or_hash_identical_to_viewed=True,narrow_line_count_notes=39,reference_relocation_representative_registered_release_pending=True,actual_selected_India_Polder_IDs=[],new_emulator_runs=0,candidate=candidate['path'],candidate_sha256=candidate['sha256'],patch=candidate['patch'],patch_sha256=candidate['patch_sha256'],no_ROM_registry_builder_manifest_patch_or_global_runtime_change=True,whole_clean_input_patch_proof_still_bound=True,original119_credit_and_metadata_only_correction_chains_verified=True,prior_ledger_updated_file_and_source_chains_verified=True,all_jobs_terminal=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('IndependentV2805 audit passes:119new contextual/native reviews;2581reread/2462integrated/119pending,source-prose2584. V2783ROM/cleanpatch preserved;full goal active.')
