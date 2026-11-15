"""Independent clean-only lead audit; preserve every completed199/release claim."""
from pathlib import Path
from copy import deepcopy
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/editorial_handoff_verification_v3111')
CHECKPOINT=Path('work/analysis/lil_next_clean_scope_checkpoint_v3110')
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
    for key in ['lil_next_clean_scope_lead_v3110','unfinished_editorial_scope_v3110']:restored.pop(key)
    restored['latest_checkpoint']=before['latest_checkpoint'];assert restored==before
    fresh=ledger['contextual_story_natural_dialogue_pass_v1871'];assert (fresh['fresh_pass_records_explicitly_reread'],fresh['fresh_pass_records_integrated'],fresh['fresh_pass_records_pending_native_actual_release'])==(3990,3990,0)
    assert (ledger['records_editorially_completed'],ledger['records_revised_and_integrated'],ledger['retained_wordings_editorially_completed'])==(3990,2800,1190)
    assert ledger['records_with_source_and_prose_pass']==ledger['records_with_source_prose_drafts']==sum(ledger['source_prose_reviewed_counts_by_file'].values())==3993
    lead=ledger['lil_next_clean_scope_lead_v3110'];source=read(lead['source_inventory']);assert sha(Path(lead['source_inventory']).read_bytes())==lead['source_inventory_sha256']
    assert not source['unclassified'] and source['editorial_credit_added']==0 and source['not_a_manuscript_or_native_consumer_approval']
    assert [b['block'] for b in source['blocks']]==list(range(81,101))
    assert (sum(b['speeches'] for b in source['blocks']),sum(b['FE_panels'] for b in source['blocks']),sum(b['choice_commands'] for b in source['blocks']),sum(len(b['commands']) for b in source['blocks']))==(198,7,1,274)
    clean=NdsImage.open('work/clean.nds');data=clean.read_file('/data/SC2.DK4');blocks=IlnkContainer.parse(data).blocks
    assert sha(Path('work/clean.nds').read_bytes())==source['source_ROM_sha256'] and sha(data)==source['source_SC2_sha256']
    known={(r['file_path'],r['id']) for r in fresh['record_keys']};rows=[(b['block'],r) for b in source['blocks'] for r in b['records']]
    assert len(rows)==198 and not known&{('/data/SC2.DK4',r['id']) for b,r in rows}
    for b in source['blocks']:
        block=blocks[b['block']];assert sha(block)==b['source_block_sha256']
        for c in b['commands']:assert block[c['offset']:c['offset']+c['native_extent']].hex()==c['whole_command_hex']
        for r in b['records']:
            at=r['offset'];assert block[at:at+r['bytes']].hex()==r['source_hex'] and block[at-5:at+1].hex()==r['source_preamble_hex']
            assert block[at+r['bytes']]==0 and block[at+1:at+r['bytes']].decode('cp932')==r['Japanese']
    candidate=ledger['current_integrated_candidate'];release=read('work/analysis/lil_Recruits_Julian_release_v3104/registered_release_verification.json')
    assert sha(Path(candidate['path']).read_bytes())==candidate['sha256']==release['candidate_sha256']
    assert sha(Path(candidate['patch']).read_bytes())==candidate['patch_sha256']==release['patch_sha256']
    assert Path(release['exact_patch_reconstruction']).read_bytes()==Path(candidate['path']).read_bytes() and release['whole_ROM_reconstruction_byte_exact']
    manifest,registry=read(candidate['manifest']),read('translations/release_stack.json')
    assert manifest['profile']==candidate['profile']=='all-routes-unified-v3103' and len(manifest['batches'])==510 and all(manifest['checks'].values())
    assert manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes()) and len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v1492'
    startup=read('work/analysis/lil_Recruits_Julian_startup_v3106/cold_boot_Lil_startup_town_verification.json')
    assert startup['candidate_sha256']==candidate['sha256'] and startup['paired_frame_count']==31 and startup['all_current_requested_and_final_framebuffers_equal_V3066']
    assert sha(Path(startup['review_sheet']).read_bytes())==startup['review_sheet_sha256']
    inventory=read(ledger['unfinished_editorial_scope_v3110']['path']);oldinventory=read(before['unfinished_editorial_scope_v3107']['path']);check=deepcopy(inventory)
    check.pop('next_clean_only_uncredited_exchange_inventory_v3109');check['next_focus']=oldinventory['next_focus'];assert check==oldinventory
    assert ledger['reviewed_but_incomplete_COMMON_IDs']==[750,751,752] and not any(ledger['reviewed_but_incomplete_route_record_IDs'].values())
    assert ledger['goal_status']=='active' and not ledger['full_goal_complete'] and Path('docs/editorial_handoff_current.md').read_text(encoding='utf8').startswith('# Current editorial handoff - V3110')
    ROOT.mkdir(parents=True);save(ROOT/'verified_handoff.json',dict(checkpoint='V3110',ledger=str(lp),ledger_sha256=sha(lp.read_bytes()),handoff_receipt=str(rp),handoff_receipt_sha256=sha(rp.read_bytes()),prior_completed_checkpoint='V3107',completed_records=3990,historical_revised=2800,historical_retained=1190,source_prose=3993,fresh_records=3990,fresh_integrated=3990,fresh_pending=0,next_clean_only_speeches=198,next_typed_menu_objects=1,next_menu_label_count_not_yet_bound=True,new_source_prose_reviews=0,new_completed_records=0,all198_exact_clean_source_speech_references_verified_without_review_credit=True,previous_editorial_counts_keys_completed_families_and_release_preserved=True,whole_clean_input_reconstruction_exact=True,manifest_batches=510,accepted_layers=114,current_gameplay_frame_pairs=31,candidate=candidate['path'],candidate_sha256=candidate['sha256'],patch=candidate['patch'],patch_sha256=candidate['patch_sha256'],all_jobs_terminal=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('IndependentV3110audit passes:3990completed/3993source-prose preserved;198clean speeches/one menu uncredited. V3103/exactpatch/current31framepairs preserved;fullgoalactive.')
