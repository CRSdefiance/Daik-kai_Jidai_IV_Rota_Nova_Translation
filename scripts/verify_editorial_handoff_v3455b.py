"""Independently audit completed B138 references, repaired registration and actual boots."""
from collections import Counter
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch import lil_B138_editorial_v1 as owned
from dk4tool.patch.grand_race_menu_release import sha
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/editorial_handoff_verification_v3455')
CHECKPOINT=Path('work/analysis/lil_B138_completion_v3454')
REG=Path('work/analysis/lil_B138_registration_v3449')
if __name__=='__main__':
    assert not ROOT.exists();rp=CHECKPOINT/'completion_receipt.json';receipt=read(rp)
    for k in ['evidence','updated_files']:
        for p,digest in receipt[k].items():assert sha(Path(p).read_bytes())==digest,(k,p)
    lp=Path('translations/editorial_review_current_v1.json');ledger=read(lp);before=read(CHECKPOINT/'editorial_review_current_v1.json.before');prior=read(receipt['prior_verified_handoff'])
    assert sha((CHECKPOINT/'editorial_review_current_v1.json.before').read_bytes())==prior['ledger_sha256']
    assert sha(Path(prior['handoff_receipt']).read_bytes())==prior['handoff_receipt_sha256']
    for p,digest in read(prior['handoff_receipt'])['updated_files'].items():
        saved=CHECKPOINT/(Path(p).name+'.before');assert sha((saved if saved.exists() else Path(p)).read_bytes())==digest
    fresh=ledger['contextual_story_natural_dialogue_pass_v1871'];oldfresh=before['contextual_story_natural_dialogue_pass_v1871'];final=read(fresh['latest_final_review']);rows=final['records'];selected={historical_key(r) for r in rows}
    assert len(rows)==len(selected)==44 and Counter(r['editorial_decision'] for r in rows)=={'revise':16,'retain-wording':28}
    assert all(all(r['review'].values()) and r['source_meaning'] and r['localization_note'] and r['all_source_native_representative_and_registered_gates_pass'] for r in rows)
    for p,digest in final['evidence'].items():assert sha(Path(p).read_bytes())==digest
    keys={historical_key(r) for r in fresh['record_keys']};integrated={historical_key(r) for r in fresh['integrated_record_keys']};complete={historical_key(r) for g in ledger['completed_editorial_families'] for r in g['records']};oldcomplete={historical_key(r) for g in before['completed_editorial_families'] for r in g['records']}
    assert keys==integrated==complete==oldcomplete|selected and not oldcomplete&selected
    assert keys=={historical_key(r) for r in oldfresh['record_keys']} and selected=={historical_key(r) for r in oldfresh['pending_record_keys']}
    assert len(keys)==len(fresh['record_keys'])==len(fresh['integrated_record_keys'])==4924 and fresh['pending_record_keys']==fresh['pending_contextual_families']==[] and fresh['latest_pending_contextual_family'] is None
    assert (fresh['fresh_pass_records_explicitly_reread'],fresh['fresh_pass_records_integrated'],fresh['fresh_pass_records_pending_native_actual_release'])==(4924,4924,0)
    assert Counter(p for p,k in keys)==ledger['completed_editorial_record_counts_by_file']=={'/COMMON/MESFILE.DK4':1599,'/data/SC2.DK4':3097,'/data/SC0.DK4':117,'/data/SC1.DK4':73,'/data/SC3.DK4':38}
    assert (ledger['records_editorially_completed'],ledger['records_revised_and_integrated'],ledger['retained_wordings_editorially_completed'])==(4924,3223,1701)
    assert ledger['records_with_source_and_prose_pass']==ledger['records_with_source_prose_drafts']==sum(ledger['source_prose_reviewed_counts_by_file'].values())==4927
    assert ledger['reviewed_but_incomplete_COMMON_IDs']==before['reviewed_but_incomplete_COMMON_IDs']==[750,751,752]
    assert not any(ledger['reviewed_but_incomplete_route_record_IDs'].values()) and not any(ledger['active_source_prose_drafts']['route_record_subsets_pending'].values())
    assert ledger['completed_editorial_families'][:-1]==before['completed_editorial_families']
    for k in ['unresolved_graphics_work','older_record_reaudit_after_full_editorial_goal','native_source_universe_inventory_v2701c','source_prose_reviewed_counts_by_file','lil_B138_scope_reconciliation_v3439','Proof_terminology_consistency_lead_v3286','lil_after_B127_next_source_lead_v3310','lil_B137_registered_hook_repair_v3415']:assert ledger[k]==before[k],k
    candidate=ledger['current_integrated_candidate'];path=Path(candidate['path']);image=NdsImage.open(path);clean=NdsImage.open('work/clean.nds');release=read('work/analysis/lil_B138_release_v3451/registered_release_verification.json')
    assert sha(path.read_bytes())==candidate['sha256']==release['candidate_sha256']==final['candidate_sha256']
    assert Path(release['exact_patch_reconstruction']).read_bytes()==path.read_bytes() and release['whole_ROM_reconstruction_byte_exact']
    for p,digest in [(candidate['patch'],candidate['patch_sha256']),(release['manifest'],release['manifest_sha256']),('work/clean.nds',release['clean_input_sha256'])]:assert sha(Path(p).read_bytes())==digest
    manifest,registry=read(candidate['manifest']),read('translations/release_stack.json')
    assert manifest['profile']==candidate['profile']=='all-routes-unified-v3450' and len(manifest['batches'])==524 and all(manifest['checks'].values())
    assert len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v1492'
    assert manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes())
    restored=deepcopy(registry);profile=restored['profiles'].pop('all-routes-unified-v3450');assert restored==read(REG/'registry_before_raw.json')
    assert profile['lil_B138_editorial']==owned.CONFIG and 'lil_B138_editorial_v2' not in profile
    parentprofile=deepcopy(restored['profiles']['all-routes-unified-v3416']);newprofile=deepcopy(profile)
    for p in [parentprofile,newprofile]:p.pop('description',None);p.pop('note',None)
    newprofile.pop('lil_B138_editorial');assert parentprofile==newprofile
    registration=read(REG/'registration_receipt.json');assert sha(Path('scripts/build_integrated_release.py').read_bytes())==registration['builder_sha256']
    assert sha(Path('translations/release_stack.json').read_bytes())==registration['release_stack_sha256']
    assert sha(Path(registration['compiler']).read_bytes())==registration['compiler_sha256'] and sha(Path(owned.CONFIG).read_bytes())==registration['config_sha256']
    # Adding experimental profiles does not retroactively change V3416's registry hash.
    assert read(before['current_integrated_candidate']['manifest'])['release_stack_sha256']==sha(Path('work/analysis/lil_B138_registration_v3449/registry_before_raw.json').read_bytes())
    failed=read('work/analysis/lil_B137_build_v3409/build_terminal.json');assert failed['terminal'] and failed['returncode']==1 and not failed['candidate_exists'] and not Path(failed['candidate']).exists()
    assert 'all-routes-unified-v3409' in restored['profiles'] and registration['stage_import_module']==owned.__name__
    parent=NdsImage.open(before['current_integrated_candidate']['path']);original_parent=NdsImage.open(before['current_integrated_candidate']['path'])
    recompiled=owned.apply_release(parent,NdsImage.open(manifest['base_rom']));assert recompiled==release['stage'] and parent.read_file(owned.PATH)==image.read_file(owned.PATH)
    assert manifest['relocations'][owned.PATH]['lil_B138_editorial']['proof']==recompiled
    assert [p for _,p,data in original_parent.iter_files() if image.read_file(p)!=data]==[owned.PATH]
    for p,data in original_parent.iter_components():assert image.read_file(p)==data
    en,jp,old=[IlnkContainer.parse(im.read_file(owned.PATH)).blocks for im in [image,clean,original_parent]]
    assert [n for n,(a,b) in enumerate(zip(old,en,strict=True)) if a!=b]==[138] and (len(old[138]),len(en[138]))==(2756,2356)
    doc=read(final['manuscript']);mapping=read(doc['reference_map']);source_rows={r['id']:r for r in doc['records']};assert set(source_rows)=={r['id'] for r in rows}
    assert sum(len(b['mapped_native_commands']) for b in mapping['blocks'])==111 and sum(len(b['relative_skip_fixups']) for b in mapping['blocks'])==45
    assert sum(len(b['target_native_skip_cases']) for b in mapping['blocks'])==225 and not any(b['choice_commands'] or b['actor_style_commands'] or b['original2000_pause_and_resume_maps'] for b in mapping['blocks'])
    for r in rows:
        b=r['block'];sr,cr=r['source_reference'],r['integrated_reference'];value=bytes.fromhex(r['integrated_hex']);original=source_rows[r['id']]
        assert jp[b][sr['offset']:sr['offset']+sr['bytes']]==bytes.fromhex(r['source_hex'])==bytes.fromhex(original['source_hex'])
        assert en[b][cr['offset']:cr['offset']+cr['bytes']]==value==bytes.fromhex(r['current_hex']) and en[b][cr['offset']+cr['bytes']]==0
        assert r['current_reference']==cr and cr['record_index']==en[b][:cr['offset']].count(b'\0') and en[b][cr['offset']-5:cr['offset']]==bytes.fromhex('0040ffff00') and value[:1]==bytes.fromhex(r['source_hex'])[:1]
        predecessor=r['historical_source_prose_predecessor_fields'];pr=predecessor['current_reference']
        assert old[b][pr['offset']:pr['offset']+pr['bytes']].hex()==predecessor['current_hex']==original['current_hex']
        assert r['english']==original['english'] and r['source_meaning']==original['source_meaning']
        assert r['source_selector'] in {2,14,20,21,22,23,92} and r['kind']=='progressive' and b'\0' not in value
        if r['editorial_decision']=='retain-wording':assert r['english'].split('}',1)[1]==r['effective_predecessor_paragraph'] and r['fresh_retained_wording_justification']
    font,padding,sample=map(read,[doc['native_font_proof'],doc['final_padding_proof'],doc['representative_proof']])
    assert len(font['cases'])==44 and font['current_original_macro_alignment_calls']==352 and len(font['source_bound_formatter_negatives'])==14 and len(font['source_consumer_negative_controls'])==23 and len(font['review_sheets'])==6
    for s in font['review_sheets']:assert sha(Path(s['path']).read_bytes())==s['sha256']
    assert padding['current_final_padded_macro_alignment_cases']==176 and len(padding['final_target_parity_cases'])==44
    assert all(c['complete_final_target_native_plane_equals_reviewed_plane'] and c['tail_padding_consumed_without_blank_page_or_lost_glyph'] for c in padding['final_target_parity_cases'])
    assert padding['no2100_objects_in_source_scope'] and padding['no_source2000_pause_commands'] and padding['all44_final_speech_prefixes_and_nonempty_bodies_preserved']
    for ident in ['DK4_MES_B138_R0078','DK4_MES_B138_R0253']:
        question=next(r for r in rows if r['id']==ident);assert question['integrated_hex']=='023f20' and question['historical_source_prose_predecessor_fields']['current_hex']=='028148' and question['editorial_decision']=='retain-wording'
        proof=next(c for c in padding['final_target_parity_cases'] if c['id']==ident);assert [(e['code'],e['x'],e['y']) for e in proof['complete_native_glyph_events'] if e['code']!=32]==[(63,0,0)]
    assert sum(bool(r.get('qa_waivers')) for r in rows)==21 and all(r.get('qa_waivers') in [None,['line-break-count']] for r in rows)
    control=read(doc['relocated_control_proof']);assert len(control['relocated_dispatch_cases'])==44 and len(control['relocated_predicate_pairs'])==11 and len(control['original_event_queries'])==1 and control['original_event_queries'][0]['event']==137 and control['all_seven_static_speaker_selectors_preserved_without_role_assignment']
    assert sample['no_open_translation_specific_display_or_control_finding'] and sample['actual_selected_B138_IDs']==[] and sample['new_emulator_runs']==0 and sample['all44_final_planes176_macros_static_dispatches10_predicates_and1_query_bound']
    assert control['source_predicate_result_constants']['0080ffff200301a1']==2 and control['portable_source_owned_adapters']['predicate'].startswith('SCOPED_RESULTS=')
    for p in control['relocated_predicate_pairs']:
        left,right=p['cases'];assert left['native_result']==right['native_result'] and left['source_command_hex']==right['source_command_hex']
        if left['source_command_hex']=='0080ffff200301a1':assert left['native_result']==[2,2,0,0,0,0]
    assert mapping['all10_predicates_and1_query_current_relocated_results_and_source_operands_equal'] and len(mapping['original_event_queries'])==1 and mapping['original_event_queries'][0]['event']==137
    negatives=read(REG/'negative_cases.json');assert len(negatives['cases'])==35 and negatives['all_rejected_before_mutation'] and all(c['rejected_before_mutation'] for c in negatives['cases'])
    start=read('work/analysis/lil_B138_startup_v3453/cold_boot_Lil_startup_town_verification.json')
    assert start['candidate_sha256']==candidate['sha256'] and start['all_current_requested_and_final_framebuffers_equal_V3416'] and start['paired_frame_count']==31
    assert start['all_five_postload_actor_model_and_captain_checks_equal'] and start['current_Lil_captain2_and_B22_payload_verified'] and start['source_and_disposable_town_donor_unchanged'] and not start['actual_selected_B138_IDs']
    assert [(r['case'],r['frames']) for r in start['runs']]==[('newgame',4001),('town',17401)]
    for run in start['runs']:
        for k in ['report','old_report','plan','terminal']:assert sha(Path(run[k]).read_bytes())==run[k+'_sha256']
    view=read(CHECKPOINT/'current_six_frame_visual_review.json');assert view['viewed'] and view['sha256']==start['review_sheet_sha256']==sha(Path(view['sheet']).read_bytes())
    inventory=read(ledger['unfinished_editorial_scope_v3454']['path']);oldinventory=read(before['unfinished_editorial_scope_v3447']['path']);assert inventory['incomplete_COMMON_count']==3 and inventory['incomplete_route_source_prose_count']==0
    for k in ['canonical_Maria_SC3_B97_uncredited32_source_lead','Proof_terminology_consistency_lead_v3286','next_clean_only_uncredited_exchange_inventory_v3258','B137_registered_hook_repair_v3415']:assert inventory[k]==oldinventory[k],k
    u=next(u for u in ledger['coverage_units'] if u['id']=='all-route-scenes');assert (u['reviewed_route_records'],u['completed_route_records'])==(3325,3325)
    assert ledger['raw_source_coverage_revisit']['status']=='open-before-whole-goal-completion' and ledger['goal_status']=='active' and not ledger['full_goal_complete']
    assert Path('docs/editorial_handoff_current.md').read_text(encoding='utf-8').startswith('# Current editorial handoff - V3454') and read('work/analysis/lil_B138_build_v3450/build_terminal.json')['returncode']==0
    ROOT.mkdir(parents=True);save(ROOT/'verified_handoff.json',dict(checkpoint='V3454',ledger=str(lp),ledger_sha256=sha(lp.read_bytes()),handoff_receipt=str(rp),handoff_receipt_sha256=sha(rp.read_bytes()),fresh_records=4924,fresh_integrated=4924,fresh_pending=0,source_prose=4927,new_source_prose_reviews=0,new_completed_records=44,revisions=16,justified_retentions=28,completed_records=4924,historical_revised=3223,historical_retained=1701,incomplete_COMMON=3,incomplete_route=0,all44_exact_source_predecessor_effective_integrated_references_verified=True,all44_speech_planes_and_all_release_gates_verified=True,two_wordless_questions_complete_and_raw_result2_query_preserved=True,all6_native_sheets_and_current6frame_sheet_reviewed=True,narrow_row_count_notes=21,canonical_Maria32_Proof_consistency_B139_B140_and_all_wider_scope_preserved=True,failed_V3409_and_separate_validated_v2_hook_preserved=True,actual_selected_B138_IDs=[],new_current_candidate_emulator_runs=2,paired_current_whole_framebuffers=31,candidate=candidate['path'],candidate_sha256=candidate['sha256'],patch=candidate['patch'],patch_sha256=candidate['patch_sha256'],manifest_batches=524,accepted_layers=114,whole_clean_input_patch_reconstruction_exact=True,prior_ROMs_profiles_translations_and_V1492_promotion_preserved=True,prior_ledger_and_updated_file_chains_verified=True,all_jobs_terminal=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('Independent V3454 audit passes:44 completed;4924 reread/integrated;4927 source-prose;524 batches/114 layers/exact patch/31 fresh frame pairs. Full goal active.')
