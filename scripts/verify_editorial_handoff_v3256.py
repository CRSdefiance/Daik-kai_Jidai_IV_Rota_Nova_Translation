"""Independent 150-target completion, cumulative release and startup audit."""
from collections import Counter
from copy import deepcopy
from pathlib import Path
import struct
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch import lil_B111_B119_editorial as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/editorial_handoff_verification_v3256')
CHECKPOINT=Path('work/analysis/lil_B111_B119_completion_v3255')
REG=Path('work/analysis/lil_B111_B119_registration_v3250')
if __name__=='__main__':
    assert not ROOT.exists();rp=CHECKPOINT/'completion_receipt.json';receipt=read(rp)
    for group in ['evidence','updated_files']:
        for p,digest in receipt[group].items():assert sha(Path(p).read_bytes())==digest,(group,p)
    lp=Path('translations/editorial_review_current_v1.json');ledger=read(lp);backup=CHECKPOINT/'editorial_review_current_v1.json.before';before=read(backup);oldproof=read(receipt['prior_verified_handoff'])
    assert sha(backup.read_bytes())==oldproof['ledger_sha256'] and sha(Path(oldproof['handoff_receipt']).read_bytes())==oldproof['handoff_receipt_sha256']
    for p,digest in read(oldproof['handoff_receipt'])['updated_files'].items():
        saved=CHECKPOINT/(Path(p).name+'.before');assert sha((saved if saved.exists() else Path(p)).read_bytes())==digest
    fresh,oldfresh=ledger['contextual_story_natural_dialogue_pass_v1871'],before['contextual_story_natural_dialogue_pass_v1871'];final=read(fresh['latest_final_review']);rows=final['records'];selected={historical_key(r) for r in rows}
    assert len(rows)==len(selected)==150 and Counter(r['editorial_decision'] for r in rows)=={'revise':47,'retain-wording':103}
    assert all(all(r['review'].values()) and r['source_meaning'] and r['localization_note'] and r['all_source_native_representative_and_registered_gates_pass'] for r in rows)
    keys={historical_key(r) for r in fresh['record_keys']};integrated={historical_key(r) for r in fresh['integrated_record_keys']};complete={historical_key(r) for g in ledger['completed_editorial_families'] for r in g['records']};oldcomplete={historical_key(r) for g in before['completed_editorial_families'] for r in g['records']}
    assert keys==integrated==complete==oldcomplete|selected and not oldcomplete&selected and keys=={historical_key(r) for r in oldfresh['record_keys']}
    assert len(keys)==len(fresh['record_keys'])==len(fresh['integrated_record_keys'])==4575
    assert fresh['pending_record_keys']==fresh['pending_contextual_families']==[] and fresh['latest_pending_contextual_family'] is None
    assert (fresh['fresh_pass_records_explicitly_reread'],fresh['fresh_pass_records_integrated'],fresh['fresh_pass_records_pending_native_actual_release'])==(4575,4575,0)
    assert Counter(p for p,k in keys)==ledger['completed_editorial_record_counts_by_file']=={'/COMMON/MESFILE.DK4':1599,'/data/SC2.DK4':2748,'/data/SC0.DK4':117,'/data/SC1.DK4':73,'/data/SC3.DK4':38}
    assert (ledger['records_editorially_completed'],ledger['records_revised_and_integrated'],ledger['retained_wordings_editorially_completed'])==(4575,3087,1488)
    assert ledger['records_with_source_and_prose_pass']==ledger['records_with_source_prose_drafts']==sum(ledger['source_prose_reviewed_counts_by_file'].values())==4578
    assert ledger['reviewed_but_incomplete_COMMON_IDs']==before['reviewed_but_incomplete_COMMON_IDs']==[750,751,752]
    assert not any(ledger['reviewed_but_incomplete_route_record_IDs'].values()) and not any(ledger['active_source_prose_drafts']['route_record_subsets_pending'].values())
    assert ledger['completed_editorial_families'][:-1]==before['completed_editorial_families']
    for k in ['unresolved_graphics_work','older_record_reaudit_after_full_editorial_goal','native_source_universe_inventory_v2701c','source_prose_reviewed_counts_by_file','lil_B111_B119_scope_reconciliation_v3237']:assert ledger[k]==before[k],k
    candidate=ledger['current_integrated_candidate'];path=Path(candidate['path']);image=NdsImage.open(path);clean=NdsImage.open('work/clean.nds');release=read('work/analysis/lil_B111_B119_release_v3252b/registered_release_verification.json')
    assert sha(path.read_bytes())==candidate['sha256']==release['candidate_sha256']==final['candidate_sha256']
    assert Path(release['exact_patch_reconstruction']).read_bytes()==path.read_bytes() and release['whole_ROM_reconstruction_byte_exact']
    for p,digest in [(candidate['patch'],candidate['patch_sha256']),(release['manifest'],release['manifest_sha256']),('work/clean.nds',release['clean_input_sha256'])]:assert sha(Path(p).read_bytes())==digest
    manifest,registry=read(candidate['manifest']),read('translations/release_stack.json')
    assert manifest['profile']==candidate['profile']=='all-routes-unified-v3251' and len(manifest['batches'])==517 and all(manifest['checks'].values()) and len(registry['accepted_layers'])==114
    assert registry['latest_promoted_build']['profile']=='all-routes-unified-v1492' and manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes())
    restored=deepcopy(registry);restored['profiles'].pop('all-routes-unified-v3251');assert restored==read(REG/'registry_before_raw.json')
    registration=read(REG/'registration_receipt.json');assert sha(Path('scripts/build_integrated_release.py').read_bytes())==registration['builder_sha256']
    assert sha((REG/'registry_before_raw.json').read_bytes())==read(before['current_integrated_candidate']['manifest'])['release_stack_sha256']
    parent=NdsImage.open(before['current_integrated_candidate']['path']);original_parent=NdsImage.open(before['current_integrated_candidate']['path']);base=NdsImage.open(manifest['base_rom']);result=owned.apply_release(parent,base)
    assert parent.read_file(owned.PATH)==image.read_file(owned.PATH) and result==release['stage']
    assert release['file_changes']==[owned.PATH] and release['component_changes']==[] and release['all517_manifest_batches_and114_accepted_layers_present']
    for p,data in original_parent.iter_components():assert image.read_file(p)==data
    assert [p for _,p,data in original_parent.iter_files() if image.read_file(p)!=data]==[owned.PATH]
    assert sha(image.read_file('/__arm9__.bin'))==before['current_integrated_candidate']['ARM9_sha256']
    en,jp,old=[IlnkContainer.parse(im.read_file(owned.PATH)).blocks for im in [image,clean,original_parent]];assert [n for n,(a,b) in enumerate(zip(old,en,strict=True)) if a!=b]==list(range(111,120))
    doc,voice=map(read,[final['manuscript'],final['actor_styles']]);mapping=read(doc['reference_map'])
    assert sum(len(b['mapped_native_commands']) for b in mapping['blocks'])==305 and sum(len(b['relative_skip_fixups']) for b in mapping['blocks'])==64 and sum(len(b['target_native_skip_cases']) for b in mapping['blocks'])==320
    assert sum(len(b['actor_style_commands']) for b in mapping['blocks'])==6 and not any(b['choice_commands'] for b in mapping['blocks'])
    assert sum(sum(c['word']==0x4000 for c in b['command_map']) for b in mapping['blocks'])==148
    source_rows={r['id']:r for d in [doc,voice] for r in d['records']};assert set(source_rows)=={r['id'] for r in rows};selectors=set()
    for r in rows:
        b=r['block'];sr,cr=r['source_reference'],r['integrated_reference'];value=bytes.fromhex(r['integrated_hex']);original=source_rows[r['id']]
        assert jp[b][sr['offset']:sr['offset']+sr['bytes']]==bytes.fromhex(r['source_hex'])==bytes.fromhex(original['source_hex'])
        assert en[b][cr['offset']:cr['offset']+cr['bytes']]==value==bytes.fromhex(r['current_hex']) and en[b][cr['offset']+cr['bytes']]==0 and r['current_reference']==cr and cr['record_index']==en[b][:cr['offset']].count(b'\0')
        predecessor=r['historical_source_prose_predecessor_fields'];pr=predecessor['current_reference'];assert old[b][pr['offset']:pr['offset']+pr['bytes']].hex()==predecessor['current_hex']==original['current_hex']
        assert r['english']==original['english'] and r['source_meaning']==original['source_meaning']
        if r['kind']=='typed-4100-actor-style-alternative':
            at=cr['command_offset'];prefix=en[b][at+19];selectors.add(prefix)
            assert en[b][at:at+2]==b'\0\x41' and en[b][at+18]==0 and prefix==r['source_selector']==cr['native_selector']
            assert r['compiled_hex']==format(prefix,'02x')+value.hex() and r['compiled_stored_alternative_hex']==value.hex() and r['current_English']==value.decode('ascii')
            assert all(at+20+struct.unpack_from('<H',en[b],at+2+2*i)[0]==cr['offset'] for i in r['style_indices'])
        else:assert en[b][cr['offset']-5:cr['offset']]==bytes.fromhex('0040ffff00') and value[:1]==bytes.fromhex(r['source_hex'])[:1]
        if r['editorial_decision']=='retain-wording':assert r['english'].split('}',1)[1]==r['effective_predecessor_paragraph'] and r['fresh_retained_wording_justification']
    assert selectors=={208,209,214,215,220}
    c=next(b for b in mapping['blocks'] if b['block']==115)['unowned_appended_copy'];a,z=c['old_offset'],c['new_offset'];assert c['bytes']==1886 and en[115][z:z+1886]==old[115][a:a+1886] and sha(en[115][z:z+1886])==c['sha256'] and en[115][z-4:z]==bytes(4)
    copy=read(doc['unowned_copy_proof']);assert copy['all32_unowned_copy_speeches_byte_exact_and_unreachable_from_ordinary_Lil_entry'] and len(copy['original_VM_return_cases'])==2 and copy['conservative_relocated_prefix_graph']['reachable_return0_commands']==[z-4]
    maria=read('work/analysis/lil_B111_B119_source_v3217/canonical_Maria32_deferred_source_lead.json');assert len(maria['records'])==32
    assert all(('/data/SC3.DK4',r['canonical_id']) not in keys and ('/data/SC2.DK4',r['lil_copy_id']) not in keys for r in maria['records'])
    font,padding,sample=map(read,[doc['native_font_proof'],doc['final_padding_proof'],doc['representative_proof']])
    assert len(font['cases'])==150 and font['current_original_macro_alignment_calls']==1200 and font['all150_current_native_planes_and_complete_glyphs_pass']
    assert len(font['source_bound_formatter_negatives'])==28 and len(font['source_consumer_negative_controls'])==43 and len(font['source_English_macro_control_invariants'])==150 and len(font['all20_review_sheets'])==20
    for s in font['all20_review_sheets']:assert sha(Path(s['path']).read_bytes())==s['sha256']
    assert padding['current_final_padded_macro_alignment_cases']==600 and len(padding['final_target_parity_cases'])==150 and all(c['complete_final_target_native_plane_equals_reviewed_plane'] and c['tail_padding_consumed_without_blank_page_or_lost_glyph'] for c in padding['final_target_parity_cases'])
    assert sum(bool(r.get('qa_waivers')) for r in rows)==46 and all(r.get('qa_waivers') in [None,['line-break-count']] for r in rows)
    fe,control=map(read,[doc['native_FE_font_proof'],doc['relocated_control_proof']])
    assert len(fe['cases'])==1 and fe['current_original_null_actor_macro_alignment_cases']==8 and fe['all1_one_native_page_consumes_complete_target'] and fe['no_source_leading_vertical_staging_in_gold_notice']
    assert len(control['relocated_dispatch_cases'])==150 and len(control['current_and_relocated_whole_original4100_command_cases'])==12 and len(control['all207_actor_style_current_and_relocated_pointer_cases']['cases'])==2484 and len(control['relocated_predicate_pairs'])==16
    assert len(control['original_event_queries'])==1 and control['original_event_queries'][0]['event']==319 and control['original_query_r0_r1_r2_and_mapped_incidental_r3_cursor_exact'] and sample['no_open_translation_specific_display_or_control_finding'] and sample['actual_selected_B111_B119_IDs']==[] and sample['new_emulator_runs']==0
    negatives=read(REG/'negative_cases.json');assert len(negatives['cases'])==54 and negatives['all_rejected_before_mutation']
    start=read('work/analysis/lil_B111_B119_startup_v3254/cold_boot_Lil_startup_town_verification.json');assert start['candidate_sha256']==candidate['sha256'] and start['all_current_requested_and_final_framebuffers_equal_V3204'] and start['paired_frame_count']==31 and start['all_five_postload_actor_model_and_captain_checks_equal'] and start['current_Lil_captain2_and_B22_payload_verified'] and start['source_and_disposable_town_donor_unchanged'] and not start['actual_selected_B111_B119_IDs']
    assert [(r['case'],r['frames']) for r in start['runs']]==[('newgame',4001),('town',17401)]
    for run in start['runs']:
        for k in ['report','old_report','plan','terminal']:assert sha(Path(run[k]).read_bytes())==run[k+'_sha256']
    view=read(CHECKPOINT/'current_six_frame_visual_review.json');assert view['viewed'] and view['sha256']==start['review_sheet_sha256']==sha(Path(view['sheet']).read_bytes())
    inventory=read(ledger['unfinished_editorial_scope_v3255']['path']);assert inventory['incomplete_COMMON_count']==3 and inventory['incomplete_route_source_prose_count']==0 and inventory['lil_B111_B119_scope_reconciled_v3255']['canonical_Maria32_pending_uncredited']
    assert inventory['canonical_Maria_SC3_B97_uncredited32_source_lead']==read(before['unfinished_editorial_scope_v3247']['path'])['canonical_Maria_SC3_B97_uncredited32_source_lead']
    u=next(u for u in ledger['coverage_units'] if u['id']=='all-route-scenes');assert (u['reviewed_route_records'],u['completed_route_records'])==(2976,2976)
    assert ledger['raw_source_coverage_revisit']['status']=='open-before-whole-goal-completion' and ledger['next_named_target_reports_source_lead_v2664']['completion_credit_added']==0 and ledger['goal_status']=='active' and not ledger['full_goal_complete']
    assert Path('docs/editorial_handoff_current.md').read_text(encoding='utf-8').startswith('# Current editorial handoff - V3255') and read('work/analysis/lil_B111_B119_build_v3251/build_terminal.json')['returncode']==0
    ROOT.mkdir(parents=True)
    save(ROOT/'verified_handoff.json',dict(checkpoint='V3255',ledger=str(lp),ledger_sha256=sha(lp.read_bytes()),handoff_receipt=str(rp),handoff_receipt_sha256=sha(rp.read_bytes()),fresh_records=4575,fresh_integrated=4575,fresh_pending=0,source_prose=4578,new_source_prose_reviews=0,new_completed_records=150,revisions=47,justified_retentions=103,completed_records=4575,historical_revised=3087,historical_retained=1488,incomplete_COMMON=3,incomplete_route=0,source_native_reference_representative_registered_release_and_current_startup_all_bound=True,all150_exact_clean_predecessor_effective_and_integrated_references_verified=True,all20_native_sheets_and_current6frame_sheet_reviewed=True,narrow_line_count_notes=46,canonical_Maria32_pending_uncredited_and_unowned_copy_byte_exact=True,actual_selected_B111_B119_IDs=[],new_current_candidate_emulator_runs=2,paired_current_whole_framebuffers=31,candidate=candidate['path'],candidate_sha256=candidate['sha256'],patch=candidate['patch'],patch_sha256=candidate['patch_sha256'],manifest_batches=517,accepted_layers=114,whole_clean_input_patch_reconstruction_exact=True,prior_ROMs_profiles_translation_and_V1492_promotion_preserved=True,prior_ledger_and_updated_file_chains_verified=True,all_jobs_terminal=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('IndependentV3255audit passes:150completed inV3251;4575reread/integrated,4578source-prose;517batches/114layers/exactpatch/31currentframepairs. CanonicalMaria32andfullwidergoal stayopen.')
