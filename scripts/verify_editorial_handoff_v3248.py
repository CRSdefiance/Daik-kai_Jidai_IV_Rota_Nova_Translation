"""Independent readiness audit with exact source/current/target and copy checks."""
from collections import Counter
from pathlib import Path
import struct
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/editorial_handoff_verification_v3248')
CHECKPOINT=Path('work/analysis/lil_B111_B119_ready_checkpoint_v3247')
if __name__=='__main__':
    assert not ROOT.exists();rp=CHECKPOINT/'checkpoint_receipt.json';receipt=read(rp)
    for group in ['evidence','updated_files']:
        for p,digest in receipt[group].items():assert sha(Path(p).read_bytes())==digest,(group,p)
    lp=Path('translations/editorial_review_current_v1.json');ledger=read(lp);before=read(CHECKPOINT/'editorial_review_current_v1.json.before');prior=read(receipt['prior_verified_handoff'])
    assert sha((CHECKPOINT/'editorial_review_current_v1.json.before').read_bytes())==prior['ledger_sha256']
    assert sha(Path(prior['handoff_receipt']).read_bytes())==prior['handoff_receipt_sha256']
    for p,digest in read(prior['handoff_receipt'])['updated_files'].items():
        saved=CHECKPOINT/(Path(p).name+'.before');assert sha((saved if saved.exists() else Path(p)).read_bytes())==digest
    for k in ['completed_editorial_families','records_editorially_completed','records_revised_and_integrated','retained_wordings_editorially_completed','completed_editorial_record_counts_by_file','current_integrated_candidate','reviewed_but_incomplete_COMMON_IDs','reviewed_but_incomplete_route_record_IDs','unresolved_graphics_work','older_record_reaudit_after_full_editorial_goal','records_with_source_and_prose_pass','records_with_source_prose_drafts','source_prose_reviewed_counts_by_file','native_source_universe_inventory_v2701c','lil_B111_B119_scope_reconciliation_v3237']:
        assert ledger[k]==before[k],k
    fresh,old=ledger['contextual_story_natural_dialogue_pass_v1871'],before['contextual_story_natural_dialogue_pass_v1871']
    for k in ['record_keys','record_IDs','integrated_record_keys','pending_record_keys','fresh_pass_records_explicitly_reread','fresh_pass_records_integrated','fresh_pass_records_pending_native_actual_release']:assert fresh[k]==old[k],k
    assert (fresh['fresh_pass_records_explicitly_reread'],fresh['fresh_pass_records_integrated'],fresh['fresh_pass_records_pending_native_actual_release'])==(4575,4425,150)
    assert ledger['records_with_source_and_prose_pass']==4578
    paths=[fresh['latest_contextual_manuscript'],fresh['latest_contextual_actor_style_draft']];doc,voice=map(read,paths);rows=doc['records']+voice['records']
    assert len(rows)==150 and Counter(r['editorial_decision'] for r in rows)=={'revise':47,'retain-wording':103}
    for d in [doc,voice]:
        validate_natural_dialogue_batch(d);previous=read(d['previous_manuscript']);assert sha(Path(d['previous_manuscript']).read_bytes())==d['previous_manuscript_sha256']
        for r,p in zip(d['records'],previous['records'],strict=True):
            for k in ['id','english','source_hex','current_hex','source_reference','current_reference','source_meaning','localization_note','review','editorial_decision']:assert r[k]==p[k],(r['id'],k)
    approval=read('work/analysis/lil_B111_B119_reference_approval_v3246/approval_receipt.json')
    for p,digest in approval['hashes'].items():assert sha(Path(p).read_bytes())==digest
    mapping=read(doc['reference_map']);assert sha(Path(doc['reference_map']).read_bytes())==doc['reference_map_sha256']
    for k in ['external_references_complete','representative_shared_rules_approved','all305_physical_nested_command_boundaries_and64_relative_sites_verified','all320_relocated_relative_skip_cases_preserve_original_targets','all15_relocated_predicate_pairs_and_one_event319_query_preserve_source_operands_results_and_mapped_cursor','all6_actor_style_objects48_slots34_strings_aliases_and_actual5_virtual_prefixes_verified','all116_active_speech_targets_and148_physical_speeches_preserved','unowned1886byte_copy_preserved_and_original_VM_return_before_copy_verified','canonical_Maria_SC3_B97_32_targets_still_pending_uncredited','no_player_choice_objects']:assert mapping[k],k
    sample=read(doc['representative_proof']);control=read(doc['relocated_control_proof']);padding=read(doc['final_padding_proof']);copy=read(doc['unowned_copy_proof'])
    assert sample['no_open_translation_specific_display_or_control_finding'] and not sample['actual_selected_B111_B119_IDs']
    assert len(control['relocated_dispatch_cases'])==150 and len(control['current_and_relocated_whole_original4100_command_cases'])==12
    assert len(control['all207_actor_style_current_and_relocated_pointer_cases']['cases'])==2484
    assert len(control['relocated_predicate_pairs'])==16 and len(control['original_event_queries'])==1 and control['original_event_queries'][0]['event']==319
    assert control['original_query_r0_r1_r2_and_mapped_incidental_r3_cursor_exact']
    assert padding['current_final_padded_macro_alignment_cases']==600 and len(padding['final_target_parity_cases'])==150 and padding['all150_final_targets_complete_native_planes_equal_reviewed_planes']
    for proof in [sample,control]:
        for p,digest in proof['evidence'].items():assert sha(Path(p).read_bytes())==digest
    assert copy['all32_unowned_copy_speeches_byte_exact_and_unreachable_from_ordinary_Lil_entry'] and len(copy['original_VM_return_cases'])==2
    parent,clean=NdsImage.open(doc['current_ROM']),NdsImage.open('work/clean.nds');research=NdsImage.open(padding['research_ROM'])
    assert sha(Path(padding['research_ROM']).read_bytes())==padding['research_ROM_sha256']==control['research_ROM_sha256']==copy['research_ROM_sha256']
    oldblocks,jpblocks,targetblocks=[IlnkContainer.parse(i.read_file('/data/SC2.DK4')).blocks for i in [parent,clean,research]]
    assert [n for n,(a,b) in enumerate(zip(oldblocks,targetblocks,strict=True)) if a!=b]==list(range(111,120))
    assert len(oldblocks)==336 and sha(research.read_file('/data/SC2.DK4'))==mapping['target_SC2_sha256']
    for path,data in parent.iter_components():assert research.read_file(path)==data,path
    assert [p for _,p,data in parent.iter_files() if research.read_file(p)!=data]==['/data/SC2.DK4']
    refs={};selectors=set()
    assert sum(len(b['mapped_native_commands']) for b in mapping['blocks'])==305
    assert sum(len(b['relative_skip_fixups']) for b in mapping['blocks'])==64 and sum(len(b['target_native_skip_cases']) for b in mapping['blocks'])==320
    assert sum(sum(c['word']==0x4000 for c in b['command_map']) for b in mapping['blocks'])==148
    for b in mapping['blocks']:
        n=b['block'];target=targetblocks[n]
        assert sha(oldblocks[n])==b['source_block_sha256'] and sha(target)==b['target_block_sha256']
        assert b['inverse_restoration_recovers_every_original_logical_byte'] and b['external_references_complete']
        for r in b['text_records']:refs[r['id']]=dict(offset=r['new_offset'],hex=r['target_hex'])
        for c in b['actor_style_commands']:
            at,old_at=c['new_offset'],c['old_offset'];selectors.add(target[at+19])
            assert target[at:at+20].hex()==c['target_hex'][:40]
            a,z=c['old_style_offsets'],c['new_style_offsets'];assert all((a[i]==a[j])==(z[i]==z[j]) for i in range(8) for j in range(8))
            assert target[at+18:at+20]==oldblocks[n][old_at+18:old_at+20] and target[at+18]==0
            for r in c['alternative_records']:
                assert r['actual_virtual_prefix_excluded_from_stored_body'];refs[r['id']]=dict(offset=r['new_offset'],hex=r['target_hex'])
        assert not b['choice_commands']
        if n==115:
            c=b['unowned_appended_copy'];at=c['new_offset'];old_at=c['old_offset'];assert c['bytes']==1886
            assert target[at:at+1886]==oldblocks[n][old_at:old_at+1886] and sha(target[at:at+1886])==c['sha256']
            assert target[at-4:at]==bytes(4) and copy['conservative_relocated_prefix_graph']['reachable_return0_commands']==[at-4]
            assert not any(p>=at for p in copy['conservative_relocated_prefix_graph']['reachable_commands'])
    assert len(refs)==150 and selectors=={208,209,214,215,220}
    for r in rows:
        for blocks,ref,key in [(jpblocks,r['source_reference'],'source_hex'),(oldblocks,r['current_reference'],'current_hex')]:
            at=ref['offset'];data=bytes.fromhex(r[key]);assert blocks[r['block']][at:at+len(data)]==data and blocks[r['block']][at+len(data)]==0
        ref=refs[r['id']];value=bytes.fromhex(ref['hex']);block=targetblocks[r['block']];assert block[ref['offset']:ref['offset']+len(value)]==value and block[ref['offset']+len(value)]==0
    candidate=ledger['current_integrated_candidate'];release=read('work/analysis/lil_Shrines_Temples_release_v3205/registered_release_verification.json')
    assert sha(Path(candidate['path']).read_bytes())==candidate['sha256']==release['candidate_sha256']
    assert sha(Path(candidate['patch']).read_bytes())==candidate['patch_sha256']==release['patch_sha256']
    assert sha(Path(release['exact_patch_reconstruction']).read_bytes())==candidate['sha256'] and release['whole_ROM_reconstruction_byte_exact']
    manifest,registry=read(candidate['manifest']),read('translations/release_stack.json')
    assert manifest['profile']==candidate['profile']=='all-routes-unified-v3204' and len(manifest['batches'])==515
    assert len(registry['accepted_layers'])==114 and all(manifest['checks'].values())
    assert manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes()) and registry['latest_promoted_build']['profile']=='all-routes-unified-v1492'
    assert ledger['goal_status']=='active' and not ledger['full_goal_complete'] and Path('docs/editorial_handoff_current.md').read_text(encoding='utf-8').startswith('# Current editorial handoff - V3247')
    ROOT.mkdir(parents=True)
    save(ROOT/'verified_handoff.json',dict(checkpoint='V3247',ledger=str(lp),ledger_sha256=sha(lp.read_bytes()),handoff_receipt=str(rp),handoff_receipt_sha256=sha(rp.read_bytes()),fresh_records=4575,fresh_integrated=4425,fresh_pending=150,source_prose=4578,new_source_prose_reviews=0,new_completed_records=0,completed_records=4425,historical_revised=3040,historical_retained=1385,incomplete_COMMON=3,incomplete_route=150,all150_source_current_target_references_exact=True,all150_five_editorial_gates_and_reference_approvals_preserved=True,unowned32_copy_moved_return0_and_canonical32_pending_scope_verified=True,prior_ledger_updated_files_and_complete_release_chain_verified=True,compiler_registration_registered_build_exact_patch_and_fresh_startup_pending=True,actual_selected_B111_B119_IDs=[],new_emulator_runs=0,candidate=candidate['path'],candidate_sha256=candidate['sha256'],patch=candidate['patch'],patch_sha256=candidate['patch_sha256'],all_jobs_terminal=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('IndependentV3247audit passes:all150source/current/target references andnative approvals exact;no count inflation.4575reread/4425integrated/150pending;canonicalMaria32queued. Guarded registered release remains next;fullgoalactive.')
