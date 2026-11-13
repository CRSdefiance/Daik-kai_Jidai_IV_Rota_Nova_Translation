"""Independent clean-only lead audit; preserve every completed200/release claim."""
from pathlib import Path
from copy import deepcopy
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/editorial_handoff_verification_v3158')
CHECKPOINT=Path('work/analysis/lil_voice_scope_checkpoint_v3157')
if __name__=='__main__':
    assert not ROOT.exists();rp=CHECKPOINT/'checkpoint_receipt.json';receipt=read(rp)
    for kind in ['evidence','updated_files']:
        for p,digest in receipt[kind].items():assert sha(Path(p).read_bytes())==digest,(kind,p)
    lp=Path('translations/editorial_review_current_v1.json');ledger=read(lp);backup=CHECKPOINT/'editorial_review_current_v1.json.before';before=read(backup)
    oldproof=read(receipt['prior_verified_handoff']);assert sha(backup.read_bytes())==oldproof['ledger_sha256']
    assert sha(Path(oldproof['handoff_receipt']).read_bytes())==oldproof['handoff_receipt_sha256']
    for p,digest in read(oldproof['handoff_receipt'])['updated_files'].items():
        saved=CHECKPOINT/(Path(p).name+'.before');assert sha((saved if saved.exists() else Path(p)).read_bytes())==digest
    restored=deepcopy(ledger)
    for key in ['lil_next_voice_scope_lead_v3157','unfinished_editorial_scope_v3157']:restored.pop(key)
    restored['latest_checkpoint']=before['latest_checkpoint'];assert restored==before
    fresh=ledger['contextual_story_natural_dialogue_pass_v1871'];assert (fresh['fresh_pass_records_explicitly_reread'],fresh['fresh_pass_records_integrated'],fresh['fresh_pass_records_pending_native_actual_release'])==(4190,4190,0)
    assert (ledger['records_editorially_completed'],ledger['records_revised_and_integrated'],ledger['retained_wordings_editorially_completed'])==(4190,2923,1267)
    assert ledger['records_with_source_and_prose_pass']==ledger['records_with_source_prose_drafts']==sum(ledger['source_prose_reviewed_counts_by_file'].values())==4193
    lead=ledger['lil_next_voice_scope_lead_v3157'];source=read(lead['source_inventory']);assert sha(Path(lead['source_inventory']).read_bytes())==lead['source_inventory_sha256']
    assert not source['unclassified'] and source['editorial_credit_added']==0 and source['all_source_0100_bodies_recursed_and_all_speech_headers_matched'] and source['explicit_last_result']==0xFFFFFFFF
    assert [b['block'] for b in source['blocks']]==list(range(101,121))
    assert (sum(b['speeches']for b in source['blocks']),sum(b['FE_panels']for b in source['blocks']),sum(b['typed_menu_4100_commands']for b in source['blocks']),sum(len(b['commands'])for b in source['blocks']))==(339,38,14,795)
    new=[b for b in source['blocks']if b['block']!=120];first=new[:10]
    assert (sum(b['speeches']for b in new),sum(b['FE_panels']for b in new),sum(len(b['commands'])for b in new))==(312,32,726)
    assert (sum(b['speeches']for b in first),sum(b['FE_panels']for b in first),sum(len(b['commands'])for b in first),sum(b['typed_menu_4100_commands']for b in first))==(164,30,421,8)
    control=read(lead['source_0400_proof']);assert sha(Path(lead['source_0400_proof']).read_bytes())==lead['source_0400_proof_sha256']
    assert len(control['sites'])==5 and len(control['cases'])==50 and control['only_last_result2_takes_source_0400_span']
    assert all(c['only_result2_skips'] and c['all4MiB_owner_stream_ABI_and_boundary_guards_exact']for c in control['cases'])
    for p,digest in source['helper_hashes'].items():assert sha(Path(p).read_bytes())==digest
    clean=NdsImage.open('work/clean.nds');data=clean.read_file('/data/SC2.DK4');blocks=IlnkContainer.parse(data).blocks
    assert sha(Path('work/clean.nds').read_bytes())==source['source_ROM_sha256'] and sha(data)==source['source_SC2_sha256']
    known={(r['file_path'],r['id']) for r in fresh['record_keys']};rows=[(b['block'],r) for b in source['blocks'] for r in b['records']]
    assert len(rows)==339 and known&{('/data/SC2.DK4',r['id'])for b,r in rows}=={('/data/SC2.DK4',r['id'])for b,r in rows if b==120}
    assert all(r['already_contextually_completed']==(b==120)for b,r in rows)
    for b in source['blocks']:
        block=blocks[b['block']];assert sha(block)==b['source_block_sha256']
        for c in b['commands']:assert block[c['offset']:c['offset']+c['native_extent']].hex()==c['whole_command_hex']
        assert [i for i in range(len(block)-4)if block[i:i+5]==bytes.fromhex('0040ffff00')]==sorted(c['offset']for c in b['commands']if c['word']==0x4000)
        for r in b['records']:
            at=r['offset'];assert block[at:at+r['bytes']].hex()==r['source_hex'] and block[at-5:at+1].hex()==r['source_preamble_hex']
            assert block[at+r['bytes']]==0 and block[at+1:at+r['bytes']].decode('cp932')==r['Japanese']
    voice=read(lead['alternative_proof']);assert sha(Path(lead['alternative_proof']).read_bytes())==lead['alternative_proof_sha256']
    assert len(voice['objects'])==14 and len(voice['records'])==90 and voice['native_inline_getter_cases']==224
    assert len([r for r in voice['records'] if r['block']<=110])==56 and lead['next_editorial_objects']==220 and lead['total_editorial_objects']==402
    assert voice['player_choice_count_pointer_VM_and_choice_renderer_must_not_be_applied'] and voice['alias_groups_preserved_in_exact_clean_current_pointer_tables']
    current_image=NdsImage.open(ledger['current_integrated_candidate']['path']);current_blocks=IlnkContainer.parse(current_image.read_file('/data/SC2.DK4')).blocks
    assert voice['candidate_sha256']==ledger['current_integrated_candidate']['sha256']
    for obj in voice['objects']:
        assert obj['not_a_player_menu'] and len(obj['versions'])==2 and sum(len(r['style_indices'])for r in obj['records'])==8
        for version,bb in zip(obj['versions'],[blocks,current_blocks],strict=True):
            block=bb[obj['block']];at=version['command_offset'];value=bytes.fromhex(version['command_hex']);assert block[at:at+len(value)]==value and value[:2]==bytes.fromhex('0041') and value[18]==0
            assert len(version['style_slots'])==8 and version['low_byte_flags']==0
            for slot in version['style_slots']:
                assert slot['relative_offset']==20+version['offsets'][slot['style_index']] and slot['offset']==at+slot['relative_offset']
                text=bytes.fromhex(slot['hex']);assert block[slot['offset']:slot['offset']+len(text)]==text and block[slot['offset']+len(text)]==0
                assert slot['native_inline_getter_ABI_all4MiB_input_owner_and_stream_guards_exact']
        assert obj['versions'][0]['offsets']==obj['versions'][1]['offsets']
    for r in voice['records']:
        for key,hexkey,bb in [('source_reference','source_hex',blocks),('current_reference','current_hex',current_blocks)]:
            ref=r[key];block=bb[r['block']];value=bytes.fromhex(r[hexkey]);assert block[ref['offset']:ref['offset']+ref['bytes']]==value and block[ref['offset']+ref['bytes']]==0
        assert r['source_prose_or_completion_credit_added']==0
    candidate=ledger['current_integrated_candidate'];release=read('work/analysis/lil_Crew_Items_release_v3145/registered_release_verification.json')
    assert sha(Path(candidate['path']).read_bytes())==candidate['sha256']==release['candidate_sha256']
    assert sha(Path(candidate['patch']).read_bytes())==candidate['patch_sha256']==release['patch_sha256']
    assert Path(release['exact_patch_reconstruction']).read_bytes()==Path(candidate['path']).read_bytes() and release['whole_ROM_reconstruction_byte_exact']
    manifest,registry=read(candidate['manifest']),read('translations/release_stack.json')
    assert manifest['profile']==candidate['profile']=='all-routes-unified-v3144' and len(manifest['batches'])==512 and all(manifest['checks'].values())
    assert manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes()) and len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v1492'
    startup=read('work/analysis/lil_Crew_Items_startup_v3147/cold_boot_Lil_startup_town_verification.json')
    assert startup['candidate_sha256']==candidate['sha256'] and startup['paired_frame_count']==31 and startup['all_current_requested_and_final_framebuffers_equal_V3103']
    assert sha(Path(startup['review_sheet']).read_bytes())==startup['review_sheet_sha256']
    inventory=read(ledger['unfinished_editorial_scope_v3157']['path']);oldinventory=read(before['unfinished_editorial_scope_v3154']['path']);check=deepcopy(inventory)
    check.pop('next_clean_current_uncredited_exchange_scope_v3156');check['next_focus']=oldinventory['next_focus'];assert check==oldinventory
    assert ledger['reviewed_but_incomplete_COMMON_IDs']==[750,751,752] and not any(ledger['reviewed_but_incomplete_route_record_IDs'].values())
    assert ledger['goal_status']=='active' and not ledger['full_goal_complete'] and Path('docs/editorial_handoff_current.md').read_text(encoding='utf8').startswith('# Current editorial handoff - V3157')
    ROOT.mkdir(parents=True);save(ROOT/'verified_handoff.json',dict(checkpoint='V3157',ledger=str(lp),ledger_sha256=sha(lp.read_bytes()),handoff_receipt=str(rp),handoff_receipt_sha256=sha(rp.read_bytes()),prior_completed_checkpoint='V3148',completed_records=4190,historical_revised=2923,historical_retained=1267,source_prose=4193,fresh_records=4190,fresh_integrated=4190,fresh_pending=0,next_clean_only_speeches=312,next_source_4100_objects=14,next_unique_alternatives=90,next_total_editorial_objects=402,next_first_ten_editorial_objects=220,next_4100_label_count_and_consumer_not_yet_bound=True,new_source_prose_reviews=0,new_completed_records=0,all339_exact_clean_source_speech_references_verified_without_review_credit=True,previous_editorial_counts_keys_completed_families_and_release_preserved=True,whole_clean_input_reconstruction_exact=True,manifest_batches=512,accepted_layers=114,current_gameplay_frame_pairs=31,candidate=candidate['path'],candidate_sha256=candidate['sha256'],patch=candidate['patch'],patch_sha256=candidate['patch_sha256'],all_jobs_terminal=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('IndependentV3157audit passes:4190completed/4193source-prose preserved;312clean speeches/90stored alternatives uncredited;first220objects. V3144/exactpatch/current31framepairs preserved;fullgoalactive.')
