"""Independent completion audit for63 with clean/predecessor/final references."""
from collections import Counter
from copy import deepcopy
from pathlib import Path
import struct
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch import lil_B131_B133_editorial_v1 as owned
from dk4tool.patch.grand_race_menu_release import sha
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/editorial_handoff_verification_v3343b')
CHECKPOINT=Path('work/analysis/lil_B131_B133_completion_v3342b')
REG=Path('work/analysis/lil_B131_B133_registration_v3337b')
if __name__=='__main__':
    assert not ROOT.exists();rp=CHECKPOINT/'completion_receipt.json';receipt=read(rp)
    for k in ['evidence','updated_files']:
        for p,digest in receipt[k].items():assert sha(Path(p).read_bytes())==digest,(k,p)
    lp=Path('translations/editorial_review_current_v1.json');ledger=read(lp);before=read(CHECKPOINT/'editorial_review_current_v1.json.before');prior=read(receipt['prior_verified_handoff'])
    assert sha((CHECKPOINT/'editorial_review_current_v1.json.before').read_bytes())==prior['ledger_sha256'] and sha(Path(prior['handoff_receipt']).read_bytes())==prior['handoff_receipt_sha256']
    for p,digest in read(prior['handoff_receipt'])['updated_files'].items():
        saved=CHECKPOINT/(Path(p).name+'.before');assert sha((saved if saved.exists() else Path(p)).read_bytes())==digest
    fresh=ledger['contextual_story_natural_dialogue_pass_v1871'];oldfresh=before['contextual_story_natural_dialogue_pass_v1871'];final=read(fresh['latest_final_review']);rows=final['records'];selected={historical_key(r) for r in rows}
    assert len(rows)==len(selected)==63 and Counter(r['editorial_decision'] for r in rows)=={'revise':27,'retain-wording':36} and all(all(r['review'].values()) and r['source_meaning'] and r['localization_note'] and r['all_source_native_representative_and_registered_gates_pass'] for r in rows)
    for p,digest in final['evidence'].items():assert sha(Path(p).read_bytes())==digest
    keys={historical_key(r) for r in fresh['record_keys']};integrated={historical_key(r) for r in fresh['integrated_record_keys']};complete={historical_key(r) for g in ledger['completed_editorial_families'] for r in g['records']};oldcomplete={historical_key(r) for g in before['completed_editorial_families'] for r in g['records']}
    assert keys==integrated==complete==oldcomplete|selected and not oldcomplete&selected and keys=={historical_key(r) for r in oldfresh['record_keys']}
    assert len(keys)==len(fresh['record_keys'])==len(fresh['integrated_record_keys'])==4797 and fresh['pending_record_keys']==fresh['pending_contextual_families']==[] and fresh['latest_pending_contextual_family'] is None
    assert (fresh['fresh_pass_records_explicitly_reread'],fresh['fresh_pass_records_integrated'],fresh['fresh_pass_records_pending_native_actual_release'])==(4797,4797,0)
    assert Counter(p for p,k in keys)==ledger['completed_editorial_record_counts_by_file']=={'/COMMON/MESFILE.DK4':1599,'/data/SC2.DK4':2970,'/data/SC0.DK4':117,'/data/SC1.DK4':73,'/data/SC3.DK4':38}
    assert (ledger['records_editorially_completed'],ledger['records_revised_and_integrated'],ledger['retained_wordings_editorially_completed'])==(4797,3169,1628)
    assert ledger['records_with_source_and_prose_pass']==ledger['records_with_source_prose_drafts']==sum(ledger['source_prose_reviewed_counts_by_file'].values())==4800
    assert ledger['reviewed_but_incomplete_COMMON_IDs']==before['reviewed_but_incomplete_COMMON_IDs']==[750,751,752] and not any(ledger['reviewed_but_incomplete_route_record_IDs'].values()) and not any(ledger['active_source_prose_drafts']['route_record_subsets_pending'].values())
    assert ledger['completed_editorial_families'][:-1]==before['completed_editorial_families']
    for k in ['unresolved_graphics_work','older_record_reaudit_after_full_editorial_goal','native_source_universe_inventory_v2701c','source_prose_reviewed_counts_by_file','lil_B131_B133_scope_reconciliation_v3327','Proof_terminology_consistency_lead_v3286','lil_after_B127_next_source_lead_v3310']:assert ledger[k]==before[k],k
    candidate=ledger['current_integrated_candidate'];path=Path(candidate['path']);image=NdsImage.open(path);clean=NdsImage.open('work/clean.nds');release=read('work/analysis/lil_B131_B133_release_v3339/registered_release_verification.json')
    assert sha(path.read_bytes())==candidate['sha256']==release['candidate_sha256']==final['candidate_sha256'] and Path(release['exact_patch_reconstruction']).read_bytes()==path.read_bytes() and release['whole_ROM_reconstruction_byte_exact']
    for p,digest in [(candidate['patch'],candidate['patch_sha256']),(release['manifest'],release['manifest_sha256']),('work/clean.nds',release['clean_input_sha256'])]:assert sha(Path(p).read_bytes())==digest
    manifest,registry=read(candidate['manifest']),read('translations/release_stack.json');assert manifest['profile']==candidate['profile']=='all-routes-unified-v3338' and len(manifest['batches'])==521 and all(manifest['checks'].values()) and len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v1492' and manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes())
    restored=deepcopy(registry);restored['profiles'].pop('all-routes-unified-v3338');assert restored==read(REG/'registry_before_raw.json');registration=read(REG/'registration_receipt.json');assert sha(Path('scripts/build_integrated_release.py').read_bytes())==registration['builder_sha256'] and sha((REG/'registry_before_raw.json').read_bytes())==read(before['current_integrated_candidate']['manifest'])['release_stack_sha256']
    parent=NdsImage.open(before['current_integrated_candidate']['path']);original_parent=NdsImage.open(before['current_integrated_candidate']['path']);recompiled=owned.apply_release(parent,NdsImage.open(manifest['base_rom']));assert recompiled==release['stage'] and parent.read_file(owned.PATH)==image.read_file(owned.PATH)
    assert [p for _,p,data in original_parent.iter_files() if image.read_file(p)!=data]==[owned.PATH]
    for p,data in original_parent.iter_components():assert image.read_file(p)==data
    en,jp,old=[IlnkContainer.parse(im.read_file(owned.PATH)).blocks for im in [image,clean,original_parent]];assert [n for n,(a,b) in enumerate(zip(old,en,strict=True)) if a!=b]==[131,133]
    doc,menu=map(read,[final['manuscript'],final['choices']]);mapping=read(doc['reference_map']);source_rows={r['id']:r for d in [doc,menu] for r in d['records']};assert set(source_rows)=={r['id'] for r in rows}
    assert sum(len(b['mapped_native_commands']) for b in mapping['blocks'])==112 and sum(len(b['relative_skip_fixups']) for b in mapping['blocks'])==24 and sum(len(b['target_native_skip_cases']) for b in mapping['blocks'])==120 and sum(len(b['choice_commands']) for b in mapping['blocks'])==1 and not any(b['actor_style_commands'] for b in mapping['blocks'])
    for r in rows:
        b=r['block'];sr,cr=r['source_reference'],r['integrated_reference'];value=bytes.fromhex(r['integrated_hex']);original=source_rows[r['id']]
        assert jp[b][sr['offset']:sr['offset']+sr['bytes']]==bytes.fromhex(r['source_hex'])==bytes.fromhex(original['source_hex'])
        assert en[b][cr['offset']:cr['offset']+cr['bytes']]==value==bytes.fromhex(r['current_hex']) and en[b][cr['offset']+cr['bytes']]==0 and r['current_reference']==cr and cr['record_index']==en[b][:cr['offset']].count(b'\0')
        predecessor=r['historical_source_prose_predecessor_fields'];pr=predecessor['current_reference'];assert old[b][pr['offset']:pr['offset']+pr['bytes']].hex()==predecessor['current_hex']==original['current_hex'] and r['english']==original['english'] and r['source_meaning']==original['source_meaning']
        if r['kind']=='typed-choice-label':
            at=cr['command_offset'];assert en[b][at:at+2]==b'\0\x21' and cr['text_base']==6 and at+6+struct.unpack_from('<H',en[b],at+2+2*r['option_index'])[0]==cr['offset'] and value==r['english'].encode('ascii')==bytes.fromhex(r['compiled_hex'])
        else:assert en[b][cr['offset']-5:cr['offset']]==bytes.fromhex('0040ffff00') and value[:1]==bytes.fromhex(r['source_hex'])[:1]
        if r['editorial_decision']=='retain-wording':assert (r['english'] if r['kind']=='typed-choice-label' else r['english'].split('}',1)[1])==r['effective_predecessor_paragraph'] and r['fresh_retained_wording_justification']
    assert not any(b['original2000_pause_and_resume_maps'] for b in mapping['blocks'])
    font,padding,sample=map(read,[doc['native_font_proof'],doc['final_padding_proof'],doc['representative_proof']]);assert len(font['cases'])==61 and font['current_original_macro_alignment_calls']==488 and len(font['source_bound_formatter_negatives'])==28 and len(font['source_consumer_negative_controls'])==22 and len(font['review_sheets'])==10
    for s in font['review_sheets']:assert sha(Path(s['path']).read_bytes())==s['sha256']
    assert padding['current_final_padded_macro_alignment_cases']==244 and len(padding['final_target_parity_cases'])==61 and all(c['complete_final_target_native_plane_equals_reviewed_plane'] and c['tail_padding_consumed_without_blank_page_or_lost_glyph'] for c in padding['final_target_parity_cases']) and padding['all1_final2100_object_two_labels_and3_selection_cancel_cases_bound'] and padding['no_source2000_pause_commands'] and padding['all18_final_source00_speech_prefixes_and_nonempty_bodies_preserved']
    assert sum(bool(r.get('qa_waivers')) for r in rows)==19 and all(r.get('qa_waivers') in [None,['line-break-count']] for r in rows)
    fe,control,typed=map(read,[doc['native_FE_font_proof'],doc['relocated_control_proof'],doc['whole_typed_speech_proof']])
    assert len(fe['cases'])==1 and fe['current_original_null_actor_macro_alignment_cases']==8 and not fe['source_leading_vertical_staging_cases']
    assert len(control['relocated_dispatch_cases'])==61 and len(control['relocated_predicate_pairs'])==5 and control['original_event_queries']==[] and control['all18_final_source00_speeches_are_static_Rafael0_without_role_assignment']
    assert len(typed['cases'])==366 and typed['all108_source00_cases_forward_nonempty_body_after_selector_to_original_display']
    zero=[r for r in rows if r.get('source_selector')==0]
    assert len(zero)==18 and all(bytes.fromhex(r['integrated_hex']).count(b'\0')==1 and bytes.fromhex(r['integrated_hex'])[0]==0 and r['english'].startswith('{SPEAKER:00}') for r in zero)
    assert any(c['case']=='shared-encoder-still-rejects-source00' and c['rejected'] for c in font['source_consumer_negative_controls'])
    assert sample['no_open_translation_specific_display_or_control_finding'] and sample['actual_selected_B131_B133_IDs']==[] and sample['new_emulator_runs']==0
    negatives=read(REG/'negative_cases.json');assert len(negatives['cases'])==50 and negatives['all_rejected_before_mutation']
    start=read('work/analysis/lil_B131_B133_startup_v3341/current_B131_B133_scoped_startup_verification.json');assert start['candidate_sha256']==candidate['sha256'] and start['all_current_requested_and_final_framebuffers_equal_V3300'] and start['paired_frame_count']==31 and start['all_five_postload_actor_model_and_captain_checks_equal'] and start['current_Lil_captain2_and_B22_payload_verified'] and start['source_and_disposable_town_donor_unchanged'] and not start['actual_selected_B131_B133_IDs'] and [(r['case'],r['frames']) for r in start['runs']]==[('newgame',4001),('town',17401)]
    for run in start['runs']:
        for k in ['report','old_report','plan','terminal']:assert sha(Path(run[k]).read_bytes())==run[k+'_sha256']
    view=read(CHECKPOINT/'current_six_frame_visual_review.json');assert view['viewed'] and view['sha256']==start['review_sheet_sha256']==sha(Path(view['sheet']).read_bytes())
    inventory=read(ledger['unfinished_editorial_scope_v3342']['path']);oldinventory=read(before['unfinished_editorial_scope_v3327']['path']);assert inventory['incomplete_COMMON_count']==3 and inventory['incomplete_route_source_prose_count']==0
    for k in ['canonical_Maria_SC3_B97_uncredited32_source_lead','Proof_terminology_consistency_lead_v3286','next_clean_only_uncredited_exchange_inventory_v3258']:assert inventory[k]==oldinventory[k],k
    u=next(u for u in ledger['coverage_units'] if u['id']=='all-route-scenes');assert (u['reviewed_route_records'],u['completed_route_records'])==(3198,3198)
    assert ledger['raw_source_coverage_revisit']['status']=='open-before-whole-goal-completion' and ledger['goal_status']=='active' and not ledger['full_goal_complete'] and Path('docs/editorial_handoff_current.md').read_text(encoding='utf-8').startswith('# Current editorial handoff - V3342') and read('work/analysis/lil_B131_B133_build_v3338/build_terminal.json')['returncode']==0
    ROOT.mkdir(parents=True);save(ROOT/'verified_handoff.json',dict(checkpoint='V3342',ledger=str(lp),ledger_sha256=sha(lp.read_bytes()),handoff_receipt=str(rp),handoff_receipt_sha256=sha(rp.read_bytes()),fresh_records=4797,fresh_integrated=4797,fresh_pending=0,source_prose=4800,new_source_prose_reviews=0,new_completed_records=63,revisions=27,justified_retentions=36,completed_records=4797,historical_revised=3169,historical_retained=1628,incomplete_COMMON=3,incomplete_route=0,all63_exact_source_predecessor_effective_integrated_references_verified=True,all61_speech_planes_two_labels_source00_and_all_release_gates_verified=True,all10_native_sheets_and_current6frame_sheet_reviewed=True,narrow_row_count_notes=19,canonical_Maria32_Proof_consistency_B135_B140_and_all_wider_scope_preserved=True,actual_selected_B131_B133_IDs=[],new_current_candidate_emulator_runs=2,paired_current_whole_framebuffers=31,candidate=candidate['path'],candidate_sha256=candidate['sha256'],patch=candidate['patch'],patch_sha256=candidate['patch_sha256'],manifest_batches=521,accepted_layers=114,whole_clean_input_patch_reconstruction_exact=True,prior_ROMs_profiles_translations_and_V1492_promotion_preserved=True,prior_ledger_and_updated_file_chains_verified=True,all_jobs_terminal=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('IndependentV3342 audit passes:63completed,4797reread/integrated,4800source-prose;521batches/114layers/exactpatch/31freshframepairs. Full widergoal remains active.')
