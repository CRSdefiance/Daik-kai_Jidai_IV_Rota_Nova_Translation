"""Independent source-only checkpoint audit;all prior editorial credit stays exact."""
from pathlib import Path
from copy import deepcopy
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/editorial_handoff_verification_v3078')
CHECKPOINT=Path('work/analysis/lil_Recruits_Julian_source_checkpoint_v3077')
if __name__=='__main__':
    assert not ROOT.exists();receiptpath=CHECKPOINT/'checkpoint_receipt.json';receipt=read(receiptpath)
    for kind in ['evidence','updated_files']:
        for p,digest in receipt[kind].items():assert sha(Path(p).read_bytes())==digest,(kind,p)
    lp=Path('translations/editorial_review_current_v1.json');ledger=read(lp);backup=CHECKPOINT/'editorial_review_current_v1.json.before';before=read(backup)
    oldproof=read(receipt['prior_verified_handoff']);assert sha(backup.read_bytes())==oldproof['ledger_sha256']
    assert sha(Path(oldproof['handoff_receipt']).read_bytes())==oldproof['handoff_receipt_sha256']
    for p,digest in read(oldproof['handoff_receipt'])['updated_files'].items():
        saved=CHECKPOINT/(Path(p).name+'.before');assert sha((saved if saved.exists() else Path(p)).read_bytes())==digest
    restored=deepcopy(ledger)
    for key in ['lil_Recruits_Julian_clean_source_lead_v3077','unfinished_editorial_scope_v3077']:restored.pop(key)
    restored['latest_checkpoint']=before['latest_checkpoint'];assert restored==before
    fresh=ledger['contextual_story_natural_dialogue_pass_v1871'];assert (fresh['fresh_pass_records_explicitly_reread'],fresh['fresh_pass_records_integrated'],fresh['fresh_pass_records_pending_native_actual_release'])==(3791,3791,0)
    assert ledger['records_editorially_completed']==3791 and ledger['records_revised_and_integrated']==2642 and ledger['retained_wordings_editorially_completed']==1149
    assert ledger['records_with_source_and_prose_pass']==ledger['records_with_source_prose_drafts']==sum(ledger['source_prose_reviewed_counts_by_file'].values())==3794
    lead=ledger['lil_Recruits_Julian_clean_source_lead_v3077'];source=read(lead['source_context']);branch=read(lead['branch_proof']);control=read(lead['control_contract']);context=read(lead['whole_exchange_context_notes']);terms=read(lead['terminology_reconciliation'])
    assert (source['total_editorial_objects'],source['speech_objects'],source['typed_choice_labels'])==(199,197,2)
    assert [b['block'] for b in source['blocks']]==[75,76,77,78,79]
    assert sum(len(b['all_clean_native_commands']) for b in source['blocks'])==372 and len(branch['cases'])==680 and len(branch['operands_requiring_adjustment_when_resizing'])==68
    assert len(control['dispatch_cases'])==394 and len(control['current_original_predicate_cases'])==16 and control['original_event_queries']==[]
    assert context['all197_complete_clean_Japanese_speeches_and2_typed_choices_read_before_old_English_comparison'] and context['nontext_B80_neighbor']['editorial_credit']==0
    assert terms['approved_item_name']=='Silla Gold Crown' and terms['current_shipyard_menu_evidence']['visible_labels']==['Dock','Remodel']
    image,clean=NdsImage.open(source['current_ROM']),NdsImage.open('work/clean.nds');en,jp=[IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks for im in [image,clean]]
    known={(r['file_path'],r['id']) for r in fresh['record_keys']};rows=source['records']+source['typed_choice_records'];assert len(rows)==len({r['id'] for r in rows})==199
    assert not known&{(r['file_path'],r['id']) for r in rows}
    for r in rows:
        b=r['block'];sr,cr=r['source_reference'],r['current_reference']
        assert jp[b][sr['offset']:sr['offset']+sr['bytes']]==bytes.fromhex(r['source_hex']) and en[b][cr['offset']:cr['offset']+cr['bytes']]==bytes.fromhex(r['current_hex'])
        if r['kind']!='typed-choice-label':assert jp[b][sr['offset']-5:sr['offset']+1]==en[b][cr['offset']-5:cr['offset']+1]==bytes.fromhex(r['source_complete_preamble_hex'])
    candidate=ledger['current_integrated_candidate'];release=read('work/analysis/lil_Christina_Mivor_release_v3067/registered_release_verification.json')
    assert sha(Path(candidate['path']).read_bytes())==candidate['sha256']==source['current_ROM_sha256']==release['candidate_sha256']
    assert sha(Path(candidate['patch']).read_bytes())==candidate['patch_sha256']==release['patch_sha256']
    assert Path(release['exact_patch_reconstruction']).read_bytes()==Path(candidate['path']).read_bytes() and release['whole_ROM_reconstruction_byte_exact']
    manifest,registry=read(candidate['manifest']),read('translations/release_stack.json')
    assert manifest['profile']==candidate['profile']=='all-routes-unified-v3066' and len(manifest['batches'])==508 and all(manifest['checks'].values())
    assert manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes()) and len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v1492'
    startup=read('work/analysis/lil_Christina_Mivor_startup_v3069/cold_boot_Lil_startup_town_verification.json');assert startup['candidate_sha256']==candidate['sha256'] and startup['paired_frame_count']==31 and startup['all_current_requested_and_final_framebuffers_equal_V3029']
    assert sha(Path(startup['review_sheet']).read_bytes())==startup['review_sheet_sha256']
    inventory=read(ledger['unfinished_editorial_scope_v3077']['path']);priorinventory=read(before['unfinished_editorial_scope_v3070']['path']);check=deepcopy(inventory)
    check.pop('next_clean_only_uncredited_recruits_Julian_scope_v3077');check['next_focus']=priorinventory['next_focus'];assert check==priorinventory
    assert ledger['reviewed_but_incomplete_COMMON_IDs']==[750,751,752] and not any(ledger['reviewed_but_incomplete_route_record_IDs'].values())
    assert ledger['goal_status']=='active' and not ledger['full_goal_complete'] and Path('docs/editorial_handoff_current.md').read_text(encoding='utf8').startswith('# Current editorial handoff - V3077')
    ROOT.mkdir(parents=True);save(ROOT/'verified_handoff.json',dict(checkpoint='V3077',ledger=str(lp),ledger_sha256=sha(lp.read_bytes()),handoff_receipt=str(receiptpath),handoff_receipt_sha256=sha(receiptpath.read_bytes()),
        prior_completed_checkpoint='V3070',completed_records=3791,historical_revised=2642,historical_retained=1149,source_prose=3794,fresh_records=3791,fresh_integrated=3791,fresh_pending=0,
        next_uncredited_clean_source_objects=199,next_uncredited_speeches=197,next_uncredited_choice_labels=2,new_source_prose_reviews=0,new_completed_records=0,
        all199_exact_clean_current_references_and_source_native_contracts_verified=True,previous_editorial_counts_keys_and_completed_families_byte_equivalent=True,
        whole_clean_input_reconstruction_exact=True,manifest_batches=508,accepted_layers=114,current_gameplay_frame_pairs=31,
        candidate=candidate['path'],candidate_sha256=candidate['sha256'],patch=candidate['patch'],patch_sha256=candidate['patch_sha256'],all_jobs_terminal=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('IndependentV3077audit passes:3791completed/3794source-prose unchanged;199next-source objects uncredited. V3066/exactpatch/current31framepairs preserved;fullgoalactive.')
