"""Independent20-object source/prose pending checkpoint and release audit."""
from pathlib import Path
from collections import Counter
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/editorial_handoff_verification_v2711')
CHECKPOINT=Path('work/analysis/lil_Seville_checkpoint_v2710')
if __name__=='__main__':
    assert not ROOT.exists();rp=CHECKPOINT/'checkpoint_receipt.json';receipt=read(rp)
    for group in ['evidence','updated_files']:
        for p,digest in receipt[group].items():assert sha(Path(p).read_bytes())==digest,(group,p)
    lp=Path('translations/editorial_review_current_v1.json');ledger=read(lp);beforepath=CHECKPOINT/'editorial_review_current_v1.json.before';before=read(beforepath)
    priorpath=Path('work/analysis/editorial_handoff_verification_v2703/verified_handoff.json');prior=read(priorpath);assert sha(beforepath.read_bytes())==prior['ledger_sha256']
    for p,digest in read(prior['handoff_receipt'])['updated_files'].items():
        backup=CHECKPOINT/(Path(p).name+'.before');assert sha((backup if backup.exists() else Path(p)).read_bytes())==digest,p
    fresh=ledger['contextual_story_natural_dialogue_pass_v1871'];oldfresh=before['contextual_story_natural_dialogue_pass_v1871']
    doc=read(fresh['latest_contextual_manuscript']);choice=read(fresh['latest_contextual_choice_draft']);rows=doc['records']+choice['records'];selected={('/data/SC2.DK4',r['id']) for r in rows};assert len(selected)==20
    keys={(r['file_path'],r['id']) for r in fresh['record_keys']};oldkeys={(r['file_path'],r['id']) for r in oldfresh['record_keys']}
    integrated={(r['file_path'],r['id']) for r in fresh['integrated_record_keys']};pending={(r['file_path'],r['id']) for r in fresh['pending_record_keys']}
    completed={historical_key(r) for g in ledger['completed_editorial_families'] for r in g['records']}
    assert keys-oldkeys==selected and oldkeys<=keys and integrated==completed==oldkeys and pending==selected and not integrated&pending and keys==integrated|pending
    assert len(keys)==len(fresh['record_keys'])==len(fresh['record_IDs'])==2276 and len(integrated)==2256 and len(pending)==20
    assert (fresh['fresh_pass_records_explicitly_reread'],fresh['fresh_pass_records_integrated'],fresh['fresh_pass_records_pending_native_actual_release'])==(2276,2256,20)
    assert Counter(path for path,key in keys)=={'/COMMON/MESFILE.DK4':1599,'/data/SC2.DK4':449,'/data/SC0.DK4':117,'/data/SC1.DK4':73,'/data/SC3.DK4':38}
    assert len(fresh['pending_contextual_families'])==1 and fresh['pending_contextual_families'][0]['records']==20 and fresh['latest_pending_contextual_family']=='Lil-Seville-Valdes-B28-B29-20-source-prose'
    assert ledger['records_with_source_and_prose_pass']==ledger['records_with_source_prose_drafts']==sum(ledger['source_prose_reviewed_counts_by_file'].values())==2279
    assert ledger['source_prose_reviewed_counts_by_file']=={**before['source_prose_reviewed_counts_by_file'],'/data/SC2.DK4':449}
    assert ledger['reviewed_but_incomplete_COMMON_IDs']==before['reviewed_but_incomplete_COMMON_IDs']==[750,751,752]
    assert set(ledger['reviewed_but_incomplete_route_record_IDs']['/data/SC2.DK4'])=={key for path,key in selected} and not any(v for p,v in ledger['reviewed_but_incomplete_route_record_IDs'].items() if p!='/data/SC2.DK4')
    for key in ['completed_editorial_families','records_editorially_completed','records_revised_and_integrated','retained_wordings_editorially_completed','completed_editorial_record_counts_by_file','current_integrated_candidate','unresolved_graphics_work','older_record_reaudit_after_full_editorial_goal','native_source_universe_inventory_v2701c']:
        assert ledger[key]==before[key],key
    assert (ledger['records_editorially_completed'],ledger['records_revised_and_integrated'],ledger['retained_wordings_editorially_completed'])==(2256,1575,681)
    assert Counter(r['editorial_decision'] for r in rows)=={'revise':17,'retain-wording':3}
    assert doc['translation_policy']==choice['translation_policy']=='natural-dialogue-v2' and doc['target_locale']==choice['target_locale']=='en-US'
    assert all(all(r['review'][g] for g in ['source','context','localization','naturalness']) and not r['review']['formatting'] and r['source_meaning'] and r['localization_note'] for r in rows)
    assert all('{LB' not in r['english'] and '{ALIGN' not in r['english'] and '{PAD}' not in r['english'] for r in rows)
    for r in rows:
        if r['editorial_decision']=='retain-wording':assert r['fresh_retained_wording_justification'] and r['english'].split('}',1)[1]==' '.join(r['current_English'].split())
    source=read(doc['source_context']);controls=read(doc['control_contract']);branch=read(doc['branch_proof']);body=read('work/analysis/lil_Seville_body_probe_v2708b/body_only_layout_and_native_fonts.json')
    assert source['total_editorial_objects']==20 and (source['progressive_speeches'],source['system_FE_panels'],source['typed_choice_labels'])==(17,1,2)
    assert len(source['records'])==18 and len(source['typed_choice_records'])==2 and sum(len(b['all_clean_native_commands']) for b in source['blocks'])==69
    assert len(branch['operands_requiring_adjustment_when_resizing'])==28 and len(branch['cases'])==280 and all(c['target_is_independently_mapped_native_boundary'] and c['source_block_owner_input_result_guards_and_ABI_exact'] for c in branch['cases'])
    assert len(controls['all36_source_current_text_contexts_dispatch_to_correct_actor_or_FE'])==36 and controls['actual_Janus4_Valdes31_or_selected_Seville_IDs']==[] and controls['new_emulator_runs']==0
    assert controls['ordinary_selector_on_FE_would_return208_but_original_dispatch_selects_FE_first'] and controls['ordinary_native_actor_selectors']=={'2':2,'4':4,'16':16,'20':20,'31':31}
    assert all(c['whole4MiB_and_input_guards_and_full_saved_register_ABI_exact'] and c['not_current_whole_display_or_live_Seville_activation'] for c in controls['all36_source_current_text_contexts_dispatch_to_correct_actor_or_FE'])
    assert body['manuscript_sha256']==sha(Path(fresh['latest_contextual_manuscript']).read_bytes()) and len(body['records'])==18 and body['failures']==[] and body['actual_progressive_planes']==17
    assert body['host_default_macro_substitution_not_native_macro_execution'] and body['FE_paper_typed_choices_current_native_macro_contexts_reference_maps_and_release_still_pending']
    assert len(body['review_sheets'])==3 and all(sha(Path(s['path']).read_bytes())==s['sha256'] for s in body['review_sheets'])
    watch=ledger['formatting_watchlist']['lil_Seville_v2710'];assert watch['all_three_body_sheets_viewed'] and watch['FE_panel_and_typed_choice_native_approval_pending'] and watch['current_macro_alignment_execution_pending'] and watch['reference_map_pending']
    notes=read('work/analysis/lil_Seville_layout_notes_v2709/line_count_waivers.json');assert len(notes['waivers'])==8 and notes['English_and_controls_unchanged']
    assert sum(bool(r.get('qa_waivers')) for r in doc['records'])==8 and all(r.get('qa_waivers') in [None,['line-break-count']] for r in doc['records'])
    original_doc=read(doc['previous_manuscript']);assert [r['english'] for r in original_doc['records']]==[r['english'] for r in doc['records']]
    candidate=ledger['current_integrated_candidate'];rom=NdsImage.open(candidate['path']);clean=NdsImage.open('work/clean.nds');jp=IlnkContainer.parse(clean.read_file('/data/SC2.DK4')).blocks;en=IlnkContainer.parse(rom.read_file('/data/SC2.DK4')).blocks
    assert sha(rom.read_file('/data/SC2.DK4'))==source['current_SC2_sha256'] and sha(clean.read_file('/data/SC2.DK4'))==source['source_SC2_sha256']
    for r in rows:
        sr,cr=r['source_reference'],r['current_reference'];block=r['block'];assert jp[block][sr['offset']:sr['offset']+sr['bytes']]==bytes.fromhex(r['source_hex']) and en[block][cr['offset']:cr['offset']+cr['bytes']]==bytes.fromhex(r['current_hex'])
        if r['kind']!='typed-choice-label':
            prefix=bytes.fromhex(r['source_presentation_prefix_hex']);assert bytes.fromhex(r['source_complete_preamble_hex'])==bytes.fromhex('0040ffff00')+prefix
            assert jp[block][sr['header_offset']:sr['offset']+1]==en[block][cr['header_offset']:cr['offset']+1]==bytes.fromhex(r['source_complete_preamble_hex'])
    silent=next(r for r in doc['records'] if r['id']=='DK4_MES_B28_R0065');assert silent['source_Japanese']=='…！！' and silent['english']=='{SPEAKER:02}...!!' and silent['source_hex']==silent['current_hex']
    assert 'and live' in next(r for r in doc['records'] if r['id']=='DK4_MES_B28_R0069')['current_English'] and all('and live' not in r['english'] for r in rows)
    assert [r['option_index'] for r in choice['records']]==[0,1] and len({r['command_offset'] for r in choice['records']})==1
    release=read('work/analysis/surrender_advice_release_v2675/registered_release_verification.json');manifestpath=Path(candidate['path']).with_suffix('.manifest.json');manifest=read(manifestpath);registry=read('translations/release_stack.json')
    assert sha(Path(candidate['path']).read_bytes())==candidate['sha256']==receipt['candidate_sha256']==release['candidate_sha256']
    assert sha(Path(candidate['patch']).read_bytes())==candidate['patch_sha256']==release['patch_sha256'] and release['whole_ROM_reconstruction_byte_exact']
    assert sha(Path(release['exact_patch_reconstruction']).read_bytes())==release['candidate_sha256'] and sha(Path('work/clean.nds').read_bytes())==release['clean_input_sha256']
    assert sha(manifestpath.read_bytes())==release['manifest_sha256'] and sha(Path('translations/release_stack.json').read_bytes())==manifest['release_stack_sha256'] and len(manifest['batches'])==494 and len(registry['accepted_layers'])==114
    assert registry['latest_promoted_build']['profile']=='all-routes-unified-v1492' and sha(Path(manifest['base_rom']).read_bytes())==manifest['base_sha256']
    assert sha(Path('scripts/build_integrated_release.py').read_bytes())==read('work/analysis/surrender_advice_registration_v2673/registration_receipt.json')['builder_sha256']
    inventory=read(ledger['unfinished_editorial_scope_v2710']['path']);assert inventory['incomplete_COMMON_count']==3 and inventory['incomplete_route_source_prose_count']==20 and set(inventory['incomplete_route_source_prose_groups'][0]['record_IDs'])=={key for path,key in selected}
    assert next(u for u in ledger['coverage_units'] if u['id']=='all-route-scenes')['reviewed_route_records']==677 and next(u for u in ledger['coverage_units'] if u['id']=='all-route-scenes')['completed_route_records']==657
    assert ledger['raw_source_coverage_revisit']['status']=='open-before-whole-goal-completion' and ledger['next_named_target_reports_source_lead_v2664']['completion_credit_added']==0
    handoff=Path('docs/editorial_handoff_current.md').read_text(encoding='utf-8');assert handoff.startswith('# Current editorial handoff - V2710') and '2276 reread /2256 integrated-reconciled /20pending' in handoff and 'later older-record technical re-audit remain open' in handoff
    assert ledger['goal_status']=='active' and not ledger['full_goal_complete']
    ROOT.mkdir(parents=True);save(ROOT/'verified_handoff.json',dict(checkpoint='V2710',ledger=str(lp),ledger_sha256=sha(lp.read_bytes()),handoff_receipt=str(rp),handoff_receipt_sha256=sha(rp.read_bytes()),fresh_records=2276,fresh_integrated=2256,fresh_pending=20,source_prose=2279,new_source_prose_reviews=20,new_completed_records=0,proposed_revisions=17,justified_retentions=3,
        completed_records=2256,historical_revised=1575,historical_retained=681,incomplete_COMMON=3,incomplete_route=20,source69commands_18headers_2typedlabels_exact=True,omitted_punctuation_only_native_speech_accounted_for=True,source_branch_cases=280,source_dispatch_contexts=36,body_layouts=18,progressive_body_font_planes=17,all_three_body_sheets_viewed=True,narrow_line_count_waivers=8,
        current_whole_macro_FE_choice_native_reference_representative_and_registered_release_still_pending=True,actual_Seville_IDs=[],new_emulator_runs=0,candidate=candidate['path'],candidate_sha256=candidate['sha256'],patch=candidate['patch'],patch_sha256=candidate['patch_sha256'],no_ROM_registry_builder_profile_manifest_or_patch_change=True,whole_clean_input_patch_proof_still_bound=True,prior_ledger_and_updated_file_chains_verified=True,all_jobs_terminal=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('IndependentV2710audit passes:20new source/prose objects;2276reread/2256reconciled/20pending.69commands/280branch/36dispatch and18body/17font proofs scoped honestly.2674ROM/patch unchanged;full goal active.')
