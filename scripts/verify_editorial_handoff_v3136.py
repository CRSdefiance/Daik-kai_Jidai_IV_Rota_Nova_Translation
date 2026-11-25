"""Independent200-review audit: references, retentions, native bytes and prior release."""
import struct
from pathlib import Path
from collections import Counter
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.dialogue.lil_crew_items_profile import profile_for
from dk4tool.dialogue.lil_crew_items_layout_v2 import encode_relocatable_dialogue,audit_relocatable_dialogue_record,DEPENDENCIES
from dk4tool.patch.grand_race_menu_release import sha
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/editorial_handoff_verification_v3136')
CHECKPOINT=Path('work/analysis/lil_Crew_Items_checkpoint_v3135')
if __name__=='__main__':
    assert not ROOT.exists();rp=CHECKPOINT/'checkpoint_receipt.json';receipt=read(rp)
    for group in ['evidence','updated_files']:
        for p,digest in receipt[group].items():assert sha(Path(p).read_bytes())==digest,(group,p)
    lp=Path('translations/editorial_review_current_v1.json');ledger=read(lp);before=read(CHECKPOINT/'editorial_review_current_v1.json.before')
    prior=read('work/analysis/editorial_handoff_verification_v3111/verified_handoff.json')
    assert sha((CHECKPOINT/'editorial_review_current_v1.json.before').read_bytes())==prior['ledger_sha256']
    assert sha(Path(prior['handoff_receipt']).read_bytes())==prior['handoff_receipt_sha256']
    for p,digest in read(prior['handoff_receipt'])['updated_files'].items():
        saved=CHECKPOINT/(Path(p).name+'.before');assert sha((saved if saved.exists() else Path(p)).read_bytes())==digest
    fresh,old=ledger['contextual_story_natural_dialogue_pass_v1871'],before['contextual_story_natural_dialogue_pass_v1871']
    doc,menu=map(read,[fresh['latest_contextual_manuscript'],fresh['latest_contextual_choice_draft']]);rows=doc['records']+menu['records']
    selected={historical_key(r) for r in rows};keys={historical_key(r) for r in fresh['record_keys']};oldkeys={historical_key(r) for r in old['record_keys']}
    integrated={historical_key(r) for r in fresh['integrated_record_keys']};pending={historical_key(r) for r in fresh['pending_record_keys']};complete={historical_key(r) for g in ledger['completed_editorial_families'] for r in g['records']}
    assert len(rows)==len(selected)==200 and keys-oldkeys==selected==pending and oldkeys==integrated==complete
    assert keys==integrated|pending and not integrated&pending and len(keys)==len(fresh['record_keys'])==len(fresh['record_IDs'])==4190
    assert (fresh['fresh_pass_records_explicitly_reread'],fresh['fresh_pass_records_integrated'],fresh['fresh_pass_records_pending_native_actual_release'])==(4190,3990,200)
    assert Counter(p for p,k in keys)=={'/COMMON/MESFILE.DK4':1599,'/data/SC2.DK4':2363,'/data/SC0.DK4':117,'/data/SC1.DK4':73,'/data/SC3.DK4':38}
    assert ledger['records_with_source_and_prose_pass']==ledger['records_with_source_prose_drafts']==sum(ledger['source_prose_reviewed_counts_by_file'].values())==4193
    assert (ledger['records_editorially_completed'],ledger['records_revised_and_integrated'],ledger['retained_wordings_editorially_completed'])==(3990,2800,1190)
    for k in ['completed_editorial_families','completed_editorial_record_counts_by_file','current_integrated_candidate','reviewed_but_incomplete_COMMON_IDs','unresolved_graphics_work','older_record_reaudit_after_full_editorial_goal','native_source_universe_inventory_v2701c']:assert ledger[k]==before[k],k
    assert ledger['reviewed_but_incomplete_COMMON_IDs']==[750,751,752] and set(ledger['reviewed_but_incomplete_route_record_IDs']['/data/SC2.DK4'])=={k for p,k in selected}
    assert Counter(r['editorial_decision'] for r in rows)=={'revise':123,'retain-wording':77}
    assert all(all(r['review'].values()) and r['source_meaning'] and r['context'] and r['localization_note'] for r in rows)
    for r in rows:
        assert not any(tag in r['english'] for tag in ['{LB','{ALIGN','{PAD'])
        if r['editorial_decision']=='retain-wording':
            text=' '.join(r['current_English'].split())
            for macro in ['FI','FA','FO']:text=text.replace(macro,'{MACRO:'+macro+'}')
            assert (r['english'] if r['kind']=='typed-choice-label' else r['english'].split('}',1)[1])==text and r['fresh_retained_wording_justification']
    image,clean=NdsImage.open(doc['current_ROM']),NdsImage.open('work/clean.nds');arm=image.read_file('/__arm9__.bin')
    en,jp=[IlnkContainer.parse(i.read_file('/data/SC2.DK4')).blocks for i in [image,clean]]
    merged=read(doc['native_font_proof']);assert sha(Path(doc['native_font_proof']).read_bytes())==doc['native_font_proof_sha256'];cases={c['id']:c for c in merged['cases']}
    assert len(cases)==198 and merged['current_original_macro_alignment_calls']==1584 and len(merged['source_bound_formatter_negatives'])==28
    assert all(n['rejected'] for n in merged['source_bound_formatter_negatives']) and len(merged['all26_review_sheets'])==26
    for s in merged['all26_review_sheets']:assert sha(Path(s['path']).read_bytes())==s['sha256']
    for p,digest in merged['evidence'].items():assert sha(Path(p).read_bytes())==digest
    for r in rows:
        b=r['block'];sr,cr=r['source_reference'],r['current_reference']
        assert jp[b][sr['offset']:sr['offset']+sr['bytes']]==bytes.fromhex(r['source_hex']) and en[b][cr['offset']:cr['offset']+cr['bytes']]==bytes.fromhex(r['current_hex'])
        if r['kind']=='typed-choice-label':continue
        assert jp[b][sr['offset']-5:sr['offset']+1]==en[b][cr['offset']-5:cr['offset']+1]==bytes.fromhex(r['source_complete_preamble_hex'])
        p=profile_for(arm,en[b],'FE-paper' if r['kind']=='system-FE' else 'progressive');encoded=encode_relocatable_dialogue(bytes.fromhex(r['source_hex']),r['english'],p)
        assert encoded.encoded.hex()==r['compiled_hex']==cases[r['id']]['encoded_hex']
        qa=audit_relocatable_dialogue_record(bytes.fromhex(r['source_hex']),r['english'],p)
        assert not [i for i in qa['issues'] if i['severity'] in ['warning','error'] and i['code'] not in r.get('qa_waivers',[])]
        assert sha(Path(cases[r['id']]['preview']).read_bytes())==cases[r['id']]['preview_sha256']
    source,control,branch=map(read,[doc['source_context'],doc['control_contract'],doc['branch_proof']])
    assert source['total_editorial_objects']==200 and sum(len(b['all_clean_native_commands']) for b in source['blocks'])==268
    assert len(branch['cases'])==40 and len(branch['operands_requiring_adjustment_when_resizing'])==4
    assert control['all198_complete_preambles_and396_historical_dispatch_contexts_pass'] and len(control['current_original_predicate_cases'])==0 and control['original_event_queries']==[]
    terms=read(doc['item_terminology_reconciliation']);assert terms['all10_clean_current_pointer_strings_equal_registered_names']
    annotations={int(k):v for k,v in terms['source_speaker_annotation_reconciliation'].items()}
    assert set(annotations)=={108,114,152,188}
    assert all(r['speaker']==annotations[r['original_actor_ID']] and r['preserved_source_packet_speaker_annotation'] for r in rows if r.get('original_actor_ID') in annotations)
    fe_rows=[r for r in rows if r['kind']=='system-FE'];assert len(fe_rows)==7
    assert len([r for r in fe_rows if '{MACRO:FI}' in r['english']])==2
    feproof=read(doc['native_FE_font_proof']);assert feproof['all7_source_unlabeled_stat_notices_and_monkey_calls_preserved'] and feproof['four_distinct_source_Luck_Spirit_notices_and_three_monkey_calls_preserved']
    assert len(feproof['source_FI_null_actor_cases'])==2 and feproof['current_original_null_actor_macro_alignment_cases']==56
    choice=read(menu['native_choice_proof']);assert sha(Path(menu['native_choice_proof']).read_bytes())==menu['native_choice_proof_sha256']
    assert (choice['native_selection_cancel_cases'],choice['complete_current_and_reviewed_style_label_planes'],choice['clean_current_reviewed_native_decoder_cases'])==(6,8,3)
    proof=read(choice['menus'][0]['proof']);assert sha(Path(choice['menus'][0]['proof']).read_bytes())==choice['menus'][0]['sha256']
    labels=[r['english'].encode('ascii') for r in sorted(menu['records'],key=lambda r:r['option_index'])]
    parts=[v+b'\0'+b'\0'*(-(len(v)+1)%2) for v in labels]
    target=b'\0\x21\0\0'+struct.pack('<H',len(parts[0]))+b''.join(parts)
    assert target.hex()==proof['typed_target_object_hex'] and len(target)==22
    reviewed=next(c for c in proof['current_and_reviewed_VM_and_font_cases'] if c['version']=='reviewed-research')
    assert reviewed['source_derived_text_canvas_width']==48 and all(p['independent_complete_native_pixels_match'] and p['storage_padding_all_blank'] and p['visible_cell_center_twice']==48 for p in reviewed['all_four_style_label_planes'])
    assert [r['english'] for r in menu['records']]==['I do.',"I don't."]
    for p,digest in DEPENDENCIES.items():assert sha(Path(p).read_bytes())==digest
    candidate=ledger['current_integrated_candidate'];release=read('work/analysis/lil_Recruits_Julian_release_v3104/registered_release_verification.json')
    assert sha(Path(candidate['path']).read_bytes())==candidate['sha256']==release['candidate_sha256']
    assert sha(Path(candidate['patch']).read_bytes())==candidate['patch_sha256']==release['patch_sha256']
    assert release['whole_ROM_reconstruction_byte_exact'] and sha(Path(release['exact_patch_reconstruction']).read_bytes())==candidate['sha256']
    manifest,registry=read(candidate['manifest']),read('translations/release_stack.json')
    assert manifest['profile']==candidate['profile']=='all-routes-unified-v3103' and len(manifest['batches'])==510 and len(registry['accepted_layers'])==114 and all(manifest['checks'].values())
    assert manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes()) and registry['latest_promoted_build']['profile']=='all-routes-unified-v1492'
    inventory=read(ledger['unfinished_editorial_scope_v3135']['path']);oldinventory=read(before['unfinished_editorial_scope_v3110']['path'])
    for k in oldinventory:
        if k not in ['incomplete_route_source_prose_groups','incomplete_route_source_prose_count','next_focus','broader_coverage_units']:assert inventory[k]==oldinventory[k],k
    assert inventory['incomplete_COMMON_count']==3 and inventory['incomplete_route_source_prose_count']==200
    route=next(u for u in ledger['coverage_units'] if u['id']=='all-route-scenes');assert (route['reviewed_route_records'],route['completed_route_records'])==(2591,2391)
    assert Path('docs/editorial_handoff_current.md').read_text(encoding='utf8').startswith('# Current editorial handoff - V3135')
    assert ledger['goal_status']=='active' and not ledger['full_goal_complete']
    ROOT.mkdir(parents=True);save(ROOT/'verified_handoff.json',dict(checkpoint='V3135',ledger=str(lp),ledger_sha256=sha(lp.read_bytes()),handoff_receipt=str(rp),handoff_receipt_sha256=sha(rp.read_bytes()),fresh_records=4190,fresh_integrated=3990,fresh_pending=200,source_prose=4193,new_source_prose_reviews=200,new_completed_records=0,proposed_revisions=123,justified_retentions=77,completed_records=3990,historical_revised=2800,historical_retained=1190,incomplete_COMMON=3,incomplete_route=200,all200_source_current_retentions_and_native_font_invariants_exact=True,prior_ledger_updated_files_and_complete_release_chain_verified=True,actual_selected_Crew_Items_IDs=[],new_emulator_runs=0,candidate=candidate['path'],candidate_sha256=candidate['sha256'],patch=candidate['patch'],patch_sha256=candidate['patch_sha256'],all_jobs_terminal=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('IndependentV3135audit passes:4190reread/3990integrated/200pending;4193source-prose. V3103/exactcleanpatch preserved;fullgoalactive.')
