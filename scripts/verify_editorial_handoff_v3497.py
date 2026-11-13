"""Audit40 uncredited leads and preserve completedV3487 plus all wider scope."""
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/editorial_handoff_verification_v3497');CHECKPOINT=Path('work/analysis/next_raw_source_checkpoint_v3496')
if __name__=='__main__':
    assert not ROOT.exists();rp=CHECKPOINT/'checkpoint_receipt.json';receipt=read(rp)
    for kind in ['evidence','updated_files']:
        for p,digest in receipt[kind].items():assert sha(Path(p).read_bytes())==digest,(kind,p)
    lp=Path('translations/editorial_review_current_v1.json');ledger=read(lp);before=read(CHECKPOINT/'editorial_review_current_v1.json.before');prior=read(receipt['prior_verified_handoff']);assert sha((CHECKPOINT/'editorial_review_current_v1.json.before').read_bytes())==prior['ledger_sha256'] and sha(Path(prior['handoff_receipt']).read_bytes())==prior['handoff_receipt_sha256']
    for p,digest in read(prior['handoff_receipt'])['updated_files'].items():
        saved=CHECKPOINT/(Path(p).name+'.before');assert sha((saved if saved.exists() else Path(p)).read_bytes())==digest
    changed={'next_raw_source_leads_v3496','unfinished_editorial_scope_v3496','raw_source_coverage_revisit','coverage_units','formatting_watchlist','next_raw_source_checkpoint_v3496','latest_checkpoint'};assert all(ledger[k]==v for k,v in before.items() if k not in changed) and set(ledger)-set(before)=={'next_raw_source_leads_v3496','unfinished_editorial_scope_v3496','next_raw_source_checkpoint_v3496'}
    raw=ledger['raw_source_coverage_revisit'];oldraw=before['raw_source_coverage_revisit']
    for k,v in oldraw.items():
        if k!='next_action':assert raw[k]==v,k
    fresh=ledger['contextual_story_natural_dialogue_pass_v1871'];known={historical_key(r) for r in fresh['record_keys']};assert len(known)==4991 and (fresh['fresh_pass_records_explicitly_reread'],fresh['fresh_pass_records_integrated'],fresh['fresh_pass_records_pending_native_actual_release'])==(4991,4991,0)
    lead=ledger['next_raw_source_leads_v3496'];p=Path(lead['packet']);packet=read(p);assert sha(p.read_bytes())==lead['packet_sha256'] and packet['physical_speeches']==40 and len(packet['records'])==40 and [g['physical_speeches'] for g in packet['blocks']]==[14,26] and len({historical_key(r) for r in packet['records']})==40 and not known&{historical_key(r) for r in packet['records']}
    image,clean=NdsImage.open(packet['current_ROM']),NdsImage.open('work/clean.nds')
    for g in packet['blocks']:
        path,n=g['file_path'],g['block'];jp,en=[IlnkContainer.parse(im.read_file(path)).blocks[n] for im in [clean,image]];assert sha(jp)==g['source_block_sha256'] and sha(en)==g['current_block_sha256'] and jp[:4].hex()==g['source_header_hex']==g['current_header_hex']==en[:4].hex()
        for r in g['records']:
            s,c=r['source_reference'],r['current_reference'];a,b=bytes.fromhex(r['source_hex']),bytes.fromhex(r['current_hex']);assert jp[s['offset']:s['offset']+s['bytes']]==a and en[c['offset']:c['offset']+c['bytes']]==b and jp[s['offset']+s['bytes']]==en[c['offset']+c['bytes']]==0 and a[0]==b[0]==r['source_selector'] and jp[s['offset']-5:s['offset']+1]==en[c['offset']-5:c['offset']+1]==bytes.fromhex(r['source_complete_preamble_hex'])
            assert a[1:].decode('cp932')==r['source_Japanese'] and not r['source_prose_or_completion_credit_added']
        assert {m:sum(bytes.fromhex(r['source_hex']).count(m.encode()) for r in g['records']) for m in ['FI','FA','FO']}==g['source_macro_counts']
    assert [g['source_selectors'] for g in packet['blocks']]==[[2,9,20,171],[3,11,21,74]] and packet['blocks'][0]['source_macro_counts']=={'FI':1,'FA':0,'FO':0} and packet['blocks'][1]['source_macro_counts']=={'FI':0,'FA':0,'FO':0}
    copies=packet['nontrivial_raw_exact_copy_candidates'];assert len(copies)==1 and copies[0]['id']=='DK4_MES_B141_R0066' and copies[0]['other_block']==142 and copies[0]['other_id']=='DK4_MES_B142_R0032' and not copies[0]['other_key_previously_reviewed'];copy=IlnkContainer.parse(clean.read_file('/data/SC2.DK4')).blocks[142];at=copies[0]['other_source_offset'];value=bytes.fromhex(copies[0]['exact_source_hex']);assert copy[at:at+len(value)]==value and copy[at+len(value)]==0
    cp=Path(lead['control_finding']);control=read(cp);assert sha(cp.read_bytes())==lead['control_finding_sha256']==packet['SC3_B109_control_finding_sha256'];jp,en=[IlnkContainer.parse(im.read_file('/data/SC3.DK4')).blocks[109] for im in [clean,image]];assert jp[8:18].hex()==control['source_prefix_hex']=='00450000008084468380' and en[8:18].hex()==control['current_prefix_hex']=='00450000004a616d2020' and en[13:18]==b'Jam  '
    assert control['changed_prefix_offsets']==[13,14,15,16,17] and control['source_UI_config']==[8,0,0] and control['current_UI_config']==[4,2,2] and control['restore_owned_range']==dict(offset=8,bytes=10,source_hex=jp[8:18].hex()) and control['source_UI_resource_bodies_explicit_unexecuted'] and control['no_observed_crash_or_visible_runtime_defect_claim']
    cases=control['successful_native_cases'];assert len(cases)==4 and [(c['word'],c['native_extent']) for c in cases]==[(0x4500,6),(0x4684,4),(0x4500,6),(0x6D61,2)] and all(c['all4MiB_input_owner_canaries_and_ABI_exact'] and c['no_resource_body_or_actual_scene_execution'] for c in cases)
    a,b=[im.read_file('/__arm9__.bin') for im in [clean,image]]
    for c in cases:
        for pc,word in c['executed_native_words'].items():at=int(pc)-0x02000000;value=bytes.fromhex(word);assert a[at:at+len(value)]==b[at:at+len(value)]==value
    assert control['current_extra2020_probe']['faults'][0]['address']==0x10 and control['extra2020_isolated_missing_initialized_context_not_a_game_crash_proof'] and control['new_emulator_runs']==0
    inventory=read(ledger['unfinished_editorial_scope_v3496']['path']);oldinventory=read(before['unfinished_editorial_scope_v3491']['path'])
    for k,v in oldinventory.items():
        if k not in ['raw_source_coverage_revisit','next_focus']:assert inventory[k]==v,k
    assert inventory['incomplete_COMMON_count']==3 and inventory['incomplete_route_source_prose_count']==0 and ledger['reviewed_but_incomplete_COMMON_IDs']==[750,751,752]
    c=ledger['current_integrated_candidate'];release=read('work/analysis/lil_B139_B140_release_v3488/registered_release_verification.json');assert sha(Path(c['path']).read_bytes())==c['sha256']==release['candidate_sha256']==packet['current_ROM_sha256'] and sha(Path(c['patch']).read_bytes())==c['patch_sha256']==release['patch_sha256'] and Path(release['exact_patch_reconstruction']).read_bytes()==Path(c['path']).read_bytes()
    manifest,registry=read(c['manifest']),read('translations/release_stack.json');assert manifest['profile']==c['profile']=='all-routes-unified-v3487' and len(manifest['batches'])==525 and len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v1492' and all(manifest['checks'].values()) and manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes())
    assert ledger['goal_status']=='active' and not ledger['full_goal_complete'] and Path('docs/editorial_handoff_current.md').read_text(encoding='utf-8').startswith('# Current editorial handoff - V3496')
    ROOT.mkdir(parents=True);save(ROOT/'verified_handoff.json',dict(checkpoint='V3496',ledger=str(lp),ledger_sha256=sha(lp.read_bytes()),handoff_receipt=str(rp),handoff_receipt_sha256=sha(rp.read_bytes()),fresh_records=4991,fresh_integrated=4991,fresh_pending=0,source_prose=4994,completed_records=4991,historical_revised=3252,historical_retained=1739,new_source_prose_reviews=0,new_completed_records=0,incomplete_COMMON=3,incomplete_route=0,next_uncredited_physical_speeches=40,next_Lil_B141_speeches=14,next_Maria_SC3_B109_speeches=26,all40_exact_clean_current_speech_references_and_nonoverlap_verified=True,SC3_B109_source_packed_UI_control_restoration_required=True,SC3_B109_original_UI_configuration8_0_0_current4_2_2_and_second_opcode_loss_bound=True,source_UI_resource_bodies_and_extra2020_actual_effects_unclaimed=True,no_actual_game_crash_inferred_from_missing_isolated_context=True,prior67_completion_exact_patch31startupframes_and_current_view_preserved=True,all_wider_scope_graphics_separation_and_later_reaudit_preserved=True,candidate=c['path'],candidate_sha256=c['sha256'],patch=c['patch'],patch_sha256=c['patch_sha256'],manifest_batches=525,accepted_layers=114,actual_selected_next_IDs=[],new_emulator_runs=0,all_jobs_terminal=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('Independent V3496 audit passes:4991 completed inV3487 preserved;40 uncredited source leads andSC3B109 packed-control repair bound. No extra credit or actual crash claim;full goal active.')
