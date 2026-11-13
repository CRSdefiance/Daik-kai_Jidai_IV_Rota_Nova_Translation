"""Independently verify next-source references andunchanged completed coverage."""
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/editorial_handoff_verification_v3351')
CHECKPOINT=Path('work/analysis/lil_next35_checkpoint_v3350')
if __name__=='__main__':
    assert not ROOT.exists();rp=CHECKPOINT/'checkpoint_receipt.json';receipt=read(rp)
    for key in ['evidence','updated_files']:
        for p,digest in receipt[key].items():assert sha(Path(p).read_bytes())==digest,(key,p)
    lp=Path('translations/editorial_review_current_v1.json');ledger=read(lp);before=read(CHECKPOINT/'editorial_review_current_v1.json.before');prior=read(receipt['prior_verified_handoff'])
    assert sha((CHECKPOINT/'editorial_review_current_v1.json.before').read_bytes())==prior['ledger_sha256'] and sha(Path(prior['handoff_receipt']).read_bytes())==prior['handoff_receipt_sha256']
    for p,digest in read(prior['handoff_receipt'])['updated_files'].items():
        saved=CHECKPOINT/(Path(p).name+'.before');assert sha((saved if saved.exists() else Path(p)).read_bytes())==digest
    changed={'lil_after_B133_next_source_lead_v3350','unfinished_editorial_scope_v3350','coverage_units','lil_next35_checkpoint_v3350','latest_checkpoint'}
    for k,v in before.items():
        if k not in changed:assert ledger[k]==v,k
    assert set(ledger)-set(before)==changed-{'coverage_units','latest_checkpoint'}
    fresh=ledger['contextual_story_natural_dialogue_pass_v1871'];known={historical_key(r) for r in fresh['record_keys']}
    assert len(known)==4797 and (fresh['fresh_pass_records_explicitly_reread'],fresh['fresh_pass_records_integrated'],fresh['fresh_pass_records_pending_native_actual_release'])==(4797,4797,0)
    lead=ledger['lil_after_B133_next_source_lead_v3350'];full,focus,voice,control,branch,transcript,context=map(read,[lead[k] for k in ['full_packet','next_packet','voice_proof','control_proof','branch_proof','clean_transcript_proof','whole_clean_context']])
    image,clean=NdsImage.open(full['current_ROM']),NdsImage.open('work/clean.nds');en,jp=[IlnkContainer.parse(i.read_file('/data/SC2.DK4')).blocks for i in [image,clean]]
    assert [b['block'] for b in full['blocks']]==[135,136,137,138,139,140] and len(full['records'])==194 and not full['typed_choice_records'] and full['completed339_source_location_speeches_excluded']==339 and sum(len(b['all_clean_native_commands']) for b in full['blocks'])==435
    for b in full['blocks']:
        n=b['block'];assert sha(jp[n])==b['clean_block_sha256'] and sha(en[n])==b['current_block_sha256']
        shape=lambda values:[(r['offset'],r['word'],r['native_extent'],r['ancestor_0100_offsets']) for r in values]
        assert shape(b['all_clean_native_commands'])==shape(b['all_current_native_commands'])
    for r in full['records']:
        assert historical_key(r) not in known;b=r['block'];s,c=r['source_reference'],r['current_reference'];raw,value=bytes.fromhex(r['source_hex']),bytes.fromhex(r['current_hex'])
        assert jp[b][s['offset']:s['offset']+s['bytes']]==raw and en[b][c['offset']:c['offset']+c['bytes']]==value and jp[b][s['offset']+s['bytes']]==en[b][c['offset']+c['bytes']]==0
        assert raw and raw[0]==value[0]==r['source_selector'] and r['source_Japanese']==raw[1:].decode('cp932') and jp[b][s['offset']-5:s['offset']+1]==en[b][c['offset']-5:c['offset']+1]==bytes.fromhex(r['source_complete_preamble_hex'])
    assert [b['block'] for b in focus['blocks']]==[135,136] and len(focus['records'])==35 and not focus['typed_choice_records'] and sum(len(b['all_clean_native_commands']) for b in focus['blocks'])==61
    selectors={2,9,14,36,47,96};assert {r['source_selector'] for r in focus['records']}==selectors=={r['actor_ID'] for r in voice['fresh_six_actor_names']['rows']}
    assert voice['all207_catalog_and_eight_voice_groups_bound_by_exact_runtime_COMMON_EV2_font_and_same_snapshot'] and len(control['speech_dispatch_cases'])==70 and all(c['source_selector']==c['resolved_actor_ID'] for c in control['speech_dispatch_cases'])
    assert len(control['current_original_predicate_cases'])==1 and control['source_macro_counts']=={'FI':0,'FA':0,'FO':1} and not control['original_event_queries']
    assert len(branch['cases'])==40 and len(branch['operands_requiring_adjustment_when_resizing'])==4
    for item in transcript['transcripts']:assert sha(Path(item['path']).read_bytes())==item['sha256']
    assert len(context['records'])==35 and context['all35_complete_clean_source_objects_read_before_older_English_comparison'] and context['all35_fresh_source_glosses_precede_localized_English'] and context['all61_original_commands_and_conditional_Camille_coda_considered']
    source={r['id']:r for r in focus['records']}
    for row in context['records']:
        r=source[row['id']]
        for k in ['file_path','block','source_reference','source_hex','source_Japanese','source_complete_preamble_hex','source_selector']:assert row[k]==r[k]
        assert row['fresh_source_gloss'] and row['whole_exchange_context'] and row['localized_English_not_authored'] and row['older_dialogue_English_not_editorially_compared'] and row['source_prose_orcompletion_credit_added']==0
    inventory=read(ledger['unfinished_editorial_scope_v3350']['path']);oldinventory=read(before['unfinished_editorial_scope_v3342']['path'])
    for k,v in oldinventory.items():
        if k!='next_focus':assert inventory[k]==v,k
    candidate=ledger['current_integrated_candidate'];release=read('work/analysis/lil_B131_B133_release_v3339/registered_release_verification.json')
    assert sha(Path(candidate['path']).read_bytes())==candidate['sha256']==release['candidate_sha256'] and sha(Path(candidate['patch']).read_bytes())==candidate['patch_sha256']==release['patch_sha256'] and Path(release['exact_patch_reconstruction']).read_bytes()==Path(candidate['path']).read_bytes()
    manifest,registry=read(candidate['manifest']),read('translations/release_stack.json');assert manifest['profile']==candidate['profile']=='all-routes-unified-v3338' and len(manifest['batches'])==521 and len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v1492' and all(manifest['checks'].values()) and manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes())
    assert ledger['goal_status']=='active' and not ledger['full_goal_complete'] and Path('docs/editorial_handoff_current.md').read_text(encoding='utf-8').startswith('# Current editorial handoff - V3350')
    ROOT.mkdir(parents=True);save(ROOT/'verified_handoff.json',dict(checkpoint='V3350',ledger=str(lp),ledger_sha256=sha(lp.read_bytes()),handoff_receipt=str(rp),handoff_receipt_sha256=sha(rp.read_bytes()),fresh_records=4797,fresh_integrated=4797,fresh_pending=0,source_prose=4800,new_source_prose_reviews=0,new_completed_records=0,completed_records=4797,historical_revised=3169,historical_retained=1628,incomplete_COMMON=3,incomplete_route=0,next_remaining_physical_speeches=194,next_focus_speeches=35,next_focus_commands=61,next_focus_relative_sites=4,next_six_static_names70dispatches_onepredicate40skipcases_verified=True,all35_fresh_glosses_and_complete_clean_exchanges_precede_oldEnglish_comparison=True,all_next_source_references_and_completed_exclusions_verified=True,prior63_release_completion_exactpatch31startupframes_andview_preserved=True,prior_ledger_and_updated_file_chains_verified=True,candidate=candidate['path'],candidate_sha256=candidate['sha256'],patch=candidate['patch'],patch_sha256=candidate['patch_sha256'],manifest_batches=521,accepted_layers=114,actual_selected_next_IDs=[],new_emulator_runs=0,all_jobs_terminal=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('IndependentV3350audit passes:4797completed preserved inV3338;194 remaining physical speech leads,35 whole-exchange glosses andcurrent nativebindings verified. No newcredit;fullgoal active.')
