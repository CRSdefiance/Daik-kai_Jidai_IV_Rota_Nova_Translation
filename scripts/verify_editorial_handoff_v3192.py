"""Independent 235-review audit: exact references, retentions and native proofs."""
from collections import Counter
from pathlib import Path
import struct
from dk4tool.dialogue.lil_shrines_temples_profile import profile_for
from dk4tool.dialogue.lil_shrines_temples_layout_v2 import encode_relocatable_dialogue, audit_relocatable_dialogue_record, DEPENDENCIES
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read, save

ROOT=Path('work/analysis/editorial_handoff_verification_v3192')
CHECKPOINT=Path('work/analysis/lil_Shrines_Temples_checkpoint_v3191')

if __name__=='__main__':
    assert not ROOT.exists()
    rp=CHECKPOINT/'checkpoint_receipt.json';receipt=read(rp)
    for group in ['evidence','updated_files']:
        for p,digest in receipt[group].items():assert sha(Path(p).read_bytes())==digest,(group,p)
    lp=Path('translations/editorial_review_current_v1.json')
    ledger=read(lp);before=read(CHECKPOINT/'editorial_review_current_v1.json.before')
    prior=read(receipt['prior_verified_handoff'])
    assert sha((CHECKPOINT/'editorial_review_current_v1.json.before').read_bytes())==prior['ledger_sha256']
    assert sha(Path(prior['handoff_receipt']).read_bytes())==prior['handoff_receipt_sha256']
    for p,digest in read(prior['handoff_receipt'])['updated_files'].items():
        saved=CHECKPOINT/(Path(p).name+'.before')
        assert sha((saved if saved.exists() else Path(p)).read_bytes())==digest
    fresh=ledger['contextual_story_natural_dialogue_pass_v1871'];old=before['contextual_story_natural_dialogue_pass_v1871']
    paths=[fresh['latest_contextual_manuscript'],fresh['latest_contextual_actor_style_draft'],fresh['latest_contextual_choice_draft']]
    doc,voice,menu=map(read,paths);rows=doc['records']+voice['records']+menu['records']
    for d in [doc,voice,menu]:validate_natural_dialogue_batch(d)
    selected={historical_key(r) for r in rows};keys={historical_key(r) for r in fresh['record_keys']}
    oldkeys={historical_key(r) for r in old['record_keys']};integrated={historical_key(r) for r in fresh['integrated_record_keys']}
    pending={historical_key(r) for r in fresh['pending_record_keys']}
    complete={historical_key(r) for g in ledger['completed_editorial_families'] for r in g['records']}
    assert len(rows)==len(selected)==235 and keys-oldkeys==selected==pending and oldkeys==integrated==complete
    assert keys==integrated|pending and not integrated&pending
    assert len(keys)==len(fresh['record_keys'])==len(fresh['record_IDs'])==4425
    assert (fresh['fresh_pass_records_explicitly_reread'],fresh['fresh_pass_records_integrated'],fresh['fresh_pass_records_pending_native_actual_release'])==(4425,4190,235)
    assert Counter(p for p,k in keys)=={'/COMMON/MESFILE.DK4':1599,'/data/SC2.DK4':2598,'/data/SC0.DK4':117,'/data/SC1.DK4':73,'/data/SC3.DK4':38}
    assert ledger['records_with_source_and_prose_pass']==ledger['records_with_source_prose_drafts']==sum(ledger['source_prose_reviewed_counts_by_file'].values())==4428
    assert (ledger['records_editorially_completed'],ledger['records_revised_and_integrated'],ledger['retained_wordings_editorially_completed'])==(4190,2923,1267)
    for k in ['completed_editorial_families','completed_editorial_record_counts_by_file','current_integrated_candidate',
        'reviewed_but_incomplete_COMMON_IDs','unresolved_graphics_work','older_record_reaudit_after_full_editorial_goal','native_source_universe_inventory_v2701c']:
        assert ledger[k]==before[k],k
    assert ledger['reviewed_but_incomplete_COMMON_IDs']==[750,751,752]
    assert set(ledger['reviewed_but_incomplete_route_record_IDs']['/data/SC2.DK4'])=={k for p,k in selected}
    assert Counter(r['editorial_decision'] for r in rows)=={'revise':117,'retain-wording':118}
    for row in rows:
        assert not any(t in row['english'] for t in ['{LB','{ALIGN','{PAD'])
        if row['editorial_decision']=='retain-wording':
            text=row['english'] if row['kind']=='typed-choice-label' else row['english'].split('}',1)[1]
            assert text==row['effective_predecessor_paragraph'] and row['fresh_retained_wording_justification']
    image,clean=NdsImage.open(doc['current_ROM']),NdsImage.open('work/clean.nds')
    arm=image.read_file('/__arm9__.bin')
    en,jp=[IlnkContainer.parse(i.read_file('/data/SC2.DK4')).blocks for i in [image,clean]]
    merged=read(doc['native_font_proof'])
    assert sha(Path(doc['native_font_proof']).read_bytes())==doc['native_font_proof_sha256']
    cases={c['id']:c for c in merged['cases']}
    assert len(cases)==220 and merged['current_original_macro_alignment_calls']==1760
    assert len(merged['source_bound_formatter_negatives'])==28 and all(n['rejected'] for n in merged['source_bound_formatter_negatives'])
    assert len(merged['all33_review_sheets'])==33
    for s in merged['all33_review_sheets']:assert sha(Path(s['path']).read_bytes())==s['sha256']
    for p,digest in merged['evidence'].items():assert sha(Path(p).read_bytes())==digest
    for r in rows:
        b=r['block'];sr,cr=r['source_reference'],r['current_reference']
        assert jp[b][sr['offset']:sr['offset']+sr['bytes']]==bytes.fromhex(r['source_hex'])
        assert en[b][cr['offset']:cr['offset']+cr['bytes']]==bytes.fromhex(r['current_hex'])
        assert jp[b][sr['offset']+sr['bytes']]==en[b][cr['offset']+cr['bytes']]==0
        if r['kind']=='typed-choice-label':continue
        isvoice=r['kind']=='typed-4100-actor-style-alternative'
        if not isvoice:
            assert jp[b][sr['offset']-5:sr['offset']+1]==en[b][cr['offset']-5:cr['offset']+1]==bytes.fromhex(r['source_complete_preamble_hex'])
        raw=bytes.fromhex(r['source_hex'])
        if isvoice:raw=b'\xd0'+raw
        p=profile_for(arm,en[b],'FE-paper' if r['kind']=='system-FE' else 'progressive')
        encoded=encode_relocatable_dialogue(raw,r['english'],p)
        assert encoded.encoded.hex()==r['compiled_hex']==cases[r['id']]['encoded_hex']
        if isvoice:assert encoded.encoded[1:].hex()==r['compiled_stored_alternative_hex'] and r['virtual_formatter_prefix_is_not_part_of_stored_alternative_text']
        qa=audit_relocatable_dialogue_record(raw,r['english'],p)
        assert not [i for i in qa['issues'] if i['severity'] in ['warning','error'] and i['code'] not in r.get('qa_waivers',[])]
        assert sha(Path(cases[r['id']]['preview']).read_bytes())==cases[r['id']]['preview_sha256']
    assert sum(len(r['style_indices']) for r in voice['records'])==64
    assert len({(r['block'],r['command_offset']) for r in voice['records']})==8
    choice=read(menu['native_choice_proof'])
    assert (choice['native_selection_cancel_cases'],choice['complete_current_and_reviewed_style_label_planes'],choice['clean_current_reviewed_native_decoder_cases'])==(40,60,15)
    for m in choice['menus']:
        assert sha(Path(m['proof']).read_bytes())==m['sha256']
        proof=read(m['proof']);rs=sorted([r for r in menu['records'] if r['block']==m['block'] and r['command_offset']==m['command_offset']],key=lambda r:r['option_index'])
        assert [r['option_index'] for r in rs]==[0,1,2]
        parts=[r['english'].encode('ascii')+b'\0' for r in rs]
        parts=[p+b'\0'*(-len(p)%2) for p in parts]
        offsets=[0,len(parts[0]),len(parts[0])+len(parts[1])]
        target=struct.pack('<4H',0x2200,*offsets)+b''.join(parts)
        assert target.hex()==proof['typed_target_object_hex'] and all(r['typed_target_object_hex']==target.hex() for r in rs)
        reviewed=next(c for c in proof['current_and_reviewed_VM_and_font_cases'] if c['version']=='reviewed-research')
        width=reviewed['source_derived_text_canvas_width']
        assert all(p['independent_complete_native_pixels_match'] and p['storage_padding_all_blank'] and p['visible_cell_center_twice']==width for p in reviewed['all_six_style_label_planes'])
        assert [r['modal_selection'] for r in reviewed['native_VM_getters_geometry_and_selection']['VM_cases']]==[0,1,2,-1]
    for p,digest in DEPENDENCIES.items():assert sha(Path(p).read_bytes())==digest
    candidate=ledger['current_integrated_candidate'];release=read('work/analysis/lil_Crew_Items_release_v3145/registered_release_verification.json')
    assert sha(Path(candidate['path']).read_bytes())==candidate['sha256']==release['candidate_sha256']
    assert sha(Path(candidate['patch']).read_bytes())==candidate['patch_sha256']==release['patch_sha256']
    assert release['whole_ROM_reconstruction_byte_exact'] and sha(Path(release['exact_patch_reconstruction']).read_bytes())==candidate['sha256']
    manifest,registry=read(candidate['manifest']),read('translations/release_stack.json')
    assert manifest['profile']==candidate['profile']=='all-routes-unified-v3144' and len(manifest['batches'])==512
    assert len(registry['accepted_layers'])==114 and all(manifest['checks'].values())
    assert manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes())
    assert registry['latest_promoted_build']['profile']=='all-routes-unified-v1492'
    inventory=read(ledger['unfinished_editorial_scope_v3191']['path']);oldinventory=read(before['unfinished_editorial_scope_v3165']['path'])
    for k in oldinventory:
        if k not in ['incomplete_route_source_prose_groups','incomplete_route_source_prose_count','next_focus','broader_coverage_units']:assert inventory[k]==oldinventory[k],k
    assert inventory['incomplete_COMMON_count']==3 and inventory['incomplete_route_source_prose_count']==235
    route=next(u for u in ledger['coverage_units'] if u['id']=='all-route-scenes')
    assert (route['reviewed_route_records'],route['completed_route_records'])==(2826,2591)
    assert Path('docs/editorial_handoff_current.md').read_text(encoding='utf-8').startswith('# Current editorial handoff - V3191')
    assert ledger['goal_status']=='active' and not ledger['full_goal_complete']
    ROOT.mkdir(parents=True)
    save(ROOT/'verified_handoff.json',dict(checkpoint='V3191',ledger=str(lp),ledger_sha256=sha(lp.read_bytes()),
        handoff_receipt=str(rp),handoff_receipt_sha256=sha(rp.read_bytes()),fresh_records=4425,fresh_integrated=4190,fresh_pending=235,
        source_prose=4428,new_source_prose_reviews=235,new_completed_records=0,proposed_revisions=117,justified_retentions=118,
        completed_records=4190,historical_revised=2923,historical_retained=1267,incomplete_COMMON=3,incomplete_route=235,
        all235_source_current_effective_retentions_and_native_font_invariants_exact=True,
        prior_ledger_updated_files_and_complete_release_chain_verified=True,actual_selected_Shrines_Temples_IDs=[],new_emulator_runs=0,
        candidate=candidate['path'],candidate_sha256=candidate['sha256'],patch=candidate['patch'],patch_sha256=candidate['patch_sha256'],
        all_jobs_terminal=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('IndependentV3191audit passes:4425reread/4190integrated/235pending;4428source-prose. V3144/exactcleanpatch preserved;fullgoalactive.')
