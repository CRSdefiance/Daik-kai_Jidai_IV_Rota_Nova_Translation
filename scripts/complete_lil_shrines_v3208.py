"""Credit 235 reviews after registered release, exact patch and fresh startup."""
from collections import Counter
from copy import deepcopy
from pathlib import Path
from shutil import copy2
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_Shrines_Temples_completion_v3208')
FINAL=Path('translations/lil_shrines_temples_contextual_final_review_v1.json')
DOC=Path('translations/lil_shrines_temples_editorial_manuscript_v8.json')
VOICE=Path('translations/lil_shrines_temples_actor_style_manuscript_v6.json')
CHOICE=Path('translations/lil_shrines_temples_choice_manuscript_v5.json')
RELEASE=Path('work/analysis/lil_Shrines_Temples_release_v3205/registered_release_verification.json')
START=Path('work/analysis/lil_Shrines_Temples_startup_v3207/cold_boot_Lil_startup_town_verification.json')
PRIOR=Path('work/analysis/editorial_handoff_verification_v3201/verified_handoff.json')
FAMILY='Lil-Shrines-Temples-235'
SUMMARY="""V3208 completes 235 fresh contextual shrine/temple reviews in registered cumulative experimental V3204: 117 revisions and 118 individually justified retentions across complete SC2 B101-B110 exchanges. These are 164 speeches (134 ordinary, 30 FE), 56 stored actor-style alternatives in eight 4100 objects with 64 aliased slots, and 15 labels in five three-option 2200 menus. Every object has exact clean, predecessor-current and integrated references, a fresh gloss, complete exchange notes and all five review gates. Three legacy raw strings differed from effective name-catalog output; the approved Camille passages and both forms of provenance are preserved.

Preserve priest ethical counsel/two Map Keys, Christian prayer/old-cross humor, Sphinx riddles/six-baby arithmetic, the fictional cult/villager alternatives, star-adornment uncertainty, ancient community lamp/hearsay/earnest Ottoman request, 59-second bean solution/Lil confidence-to-hunch humor, and the left-hand jar riddle solved by turning right. No invented relationships, ranks, denomination, cause or earned reward. Eight native item names and Santiago Cathedral match clean/current source pointers.

All 421 commands, 114 relative spans and 570 relocated skip cases including0400/result2 pass; inverse restoration recovers every original logical byte. All326 other SC2 blocks, every other file/component, ARM9, COMMON, fonts, graphics, cache/BSS and123040 staged bytes remain exact toV3144. Both images pass336 whole loaders/cache hits and672 parent modes; three entry censuses pass. All220 relocated dispatches,16 whole actor-style commands,3312 catalog/style pointers and21 current/target predicate pairs pass without forced roles,flags,events,roster,RNG,health or outcomes; zero event queries.

All220 paragraph native planes/1760 logical-compiled macro cases/880 final stored-target cases preserve every leading/trailing/internal glyph, source control, FI substitution, blank paper, origin, bounds, four rows and single page. VirtualD0 is excluded from56 stored bodies; realD0 remains in20-byte4100 headers and all64 aliases survive. Thirty FE panels retain calibrated228x48 logical/228x64 physical paper; two source-leading-LF cases start English safely. Five three-option menus retain8-byte headers,count3,indices0/1/2/cancel,native rectangles and complete labels in40 VM cases/60 style planes. The modal input loop is bridged; actual third-answer button/visible-selection gameplay is unclaimed. Fixed historical actual menu margins and native three-row geometry/screen bounds are checked offline.

All33 final progressive/FE/menu sheets were viewed or match viewed predecessors. Concrete wrap and leading-T findings were resolved faithfully and retested. Only54 row-count notes remain;31 source/consumer,28 formatter and44 compiler negative controls pass without orphan,weak-ending,glyph,bounds,pagination orcontrol waivers. Shared actual progressive/FE/menu rules inherit by exact runtime,COMMON,EV2,font andB74/B22 bytes; offline checks remain distinct from gameplay.

V3204 rebuilds the complete canonical cumulative stack with515 manifest batches/114 accepted layers. Its clean-input patch reconstructs the whole ROM byte for byte. Two fresh targeted headless cold boots complete4001 Lil NewGame and17401 town/Refit frames;31 whole framebuffers matchV3144, five actor/captain checks and donor hashes pass, and the current six-frame sheet was viewed. Inherited five-ship Copenhagen battery/three access fixtures remain unearned. No selected shrine activation,new nameplate,earned item/injury/progress,full route orhardware claim.

Coverage is4425 contextual rereads/4425 integrated/completed/zero pending reviewed route objects:3040 historically revised plus1385 retained. Source/prose4428 includes2598 SC2; all2826 reviewed route objects are integrated. RemainingB111-B119 has182 unreviewed objects; B120 and every earlier completed family remain completed. COMMON750-752 callers, every wider untouched storyline/shared shop-town/random/help/player prose,SourceItems/LocalProduct,five named-target leads and raw classification includingB141/SC3B109 remain open. Graphics/all18 plaques stay separate. Retain the later older-record technical re-audit and queued0D validation-gap lead without asserting an older runtime defect. Preserve every ROM,translation,executed producer/proof/failure and clean/canonical input. V1492 remains promoted; V3204 is experimental. Full goal active; all jobs terminal."""

if __name__=='__main__':
    assert not ROOT.exists() and not FINAL.exists()
    lp=Path('translations/editorial_review_current_v1.json');ledger=read(lp);before=deepcopy(ledger)
    assert sha(lp.read_bytes())==read(PRIOR)['ledger_sha256']
    release,start=map(read,[RELEASE,START])
    assert release['whole_ROM_reconstruction_byte_exact'] and release['all515_manifest_batches_and114_accepted_layers_present']
    assert start['all_current_requested_and_final_framebuffers_equal_V3144'] and start['paired_frame_count']==31
    assert start['all_five_postload_actor_model_and_captain_checks_equal'] and start['current_Lil_captain2_and_B22_payload_verified']
    assert start['source_and_disposable_town_donor_unchanged'] and start['actual_selected_Shrines_Temples_IDs']==[]
    assert sha(Path(start['review_sheet']).read_bytes())==start['review_sheet_sha256']
    # All six current frames must have been viewed before this producer runs.
    doc,voice,menu=map(read,[DOC,VOICE,CHOICE]);mapping=read(doc['reference_map'])
    rows=deepcopy(doc['records']+voice['records']+menu['records'])
    assert Counter(r['editorial_decision'] for r in rows)=={'revise':117,'retain-wording':118}
    assert all(all(r['review'].values()) and r['source_meaning'] and r['localization_note'] for r in rows)
    image=NdsImage.open(release['candidate']);blocks=IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks
    assert sha(Path(release['candidate']).read_bytes())==release['candidate_sha256']==start['candidate_sha256']
    refs={r['id']:r for b in mapping['blocks'] for r in b['text_records']}
    styles={r['id']:(r,c) for b in mapping['blocks'] for c in b['actor_style_commands'] for r in c['alternative_records']}
    choices={r['id']:(r,c) for b in mapping['blocks'] for c in b['choice_commands'] for r in c['label_references']}
    parity={c['id']:c for c in read(doc['final_padding_proof'])['final_target_parity_cases']}
    stage={r['id']:r for r in release['stage']['changed_records']}
    for row in rows:
        ident=row['id'];block=blocks[row['block']];kind=row['kind']
        if kind=='typed-choice-label':
            spec,owner=choices[ident];offset=spec['new_offset'];value=row['english'].encode('ascii')
            manuscript=CHOICE;body=value;effective=value
        elif kind=='typed-4100-actor-style-alternative':
            spec,owner=styles[ident];offset=spec['new_offset'];value=bytes.fromhex(spec['target_hex'])
            manuscript=VOICE;body=value
            effective=bytes.fromhex(parity[ident]['current_final_target_macro_alignment_cases']['cases'][0]['output_hex'])
            assert row['compiled_hex']=='d0'+value.hex()
            assert block[owner['new_offset']+18:owner['new_offset']+20]==b'\0\xd0'
        else:
            spec=refs[ident];offset=spec['new_offset'];value=bytes.fromhex(spec['target_hex'])
            manuscript=DOC;body=value[1:]
            effective=bytes.fromhex(parity[ident]['current_final_target_macro_alignment_cases']['cases'][0]['output_hex'])
            assert block[offset-5:offset]==bytes.fromhex('0040ffff00')
        assert stage[ident]['new_offset']==offset and block[offset:offset+len(value)]==value and block[offset+len(value)]==0
        oldfields=['current_reference','current_hex','current_English','current_record_index','record_index',
            'current_raw_storage_English','current_effective_runtime_English','current_effective_macro_template_hex',
            'current_effective_macro_template_English','current_effective_paragraph','registered_runtime_catalog_entry']
        row['historical_source_prose_predecessor_fields']={k:deepcopy(row[k]) for k in oldfields if k in row}
        reference=dict(block=row['block'],offset=offset,bytes=len(value),record_index=block[:offset].count(b'\0'))
        if kind=='typed-choice-label':reference.update(command_offset=owner['new_offset'],option_index=row['option_index'],text_base=8)
        elif kind=='typed-4100-actor-style-alternative':reference.update(command_offset=owner['new_offset'],style_indices=row['style_indices'],text_base=20,native_selector=208)
        else:reference['header_offset']=offset-5
        row.update(current_reference=reference,current_hex=value.hex(),current_text_hex=value.hex(),integrated_reference=reference,
            integrated_hex=value.hex(),completed_candidate_reference=release['candidate'],registered_prose_owner='lil_shrines_temples_editorial',
            registered_manuscript=str(manuscript),historical_editorial_decision='revise' if row['editorial_decision']=='revise' else 'retain',
            decision='revised-and-integrated' if row['editorial_decision']=='revise' else 'retained-and-editorially-reviewed',
            individual_actual_activation_not_claimed=True,actual_three_option_menu_gameplay_not_claimed=True,
            all_source_native_representative_and_registered_gates_pass=True,
            status='complete-contextual-current-native-references-representative-and-registered-release',
            current_English=body.decode('ascii'),current_raw_storage_English=body.decode('ascii'),
            current_effective_runtime_English=effective.decode('ascii'),current_effective_macro_template_hex=body.hex(),
            current_effective_macro_template_English=body.decode('ascii'),
            current_effective_paragraph=row['english'] if kind=='typed-choice-label' else row['english'].split('}',1)[1],
            registered_runtime_catalog_entry=None,current_record_index=reference['record_index'],record_index=reference['record_index'])
        if row['editorial_decision']=='retain-wording':
            assert row['fresh_retained_wording_justification'] and row['current_effective_paragraph']==row['effective_predecessor_paragraph']
    selected={historical_key(r) for r in rows};fresh=ledger['contextual_story_natural_dialogue_pass_v1871']
    assert len(selected)==235 and {historical_key(r) for r in fresh['pending_record_keys']}==selected
    assert (fresh['fresh_pass_records_explicitly_reread'],fresh['fresh_pass_records_integrated'],fresh['fresh_pass_records_pending_native_actual_release'])==(4425,4190,235)
    oldkeys={historical_key(r) for g in ledger['completed_editorial_families'] for r in g['records']}
    assert not oldkeys&selected
    documents=[Path('docs')/n for n in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']]
    assert documents[0].read_text(encoding='utf-8').startswith('# Current editorial handoff - V3200')
    ROOT.mkdir(parents=True)
    for p in [lp,*documents]:copy2(p,ROOT/(p.name+'.before'))
    review=ROOT/'current_six_frame_visual_review.json'
    save(review,dict(sheet=start['review_sheet'],sha256=start['review_sheet_sha256'],viewed=True,
        findings='Lil selection,opening dialogue andinherited town/Refit screens arelegible andmatchV3144. Current startup only;no selected shrine oractualthree-option menu activation.'))
    proofpaths=[DOC,VOICE,CHOICE,Path(doc['reference_map']),Path(doc['native_font_proof']),Path(doc['representative_proof']),
        Path(doc['historical_representative_sheet_review']),Path(doc['prior_current_sheet_review']),Path(doc['final_padding_proof']),
        Path(doc['relocated_control_proof']),RELEASE,START,PRIOR,review,Path(__file__),
        Path('work/analysis/lil_Shrines_Temples_registration_v3203b/registration_receipt.json'),
        Path('work/analysis/lil_Shrines_Temples_registration_v3203b/negative_cases.json'),
        Path('work/analysis/lil_Shrines_Temples_reference_census_v3196/all421_commands114_relative_sites_and_shipped_entry_census.json'),
        Path('work/analysis/lil_Shrines_Temples_loader_v3195b/whole_SC2_and_ten_selected_blocks_initial_entry_proof.json')]
    evidence={str(p):sha(p.read_bytes()) for p in proofpaths}
    save(FINAL,dict(format='dk4-natural-dialogue-final-review-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',
        id=FAMILY,manuscript=str(DOC),actor_styles=str(VOICE),choices=str(CHOICE),candidate=release['candidate'],
        candidate_sha256=release['candidate_sha256'],revised=117,retained=118,records=rows,summary=SUMMARY,evidence=evidence,
        actual_selected_Shrines_Temples_IDs=[],actual_three_option_menu_gameplay_coverage=[],
        new_current_candidate_emulator_runs=2,new_independent_control_runs=0,current_six_frame_sheet_viewed=True,full_goal_complete=False))
    ledger['completed_editorial_families'].append(dict(id=FAMILY,file_path='/data/SC2.DK4',blocks=list(range(101,111)),
        record_IDs=[r['id'] for r in rows],final_review=str(FINAL),revised_count=117,retained_count=118,fresh_revisions=117,fresh_retentions=118,
        actual_verification_scope='Historical actual progressive/FE/menu rules plus two current cold-start/story/town samples;220panels/8aliased4100objects/5three-option menus/21predicate pairs separately offline native-tested. No selectedshrine oractualthree-option button/visible-selection gameplay.',records=rows))
    ledger.update(records_editorially_completed=4425,records_revised_and_integrated=3040,retained_wordings_editorially_completed=1385)
    ledger['completed_editorial_record_counts_by_file']['/data/SC2.DK4']=2598
    ledger['reviewed_but_incomplete_route_record_IDs']['/data/SC2.DK4']=[]
    active=ledger['active_source_prose_drafts']
    for p,ids in active['route_record_subsets_pending'].items():
        active['route_record_subsets_pending'][p]=[i for i in ids if ('/data/SC2.DK4',i) not in selected]
    for p in [DOC,VOICE,CHOICE]:
        if str(p) not in active['manuscripts']:active['manuscripts'].append(str(p))
        active['route_record_subsets_pending'][str(p)]=[]
    active.update(status='3-reviewed-COMMON-incomplete;no-pending-route-drafts;historical-manuscripts-preserved',
        note='4425fresh contextual rereads integrated;source/prose4428. COMMON750-752callers unresolved;remaining182B111-B119 andallwider untouchedprose remainin scope.')
    fresh['integrated_record_keys'].extend(fresh['pending_record_keys'])
    fresh.update(fresh_pass_records_integrated=4425,fresh_pass_records_pending_native_actual_release=0,pending_record_keys=[],
        pending_contextual_families=[],latest_pending_contextual_family=None,latest_contextual_manuscript=str(DOC),
        latest_contextual_actor_style_draft=str(VOICE),latest_contextual_choice_draft=str(CHOICE),
        latest_completed_family=FAMILY,latest_final_review=str(FINAL),coverage_note=active['note'])
    fresh['reconciled_families'].append(dict(id=FAMILY,records=235,final_review=str(FINAL),new_revisions=117,justified_retentions=118,
        new_completed_records=235,historical_reconciliation_only=False,historical_decisions_newly_completed=dict(revised=117,retained=118),
        actual_selected_Shrines_Temples_IDs=[],actual_three_option_menu_gameplay_coverage=[],
        new_current_candidate_emulator_runs=2,new_independent_control_runs=0))
    for u in ledger['coverage_units']:
        if u['id']=='all-route-scenes':u.update(reviewed_route_records=2826,completed_route_records=2826,
            next='Continue182unreviewed B111-B119objects andevery wider untouched route/sharedshop-town/random/help/playerprose family.')
        if u['id']==FAMILY:u.update(status='complete-contextual-current-native-references-representative-and-registered-release',
            pending=None,completion_credit_added=235,final_review=str(FINAL),full_goal_complete=False)
    for key in ['lil_Shrines_Temples_v3191','lil_Shrines_Temples_v3200']:
        ledger['formatting_watchlist'][key].update(status='complete-through-V3208',reference_map_pending=False,
            representative_reconciliation_pending=False,superseded_by='lil_Shrines_Temples_v3208',final_review=str(FINAL))
    ledger['formatting_watchlist']['lil_Shrines_Temples_v3208']=dict(status='all235-source-native-reference-representative-release-checks-pass',
        final_review=str(FINAL),evidence=evidence,actual_selected_Shrines_Temples_IDs=[],actual_three_option_menu_gameplay_coverage=[],
        individual_conditional_visits_not_required_under_user_policy=True,no_orphan_predicate_or_missing_glyph_waivers=True)
    oldcandidate=deepcopy(ledger['current_integrated_candidate'])
    ledger['previous_current_integrated_candidate_before_V3204']=oldcandidate
    ledger['integrated_candidate_reference_history'].append(oldcandidate)
    candidate=dict(path=release['candidate'],sha256=release['candidate_sha256'],profile=release['profile'],
        MESFILE_sha256=release['COMMON_sha256'],ARM9_sha256=release['ARM9_sha256'],patch=release['patch'],patch_sha256=release['patch_sha256'],
        manifest=release['manifest'],status='experimental-verified-editorial-checkpoint-not-promoted',details=SUMMARY,full_goal_complete=False,
        **{k+'_sha256':v for k,v in release['story_hashes'].items()})
    ledger['current_integrated_candidate']=candidate;ledger['latest_registered_editorial_candidate']=deepcopy(candidate)
    inventory=deepcopy(read(ledger['unfinished_editorial_scope_v3200']['path']))
    inventory['lil_B101_B110_fresh_context_review_checkpoint'].update(checkpoint='V3208',
        status='complete-contextual-current-native-references-representative-and-registered-release',final_review=str(FINAL))
    inventory['lil_B101_B110_reference_approved_checkpoint'].update(reconciled_by='V3208registeredrelease/exactpatch/currentstartup',
        completion_credit_added=235,final_review=str(FINAL))
    inventory.update(incomplete_route_source_prose_groups=[],incomplete_route_source_prose_count=0,
        next_focus='Review remaining182B111-B119objects inwhole clean exchanges;B120alreadycompleted. Continue everywider untouched storyline/sharedshop-town/random/help/playerprose. PreserveCOMMON750-752callers,SourceItems/LocalProduct,five namedtargets,rawclassificationB141/SC3B109,graphics/all18plaques andlaterolder-record technical re-audit.')
    inventory['lil_shrines_scope_reconciled_v3208']=dict(completed_B101_B110=235,remaining_B111_B119=182,
        broader_historical_source_scope417_preserved=True,B120_already_completed=True,final_review=str(FINAL))
    for u in inventory['broader_coverage_units']:
        if u['id']=='all-route-scenes':u.update(reviewed_route_records=2826,completed_route_records=2826,
            source_prose_pending_records=0,source_prose_pending_family=None,next=inventory['next_focus'])
    inv=ROOT/'unfinished_editorial_scope_inventory.json';save(inv,inventory)
    ledger['unfinished_editorial_scope_v3208']=dict(path=str(inv),sha256=sha(inv.read_bytes()),
        incomplete_COMMON=3,incomplete_route_source_prose=0,remaining_B111_B119=182,full_goal_complete=False)
    ledger['lil_Shrines_Temples_completion_v3208']=dict(summary=SUMMARY,final_review=str(FINAL),evidence=evidence,
        goal_turn_classification='progress',full_goal_complete=False);ledger['latest_checkpoint']=SUMMARY
    keys={historical_key(r) for g in ledger['completed_editorial_families'] for r in g['records']}
    assert keys==oldkeys|selected=={historical_key(r) for r in fresh['integrated_record_keys']}=={historical_key(r) for r in fresh['record_keys']}
    assert len(keys)==len(fresh['integrated_record_keys'])==4425
    assert ledger['records_with_source_and_prose_pass']==ledger['records_with_source_prose_drafts']==4428
    for key in ['reviewed_but_incomplete_COMMON_IDs','unresolved_graphics_work','older_record_reaudit_after_full_editorial_goal',
        'native_source_universe_inventory_v2701c','source_prose_reviewed_counts_by_file']:assert ledger[key]==before[key],key
    assert ledger['completed_editorial_families'][:-1]==before['completed_editorial_families']
    assert ledger['goal_status']=='active' and not ledger['full_goal_complete'];save(lp,ledger)
    release_note=('Experimental profile '+release['profile']+'. Candidate '+release['candidate']+', SHA-256 '+release['candidate_sha256']+'. '
        'Canonical base '+release['canonical_base']+', SHA-256 '+release['canonical_base_sha256']+'. '
        'Clean-input patch '+release['patch']+', SHA-256 '+release['patch_sha256']+'. '
        'Manifest515batches/114accepted layers:fullV3144 plus164speech/56actor-style/15choice manuscripts. '
        'Delta fromV3144:SC2blocks101-110 only. Allother files/components exact.44compiler negatives,verify_lil_shrines_release_v3205.py andverify_lil_shrines_startup_v3207.py pass. '
        'Fresh coldboot:title/character selection,Lilopening,town/Refit. Human acceptance isrequired forpromotion;V1492remainspromoted.\n\n')
    section='## V3208: 235 shrine/temple objects completed in V3204\n\n'+SUMMARY+'\n\n'+release_note+'Final review: '+FINAL.as_posix()+'. Release: '+RELEASE.as_posix()+'. Startup: '+START.as_posix()+'. Unfinished scope: '+inv.as_posix()+'.\n\n'
    for i,p in enumerate(documents):
        first,rest=p.read_text(encoding='utf-8').split('\n',1)
        p.write_text(('# Current editorial handoff - V3208' if i==0 else first)+'\n\n'+section+rest,encoding='utf-8',newline='\n')
    save(ROOT/'completion_receipt.json',dict(checkpoint='V3208',summary=SUMMARY,
        evidence={**evidence,str(FINAL):sha(FINAL.read_bytes()),str(inv):sha(inv.read_bytes())},
        updated_files={str(p):sha(p.read_bytes()) for p in [lp,*documents]},prior_verified_handoff=str(PRIOR),
        new_completed_records=235,new_source_prose_reviews=0,revisions=117,justified_retentions=118,
        fresh_reread=4425,fresh_integrated=4425,fresh_pending=0,source_prose=4428,completed=4425,historical_revised=3040,historical_retained=1385,
        incomplete_COMMON=3,incomplete_route=0,candidate=candidate['path'],candidate_sha256=candidate['sha256'],
        patch=candidate['patch'],patch_sha256=candidate['patch_sha256'],actual_selected_Shrines_Temples_IDs=[],
        actual_three_option_menu_gameplay_coverage=[],new_current_candidate_emulator_runs=2,new_independent_control_runs=0,
        goal_turn_classification='progress',all_jobs_terminal=True,full_goal_complete=False))
    print('V3208:235completed inregisteredV3204;117revisions/118retentions;4425reread/integrated,source-prose4428. Remaining182andallwider prose/COMMON3remainopen;fullgoalactive.')
