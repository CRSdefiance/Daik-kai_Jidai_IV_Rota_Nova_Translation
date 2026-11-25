"""Independent readiness audit; no review inflation or premature integration."""
from collections import Counter
from pathlib import Path
import struct
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/editorial_handoff_verification_v3201')
CHECKPOINT=Path('work/analysis/lil_Shrines_Temples_ready_checkpoint_v3200')

if __name__=='__main__':
    assert not ROOT.exists()
    rp=CHECKPOINT/'checkpoint_receipt.json';receipt=read(rp)
    for group in ['evidence','updated_files']:
        for p,digest in receipt[group].items():assert sha(Path(p).read_bytes())==digest,(group,p)
    lp=Path('translations/editorial_review_current_v1.json')
    ledger=read(lp);before=read(CHECKPOINT/'editorial_review_current_v1.json.before')
    prior=read(receipt['prior_verified_handoff'])
    assert sha((CHECKPOINT/'editorial_review_current_v1.json.before').read_bytes())==prior['ledger_sha256']
    assert sha(Path(prior['handoff_receipt']).read_bytes())==prior['handoff_receipt_sha256']
    for p,digest in read(prior['handoff_receipt'])['updated_files'].items():
        saved=CHECKPOINT/(Path(p).name+'.before')
        assert sha((saved if saved.exists() else Path(p)).read_bytes())==digest
    for key in ['completed_editorial_families','records_editorially_completed','records_revised_and_integrated',
        'retained_wordings_editorially_completed','completed_editorial_record_counts_by_file','current_integrated_candidate',
        'reviewed_but_incomplete_COMMON_IDs','reviewed_but_incomplete_route_record_IDs','unresolved_graphics_work',
        'older_record_reaudit_after_full_editorial_goal','records_with_source_and_prose_pass','records_with_source_prose_drafts',
        'source_prose_reviewed_counts_by_file','native_source_universe_inventory_v2701c']:
        assert ledger[key]==before[key],key
    fresh,old=ledger['contextual_story_natural_dialogue_pass_v1871'],before['contextual_story_natural_dialogue_pass_v1871']
    for key in ['record_keys','record_IDs','integrated_record_keys','pending_record_keys',
        'fresh_pass_records_explicitly_reread','fresh_pass_records_integrated','fresh_pass_records_pending_native_actual_release']:
        assert fresh[key]==old[key],key
    assert (fresh['fresh_pass_records_explicitly_reread'],fresh['fresh_pass_records_integrated'],fresh['fresh_pass_records_pending_native_actual_release'])==(4425,4190,235)
    assert ledger['records_with_source_and_prose_pass']==4428
    paths=[fresh['latest_contextual_manuscript'],fresh['latest_contextual_actor_style_draft'],fresh['latest_contextual_choice_draft']]
    doc,voice,menu=map(read,paths);rows=doc['records']+voice['records']+menu['records']
    assert len(rows)==235 and Counter(r['editorial_decision'] for r in rows)=={'revise':117,'retain-wording':118}
    for d in [doc,voice,menu]:
        validate_natural_dialogue_batch(d)
        previous=read(d['previous_manuscript'])
        assert sha(Path(d['previous_manuscript']).read_bytes())==d['previous_manuscript_sha256']
        for r,p in zip(d['records'],previous['records'],strict=True):
            for key in ['id','english','source_hex','current_hex','source_reference','current_reference','source_meaning','localization_note','review','editorial_decision']:
                assert r[key]==p[key],(r['id'],key)
    approval=read('work/analysis/lil_Shrines_Temples_reference_approval_v3199/approval_receipt.json')
    for p,digest in approval['hashes'].items():assert sha(Path(p).read_bytes())==digest
    mapping=read(doc['reference_map'])
    assert sha(Path(doc['reference_map']).read_bytes())==doc['reference_map_sha256']
    assert mapping['external_references_complete'] and mapping['representative_shared_rules_approved']
    assert mapping['all421_nested_command_boundaries_and114_relative_sites_verified']
    assert mapping['all570_relocated_relative_skip_cases_preserve_original_targets']
    assert mapping['all21_relocated_predicate_pairs_preserve_source_operands_and_results']
    sample=read(doc['representative_proof']);control=read(doc['relocated_control_proof']);padding=read(doc['final_padding_proof'])
    assert sample['no_open_translation_specific_display_or_control_finding'] and sample['actual_selected_Shrines_Temples_IDs']==[]
    assert sample['actual_three_option_menu_gameplay_coverage']==[] and len(sample['three_option_distinct_count_geometry_and_result_tests'])==5
    assert len(control['relocated_dispatch_cases'])==220
    assert len(control['current_and_relocated_whole_original4100_command_cases'])==16
    assert len(control['all207_actor_style_current_and_relocated_pointer_cases']['cases'])==3312
    assert len(control['relocated_predicate_pairs'])==21 and control['original_event_queries']==[]
    assert padding['current_final_padded_macro_alignment_cases']==880 and len(padding['final_target_parity_cases'])==220
    assert padding['all220_final_targets_complete_native_planes_equal_reviewed_planes']
    for proof in [sample,control]:
        for p,digest in proof['evidence'].items():assert sha(Path(p).read_bytes())==digest
    parent=NdsImage.open(doc['current_ROM']);clean=NdsImage.open('work/clean.nds')
    research=NdsImage.open(padding['research_ROM'])
    assert sha(Path(padding['research_ROM']).read_bytes())==padding['research_ROM_sha256']==control['research_ROM_sha256']
    oldblocks,jpblocks,targetblocks=[IlnkContainer.parse(i.read_file('/data/SC2.DK4')).blocks for i in [parent,clean,research]]
    assert [n for n,(a,b) in enumerate(zip(oldblocks,targetblocks,strict=True)) if a!=b]==list(range(101,111))
    assert len(oldblocks)==336 and sha(research.read_file('/data/SC2.DK4'))==mapping['target_SC2_sha256']
    for path,data in parent.iter_components():assert research.read_file(path)==data,path
    assert [p for _,p,data in parent.iter_files() if research.read_file(p)!=data]==['/data/SC2.DK4']
    refs={}
    assert sum(len(b['mapped_native_commands']) for b in mapping['blocks'])==421
    assert sum(len(b['relative_skip_fixups']) for b in mapping['blocks'])==114
    assert sum(len(b['target_native_skip_cases']) for b in mapping['blocks'])==570
    for b in mapping['blocks']:
        n=b['block'];target=targetblocks[n]
        assert sha(oldblocks[n])==b['source_block_sha256'] and sha(target)==b['target_block_sha256']
        assert b['inverse_restoration_recovers_every_original_logical_byte'] and b['external_references_complete']
        for r in b['text_records']:
            refs[r['id']]=dict(offset=r['new_offset'],hex=r['target_hex'])
        for c in b['actor_style_commands']:
            assert target[c['new_offset']:c['new_offset']+20].hex()==c['target_hex'][:40]
            a,z=c['old_style_offsets'],c['new_style_offsets']
            assert all((a[i]==a[j])==(z[i]==z[j]) for i in range(8) for j in range(8))
            assert target[c['new_offset']+18:c['new_offset']+20]==b'\0\xd0'
            for r in c['alternative_records']:
                assert r['virtual_D0_excluded_from_stored_body']
                refs[r['id']]=dict(offset=r['new_offset'],hex=r['target_hex'])
        for c in b['choice_commands']:
            assert c['count']==3 and c['text_base']==8 and target[c['new_offset']:c['new_offset']+2]==b'\0\x22'
            for i,r in enumerate(c['label_references']):
                assert r['option_index']==i
                refs[r['id']]=dict(offset=r['new_offset'],hex=c['labels'][i].encode('ascii').hex())
    assert len(refs)==235
    for r in rows:
        for blocks,reference,hexkey in [(jpblocks,r['source_reference'],'source_hex'),(oldblocks,r['current_reference'],'current_hex')]:
            at=reference['offset'];data=bytes.fromhex(r[hexkey])
            assert blocks[r['block']][at:at+len(data)]==data and blocks[r['block']][at+len(data)]==0
        ref=refs[r['id']];value=bytes.fromhex(ref['hex']);block=targetblocks[r['block']]
        assert block[ref['offset']:ref['offset']+len(value)]==value and block[ref['offset']+len(value)]==0
    candidate=ledger['current_integrated_candidate'];release=read('work/analysis/lil_Crew_Items_release_v3145/registered_release_verification.json')
    assert sha(Path(candidate['path']).read_bytes())==candidate['sha256']==release['candidate_sha256']
    assert sha(Path(candidate['patch']).read_bytes())==candidate['patch_sha256']==release['patch_sha256']
    assert sha(Path(release['exact_patch_reconstruction']).read_bytes())==candidate['sha256'] and release['whole_ROM_reconstruction_byte_exact']
    manifest,registry=read(candidate['manifest']),read('translations/release_stack.json')
    assert manifest['profile']==candidate['profile']=='all-routes-unified-v3144' and len(manifest['batches'])==512
    assert len(registry['accepted_layers'])==114 and all(manifest['checks'].values())
    assert manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes())
    assert registry['latest_promoted_build']['profile']=='all-routes-unified-v1492'
    assert ledger['goal_status']=='active' and not ledger['full_goal_complete']
    assert Path('docs/editorial_handoff_current.md').read_text(encoding='utf-8').startswith('# Current editorial handoff - V3200')
    ROOT.mkdir(parents=True)
    save(ROOT/'verified_handoff.json',dict(checkpoint='V3200',ledger=str(lp),ledger_sha256=sha(lp.read_bytes()),
        handoff_receipt=str(rp),handoff_receipt_sha256=sha(rp.read_bytes()),
        fresh_records=4425,fresh_integrated=4190,fresh_pending=235,source_prose=4428,new_source_prose_reviews=0,
        new_completed_records=0,completed_records=4190,historical_revised=2923,historical_retained=1267,incomplete_COMMON=3,incomplete_route=235,
        all235_source_current_target_references_exact=True,all235_five_editorial_gates_and_reference_approvals_preserved=True,
        prior_ledger_updated_files_and_complete_release_chain_verified=True,
        compiler_registration_registered_build_exact_patch_and_fresh_startup_pending=True,
        actual_selected_Shrines_Temples_IDs=[],actual_three_option_menu_gameplay_coverage=[],new_emulator_runs=0,
        candidate=candidate['path'],candidate_sha256=candidate['sha256'],patch=candidate['patch'],patch_sha256=candidate['patch_sha256'],
        all_jobs_terminal=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('IndependentV3200audit passes:all235source/current/target references andnative approvals exact;no count inflation.4425reread/4190integrated/235pending. Guarded registered release remains next;fullgoalactive.')
