"""Independent34-review checkpoint audit; no release credit for pending work."""
from pathlib import Path
from collections import Counter
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.dialogue.lil_post_seville_profile import profile_for
from dk4tool.dialogue.encoder import encode_relocatable_dialogue
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/editorial_handoff_verification_v2742')
CHECKPOINT=Path('work/analysis/lil_post_Seville_checkpoint_v2741')
if __name__=='__main__':
    assert not ROOT.exists();rp=CHECKPOINT/'checkpoint_receipt.json';receipt=read(rp)
    for group in ['evidence','updated_files']:
        for p,digest in receipt[group].items():assert sha(Path(p).read_bytes())==digest,(group,p)
    lp=Path('translations/editorial_review_current_v1.json');ledger=read(lp);bp=CHECKPOINT/'editorial_review_current_v1.json.before';before=read(bp)
    previous=read('work/analysis/editorial_handoff_verification_v2729/verified_handoff.json');assert sha(bp.read_bytes())==previous['ledger_sha256']
    for p,digest in read(previous['handoff_receipt'])['updated_files'].items():
        old=CHECKPOINT/(Path(p).name+'.before');assert sha((old if old.exists() else Path(p)).read_bytes())==digest
    fresh,oldfresh=ledger['contextual_story_natural_dialogue_pass_v1871'],before['contextual_story_natural_dialogue_pass_v1871']
    docpath=Path(fresh['latest_contextual_manuscript']);doc=read(docpath);rows=doc['records'];selected={(r['file_path'],r['id']) for r in rows}
    keys={(r['file_path'],r['id']) for r in fresh['record_keys']};oldkeys={(r['file_path'],r['id']) for r in oldfresh['record_keys']}
    integrated={(r['file_path'],r['id']) for r in fresh['integrated_record_keys']};pending={(r['file_path'],r['id']) for r in fresh['pending_record_keys']}
    complete={historical_key(r) for g in ledger['completed_editorial_families'] for r in g['records']}
    assert len(selected)==len(rows)==34 and keys-oldkeys==selected and oldkeys==integrated==complete and pending==selected
    assert not integrated&pending and keys==integrated|pending
    assert len(keys)==len(fresh['record_keys'])==len(fresh['record_IDs'])==2310 and len(integrated)==2276
    assert (fresh['fresh_pass_records_explicitly_reread'],fresh['fresh_pass_records_integrated'],fresh['fresh_pass_records_pending_native_actual_release'])==(2310,2276,34)
    assert Counter(p for p,k in keys)=={'/COMMON/MESFILE.DK4':1599,'/data/SC2.DK4':483,'/data/SC0.DK4':117,'/data/SC1.DK4':73,'/data/SC3.DK4':38}
    assert ledger['records_with_source_and_prose_pass']==ledger['records_with_source_prose_drafts']==sum(ledger['source_prose_reviewed_counts_by_file'].values())==2313
    assert ledger['source_prose_reviewed_counts_by_file']=={**before['source_prose_reviewed_counts_by_file'],'/data/SC2.DK4':483}
    assert (ledger['records_editorially_completed'],ledger['records_revised_and_integrated'],ledger['retained_wordings_editorially_completed'])==(2276,1592,684)
    for key in ['completed_editorial_families','completed_editorial_record_counts_by_file','current_integrated_candidate','reviewed_but_incomplete_COMMON_IDs','unresolved_graphics_work','older_record_reaudit_after_full_editorial_goal','native_source_universe_inventory_v2701c']:
        assert ledger[key]==before[key],key
    assert ledger['reviewed_but_incomplete_COMMON_IDs']==[750,751,752]
    assert set(ledger['reviewed_but_incomplete_route_record_IDs']['/data/SC2.DK4'])=={k for p,k in selected}
    assert not any(v for p,v in ledger['reviewed_but_incomplete_route_record_IDs'].items() if p!='/data/SC2.DK4')
    assert len(fresh['pending_contextual_families'])==1 and fresh['pending_contextual_families'][0]['records']==34
    assert Counter(r['editorial_decision'] for r in rows)=={'revise':22,'retain-wording':12}
    assert doc['translation_policy']=='natural-dialogue-v2' and doc['target_locale']=='en-US' and not doc['formatting_review_pending']
    assert all(all(r['review'].values()) and r['source_meaning'] and r['localization_note'] for r in rows)
    assert all('{LB' not in r['english'] and '{PAD}' not in r['english'] and '{ALIGN' not in r['english'] for r in rows)
    for r in rows:
        if r['editorial_decision']=='retain-wording':assert r['fresh_retained_wording_justification'] and r['english'].split('}',1)[1]==' '.join(r['current_English'].split()).replace('FI','{MACRO:FI}').replace('FA','{MACRO:FA}').replace('FO','{MACRO:FO}')
    source,control,branch,font=map(read,[doc['source_context'],doc['control_contract'],doc['branch_proof'],doc['native_font_proof']])
    assert source['total_editorial_objects']==source['progressive_speeches']==34 and source['system_FE_panels']==source['typed_choice_labels']==0
    assert [(b['block'],len(b['records'])) for b in source['blocks']]==[(30,14),(31,12),(132,8)]
    assert sum(len(b['all_clean_native_commands']) for b in source['blocks'])==91 and len(branch['cases'])==320 and len(branch['operands_requiring_adjustment_when_resizing'])==32
    assert all(c['target_is_independently_mapped_native_boundary'] and c['source_block_owner_input_result_guards_and_ABI_exact'] for c in branch['cases'])
    assert next(c for c in branch['cases'] if c['version']=='current' and c['block']==31 and c['offset']==140 and c['last_choice_or_result']==1)['original_next_command_offset']==448
    assert control['all34_complete_preambles_and68_historical_dispatch_contexts_pass'] and len(control['dispatch_cases'])==68 and len(control['current_original_predicate_cases'])==8
    assert control['ordinary_native_actor_selectors']=={'2':2,'4':4,'9':9,'16':16,'20':20,'28':28,'31':31,'92':92,'113':113}
    assert control['warning_reference_is_B132_Barkeep_not_Clifford'] and control['all_predicates_current_instruction_and_unowned4MiB_exact'] and control['source_owned_unaligned_read_scratch_restored_all4MiB_exact']
    pred=next(p for p in control['current_original_predicate_cases'] if p['block']==31 and p['offset']==132)
    assert pred['original_event_completion_calls'][0]['address']==0x02023840 and pred['original_event_completion_calls'][0]['args'][1]==132
    assert all(p['all_unowned4MiB_actor_models_ABI_input_owner_and_output_canaries_exact'] and p['sole_scratch_restore_recovers_all4MiB_exact'] and p['no_predicate_or_event_flag_forced'] for p in control['current_original_predicate_cases'])
    for p in control['current_original_predicate_cases']:
        for w in p['original_unaligned_operand_read_scratch_writes']:
            assert w['PC']==0x0202A5D8 and w['address']==0x02279600 and w['size']==4 and w['value']==int.from_bytes(bytes.fromhex(p['source_command_hex'])[4:8],'little')
    assert font['candidate_sha256']==doc['current_ROM_sha256'] and len(font['cases'])==len(font['all34_full_QA_reports'])==34 and font['current_original_macro_alignment_calls']==272
    assert font['newly_executed_current_macro_alignment_calls']==32 and font['reused_current_macro_alignment_calls']==240
    assert font['newly_executed_font_cases']==4 and font['reused_unchanged_font_cases']==30
    assert sha(Path(font['manuscript']).read_bytes())==font['manuscript_sha256'] and sha(Path(font['reused_proof']).read_bytes())==font['reused_proof_sha256']
    assert len(font['negative_controls'])==7 and all(n['rejected'] for n in font['negative_controls'])
    assert len(font['review_sheets'])==5 and all(sha(Path(s['path']).read_bytes())==s['sha256'] for s in font['review_sheets'])
    assert doc['all5_review_sheets_viewed_or_identical_to_previously_viewed'] and doc['four_detected_phrase_flow_findings_resolved_without_waiver']
    assert sum(bool(r.get('qa_waivers')) for r in rows)==11 and all(r.get('qa_waivers') in [None,['line-break-count']] for r in rows)
    assert len(doc['phrase_flow_refinements'])==4
    candidate=ledger['current_integrated_candidate'];im=NdsImage.open(candidate['path']);jp=NdsImage.open('work/clean.nds')
    en,jb=[IlnkContainer.parse(i.read_file('/data/SC2.DK4')).blocks for i in [im,jp]];arm=im.read_file('/__arm9__.bin');cases={r['id']:r for r in font['cases']}
    assert sha(im.read_file('/data/SC2.DK4'))==source['current_SC2_sha256'] and sha(jp.read_file('/data/SC2.DK4'))==source['source_SC2_sha256']
    for r in rows:
        sr,cr=r['source_reference'],r['current_reference'];b=r['block'];prefix=bytes.fromhex(r['source_presentation_prefix_hex'])
        assert jb[b][sr['offset']:sr['offset']+sr['bytes']]==bytes.fromhex(r['source_hex']) and en[b][cr['offset']:cr['offset']+cr['bytes']]==bytes.fromhex(r['current_hex'])
        assert jb[b][sr['offset']-5:sr['offset']+1]==en[b][cr['offset']-5:cr['offset']+1]==bytes.fromhex('0040ffff00')+prefix
        result=encode_relocatable_dialogue(bytes.fromhex(r['source_hex']),r['english'],profile_for(arm,en[b]));assert result.encoded.hex()==r['compiled_hex']==cases[r['id']]['encoded_hex'] and result.encoded[:1]==prefix
        assert cases[r['id']]['complete_native_independent216x64_plane_equal'] and cases[r['id']]['all_first_final_internal_glyphs_in_order_and_unique_cells']
    changed=next(r for r in rows if r['id']=='DK4_MES_B31_R0059');assert 'Clifford' not in changed['english'] and 'warning meant' in changed['english']
    earlier=next(b for b in source['blocks'] if b['block']==132);assert earlier['original_event_source']['must_not_be_completed']==[31,32] and source['speaker_catalog']['92']['historical_native_catalog_name']=='Barkeep'
    assert control['actual_B30_B31_B132_IDs']==[] and control['new_emulator_runs']==0
    manifest=read(candidate['manifest']);release=read('work/analysis/lil_Seville_release_v2725/registered_release_verification.json');registry=read('translations/release_stack.json')
    assert sha(Path(candidate['path']).read_bytes())==candidate['sha256']==release['candidate_sha256'] and sha(Path(candidate['patch']).read_bytes())==candidate['patch_sha256']==release['patch_sha256']
    assert Path(release['exact_patch_reconstruction']).read_bytes()==Path(candidate['path']).read_bytes()
    assert sha(Path(candidate['manifest']).read_bytes())==release['manifest_sha256'] and manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes())
    assert manifest['profile']=='all-routes-unified-v2724' and len(manifest['batches'])==496 and len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v1492'
    assert sha(Path('scripts/build_integrated_release.py').read_bytes())==read('work/analysis/lil_Seville_registration_v2723/registration_receipt.json')['builder_sha256']
    inventory=read(ledger['unfinished_editorial_scope_v2741']['path']);assert inventory['incomplete_COMMON_count']==3 and inventory['incomplete_route_source_prose_count']==34
    unit=next(u for u in ledger['coverage_units'] if u['id']=='all-route-scenes');assert unit['reviewed_route_records']==711 and unit['completed_route_records']==677
    assert ledger['raw_source_coverage_revisit']['status']=='open-before-whole-goal-completion' and ledger['next_named_target_reports_source_lead_v2664']['completion_credit_added']==0
    text=Path('docs/editorial_handoff_current.md').read_text(encoding='utf-8');assert text.startswith('# Current editorial handoff - V2741') and '2310 reread /2276 integrated-reconciled /34 pending' in text and 'later older-record technical re-audit remain open' in text
    assert ledger['goal_status']=='active' and not ledger['full_goal_complete']
    ROOT.mkdir(parents=True);save(ROOT/'verified_handoff.json',dict(checkpoint='V2741',ledger=str(lp),ledger_sha256=sha(lp.read_bytes()),handoff_receipt=str(rp),handoff_receipt_sha256=sha(rp.read_bytes()),
        fresh_records=2310,fresh_integrated=2276,fresh_pending=34,source_prose=2313,new_source_prose_reviews=34,new_completed_records=0,proposed_revisions=22,justified_retentions=12,
        completed_records=2276,historical_revised=1592,historical_retained=684,incomplete_COMMON=3,incomplete_route=34,
        source91commands34complete_preambles_32relative_sites320cases_exact=True,B132_warning_attribution_native_source_bound=True,
        native68dispatch_and8current_predicates_scoped_with_source_owned_alignment_scratch=True,current34font_planes272macro_calls_and_full_QA_bound=True,
        four_visual_phrase_findings_resolved_without_orphan_predicate_waiver=True,all5_sheets_viewed_or_identical=True,narrow_line_count_notes=11,
        reference_relocation_representative_registered_release_still_pending=True,actual_B30_B31_B132_IDs=[],new_emulator_runs=0,
        candidate=candidate['path'],candidate_sha256=candidate['sha256'],patch=candidate['patch'],patch_sha256=candidate['patch_sha256'],
        no_ROM_registry_builder_profile_manifest_or_patch_change=True,whole_clean_input_patch_proof_still_bound=True,
        prior_ledger_and_updated_file_chains_verified=True,all_jobs_terminal=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('IndependentV2741audit passes:34new source/prose/native reviews;2310reread/2276integrated/34pending;source/prose2313. V2724ROM/patch unchanged;full goal active.')
