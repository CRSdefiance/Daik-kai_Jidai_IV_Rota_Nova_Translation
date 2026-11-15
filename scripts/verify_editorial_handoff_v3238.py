"""Independently audit V3237 references, credits, canonical scope and native proofs."""
from collections import Counter
from pathlib import Path
from dk4tool.dialogue.lil_B111_B119_profile import profile_for
from dk4tool.dialogue.lil_B111_B119_layout_v2 import encode_relocatable_dialogue,audit_relocatable_dialogue_record,DEPENDENCIES
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/editorial_handoff_verification_v3238')
CHECKPOINT=Path('work/analysis/lil_B111_B119_checkpoint_v3237')
if __name__=='__main__':
    assert not ROOT.exists()
    rp=CHECKPOINT/'checkpoint_receipt.json';receipt=read(rp)
    for group in ['evidence','updated_files']:
        for p,digest in receipt[group].items():assert sha(Path(p).read_bytes())==digest,(group,p)
    lp=Path('translations/editorial_review_current_v1.json');ledger=read(lp);before=read(CHECKPOINT/'editorial_review_current_v1.json.before')
    prior=read(receipt['prior_verified_handoff'])
    assert sha((CHECKPOINT/'editorial_review_current_v1.json.before').read_bytes())==prior['ledger_sha256']
    assert sha(Path(prior['handoff_receipt']).read_bytes())==prior['handoff_receipt_sha256']
    for p,digest in read(prior['handoff_receipt'])['updated_files'].items():
        saved=CHECKPOINT/(Path(p).name+'.before');assert sha((saved if saved.exists() else Path(p)).read_bytes())==digest
    fresh=ledger['contextual_story_natural_dialogue_pass_v1871'];old=before['contextual_story_natural_dialogue_pass_v1871']
    doc,voice=map(read,[fresh['latest_contextual_manuscript'],fresh['latest_contextual_actor_style_draft']]);rows=doc['records']+voice['records']
    for d in [doc,voice]:validate_natural_dialogue_batch(d)
    selected={historical_key(r) for r in rows};keys={historical_key(r) for r in fresh['record_keys']};oldkeys={historical_key(r) for r in old['record_keys']}
    integrated={historical_key(r) for r in fresh['integrated_record_keys']};pending={historical_key(r) for r in fresh['pending_record_keys']}
    complete={historical_key(r) for g in ledger['completed_editorial_families'] for r in g['records']}
    assert len(rows)==len(selected)==150 and keys-oldkeys==selected==pending and oldkeys==integrated==complete
    assert keys==integrated|pending and not integrated&pending
    assert len(keys)==len(fresh['record_keys'])==len(fresh['record_IDs'])==4575
    assert (fresh['fresh_pass_records_explicitly_reread'],fresh['fresh_pass_records_integrated'],fresh['fresh_pass_records_pending_native_actual_release'])==(4575,4425,150)
    assert Counter(p for p,k in keys)=={'/COMMON/MESFILE.DK4':1599,'/data/SC2.DK4':2748,'/data/SC0.DK4':117,'/data/SC1.DK4':73,'/data/SC3.DK4':38}
    assert ledger['records_with_source_and_prose_pass']==ledger['records_with_source_prose_drafts']==sum(ledger['source_prose_reviewed_counts_by_file'].values())==4578
    assert (ledger['records_editorially_completed'],ledger['records_revised_and_integrated'],ledger['retained_wordings_editorially_completed'])==(4425,3040,1385)
    for k in ['completed_editorial_families','completed_editorial_record_counts_by_file','current_integrated_candidate','reviewed_but_incomplete_COMMON_IDs','unresolved_graphics_work','older_record_reaudit_after_full_editorial_goal','native_source_universe_inventory_v2701c','lil_B111_B119_next_source_lead_v3214']:
        assert ledger[k]==before[k],k
    assert ledger['reviewed_but_incomplete_COMMON_IDs']==[750,751,752]
    assert set(ledger['reviewed_but_incomplete_route_record_IDs']['/data/SC2.DK4'])=={k for p,k in selected}
    assert Counter(r['editorial_decision'] for r in rows)=={'revise':47,'retain-wording':103}
    for row in rows:
        assert not any(t in row['english'] for t in ['{LB','{ALIGN','{PAD'])
        if row['editorial_decision']=='retain-wording':assert row['english'].split('}',1)[1]==row['effective_predecessor_paragraph'] and row['fresh_retained_wording_justification']
    image,clean=NdsImage.open(doc['current_ROM']),NdsImage.open('work/clean.nds');arm=image.read_file('/__arm9__.bin')
    en,jp=[IlnkContainer.parse(i.read_file('/data/SC2.DK4')).blocks for i in [image,clean]]
    merged=read(doc['native_font_proof']);assert sha(Path(doc['native_font_proof']).read_bytes())==doc['native_font_proof_sha256']
    cases={c['id']:c for c in merged['cases']}
    assert len(cases)==150 and merged['current_original_macro_alignment_calls']==1200
    assert len(merged['source_bound_formatter_negatives'])==28 and all(n['rejected'] for n in merged['source_bound_formatter_negatives'])
    assert len(merged['source_consumer_negative_controls'])==43 and all(n['rejected'] for n in merged['source_consumer_negative_controls'])
    assert len(merged['all20_review_sheets'])==20
    for s in merged['all20_review_sheets']:assert sha(Path(s['path']).read_bytes())==s['sha256']
    for p,digest in merged['evidence'].items():assert sha(Path(p).read_bytes())==digest
    for r in rows:
        b=r['block'];sr,cr=r['source_reference'],r['current_reference']
        assert jp[b][sr['offset']:sr['offset']+sr['bytes']]==bytes.fromhex(r['source_hex'])
        assert en[b][cr['offset']:cr['offset']+cr['bytes']]==bytes.fromhex(r['current_hex'])
        assert jp[b][sr['offset']+sr['bytes']]==en[b][cr['offset']+cr['bytes']]==0
        isvoice=r['kind']=='typed-4100-actor-style-alternative';raw=bytes.fromhex(r['source_hex'])
        if isvoice:
            raw=bytes.fromhex(r['virtual_formatter_prefix_hex'])+raw
            at=r['command_offset'];assert jp[b][at+19]==en[b][at+19]==raw[0]==r['source_selector']
        else:assert jp[b][sr['offset']-5:sr['offset']+1]==en[b][cr['offset']-5:cr['offset']+1]==bytes.fromhex(r['source_complete_preamble_hex'])
        p=profile_for(arm,en[b],'FE-paper' if r['kind']=='system-FE' else 'progressive');encoded=encode_relocatable_dialogue(raw,r['english'],p)
        assert encoded.encoded.hex()==r['compiled_hex']==cases[r['id']]['encoded_hex']
        if isvoice:assert encoded.encoded[1:].hex()==r['compiled_stored_alternative_hex'] and r['virtual_formatter_prefix_is_not_part_of_stored_alternative_text']
        qa=audit_relocatable_dialogue_record(raw,r['english'],p)
        assert not [i for i in qa['issues'] if i['severity'] in ['warning','error'] and i['code'] not in r.get('qa_waivers',[])]
        assert sha(Path(cases[r['id']]['preview']).read_bytes())==cases[r['id']]['preview_sha256']
    assert sum(len(r['style_indices']) for r in voice['records'])==48 and len({(r['block'],r['command_offset']) for r in voice['records']})==6
    assert {r['virtual_formatter_prefix_hex'] for r in voice['records']}=={'d0','d1','d6','d7','dc'}
    assert sum(bool(r.get('qa_waivers')) for r in rows)==46
    source=read(doc['source_context']);classification=read(doc['appended_copy_classification'])
    assert source['total_editorial_objects']==150 and source['total_stored_physical_source_objects_including_unreachable_copies']==182
    assert source['total_stored_physical_speeches_including_unreachable_copies']==148 and len(source['unowned_appended_Maria_copy_records'])==32
    assert sum(len(b['all_clean_native_commands']) for b in source['blocks'])==305
    assert classification['all12_original_VM_return0_cases_stop_before_cursor_advance'] and classification['all_original_prefix_branch_results_cannot_reach_appended_SC0_SC1_SC2_copies']
    assert classification['ordinary_SC3_B97_entry8_reaches_canonical_region_at16']
    b115=next(b for b in source['blocks'] if b['block']==115);tail=bytes(en[115][440:440+classification['tail_bytes']])
    assert sha(tail)==b115['unowned_appended_copy_current_sha256'] and classification['tail_bytes']==1886
    maria=read('work/analysis/lil_B111_B119_source_v3217/canonical_Maria32_deferred_source_lead.json')
    men,mjp=[IlnkContainer.parse(i.read_file('/data/SC3.DK4')).blocks for i in [image,clean]]
    assert len(maria['records'])==32
    for r in maria['records']:
        sr,cr=r['canonical_source_reference'],r['canonical_current_reference'];b=r['canonical_block']
        assert mjp[b][sr['offset']:sr['offset']+sr['bytes']]==bytes.fromhex(r['source_hex'])
        assert men[b][cr['offset']:cr['offset']+cr['bytes']]==bytes.fromhex(r['canonical_current_hex'])
        assert ('/data/SC3.DK4',r['canonical_id']) not in keys and ('/data/SC2.DK4',r['lil_copy_id']) not in keys
    control=read(doc['control_contract']);branch=read(doc['branch_proof'])
    assert len(control['speech_and_stored_alternative_dispatch_cases'])==300 and len(control['whole_original4100_command_cases'])==12
    assert control['all2484_catalog_getters_preserve_each_original_style_pointer_and_alias']
    assert len(control['current_original_predicate_cases'])==16 and len(control['original_event_queries'])==1
    assert len(branch['cases'])==640 and len(branch['operands_requiring_adjustment_when_resizing'])==64
    for p,digest in DEPENDENCIES.items():assert sha(Path(p).read_bytes())==digest
    candidate=ledger['current_integrated_candidate'];release=read('work/analysis/lil_Shrines_Temples_release_v3205/registered_release_verification.json')
    assert sha(Path(candidate['path']).read_bytes())==candidate['sha256']==release['candidate_sha256']
    assert sha(Path(candidate['patch']).read_bytes())==candidate['patch_sha256']==release['patch_sha256']
    assert release['whole_ROM_reconstruction_byte_exact'] and sha(Path(release['exact_patch_reconstruction']).read_bytes())==candidate['sha256']
    manifest,registry=read(candidate['manifest']),read('translations/release_stack.json')
    assert manifest['profile']==candidate['profile']=='all-routes-unified-v3204' and len(manifest['batches'])==515
    assert len(registry['accepted_layers'])==114 and all(manifest['checks'].values())
    assert manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes()) and registry['latest_promoted_build']['profile']=='all-routes-unified-v1492'
    inventory=read(ledger['unfinished_editorial_scope_v3237']['path']);oldinventory=read(before['unfinished_editorial_scope_v3214']['path'])
    for k in oldinventory:
        if k not in ['incomplete_route_source_prose_groups','incomplete_route_source_prose_count','next_focus','broader_coverage_units']:assert inventory[k]==oldinventory[k],k
    assert inventory['incomplete_COMMON_count']==3 and inventory['incomplete_route_source_prose_count']==150
    assert inventory['canonical_Maria_SC3_B97_uncredited32_source_lead']['records']==32
    route=next(u for u in ledger['coverage_units'] if u['id']=='all-route-scenes');assert (route['reviewed_route_records'],route['completed_route_records'])==(2976,2826)
    assert Path('docs/editorial_handoff_current.md').read_text(encoding='utf-8').startswith('# Current editorial handoff - V3237')
    assert ledger['goal_status']=='active' and not ledger['full_goal_complete']
    ROOT.mkdir(parents=True)
    save(ROOT/'verified_handoff.json',dict(checkpoint='V3237',ledger=str(lp),ledger_sha256=sha(lp.read_bytes()),handoff_receipt=str(rp),handoff_receipt_sha256=sha(rp.read_bytes()),fresh_records=4575,fresh_integrated=4425,fresh_pending=150,source_prose=4578,new_source_prose_reviews=150,new_completed_records=0,proposed_revisions=47,justified_retentions=103,completed_records=4425,historical_revised=3040,historical_retained=1385,incomplete_COMMON=3,incomplete_route=150,canonical_Maria32_pending=True,all150_source_current_retentions_actual_variable_prefixes_and_native_fonts_exact=True,unowned32_copy_and_canonical32_exact_uncredited=True,prior_ledger_updated_files_and_complete_release_chain_verified=True,actual_selected_B111_B119_IDs=[],new_emulator_runs=0,candidate=candidate['path'],candidate_sha256=candidate['sha256'],patch=candidate['patch'],patch_sha256=candidate['patch_sha256'],all_jobs_terminal=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('Independent V3237 audit passes:4575reread/4425integrated/150pending;4578source-prose. CanonicalMaria32uncredited;V3204/exactcleanpatch preserved;fullgoalactive.')
