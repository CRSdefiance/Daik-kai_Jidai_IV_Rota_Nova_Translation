"""Independent 152-review ledger/source/format audit; no pending release credit."""
from pathlib import Path
from collections import Counter
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.dialogue.lil_mediterranean_africa_profile import profile_for
from dk4tool.dialogue.lil_mediterranean_africa_layout_v3 import encode_relocatable_dialogue,audit_relocatable_dialogue_record,DEPENDENCIES
from dk4tool.patch.grand_race_menu_release import sha
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/editorial_handoff_verification_v2775')
CHECKPOINT=Path('work/analysis/lil_Mediterranean_Africa_checkpoint_v2774')
if __name__=='__main__':
    assert not ROOT.exists();rp=CHECKPOINT/'checkpoint_receipt.json';receipt=read(rp)
    for group in ['evidence','updated_files']:
        for path,digest in receipt[group].items():assert sha(Path(path).read_bytes())==digest,(group,path)
    lp=Path('translations/editorial_review_current_v1.json');ledger=read(lp);bp=CHECKPOINT/'editorial_review_current_v1.json.before';before=read(bp)
    previous=read('work/analysis/editorial_handoff_verification_v2755/verified_handoff.json');assert sha(bp.read_bytes())==previous['ledger_sha256']
    for path,digest in read(previous['handoff_receipt'])['updated_files'].items():
        saved=CHECKPOINT/(Path(path).name+'.before');assert sha((saved if saved.exists() else Path(path)).read_bytes())==digest,path
    fresh,oldfresh=ledger['contextual_story_natural_dialogue_pass_v1871'],before['contextual_story_natural_dialogue_pass_v1871']
    doc=read(fresh['latest_contextual_manuscript']);menu=read(fresh['latest_contextual_choice_draft']);rows=doc['records']+menu['records'];selected={historical_key(r) for r in rows}
    keys={historical_key(r) for r in fresh['record_keys']};oldkeys={historical_key(r) for r in oldfresh['record_keys']};integrated={historical_key(r) for r in fresh['integrated_record_keys']};pending={historical_key(r) for r in fresh['pending_record_keys']}
    complete={historical_key(r) for g in ledger['completed_editorial_families'] for r in g['records']}
    assert len(selected)==len(rows)==152 and keys-oldkeys==selected==pending and oldkeys==integrated==complete
    assert not integrated&pending and keys==integrated|pending and len(keys)==len(fresh['record_keys'])==len(fresh['record_IDs'])==2462
    assert (fresh['fresh_pass_records_explicitly_reread'],fresh['fresh_pass_records_integrated'],fresh['fresh_pass_records_pending_native_actual_release'])==(2462,2310,152)
    assert Counter(p for p,k in keys)=={'/COMMON/MESFILE.DK4':1599,'/data/SC2.DK4':635,'/data/SC0.DK4':117,'/data/SC1.DK4':73,'/data/SC3.DK4':38}
    assert ledger['records_with_source_and_prose_pass']==ledger['records_with_source_prose_drafts']==sum(ledger['source_prose_reviewed_counts_by_file'].values())==2465
    assert (ledger['records_editorially_completed'],ledger['records_revised_and_integrated'],ledger['retained_wordings_editorially_completed'])==(2310,1614,696)
    for key in ['completed_editorial_families','completed_editorial_record_counts_by_file','current_integrated_candidate','reviewed_but_incomplete_COMMON_IDs','unresolved_graphics_work','older_record_reaudit_after_full_editorial_goal','native_source_universe_inventory_v2701c']:
        assert ledger[key]==before[key],key
    assert ledger['reviewed_but_incomplete_COMMON_IDs']==[750,751,752]
    assert set(ledger['reviewed_but_incomplete_route_record_IDs']['/data/SC2.DK4'])=={k for p,k in selected}
    assert Counter(r['editorial_decision'] for r in rows)=={'revise':110,'retain-wording':42}
    assert all(all(r['review'].values()) and r['source_meaning'] and r['context'] and r['localization_note'] for r in rows)
    assert all(not any(tag in r['english'] for tag in ['{LB','{ALIGN','{PAD']) for r in rows)
    for r in rows:
        if r['editorial_decision']=='retain-wording':
            old=' '.join(r['current_English'].split())
            for macro in ['FI','FA','FO']:old=old.replace(macro,'{MACRO:'+macro+'}')
            assert r['english'].split('}',1)[-1]==old and r['localization_note'],r['id']
    source,control,branch,font=map(read,[doc['source_context'],doc['control_contract'],doc['branch_proof'],doc['native_font_proof']])
    assert source['total_editorial_objects']==152 and (source['progressive_speeches'],source['system_FE_panels'],source['typed_choice_labels'])==(145,1,6)
    assert [b['block'] for b in source['blocks']]==[20,32,33,34,35,36,134]
    assert sum(len(b['all_clean_native_commands']) for b in source['blocks'])==353 and len(branch['cases'])==1240 and len(branch['operands_requiring_adjustment_when_resizing'])==124
    for n,dep in [(32,20),(33,134)]:assert next(b for b in source['blocks'] if b['block']==n)['original_event_source']['must_be_completed']==[dep]
    assert len(control['dispatch_cases'])==292 and len(control['current_original_predicate_cases'])==28 and control['all146_complete_preambles_and292_historical_dispatch_contexts_pass']
    assert control['source_owned_unaligned_read_scratch_restored_all4MiB_exact'] and control['FE_before_fallback208_uses5473C_and_null_macro_actor']
    assert all(c['target_is_independently_mapped_native_boundary'] and c['source_block_owner_input_result_guards_and_ABI_exact'] for c in branch['cases'])
    assert all(p['all_unowned4MiB_actor_models_ABI_input_owner_and_output_canaries_exact'] and p['sole_scratch_restore_recovers_all4MiB_exact'] and p['no_predicate_or_event_flag_forced'] for p in control['current_original_predicate_cases'])
    assert len(font['cases'])==146 and font['current_original_macro_alignment_calls']==1168 and font['all146_current_native_planes_and_complete_glyphs_pass']
    assert len(font['source_bound_formatter_negatives'])==13 and all(n['rejected'] for n in font['source_bound_formatter_negatives'])
    assert len(font['source_English_macro_control_invariants'])==146 and len(font['all23_review_sheets'])==23
    for s in font['all23_review_sheets']:assert sha(Path(s['path']).read_bytes())==s['sha256']
    for path,digest in DEPENDENCIES.items():assert sha(Path(path).read_bytes())==digest
    progressive=read(doc['native_progressive_proof']);fe=read(doc['native_FE_proof']);choice=read(doc['native_choice_proof'])
    assert len(progressive['cases'])==145 and len(progressive['all146_full_QA_reports'])==146 and progressive['current_original_macro_alignment_calls']==1160
    assert (progressive['newly_executed_font_cases'],progressive['reused_unchanged_font_cases'])==(9,136)
    assert progressive['newly_executed_current_macro_alignment_calls']==72 and progressive['reused_current_macro_alignment_calls']==1088
    assert fe['current_original_null_actor_macro_alignment_cases']==8 and fe['one_native_page_consumes_complete_target'] and fe['complete_native_independent_plane_and_all_glyphs_and_canaries_equal']
    assert choice['native_selection_cancel_cases']==18 and choice['complete_current_and_reviewed_style_label_planes']==24
    for m in choice['menus']:
        assert sha(Path(m['proof']).read_bytes())==m['sha256'];c=read(m['proof'])
        assert c['six_original_VM_selection_and_cancel_cases_pass'] and c['eight_complete_native_style_label_planes_pass']
        assert c['stored_option_indices_and_original_selection_return_values_preserved'] and c['input_loop_is_bridged_not_actual_selected_branch_gameplay']
    candidate=ledger['current_integrated_candidate'];image=NdsImage.open(candidate['path']);clean=NdsImage.open('work/clean.nds');arm=image.read_file('/__arm9__.bin')
    en,jp=[IlnkContainer.parse(i.read_file('/data/SC2.DK4')).blocks for i in [image,clean]];cases={c['id']:c for c in font['cases']}
    assert sha(image.read_file('/data/SC2.DK4'))==source['current_SC2_sha256'] and sha(clean.read_file('/data/SC2.DK4'))==source['source_SC2_sha256']
    for r in rows:
        b=r['block'];sr,cr=r['source_reference'],r['current_reference']
        assert jp[b][sr['offset']:sr['offset']+sr['bytes']]==bytes.fromhex(r['source_hex']) and en[b][cr['offset']:cr['offset']+cr['bytes']]==bytes.fromhex(r['current_hex']),r['id']
        if r['kind']=='typed-choice-label':continue
        assert jp[b][sr['offset']-5:sr['offset']+1]==en[b][cr['offset']-5:cr['offset']+1]==bytes.fromhex('0040ffff00'+r['source_presentation_prefix_hex'])
        p=profile_for(arm,en[b],'FE-paper' if r['kind']=='system-FE' else 'progressive');encoded=encode_relocatable_dialogue(bytes.fromhex(r['source_hex']),r['english'],p)
        assert encoded.encoded.hex()==r['compiled_hex']==cases[r['id']]['encoded_hex']
        qa=audit_relocatable_dialogue_record(bytes.fromhex(r['source_hex']),r['english'],p)
        assert not [i for i in qa['issues'] if i['severity'] in ['warning','error'] and i['code'] not in r.get('qa_waivers',[])]
    assert sum(bool(r.get('qa_waivers')) for r in doc['records'])==54 and all(r.get('qa_waivers') in [None,['line-break-count']] for r in doc['records'])
    assert doc['all23_review_sheets_viewed_or_identical'] and doc['formatter_phrase_flow_findings_resolved_without_waiver']
    release=read('work/analysis/lil_post_Seville_release_v2751/registered_release_verification.json');manifest=read(candidate['manifest']);registry=read('translations/release_stack.json')
    assert sha(Path(candidate['path']).read_bytes())==candidate['sha256']==release['candidate_sha256'] and sha(Path(candidate['patch']).read_bytes())==candidate['patch_sha256']==release['patch_sha256']
    assert sha(Path(candidate['manifest']).read_bytes())==release['manifest_sha256'] and manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes())
    assert release['whole_ROM_reconstruction_byte_exact'] and sha(Path(release['exact_patch_reconstruction']).read_bytes())==candidate['sha256']
    assert manifest['profile']=='all-routes-unified-v2750' and len(manifest['batches'])==497 and len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v1492'
    assert sha(Path('scripts/build_integrated_release.py').read_bytes())==read('work/analysis/lil_post_Seville_registration_v2749/registration_receipt.json')['builder_sha256']
    assert control['actual_selected_Mediterranean_Africa_IDs']==doc['actual_selected_Mediterranean_Africa_IDs']==[] and control['new_emulator_runs']==doc['new_emulator_runs']==0
    inventory=read(ledger['unfinished_editorial_scope_v2774']['path']);assert inventory['incomplete_COMMON_count']==3 and inventory['incomplete_route_source_prose_count']==152
    unit=next(u for u in ledger['coverage_units'] if u['id']=='all-route-scenes');assert (unit['reviewed_route_records'],unit['completed_route_records'])==(863,711)
    assert ledger['raw_source_coverage_revisit']['status']=='open-before-whole-goal-completion' and ledger['next_named_target_reports_source_lead_v2664']['completion_credit_added']==0
    text=Path('docs/editorial_handoff_current.md').read_text(encoding='utf8');assert text.startswith('# Current editorial handoff - V2774') and '2462 reread /2310 integrated-reconciled /152 pending' in text
    assert ledger['goal_status']=='active' and not ledger['full_goal_complete']
    ROOT.mkdir(parents=True);save(ROOT/'verified_handoff.json',dict(checkpoint='V2774',ledger=str(lp),ledger_sha256=sha(lp.read_bytes()),handoff_receipt=str(rp),handoff_receipt_sha256=sha(rp.read_bytes()),fresh_records=2462,fresh_integrated=2310,fresh_pending=152,source_prose=2465,new_source_prose_reviews=152,new_completed_records=0,proposed_revisions=110,justified_retentions=42,completed_records=2310,historical_revised=1614,historical_retained=696,incomplete_COMMON=3,incomplete_route=152,native353commands146preambles_124sites1240cases_and292dispatch_28predicates_bound=True,current146panels1168macro_cases_24menu_planes18VMreturns_bound=True,all23_final_sheets_viewed_or_identical=True,narrow_line_count_notes=54,reference_relocation_representative_registered_release_pending=True,actual_selected_Mediterranean_Africa_IDs=[],new_emulator_runs=0,candidate=candidate['path'],candidate_sha256=candidate['sha256'],patch=candidate['patch'],patch_sha256=candidate['patch_sha256'],no_ROM_registry_builder_manifest_patch_or_global_runtime_change=True,whole_clean_input_patch_proof_still_bound=True,prior_ledger_updated_file_and_source_chains_verified=True,all_jobs_terminal=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('IndependentV2774 audit passes:152new contextual/native reviews;2462reread/2310integrated/152pending. V2750ROM/cleanpatch preserved;full goal active.')
