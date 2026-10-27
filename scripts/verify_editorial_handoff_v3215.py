"""Independent next-source audit; preserve completed V3204 and all coverage."""
from copy import deepcopy
from pathlib import Path
import struct
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/editorial_handoff_verification_v3215')
CHECKPOINT=Path('work/analysis/lil_B111_B119_scope_checkpoint_v3214')

if __name__=='__main__':
    assert not ROOT.exists()
    rp=CHECKPOINT/'checkpoint_receipt.json';receipt=read(rp)
    for group in ['evidence','updated_files']:
        for p,digest in receipt[group].items():assert sha(Path(p).read_bytes())==digest,(group,p)
    lp=Path('translations/editorial_review_current_v1.json');ledger=read(lp)
    backup=CHECKPOINT/'editorial_review_current_v1.json.before';before=read(backup)
    previous=read(receipt['prior_verified_handoff'])
    assert sha(backup.read_bytes())==previous['ledger_sha256']
    assert sha(Path(previous['handoff_receipt']).read_bytes())==previous['handoff_receipt_sha256']
    for p,digest in read(previous['handoff_receipt'])['updated_files'].items():
        saved=CHECKPOINT/(Path(p).name+'.before')
        assert sha((saved if saved.exists() else Path(p)).read_bytes())==digest
    restored=deepcopy(ledger)
    for k in ['unfinished_editorial_scope_v3214','lil_B111_B119_next_source_lead_v3214']:restored.pop(k)
    restored['latest_checkpoint']=before['latest_checkpoint'];assert restored==before
    fresh=ledger['contextual_story_natural_dialogue_pass_v1871']
    assert (fresh['fresh_pass_records_explicitly_reread'],fresh['fresh_pass_records_integrated'],fresh['fresh_pass_records_pending_native_actual_release'])==(4425,4425,0)
    assert (ledger['records_editorially_completed'],ledger['records_revised_and_integrated'],ledger['retained_wordings_editorially_completed'])==(4425,3040,1385)
    assert ledger['records_with_source_and_prose_pass']==ledger['records_with_source_prose_drafts']==sum(ledger['source_prose_reviewed_counts_by_file'].values())==4428
    lead=ledger['lil_B111_B119_next_source_lead_v3214']
    for key in ['source_packet','branch_proof','clean_context_notes','clean_transcripts']:
        assert sha(Path(lead[key]).read_bytes())==lead[key+'_sha256']
    source,branch,context,transcripts=[read(lead[k]) for k in ['source_packet','branch_proof','clean_context_notes','clean_transcripts']]
    assert source['total_editorial_objects']==182 and len(source['records'])==148 and len(source['typed_actor_style_records'])==34
    assert source['system_FE_panels']==2 and source['actor_style_objects']==6 and source['actor_style_slots']==48
    assert source['typed_choice_objects']==0 and source['typed_choice_records']==[]
    assert [b['block'] for b in source['blocks']]==list(range(111,120))
    assert sum(len(b['all_clean_native_commands']) for b in source['blocks'])==305
    assert len(branch['operands_requiring_adjustment_when_resizing'])==64 and len(branch['cases'])==640
    assert all(c['target_is_independently_mapped_native_boundary'] and c['source_block_owner_input_result_guards_and_ABI_exact'] for c in branch['cases'])
    assert len(source['original_clean_current_inline_getter_cases'])==96
    assert source['distinct_actor_style_presentation_selectors']==[208,209,214,215,220]
    assert context['all148speech_and34_actor_style_alternatives_read_in_complete_clean_exchanges']
    assert context['older_English_not_yet_editorially_compared'] and context['macro_company_identity_not_inferred_from_speaker_portrait']
    assert (context['original_predicate_commands'],context['original_event_queries'])==(15,1)
    assert sum(b['source_objects'] for b in context['blocks'])==182
    for t in transcripts['files']:assert sha(Path(t['path']).read_bytes())==t['sha256']
    candidate=ledger['current_integrated_candidate'];image=NdsImage.open(candidate['path']);clean=NdsImage.open('work/clean.nds')
    assert sha(Path(candidate['path']).read_bytes())==candidate['sha256']==source['current_ROM_sha256']
    en,jp=[IlnkContainer.parse(i.read_file('/data/SC2.DK4')).blocks for i in [image,clean]]
    known={(r['file_path'],r['id']) for r in fresh['record_keys']}
    rows=source['records']+source['typed_actor_style_records']
    assert len({r['id'] for r in rows})==182 and not known&{(r['file_path'],r['id']) for r in rows}
    assert len(lead['source_current_references'])==182
    for r in rows:
        for data,refkey,hexkey in [(jp,'source_reference','source_hex'),(en,'current_reference','current_hex')]:
            ref=r[refkey];at=ref['offset'];value=bytes.fromhex(r[hexkey]);block=data[r['block']]
            assert block[at:at+ref['bytes']]==value and block[at+len(value)]==0
        assert r['source_prose_or_completion_credit_added']==0
    for b in source['blocks']:
        n=b['block'];assert sha(jp[n])==b['clean_block_sha256'] and sha(en[n])==b['current_block_sha256']
        for field,data in [('all_clean_native_commands',jp),('all_current_native_commands',en)]:
            for c in b[field]:assert data[n][c['offset']:c['offset']+c['native_extent']].hex()==c['whole_command_hex']
        assert [a for a in range(len(jp[n])-4) if jp[n][a:a+5]==bytes.fromhex('0040ffff00')]==sorted(c['offset'] for c in b['all_clean_native_commands'] if c['word']==0x4000)
        assert not any(0x2000<=c['word']<0x4000 for c in b['all_clean_native_commands'])
        for o in b['actor_style_objects']:
            assert sum(len(r['style_indices']) for r in o['records'])==8
            for version,data,key in [('clean',jp,'source_command'),('current',en,'current_command')]:
                at=o[key]['offset'];value=data[n][at:at+o[key]['native_extent']]
                assert value[:2]==b'\0\x41' and value[18]==0
                assert all(r['source_selector']==value[19] for r in o['records'])
                cases=[c for c in source['original_clean_current_inline_getter_cases'] if c['block']==n and c['command_offset']==at and c['version']==version]
                assert [c['style_index'] for c in cases]==list(range(8))
                for c in cases:
                    relative=20+struct.unpack_from('<H',value,2+2*c['style_index'])[0]
                    assert c['source_selector']==value[19] and c['relative_offset']==relative
                    assert value[relative:value.index(b'\0',relative)].hex()==c['hex'] and c['original_inline_getter_ABI_all4MiB_and_guards_exact']
    assert jp[115][0x1B4:0x1B8]==bytes(4) and jp[115][0x1B8:0x1BE]==bytes.fromhex('0040ffff00fe')
    assert any(c['word']==0x8100 and c['whole_command_hex']=='00813f01' for b in source['blocks'] for c in b['all_clean_native_commands'])
    release=read('work/analysis/lil_Shrines_Temples_release_v3205/registered_release_verification.json')
    assert release['candidate_sha256']==candidate['sha256'] and release['whole_ROM_reconstruction_byte_exact']
    assert Path(release['exact_patch_reconstruction']).read_bytes()==Path(candidate['path']).read_bytes()
    assert sha(Path(candidate['patch']).read_bytes())==candidate['patch_sha256']==release['patch_sha256']
    manifest=read(candidate['manifest']);registry=read('translations/release_stack.json')
    assert manifest['profile']==candidate['profile']=='all-routes-unified-v3204' and len(manifest['batches'])==515
    assert all(manifest['checks'].values()) and len(registry['accepted_layers'])==114
    assert registry['latest_promoted_build']['profile']=='all-routes-unified-v1492'
    assert manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes())
    start=read('work/analysis/lil_Shrines_Temples_startup_v3207/cold_boot_Lil_startup_town_verification.json')
    assert start['candidate_sha256']==candidate['sha256'] and start['paired_frame_count']==31
    assert start['all_current_requested_and_final_framebuffers_equal_V3144']
    review=read('work/analysis/lil_Shrines_Temples_completion_v3208/current_six_frame_visual_review.json')
    assert review['viewed'] and sha(Path(review['sheet']).read_bytes())==review['sha256']==start['review_sheet_sha256']
    assert ledger['goal_status']=='active' and not ledger['full_goal_complete']
    assert Path('docs/editorial_handoff_current.md').read_text(encoding='utf-8').startswith('# Current editorial handoff - V3214')
    ROOT.mkdir(parents=True)
    save(ROOT/'verified_handoff.json',dict(checkpoint='V3214',ledger=str(lp),ledger_sha256=sha(lp.read_bytes()),
        handoff_receipt=str(rp),handoff_receipt_sha256=sha(rp.read_bytes()),fresh_records=4425,fresh_integrated=4425,fresh_pending=0,
        source_prose=4428,new_source_prose_reviews=0,new_completed_records=0,completed_records=4425,
        historical_revised=3040,historical_retained=1385,incomplete_COMMON=3,incomplete_route=0,
        next_uncredited_editorial_objects=182,next_source_speech=148,next_stored_actor_style_alternatives=34,
        next_source_style_selectors=[208,209,214,215,220],native_inline_getter_cases=96,relative_sites=64,clean_current_skip_cases=640,
        whole_clean_context_read_before_older_English_comparison=True,
        mixed_B115_entry_route_macro_current_binding_and_all_prose_native_release_gates_pending=True,
        prior_completed235_exact_release_patch_and_currentstartup_preserved=True,prior_ledger_and_updated_file_chains_verified=True,
        candidate=candidate['path'],candidate_sha256=candidate['sha256'],patch=candidate['patch'],patch_sha256=candidate['patch_sha256'],
        actual_selected_B111_B119_IDs=[],new_emulator_runs=0,all_jobs_terminal=True,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('IndependentV3214audit passes:next182source/current/clean-context objects uncredited;96getters/64spans/640cases.4425completed/V3204/exactpatch/31currentframes preserved. Fullgoalactive.')
