"""Audit the uncredited B138-B140 refresh and preserve completed V3416 coverage."""
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/editorial_handoff_verification_v3424')
CHECKPOINT=Path('work/analysis/lil_next44_checkpoint_v3423')
if __name__=='__main__':
    assert not ROOT.exists();rp=CHECKPOINT/'checkpoint_receipt.json';receipt=read(rp)
    for k in ['evidence','updated_files']:
        for p,digest in receipt[k].items():assert sha(Path(p).read_bytes())==digest,(k,p)
    lp=Path('translations/editorial_review_current_v1.json');ledger=read(lp);before=read(CHECKPOINT/'editorial_review_current_v1.json.before');prior=read(receipt['prior_verified_handoff'])
    assert sha((CHECKPOINT/'editorial_review_current_v1.json.before').read_bytes())==prior['ledger_sha256'] and sha(Path(prior['handoff_receipt']).read_bytes())==prior['handoff_receipt_sha256']
    for p,digest in read(prior['handoff_receipt'])['updated_files'].items():
        saved=CHECKPOINT/(Path(p).name+'.before');assert sha((saved if saved.exists() else Path(p)).read_bytes())==digest
    changed={'lil_after_B137_next_source_lead_v3423','unfinished_editorial_scope_v3423','coverage_units','lil_next44_checkpoint_v3423','latest_checkpoint'}
    for k,v in before.items():
        if k not in changed:assert ledger[k]==v,k
    assert set(ledger)-set(before)==changed-{'coverage_units','latest_checkpoint'}
    fresh=ledger['contextual_story_natural_dialogue_pass_v1871'];known={historical_key(r) for r in fresh['record_keys']}
    assert len(known)==4880 and (fresh['fresh_pass_records_explicitly_reread'],fresh['fresh_pass_records_integrated'],fresh['fresh_pass_records_pending_native_actual_release'])==(4880,4880,0)
    lead=ledger['lil_after_B137_next_source_lead_v3423'];full,focus=map(read,[lead['full_packet'],lead['next_packet']]);image,clean=NdsImage.open(full['current_ROM']),NdsImage.open('work/clean.nds')
    en,jp=[IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks for im in [image,clean]]
    assert [b['block'] for b in full['blocks']]==[138,139,140] and len(full['records'])==111 and full['completed422_source_location_speeches_excluded']==422
    assert sum(len(b['all_clean_native_commands']) for b in full['blocks'])==257
    physical=read('work/analysis/lil_after_B119_clean_scope_v3257c/complete_clean_next_exchange_inventory.json');oldrows=[r for b in physical['blocks'] for r in b['records']]
    assert len(oldrows)==533 and {historical_key(r) for r in oldrows if historical_key(r) not in known}=={historical_key(r) for r in full['records']} and len(full['records'])==len({historical_key(r) for r in full['records']})
    for b in full['blocks']:
        n=b['block'];assert sha(jp[n])==b['clean_block_sha256'] and sha(en[n])==b['current_block_sha256']
        shape=lambda values:[(r['offset'],r['word'],r['native_extent'],r['ancestor_0100_offsets']) for r in values];assert shape(b['all_clean_native_commands'])==shape(b['all_current_native_commands'])
    for r in full['records']:
        assert historical_key(r) not in known;b=r['block'];s,c=r['source_reference'],r['current_reference'];raw,value=bytes.fromhex(r['source_hex']),bytes.fromhex(r['current_hex'])
        assert jp[b][s['offset']:s['offset']+s['bytes']]==raw and en[b][c['offset']:c['offset']+c['bytes']]==value and jp[b][s['offset']+s['bytes']]==en[b][c['offset']+c['bytes']]==0
        assert raw[0]==value[0]==r['source_selector'] and r['source_Japanese']==raw[1:].decode('cp932')
        assert jp[b][s['offset']-5:s['offset']+1]==en[b][c['offset']-5:c['offset']+1]==bytes.fromhex(r['source_complete_preamble_hex'])
    assert len(focus['records'])==44 and [b['block'] for b in focus['blocks']]==[138]
    commands=focus['blocks'][0]['all_clean_native_commands'];assert len(commands)==111 and sum(c['word'] in [0x100,0x200,0x300,0x400] for c in commands)==45 and sum(c['word']==0x8000 for c in commands)==10 and sum(c['word']==0x8100 for c in commands)==1
    assert len({r['source_selector'] for r in focus['records']})==7 and {m:sum(bytes.fromhex(r['source_hex']).count(m.encode()) for r in focus['records']) for m in ['FI','FA','FO']}=={'FI':0,'FA':0,'FO':1}
    assert all(r['kind']=='progressive' and r['source_selector']!=0 for r in focus['records']) and not any(c['word'] in [0x2000,0x2100,0x4100] for c in commands)
    assert lead['current_actor_voice_entry_and_macro_binding_pending'] and lead['current_original_event_query_binding_pending'] and lead['whole_clean_exchange_and_fresh_glosses_and_oldEnglish_comparison_pending']
    inventory=read(ledger['unfinished_editorial_scope_v3423']['path']);oldinventory=read(before['unfinished_editorial_scope_v3420']['path'])
    for k,v in oldinventory.items():
        if k!='next_focus':assert inventory[k]==v,k
    c=ledger['current_integrated_candidate'];release=read('work/analysis/lil_B137_release_v3417/registered_release_verification.json')
    assert sha(Path(c['path']).read_bytes())==c['sha256']==release['candidate_sha256']==full['current_ROM_sha256'] and sha(Path(c['patch']).read_bytes())==c['patch_sha256']==release['patch_sha256']
    assert Path(release['exact_patch_reconstruction']).read_bytes()==Path(c['path']).read_bytes()
    manifest,registry=read(c['manifest']),read('translations/release_stack.json')
    assert manifest['profile']==c['profile']=='all-routes-unified-v3416' and len(manifest['batches'])==523 and len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v1492'
    assert all(manifest['checks'].values()) and manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes())
    assert ledger['goal_status']=='active' and not ledger['full_goal_complete'] and Path('docs/editorial_handoff_current.md').read_text(encoding='utf-8').startswith('# Current editorial handoff - V3423')
    ROOT.mkdir(parents=True);save(ROOT/'verified_handoff.json',dict(checkpoint='V3423',ledger=str(lp),ledger_sha256=sha(lp.read_bytes()),handoff_receipt=str(rp),handoff_receipt_sha256=sha(rp.read_bytes()),fresh_records=4880,fresh_integrated=4880,fresh_pending=0,source_prose=4883,completed_records=4880,historical_revised=3207,historical_retained=1673,new_source_prose_reviews=0,new_completed_records=0,incomplete_COMMON=3,incomplete_route=0,next_remaining_physical_speeches=111,next_focus_speeches=44,next_focus_commands=111,next_focus_relative_sites=45,next_focus_predicates=10,next_focus_event_queries=1,next_focus_macro_counts={'FI':0,'FA':0,'FO':1},all_source_current_preambles_and_completed_exclusions_verified=True,next_actors_entry_query_whole_context_and_glosses_still_pending=True,prior48_release_completion_exactpatch31startupframes_and_view_preserved=True,prior_ledger_and_updated_file_chains_verified=True,candidate=c['path'],candidate_sha256=c['sha256'],patch=c['patch'],patch_sha256=c['patch_sha256'],manifest_batches=523,accepted_layers=114,actual_selected_next_IDs=[],new_emulator_runs=0,all_jobs_terminal=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('Independent V3423 audit passes:4880 completed preserved in V3416;111 physical source leads,next B138 44 speeches/111 commands/one query. Zero new credit;full goal active.')
