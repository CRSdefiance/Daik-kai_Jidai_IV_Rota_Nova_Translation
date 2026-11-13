"""Persist final relocation/reference readiness without integration credit."""
from copy import deepcopy
from pathlib import Path
from shutil import copy2
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_Shrines_Temples_ready_checkpoint_v3200')
PRIOR=Path('work/analysis/editorial_handoff_verification_v3192/verified_handoff.json')
APPROVAL=Path('work/analysis/lil_Shrines_Temples_reference_approval_v3199/approval_receipt.json')
MANUSCRIPTS=[Path('translations/lil_shrines_temples_editorial_manuscript_v8.json'),
             Path('translations/lil_shrines_temples_actor_style_manuscript_v6.json'),
             Path('translations/lil_shrines_temples_choice_manuscript_v5.json')]
SUMMARY="""V3200 seals source, prose, native display, relocation, external references and representative-rule approval for all 235 Lil shrine/temple objects in SC2 B101-B110. The batch remains 117 proposed revisions and 118 justified retentions: 164 speeches (134 ordinary, 30 FE), 56 unique actor-style alternatives in eight 4100 objects with 64 aliased style slots, and 15 labels in five three-option 2200 menus. All five editorial gates are true. English is unchanged from the independently audited V3191 review checkpoint.

Relocation preserves all 421 commands, 114 relative spans and 570 native result/skip cases, including result2/0400. Inverse restoration recovers every original logical byte; all 326 other SC2 blocks, every other file/component, ARM9, COMMON, fonts, graphics and the 123040-byte staged payload remain exact. All 220 final stored paragraph planes and 880 macro alignment cases match the reviewed complete planes. Virtual D0 prefixes are excluded from the 56 stored alternative bodies. Both current and research images pass 336 whole-file loads/cache hits and 672 parent entry modes; three shipped-entry censuses pass. All 220 relocated dispatches, 16 whole current/relocated actor-style commands, 3312 catalog/style pointer cases and 21 current/target predicate pairs pass, with no forced role, flag, event, roster, RNG, health or outcome fixture. No event-query commands occur.

The distinct three-option menus preserve indices0/1/2, cancel, source getter counts, native rectangles and complete label planes: 40 VM cases and 60 style planes. Fixed margins from actual historical two-option evidence are combined with original three-row geometry and screen bounds; this is an offline native check. No actual shrine activation, three-option button/visible-selection gameplay, new nameplate, earned item/injury/progress, full route or hardware claim is made. Shared actual progressive/FE/menu rules inherit by exact runtime, COMMON, EV2, font and B74/B22 bytes. Historical actual sheets and the V3144 six-frame startup sheet retain their viewed receipts. All concrete wrap and leading-T findings are resolved without a glyph, bounds, pagination, orphan or weak-ending waiver; only 54 documented row-count differences remain.

Coverage is unchanged: 4425 contextual rereads, 4190 integrated/completed and 235 pending registered release; source/prose4428, including2598 SC2. Completion remains2923 historically revised plus1267 retained. Routes2826 reviewed/2591 completed. The unregistered V3144-derived research ROM is preserved strictly as evidence, never a release or construction parent. Next: implement a guarded three-manuscript compiler stage after the complete registered V3144 stack; preserve the 20-byte4100 headers/eight aliases and 8-byte2200 headers/count3; register the cumulative profile (expected515 manifest batches/114 accepted layers), prove compiler rejection cases, build through build_integrated_release.py, reconstruct the entire ROM from the clean-input patch, and run/view fresh required startup checks before crediting235 integration/completion.

Registered experimental V3144 remains the current cumulative candidate with512 manifest batches/114 accepted layers, exact whole clean-input reconstruction and31 current opening/town frame matches; V1492 remains promoted. Every ROM, translation, draft, executed producer, proof and failure is preserved. Remaining B111-B119 has182 unreviewed objects; B120 and every earlier completed family remain completed. All wider untouched storylines/shared shop-town/random/help/player prose, COMMON750-752 callers, SourceItems/LocalProduct, five named-target leads and raw classification includingB141/SC3B109 remain open. Graphics/all18 plaques stay separate; the later older-record technical re-audit and queued0D validation-gap lead remain deferred without asserting an older runtime defect. Full goal active; all jobs terminal."""

if __name__=='__main__':
    assert not ROOT.exists()
    lp=Path('translations/editorial_review_current_v1.json');ledger=read(lp);before=deepcopy(ledger)
    assert sha(lp.read_bytes())==read(PRIOR)['ledger_sha256']
    approval=read(APPROVAL)
    assert approval['all235_source_native_reference_and_representative_rules_approved'] and approval['source_prose_English_unchanged']
    for p,digest in approval['hashes'].items():assert sha(Path(p).read_bytes())==digest
    docs=map(read,MANUSCRIPTS);doc,voice,menu=docs
    rows=doc['records']+voice['records']+menu['records']
    assert len(rows)==235 and all(all(r['review'].values()) for r in rows)
    fresh=ledger['contextual_story_natural_dialogue_pass_v1871']
    assert (fresh['fresh_pass_records_explicitly_reread'],fresh['fresh_pass_records_integrated'],fresh['fresh_pass_records_pending_native_actual_release'])==(4425,4190,235)
    assert ledger['records_editorially_completed']==4190 and ledger['records_with_source_and_prose_pass']==4428
    documents=[Path('docs')/n for n in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']]
    assert documents[0].read_text(encoding='utf-8').startswith('# Current editorial handoff - V3191')
    ROOT.mkdir(parents=True)
    for p in [lp,*documents]:copy2(p,ROOT/(p.name+'.before'))
    active=ledger['active_source_prose_drafts']
    oldpaths=[fresh['latest_contextual_manuscript'],fresh['latest_contextual_actor_style_draft'],fresh['latest_contextual_choice_draft']]
    for old,new,d in zip(oldpaths,MANUSCRIPTS,[doc,voice,menu],strict=True):
        active['route_record_subsets_pending'][old]=[]
        active['manuscripts'].append(str(new))
        active['route_record_subsets_pending'][str(new)]=[r['id'] for r in d['records']]
    active.update(status='3-reviewed-COMMON-incomplete;235-Shrines-Temples-reference-approved-pending-registered-release',
        note='4425 fresh contextual rereads:4190 integrated and235 ready for guarded registration/build,exact clean-input patch andfresh startup. No additional source/prose orcompletion credit atV3200.')
    pending=deepcopy(fresh['pending_contextual_families'][0])
    assert pending['id']=='Lil-Shrines-Temples-235'
    pending.update(manuscript=str(MANUSCRIPTS[0]),manuscript_sha256=sha(MANUSCRIPTS[0].read_bytes()),
        actor_styles=str(MANUSCRIPTS[1]),actor_styles_sha256=sha(MANUSCRIPTS[1].read_bytes()),
        choices=str(MANUSCRIPTS[2]),choices_sha256=sha(MANUSCRIPTS[2].read_bytes()),
        manuscripts={str(p):sha(p.read_bytes()) for p in MANUSCRIPTS},
        reference_map=doc['reference_map'],reference_map_sha256=doc['reference_map_sha256'],
        representative_proof=doc['representative_proof'],representative_proof_sha256=doc['representative_proof_sha256'],
        source_reference_approval=str(APPROVAL),source_reference_approval_sha256=sha(APPROVAL.read_bytes()),
        pending='Guarded3-manuscript compiler/registration afterfullV3144;compiler negatives;registered cumulative build/exactcleanpatch/freshcurrentstartup;then235completion.',
        status='source-prose-native-references-representative-approved;registered-release-startup-pending')
    fresh.update(latest_contextual_manuscript=str(MANUSCRIPTS[0]),latest_contextual_actor_style_draft=str(MANUSCRIPTS[1]),
        latest_contextual_choice_draft=str(MANUSCRIPTS[2]),pending_contextual_families=[pending],coverage_note=active['note'])
    for unit in ledger['coverage_units']:
        if unit['id']=='Lil-Shrines-Temples-235':unit.update(pending)
        if unit['id']=='all-route-scenes':unit['next']='Register/build235 reviewed shrine/temple objects;then continue182 B111-B119 objects andevery wider untouched route/shared shop-town/random/help/player prose family.'
    requirement=ROOT/'next_registered_integration_requirements.json'
    old_requirement=read('work/analysis/lil_Shrines_Temples_checkpoint_v3191/next_registered_integration_requirements.json')
    requirement_doc={**old_requirement,'manuscripts':pending['manuscripts'],'reference_map':doc['reference_map'],
        'reference_map_sha256':doc['reference_map_sha256'],'representative_proof':doc['representative_proof'],
        'relocated_control_proof':doc['relocated_control_proof'],'final_padding_proof':doc['final_padding_proof'],
        'source_reference_approval':str(APPROVAL),'all_source_native_reference_and_representative_gates_pass':True,
        'compiler_registered_release_exact_patch_and_fresh_startup_pending':True,
        'expected_manifest_batches':515,'accepted_layers_to_preserve':114,
        'next':'Implement exact clean/current/target-locked three-manuscript stage for164speeches,8alias-preserving4100objects/56unique strings and5three-option2200menus/15labels. Preserve421commands/114spans/570cases/21predicates/noqueries/326otherblocks/ARM9/COMMON/staged123040bytes. Register afterfullV3144beforefinalpercentguard. Run compiler negatives,build_integrated_release.py,exact clean-input patch reconstruction andfresh startup/visual checks. Do not use the unregistered research image as a parent.'}
    save(requirement,requirement_doc)
    inventory=deepcopy(read(ledger['unfinished_editorial_scope_v3191']['path']))
    inventory['lil_B101_B110_reference_approved_checkpoint']=dict(checkpoint='V3200',manuscripts=[str(p) for p in MANUSCRIPTS],
        approval=str(APPROVAL),remaining_release_requirements=str(requirement),new_reviews=0,new_completion_credit=0,
        remaining_B111_B119_unreviewed_objects=182)
    inventory['next_focus']=requirement_doc['next']+' Then continue every broader unfinished editorial family;graphics remains separate andolder technical re-audit stayslater.'
    inv=ROOT/'unfinished_editorial_scope_inventory.json';save(inv,inventory)
    ledger['unfinished_editorial_scope_v3200']=dict(path=str(inv),sha256=sha(inv.read_bytes()),
        incomplete_COMMON=3,incomplete_route_source_prose=235,remaining_B111_B119=182,full_goal_complete=False)
    ledger['formatting_watchlist']['lil_Shrines_Temples_v3200']=dict(
        status='All235source/native/reference/representative gates pass;registered compiler/build/exactpatch/currentstartup pending',
        approval=str(APPROVAL),reference_map=doc['reference_map'],representative_proof=doc['representative_proof'],
        relocated_control_proof=doc['relocated_control_proof'],final_padding_proof=doc['final_padding_proof'],
        exact_command_count=421,relative_spans=114,relocated_skip_cases=570,final_parity_macro_cases=880,
        actual_selected_Shrines_Temples_IDs=[],actual_three_option_menu_gameplay_coverage=[],new_emulator_runs=0)
    evidence={str(p):sha(p.read_bytes()) for p in [PRIOR,APPROVAL,*MANUSCRIPTS,Path(doc['reference_map']),
        Path(doc['representative_proof']),Path(doc['relocated_control_proof']),Path(doc['final_padding_proof']),
        requirement,inv,Path(__file__)]}
    ledger['lil_Shrines_Temples_reference_ready_v3200']=dict(summary=SUMMARY,**pending,evidence=evidence,
        new_source_prose_reviews=0,new_completed_records=0,full_goal_complete=False)
    ledger['latest_checkpoint']=SUMMARY
    for key in ['completed_editorial_families','records_editorially_completed','records_revised_and_integrated',
        'retained_wordings_editorially_completed','completed_editorial_record_counts_by_file','current_integrated_candidate',
        'reviewed_but_incomplete_COMMON_IDs','reviewed_but_incomplete_route_record_IDs','unresolved_graphics_work',
        'older_record_reaudit_after_full_editorial_goal','records_with_source_and_prose_pass','records_with_source_prose_drafts',
        'source_prose_reviewed_counts_by_file','native_source_universe_inventory_v2701c']:
        assert ledger[key]==before[key],key
    for key in ['record_keys','record_IDs','integrated_record_keys','pending_record_keys','fresh_pass_records_explicitly_reread',
        'fresh_pass_records_integrated','fresh_pass_records_pending_native_actual_release']:
        assert fresh[key]==before['contextual_story_natural_dialogue_pass_v1871'][key],key
    assert ledger['goal_status']=='active' and not ledger['full_goal_complete']
    save(lp,ledger)
    section='## V3200: 235 reviews ready for registered integration\n\n'+SUMMARY+'\n\nReference approval: '+APPROVAL.as_posix()+'. Next integration: '+requirement.as_posix()+'. Unfinished scope: '+inv.as_posix()+'.\n\n'
    for i,p in enumerate(documents):
        first,rest=p.read_text(encoding='utf-8').split('\n',1)
        p.write_text(('# Current editorial handoff - V3200' if i==0 else first)+'\n\n'+section+rest,encoding='utf-8',newline='\n')
    candidate=ledger['current_integrated_candidate']
    save(ROOT/'checkpoint_receipt.json',dict(checkpoint='V3200',summary=SUMMARY,evidence=evidence,
        updated_files={str(p):sha(p.read_bytes()) for p in [lp,*documents]},prior_verified_handoff=str(PRIOR),
        new_completed_records=0,new_source_prose_reviews=0,fresh_reread=4425,fresh_integrated=4190,fresh_pending=235,
        source_prose=4428,completed=4190,historical_revised=2923,historical_retained=1267,incomplete_COMMON=3,incomplete_route=235,
        candidate=candidate['path'],candidate_sha256=candidate['sha256'],patch=candidate['patch'],patch_sha256=candidate['patch_sha256'],
        next_requirements=str(requirement),all_jobs_terminal=True,new_emulator_runs=0,
        goal_turn_classification='progress',full_goal_complete=False))
    print('V3200:235 reviews source/native/reference/representative-ready;registered compiler/build/patch/startup pending.4425reread/4190integrated/235pending;no newcredit. Fullgoalactive.')
