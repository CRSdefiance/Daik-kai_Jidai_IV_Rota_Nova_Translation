"""Audit uncredited next63 references,selector00 and unchanged release completion."""
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/editorial_handoff_verification_v3311')
CHECKPOINT=Path('work/analysis/lil_next63_checkpoint_v3310')
if __name__=='__main__':
    assert not ROOT.exists();rp=CHECKPOINT/'checkpoint_receipt.json';receipt=read(rp)
    for k in ['evidence','updated_files']:
        for p,digest in receipt[k].items():assert sha(Path(p).read_bytes())==digest,(k,p)
    lp=Path('translations/editorial_review_current_v1.json');ledger=read(lp);before=read(CHECKPOINT/'editorial_review_current_v1.json.before');prior=read(receipt['prior_verified_handoff']);assert sha((CHECKPOINT/'editorial_review_current_v1.json.before').read_bytes())==prior['ledger_sha256'] and sha(Path(prior['handoff_receipt']).read_bytes())==prior['handoff_receipt_sha256']
    for p,digest in read(prior['handoff_receipt'])['updated_files'].items():
        saved=CHECKPOINT/(Path(p).name+'.before');assert sha((saved if saved.exists() else Path(p)).read_bytes())==digest
    for k in ['completed_editorial_families','records_editorially_completed','records_revised_and_integrated','retained_wordings_editorially_completed','completed_editorial_record_counts_by_file','current_integrated_candidate','reviewed_but_incomplete_COMMON_IDs','reviewed_but_incomplete_route_record_IDs','unresolved_graphics_work','older_record_reaudit_after_full_editorial_goal','records_with_source_and_prose_pass','records_with_source_prose_drafts','source_prose_reviewed_counts_by_file','native_source_universe_inventory_v2701c','contextual_story_natural_dialogue_pass_v1871','lil_B122_B127_completion_v3304','active_source_prose_drafts','Proof_terminology_consistency_lead_v3286']:assert ledger[k]==before[k],k
    fresh=ledger['contextual_story_natural_dialogue_pass_v1871'];known={historical_key(r) for r in fresh['record_keys']};assert len(known)==4734 and (fresh['fresh_pass_records_explicitly_reread'],fresh['fresh_pass_records_integrated'],fresh['fresh_pass_records_pending_native_actual_release'])==(4734,4734,0)
    lead=ledger['lil_after_B127_next_source_lead_v3310'];full,nextpacket,voice,control,branch,transcript=map(read,[lead['full_packet'],lead['next_packet'],lead['voice_proof'],lead['control_proof'],lead['branch_proof'],lead['clean_transcript_proof']])
    image,clean=NdsImage.open(full['current_ROM']),NdsImage.open('work/clean.nds');en,jp=[IlnkContainer.parse(i.read_file('/data/SC2.DK4')).blocks for i in [image,clean]]
    assert [b['block'] for b in full['blocks']]==[131,133,135,136,137,138,139,140] and sum(len(b['all_clean_native_commands']) for b in full['blocks'])==547
    for b in full['blocks']:
        assert sha(jp[b['block']])==b['clean_block_sha256'] and sha(en[b['block']])==b['current_block_sha256']
        shape=lambda values:[(r['offset'],r['word'],r['native_extent'],r['ancestor_0100_offsets']) for r in values];assert shape(b['all_clean_native_commands'])==shape(b['all_current_native_commands'])
    for row in full['records']+full['typed_choice_records']:
        assert historical_key(row) not in known;b=row['block'];s,c=row['source_reference'],row['current_reference'];raw,value=bytes.fromhex(row['source_hex']),bytes.fromhex(row['current_hex'])
        assert jp[b][s['offset']:s['offset']+s['bytes']]==raw and en[b][c['offset']:c['offset']+c['bytes']]==value and jp[b][s['offset']+s['bytes']]==en[b][c['offset']+c['bytes']]==0
        if row['kind']!='typed-choice-label':
            assert raw and raw[0]==value[0]==row['source_selector'] and row['source_Japanese']==raw[1:].decode('cp932') and jp[b][s['offset']-5:s['offset']+1]==en[b][c['offset']-5:c['offset']+1]==bytes.fromhex(row['source_complete_preamble_hex'])
    assert len(full['records'])==255 and len(full['typed_choice_records'])==2 and full['completed278_source_location_speeches_excluded']==278 and len(nextpacket['records'])==61 and len(nextpacket['typed_choice_records'])==2
    assert [b['block'] for b in nextpacket['blocks']]==[131,133] and sum(len(b['all_clean_native_commands']) for b in nextpacket['blocks'])==112 and sum(r['source_selector']==0 for r in nextpacket['records'])==18
    assert voice['source00_is_static_actor0_not_empty_text_or_dynamic_role'] and len(voice['fresh_five_actor_names']['rows'])==5 and next(r for r in voice['fresh_five_actor_names']['rows'] if r['actor_ID']==0)['current_catalog_name']=='Rafael Castor'
    assert len(control['speech_dispatch_cases'])==122 and sum(c['source_selector']==0 and c['resolved_actor_ID']==0 for c in control['speech_dispatch_cases'])==36 and sum(c['source_selector']==254 for c in control['speech_dispatch_cases'])==2 and len(control['current_original_predicate_cases'])==5 and control['source_macro_counts']=={'FI':6,'FA':0,'FO':1}
    assert len(branch['cases'])==240 and len(branch['operands_requiring_adjustment_when_resizing'])==24 and transcript['whole_clean_exchange_reading_not_yet_claimed']
    for t in transcript['transcripts']:assert sha(Path(t['path']).read_bytes())==t['sha256']
    inventory=read(ledger['unfinished_editorial_scope_v3310']['path']);oldinventory=read(before['unfinished_editorial_scope_v3304']['path'])
    for k in oldinventory:
        if k!='next_focus':assert inventory[k]==oldinventory[k],k
    c=ledger['current_integrated_candidate'];release=read('work/analysis/lil_B122_B127_release_v3301/registered_release_verification.json');assert sha(Path(c['path']).read_bytes())==c['sha256']==release['candidate_sha256'] and sha(Path(c['patch']).read_bytes())==c['patch_sha256']==release['patch_sha256'] and Path(release['exact_patch_reconstruction']).read_bytes()==Path(c['path']).read_bytes()
    manifest,registry=read(c['manifest']),read('translations/release_stack.json');assert manifest['profile']==c['profile']=='all-routes-unified-v3300' and len(manifest['batches'])==519 and len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v1492' and all(manifest['checks'].values()) and manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes())
    assert ledger['goal_status']=='active' and not ledger['full_goal_complete'] and Path('docs/editorial_handoff_current.md').read_text(encoding='utf-8').startswith('# Current editorial handoff - V3310')
    ROOT.mkdir(parents=True);save(ROOT/'verified_handoff.json',dict(checkpoint='V3310',ledger=str(lp),ledger_sha256=sha(lp.read_bytes()),handoff_receipt=str(rp),handoff_receipt_sha256=sha(rp.read_bytes()),fresh_records=4734,fresh_integrated=4734,fresh_pending=0,source_prose=4737,new_source_prose_reviews=0,new_completed_records=0,completed_records=4734,historical_revised=3142,historical_retained=1592,incomplete_COMMON=3,incomplete_route=0,next_remaining_physical_speeches=255,next_remaining_typed_labels=2,next_focus_speeches=61,next_focus_typed_labels=2,next_focus_commands=112,next_focus_relative_sites=24,source00_Rafael_identity_and36_dispatch_cases_verified=True,whole_clean_exchange_editorial_review_not_yet_claimed=True,all_next_source_current_preambles_references_and_completed_exclusions_verified=True,prior159_release_completion_exactpatch_31startupframes_and_view_preserved=True,prior_ledger_and_updated_file_chains_verified=True,candidate=c['path'],candidate_sha256=c['sha256'],patch=c['patch'],patch_sha256=c['patch_sha256'],actual_selected_next_IDs=[],new_emulator_runs=0,all_jobs_terminal=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('IndependentV3310 audit passes:4734 completed preserved inV3300;next255speech/two-label leads and63 focused source/control objects verified;source00 Rafael is bound. Zero newreviewcredit;full goal active.')
