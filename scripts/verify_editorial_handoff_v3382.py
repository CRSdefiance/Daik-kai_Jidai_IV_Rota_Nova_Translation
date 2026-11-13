"""Audit refreshed159 source leads andunchanged completed cumulative release."""
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/editorial_handoff_verification_v3382');CHECKPOINT=Path('work/analysis/lil_next48_checkpoint_v3381')
if __name__=='__main__':
    assert not ROOT.exists();rp=CHECKPOINT/'checkpoint_receipt.json';receipt=read(rp)
    for k in ['evidence','updated_files']:
        for p,digest in receipt[k].items():assert sha(Path(p).read_bytes())==digest,(k,p)
    lp=Path('translations/editorial_review_current_v1.json');ledger=read(lp);before=read(CHECKPOINT/'editorial_review_current_v1.json.before');prior=read(receipt['prior_verified_handoff'])
    assert sha((CHECKPOINT/'editorial_review_current_v1.json.before').read_bytes())==prior['ledger_sha256'] and sha(Path(prior['handoff_receipt']).read_bytes())==prior['handoff_receipt_sha256']
    for p,digest in read(prior['handoff_receipt'])['updated_files'].items():
        saved=CHECKPOINT/(Path(p).name+'.before');assert sha((saved if saved.exists() else Path(p)).read_bytes())==digest
    changed={'lil_after_B136_next_source_lead_v3381','unfinished_editorial_scope_v3381','coverage_units','lil_next48_checkpoint_v3381','latest_checkpoint'}
    for k,v in before.items():
        if k not in changed:assert ledger[k]==v,k
    assert set(ledger)-set(before)==changed-{'coverage_units','latest_checkpoint'}
    fresh=ledger['contextual_story_natural_dialogue_pass_v1871'];known={historical_key(r) for r in fresh['record_keys']};assert len(known)==4832 and (fresh['fresh_pass_records_explicitly_reread'],fresh['fresh_pass_records_integrated'],fresh['fresh_pass_records_pending_native_actual_release'])==(4832,4832,0)
    lead=ledger['lil_after_B136_next_source_lead_v3381'];full,focus=map(read,[lead['full_packet'],lead['next_packet']]);image,clean=NdsImage.open(full['current_ROM']),NdsImage.open('work/clean.nds');en,jp=[IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks for im in [image,clean]]
    assert [b['block'] for b in full['blocks']]==[137,138,139,140] and len(full['records'])==159 and full['completed374_source_location_speeches_excluded']==374 and sum(len(b['all_clean_native_commands']) for b in full['blocks'])==374
    physical=read('work/analysis/lil_after_B119_clean_scope_v3257c/complete_clean_next_exchange_inventory.json');oldrows=[r for b in physical['blocks'] for r in b['records']];assert len(oldrows)==533 and {historical_key(r) for r in oldrows if historical_key(r) not in known}=={historical_key(r) for r in full['records']}
    for b in full['blocks']:
        n=b['block'];assert sha(jp[n])==b['clean_block_sha256'] and sha(en[n])==b['current_block_sha256'];shape=lambda values:[(r['offset'],r['word'],r['native_extent'],r['ancestor_0100_offsets']) for r in values];assert shape(b['all_clean_native_commands'])==shape(b['all_current_native_commands'])
    for r in full['records']:
        assert historical_key(r) not in known;b=r['block'];s,c=r['source_reference'],r['current_reference'];raw,value=bytes.fromhex(r['source_hex']),bytes.fromhex(r['current_hex'])
        assert jp[b][s['offset']:s['offset']+s['bytes']]==raw and en[b][c['offset']:c['offset']+c['bytes']]==value and jp[b][s['offset']+s['bytes']]==en[b][c['offset']+c['bytes']]==0 and raw[0]==value[0]==r['source_selector']
        assert r['source_Japanese']==raw[1:].decode('cp932') and jp[b][s['offset']-5:s['offset']+1]==en[b][c['offset']-5:c['offset']+1]==bytes.fromhex(r['source_complete_preamble_hex'])
    assert len(focus['records'])==48 and [b['block'] for b in focus['blocks']]==[137];commands=focus['blocks'][0]['all_clean_native_commands'];assert len(commands)==117 and sum(c['word'] in [0x100,0x200,0x300,0x400] for c in commands)==48 and sum(c['word']==0x8000 for c in commands)==12 and len({r['source_selector'] for r in focus['records']})==11
    assert {m:sum(bytes.fromhex(r['source_hex']).count(m.encode()) for r in focus['records']) for m in ['FI','FA','FO']}=={'FI':3,'FA':0,'FO':0}
    assert lead['current_actor_voice_entry_and_macro_binding_pending'] and lead['whole_clean_exchange_and_fresh_glosses_and_oldEnglish_comparison_pending']
    inventory=read(ledger['unfinished_editorial_scope_v3381']['path']);oldinventory=read(before['unfinished_editorial_scope_v3376']['path'])
    for k,v in oldinventory.items():
        if k!='next_focus':assert inventory[k]==v,k
    c=ledger['current_integrated_candidate'];release=read('work/analysis/lil_B135_B136_release_v3373/registered_release_verification.json');assert sha(Path(c['path']).read_bytes())==c['sha256']==release['candidate_sha256'] and sha(Path(c['patch']).read_bytes())==c['patch_sha256']==release['patch_sha256'] and Path(release['exact_patch_reconstruction']).read_bytes()==Path(c['path']).read_bytes()
    manifest,registry=read(c['manifest']),read('translations/release_stack.json');assert manifest['profile']==c['profile']=='all-routes-unified-v3372' and len(manifest['batches'])==522 and len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v1492' and all(manifest['checks'].values()) and manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes())
    assert ledger['goal_status']=='active' and not ledger['full_goal_complete'] and Path('docs/editorial_handoff_current.md').read_text(encoding='utf-8').startswith('# Current editorial handoff - V3381')
    ROOT.mkdir(parents=True);save(ROOT/'verified_handoff.json',dict(checkpoint='V3381',ledger=str(lp),ledger_sha256=sha(lp.read_bytes()),handoff_receipt=str(rp),handoff_receipt_sha256=sha(rp.read_bytes()),fresh_records=4832,fresh_integrated=4832,fresh_pending=0,source_prose=4835,completed_records=4832,historical_revised=3185,historical_retained=1647,new_source_prose_reviews=0,new_completed_records=0,incomplete_COMMON=3,incomplete_route=0,next_remaining_physical_speeches=159,next_focus_speeches=48,next_focus_commands=117,next_focus_relative_sites=48,next_focus_predicates=12,next_focus_macro_counts={'FI':3,'FA':0,'FO':0},all_source_current_preambles_and_completed_exclusions_verified=True,next_actors_entry_whole_context_and_glosses_still_pending=True,prior35_release_completion_exactpatch31startupframes_andview_preserved=True,prior_ledger_and_updated_file_chains_verified=True,candidate=c['path'],candidate_sha256=c['sha256'],patch=c['patch'],patch_sha256=c['patch_sha256'],manifest_batches=522,accepted_layers=114,actual_selected_next_IDs=[],new_emulator_runs=0,all_jobs_terminal=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('IndependentV3381audit passes:4832completed preserved inV3372;159remainingphysicalsourceleads,nextB13748speech/117commands verified. No newcredit;fullgoal active.')
