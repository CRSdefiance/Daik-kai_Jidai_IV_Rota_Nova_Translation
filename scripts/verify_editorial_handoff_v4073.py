"""Independently verify the uncredited B166 checkpoint and unchanged registered V4046 completion."""
from collections import Counter
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/editorial_handoff_verification_v4073')
CHECKPOINT=Path('work/analysis/lil_B166_checkpoint_v4072')
if __name__=='__main__':
    assert not ROOT.exists();rp=CHECKPOINT/'checkpoint_receipt.json';receipt=read(rp);lp=Path('translations/editorial_review_current_v1.json');ledger=read(lp);before=read(CHECKPOINT/(lp.name+'.before'))
    for p,digest in receipt['updated_files'].items():assert sha(Path(p).read_bytes())==digest,p
    for p,digest in receipt['evidence'].items():assert sha(Path(p).read_bytes())==digest,p
    assert receipt['new_source_prose_reviews']==receipt['new_completed_records']==0 and receipt['uncredited_reviewed_objects']==44
    for k in ['completed_editorial_families','contextual_story_natural_dialogue_pass_v1871','records_with_source_and_prose_pass','records_with_source_prose_drafts','records_editorially_completed','records_revised_and_integrated','retained_wordings_editorially_completed','current_integrated_candidate','reviewed_but_incomplete_COMMON_IDs','unresolved_graphics_work','older_record_reaudit_after_full_editorial_goal','native_source_universe_inventory_v2701c','Proof_terminology_consistency_lead_v3286','lil_B157_provenance_amendment_v3784']:assert ledger[k]==before[k],k
    assert ledger['goal_status']=='active' and not ledger['full_goal_complete'];fresh=ledger['contextual_story_natural_dialogue_pass_v1871'];allrows=[r for g in ledger['completed_editorial_families'] for r in g['records']];known={historical_key(r) for r in allrows}
    assert len(allrows)==len(known)==len(fresh['record_keys'])==len(fresh['integrated_record_keys'])==5529
    assert (fresh['fresh_pass_records_explicitly_reread'],fresh['fresh_pass_records_integrated'],fresh['fresh_pass_records_pending_native_actual_release'])==(5529,5529,0)
    assert fresh['pending_record_keys']==fresh['pending_contextual_families']==[]
    assert (ledger['records_with_source_and_prose_pass'],ledger['records_with_source_prose_drafts'],ledger['records_editorially_completed'],ledger['records_revised_and_integrated'],ledger['retained_wordings_editorially_completed'])==(5532,5532,5529,3527,2002)
    status=ledger['lil_B166_preintegration_review_v4072'];docs=[read(p) for p in status['manuscripts']];rows=[r for d in docs for r in d['records']]
    for p,digest in status['manuscripts'].items():assert sha(Path(p).read_bytes())==digest
    assert len(rows)==44 and Counter(r['editorial_decision'] for r in rows)=={'revise':24,'retain-wording':20}
    assert not known&{historical_key(r) for r in rows}
    assert all(all(r['review'][k] for k in ['source','context','localization','naturalness']) and not r['review']['formatting'] and r['full_clean_context_precedes_comparison'] and r['source_meaning']==r['fresh_source_gloss'] for r in rows)
    for r in rows:
        if r['editorial_decision']=='retain-wording':assert r['fresh_retained_wording_justification'] and (r['english'] if r['kind']=='typed-choice-label' else r['english'].split('}',1)[1])==r['effective_predecessor_paragraph']
    assert sum(bytes.fromhex(r['source_hex']).count(b'FI') for r in rows)==3 and sum(r['english'].count('{MACRO:FI}') for r in rows)==3
    assert Counter(r['kind'] for r in rows)=={'progressive':42,'typed-choice-label':2}
    findings=read(status['findings']);assert sha(Path(status['findings']).read_bytes())==status['findings_sha256'] and len(findings['all_six_native_sheets_viewed'])==6 and len(findings['nine_phrase_flow_findings'])==9
    for s in findings['all_six_native_sheets_viewed']:assert s['viewed'] and sha(Path(s['path']).read_bytes())==s['sha256']
    assert findings['menu_diagnostic_sheet_viewed'] and findings['no_menu_or_formatting_approval'] and findings['standalone_painter_mismatch_not_confirmed_actual_gameplay_defect']
    native=read('work/analysis/lil_B166_fonts_v4068/current_macro_QA_and_progressive_font_proof.json');assert len(native['cases'])==42 and native['current_original_macro_alignment_calls']==336 and len(native['negative_controls'])==17 and all(c['rejected'] for c in native['negative_controls'])
    for c in native['cases']:
        assert c['complete_native_independent216x64_plane_equal'] and c['all_first_final_internal_glyphs_in_order_and_unique_cells'] and c['all_visible_origins_zero_and16px_rows_within4rows']
        assert sha(Path(c['preview']).read_bytes())==c['preview_sha256'] and sum(len(p['cases']) for p in c['current_native_macro_pipelines'])==8
    diag=read('work/analysis/lil_B166_menu_pixels_v4071/width_cases_no_mismatch_approval.json')
    assert [(r['logical_width'],r['storage_stride'],r['independent_complete_native_pixels_match']) for r in diag['cases']]==[(54,56,False),(56,56,False),(58,60,True),(60,60,True)] and diag['no_menu_approval_or_credit']
    widths=read('work/analysis/lil_B166_menu_diagnostic_v4070/original_VM_widths_and_preserved_failed_probe.json');assert [r['width_px'] for r in widths['cases']]==[60,54] and widths['failure']
    scope=ledger['unfinished_editorial_scope_v4072'];assert sha(Path(scope['path']).read_bytes())==scope['sha256'] and scope['uncredited_B166_draft_objects']==44 and scope['remaining_B167_B180_physical_speeches']==348 and scope['remaining_B167_B180_choice_command_leads']==1
    inv=read('work/analysis/lil_B161_B180_clean_scope_v3910/complete_clean_B161_B180_next_exchange_inventory.json');remaining=[b for b in inv['blocks'] if 167<=b['block']<=180]
    assert sum(b['speeches'] for b in remaining)==348 and sum(b['typed_menu_2100_commands'] for b in remaining)==1
    assert ledger['coverage_units']==[{**u,'next':next(v for v in ledger['coverage_units'] if v['id']=='all-route-scenes')['next']} if u['id']=='all-route-scenes' else u for u in before['coverage_units']]
    candidate=ledger['current_integrated_candidate'];release=read('work/analysis/lil_B165_release_v4047/registered_release_verification.json');manifest=read(candidate['manifest']);registry=read('translations/release_stack.json')
    assert sha(Path(candidate['path']).read_bytes())==candidate['sha256']==receipt['candidate_sha256']==release['candidate_sha256'] and sha(Path(candidate['patch']).read_bytes())==candidate['patch_sha256']==receipt['patch_sha256']==release['patch_sha256']
    assert Path(release['exact_patch_reconstruction']).read_bytes()==Path(candidate['path']).read_bytes() and release['whole_ROM_reconstruction_byte_exact']
    assert manifest['profile']==candidate['profile']=='all-routes-unified-v4046' and len(manifest['batches'])==539 and all(manifest['checks'].values()) and manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes())
    assert len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v1492'
    assert Path('docs/editorial_handoff_current.md').read_text(encoding='utf-8').startswith('# Current editorial handoff - V4072')
    ROOT.mkdir(parents=True)
    save(ROOT/'verified_handoff.json',dict(checkpoint='V4072',ledger_sha256=sha(lp.read_bytes()),handoff_receipt=str(rp),handoff_receipt_sha256=sha(rp.read_bytes()),fresh_reread=5529,integrated=5529,pending=0,source_prose=5532,revised=3527,retained=2002,candidate=candidate['path'],candidate_sha256=candidate['sha256'],patch=candidate['patch'],patch_sha256=candidate['patch_sha256'],manifest_batches=539,accepted_layers=114,B165_completed_verification='work/analysis/editorial_handoff_verification_v4051/verified_handoff.json',uncredited_B166_reviewed_objects=44,B166_proposed_revisions=24,B166_justified_retentions=20,B166_native_speech_planes=42,B166_macro_alignment_cases=336,all_six_native_sheets_viewed=True,nine_phrase_flow_findings_preserved=True,typed_menu_painter_storage_ownership_unresolved_without_false_gameplay_claim=True,no_new_credit_ROM_registry_or_gameplay_claim=True,remaining_B167_B180_physical_speeches=348,remaining_choice_command_leads=1,all_prior_completions_graphics_and_wider_scope_preserved=True,full_goal_active=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('V4072 independently verified:V4046 exact clean patch preserved;5529/5529/0;44 B166 drafts uncredited;9phrase-flow findings/menu-painter ownership open. Full goal active.')
