"""Audit the uncredited next inventory and the preserved completed release chain."""
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/editorial_handoff_verification_v3259')
CHECKPOINT=Path('work/analysis/lil_next_clean_scope_checkpoint_v3258')
if __name__=='__main__':
    assert not ROOT.exists();rp=CHECKPOINT/'checkpoint_receipt.json';receipt=read(rp)
    for group in ['evidence','updated_files']:
        for p,digest in receipt[group].items():assert sha(Path(p).read_bytes())==digest,(group,p)
    lp=Path('translations/editorial_review_current_v1.json');ledger=read(lp);before=read(CHECKPOINT/'editorial_review_current_v1.json.before');prior=read(receipt['prior_verified_handoff'])
    assert sha((CHECKPOINT/'editorial_review_current_v1.json.before').read_bytes())==prior['ledger_sha256'] and sha(Path(prior['handoff_receipt']).read_bytes())==prior['handoff_receipt_sha256']
    for p,digest in read(prior['handoff_receipt'])['updated_files'].items():
        saved=CHECKPOINT/(Path(p).name+'.before');assert sha((saved if saved.exists() else Path(p)).read_bytes())==digest
    for k in ['completed_editorial_families','records_editorially_completed','records_revised_and_integrated','retained_wordings_editorially_completed','completed_editorial_record_counts_by_file','current_integrated_candidate','reviewed_but_incomplete_COMMON_IDs','reviewed_but_incomplete_route_record_IDs','unresolved_graphics_work','older_record_reaudit_after_full_editorial_goal','records_with_source_and_prose_pass','records_with_source_prose_drafts','source_prose_reviewed_counts_by_file','native_source_universe_inventory_v2701c','contextual_story_natural_dialogue_pass_v1871','lil_B111_B119_scope_reconciliation_v3237','active_source_prose_drafts']:assert ledger[k]==before[k],k
    fresh=ledger['contextual_story_natural_dialogue_pass_v1871'];keys={historical_key(r) for r in fresh['record_keys']}
    assert len(keys)==4575 and (fresh['fresh_pass_records_explicitly_reread'],fresh['fresh_pass_records_integrated'],fresh['fresh_pass_records_pending_native_actual_release'])==(4575,4575,0)
    assert (ledger['records_editorially_completed'],ledger['records_revised_and_integrated'],ledger['retained_wordings_editorially_completed'],ledger['records_with_source_and_prose_pass'])==(4575,3087,1488,4578)
    lead=ledger['lil_after_B119_next_clean_source_lead_v3258'];packet=read(lead['source_packet']);assert sha(Path(lead['source_packet']).read_bytes())==lead['source_packet_sha256']
    clean=NdsImage.open('work/clean.nds');arm=clean.read_file('/__arm9__.bin');blocks=IlnkContainer.parse(clean.read_file('/data/SC2.DK4')).blocks
    assert sha(Path('work/clean.nds').read_bytes())==packet['source_ROM_sha256'] and sha(clean.read_file('/data/SC2.DK4'))==packet['source_SC2_sha256']
    assert len(packet['blocks'])==19 and packet['unclassified']==[] and [b['block'] for b in packet['blocks']]==list(range(122,141))
    inventory,_,_=scoped_inventory();rows=[];commands=0
    for b in packet['blocks']:
        block=blocks[b['block']];assert sha(block)==b['source_block_sha256'];native,speeches=inventory(arm,block)
        assert native==b['commands'] and len(speeches)==len(b['records']);commands+=len(native)
        for c,r in zip(speeches,b['records'],strict=True):
            at=r['source_reference']['offset'];value=bytes.fromhex(r['source_hex']);assert at==c['offset']+5 and value and block[at:at+len(value)]==value and block[at+len(value)]==0
            assert c['native_extent']==r['native_extent']==(5+len(value)+1+1)//2*2 and c['whole_command_hex']==r['whole_native_command_hex']
            assert r['source_complete_preamble_hex']==block[at-5:at+1].hex() and r['source_selector']==value[0] and r['source_Japanese']==value[1:].decode('cp932')
            assert r['already_contextually_completed']==(historical_key(r) in keys)
            assert r['zero_valued_native_actor_selector_requires_current_binding']==(value[0]==0)
            assert r['complete_prefix_native_binding_and_whole_exchange_review_pending'];rows.append(r)
    assert len(rows)==533 and sum(not r['already_contextually_completed'] for r in rows)==410 and sum(r['source_selector']==0 for r in rows)==18
    nextrows=[r for r in rows if r['block'] in range(122,128)];assert len(nextrows)==155 and not any(r['already_contextually_completed'] for r in nextrows) and sum(r['source_selector']==254 for r in nextrows)==10
    assert sum(len(b['commands']) for b in packet['blocks'] if b['block'] in range(122,128))==312
    for word,n in [(0x2000,2),(0x2100,5)]:assert sum(c['word']==word for b in packet['blocks'] for c in b['commands'])==n
    assert lead['source_prose_or_completion_credit_added']==0 and lead['unique_player_facing_target_count_not_yet_classified']
    c=ledger['current_integrated_candidate'];release=read('work/analysis/lil_B111_B119_release_v3252b/registered_release_verification.json');assert sha(Path(c['path']).read_bytes())==c['sha256']==release['candidate_sha256'] and sha(Path(c['patch']).read_bytes())==c['patch_sha256']==release['patch_sha256']
    assert release['whole_ROM_reconstruction_byte_exact'] and Path(release['exact_patch_reconstruction']).read_bytes()==Path(c['path']).read_bytes()
    manifest,registry=read(c['manifest']),read('translations/release_stack.json');assert manifest['profile']==c['profile']=='all-routes-unified-v3251' and len(manifest['batches'])==517 and len(registry['accepted_layers'])==114 and all(manifest['checks'].values())
    assert manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes()) and registry['latest_promoted_build']['profile']=='all-routes-unified-v1492'
    inventorydoc=read(ledger['unfinished_editorial_scope_v3258']['path']);oldinventory=read(before['unfinished_editorial_scope_v3255']['path'])
    for k in oldinventory:
        if k!='next_focus':assert inventorydoc[k]==oldinventory[k],k
    assert inventorydoc['incomplete_COMMON_count']==3 and inventorydoc['incomplete_route_source_prose_count']==0 and inventorydoc['canonical_Maria_SC3_B97_uncredited32_source_lead']['records']==32
    assert ledger['goal_status']=='active' and not ledger['full_goal_complete'] and Path('docs/editorial_handoff_current.md').read_text(encoding='utf-8').startswith('# Current editorial handoff - V3258')
    ROOT.mkdir(parents=True)
    save(ROOT/'verified_handoff.json',dict(checkpoint='V3258',ledger=str(lp),ledger_sha256=sha(lp.read_bytes()),handoff_receipt=str(rp),handoff_receipt_sha256=sha(rp.read_bytes()),fresh_records=4575,fresh_integrated=4575,fresh_pending=0,source_prose=4578,new_source_prose_reviews=0,new_completed_records=0,completed_records=4575,historical_revised=3087,historical_retained=1488,incomplete_COMMON=3,incomplete_route=0,next_clean_physical_speech_objects=533,next_already_completed_objects_excluded=123,next_not_previously_completed_physical_speech_objects=410,next_focus_speeches=155,next_focus_FE=10,next_focus_commands=312,source00_B133_18_complete_prefix_objects_preserved_unbound=True,next_typed2100_2000_and_unique_player_facing_scope_pending=True,all533_complete_native_speech_extents_and_source_references_verified=True,canonical_Maria32_pending_uncredited=True,prior_completed150_exact_release_patch_and_currentstartup_preserved=True,prior_ledger_and_updated_file_chains_verified=True,candidate=c['path'],candidate_sha256=c['sha256'],patch=c['patch'],patch_sha256=c['patch_sha256'],actual_selected_next_IDs=[],new_emulator_runs=0,all_jobs_terminal=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('IndependentV3258audit passes:4575completed preserved inV3251;next533source objects/123completed exclusions/410uncovered physical speeches verified;155next focus,zero addedreviewcredit. Fullgoalactive.')
