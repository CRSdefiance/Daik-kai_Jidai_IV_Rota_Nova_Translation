"""Reconcile 29 complete sail-lesson reviews once, pending registered integration."""
from collections import Counter
from copy import deepcopy
from pathlib import Path
from shutil import copy2
from dk4tool.patch.grand_race_menu_release import sha
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B167_checkpoint_v4136')
PRIOR=Path('work/analysis/editorial_handoff_verification_v4115/verified_handoff.json')
APPROVAL=Path('work/analysis/lil_B167_native_approval_v4135/approval_receipt.json')
DOCS=[Path('translations/lil_B167_editorial_manuscript_v12.json'),Path('translations/lil_B167_choice_manuscript_v2.json')]
FAMILY='Lil-B167-Shipwright-complete-sail-lesson-accept-refuse29'
NEXT='Complete B167 relocation and stored/native references, representative Japanese/English scene, both menu outcomes and both returns; then registered cumulative build, exact clean-input patch and startup. Continue B168-B180 and all wider editorial families. V4046 stays main; V4110 stays the latest verified experimental candidate until integration.'
SUMMARY='''V4136 records 29 fresh contextual/native reviews for the complete Lil SC2 B167 Shipwright sail lesson: 16 proposed revisions and 13 individually justified retentions. All 27 clean Japanese speeches and two labels were read and individually glossed as one exchange before predecessor English comparison. Preserve the bored Shipwright's favor, Admiral address, flattering encouragement, refusal banter, optional Cesare's formal boast or later realization on separate paths, Manuel's mast-order answer, Janus's understanding and the return-to-work farewell. Keep square/lateen orientation and wind tradeoffs, topsail, staysail overlap restriction, Spritsail, Jigger Spanker, size restrictions, the two-or-more-masts comparison, only the rear mast catching directly following wind, ineffective forward masts and the rear-quarter sail-angle condition. Terms bind to current reviewed Refit bodies and active labels. No fee, reward, relationship, rank, named source port, numeric wind angle or real-world correction is invented.

Source/current bindings preserve 46 commands, all 27 complete progressive preambles and five static actors 2/4/13/23/109. Printable 6D is the Shipwright actor, not literal m; 0D remains Cesare's executable selector. Twelve relative sites/120 clean-current native cases, two separate original Cesare queries, two resources/20 boundary cases and two distinct ends at source 430/2172 remain source-owned. The one typed menu has Okay/No thanks in source order. Each path's later membership query updates final result state separately from the selected menu index. Ten original name consumers preserve eight owned scratch paths and the Shipwright's two direct read-only paths across all 4MiB. Native getter/structural tests establish no natural source-event eligibility. There are no source macros, FE, A000 or other presentation commands in this block. The later older-record technical re-audit remains open.

Native approval V4135 covers 27 complete 216x64 speech planes, 216 logical/compiled alignment cases, 19 source-consumer and 14 formatter rejection controls, three decoder objects, six menu selection/cancel cases and eight complete native style-label planes. All four final speech sheets and the menu sheet were viewed. Eleven narrow row-count notes exempt no glyph, bounds, pagination, control, weak ending, orphan, macro or blank-page issue. Final phrase-flow refinements preserve complete facts and character voices; all earlier drafts, failed plans and proofs remain. No authored breaks, padding, metric/guard change or wording waiver. Menu backing ownership is inherited by exact entire-ARM9 equality to the observed constructor; no new B167 gameplay, accepted menu outcome or return is claimed.

Coverage becomes 5602 fresh contextual rereads: 5573 integrated/completed and 29 pending integration. Source/prose becomes 5605, including 3749 SC2 and unchanged 64 SC3; route reviewed/completed is 4003/3974. Historical completed decisions remain 3551 revised/2022 retained. This adds each B167 object once as pending and adds no completion credit. Verified experimental V4110 remains 541 manuscript batches/114 accepted layers with its exact clean-input patch. V4046 remains promoted main; the immutable construction baseline and every earlier ROM/translation are preserved.

Remaining B168-B180 contains 321 physical speeches and zero remaining typed choice-command leads; this is not a full Lil/project denominator. Every wider storyline, shared shop/town dialogue, random scene, help and remaining player-facing prose stays open. Preserve COMMON 750-752, canonical Maria32 SC3 B97, SourceItems/LocalProduct, five named-target leads, exact-record Proof consistency and Samwell's uncredited full-catalogue middle-field lead. Graphics/all 18 plaques remain separate; retain the later older-record technical re-audit/queued 0D gap and B157 provenance amendment. Full goal active.'''
UNCHANGED=['completed_editorial_families','records_editorially_completed','records_revised_and_integrated','retained_wordings_editorially_completed','completed_editorial_record_counts_by_file','current_integrated_candidate','reviewed_but_incomplete_COMMON_IDs','unresolved_graphics_work','older_record_reaudit_after_full_editorial_goal','native_source_universe_inventory_v2701c','Proof_terminology_consistency_lead_v3286','lil_B157_provenance_amendment_v3784','promoted_main_build_v4083']
if __name__=='__main__':
    assert not ROOT.exists();lp=Path('translations/editorial_review_current_v1.json');ledger=read(lp);before=deepcopy(ledger)
    assert sha(lp.read_bytes())==read(PRIOR)['ledger_sha256']
    approval=read(APPROVAL);manuscripts=[read(p) for p in DOCS]
    assert approval['manuscripts']=={str(p):sha(p.read_bytes()) for p in DOCS}
    rows=[r for d in manuscripts for r in d['records']]
    assert len(rows)==len({r['id'] for r in rows})==29 and Counter(r['editorial_decision'] for r in rows)=={'revise':16,'retain-wording':13}
    assert all(all(r['review'].values()) for r in rows) and approval['new_completed_records']==approval['new_source_prose_reviews']==0
    fresh=ledger['contextual_story_natural_dialogue_pass_v1871']
    assert (fresh['fresh_pass_records_explicitly_reread'],fresh['fresh_pass_records_integrated'],fresh['fresh_pass_records_pending_native_actual_release'])==(5573,5573,0)
    selected=[dict(file_path='/data/SC2.DK4',id=r['id']) for r in rows]
    assert not {historical_key(r) for r in selected}&{historical_key(r) for r in fresh['record_keys']}
    assert ledger['records_with_source_and_prose_pass']==5576 and ledger['source_prose_reviewed_counts_by_file']['/data/SC2.DK4']==3720
    docs=[Path('docs')/n for n in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']]
    assert docs[0].read_text(encoding='utf-8').startswith('# Current editorial handoff - V4114')
    ROOT.mkdir(parents=True)
    for p in [lp,*docs]:copy2(p,ROOT/(p.name+'.before'))
    ledger['records_with_source_and_prose_pass']=ledger['records_with_source_prose_drafts']=5605
    ledger['source_prose_reviewed_counts_by_file']['/data/SC2.DK4']=3749
    ledger['reviewed_but_incomplete_route_record_IDs']['/data/SC2.DK4']=[r['id'] for r in rows]
    active=ledger['active_source_prose_drafts']
    for path,doc in zip(DOCS,manuscripts,strict=True):
        assert str(path) not in active['manuscripts'];active['manuscripts'].append(str(path));active['route_record_subsets_pending'][str(path)]=[r['id'] for r in doc['records']]
    note='5602 fresh rereads:5573 integrated/29 pending;source/prose5605. B167 credited once as pending;no completion or actual scene credit.'
    active.update(status='3-reviewed-COMMON-incomplete;29-Lil-B167-native-approved-pending-release',note=note)
    pending=dict(id=FAMILY,file_path='/data/SC2.DK4',blocks=[167],records=29,record_keys=selected,manuscript=str(DOCS[0]),manuscript_sha256=sha(DOCS[0].read_bytes()),manuscripts=approval['manuscripts'],proposed_revisions=16,retentions=13,source_prose_reviews_added=29,completion_credit_added=0,pending=NEXT,new_emulator_runs=0,actual_selected_B167_IDs=[])
    fresh['record_keys'].extend(selected);fresh['record_IDs'].extend(r['id'] for r in rows)
    fresh.update(fresh_pass_records_explicitly_reread=5602,fresh_pass_records_integrated=5573,fresh_pass_records_pending_native_actual_release=29,pending_record_keys=selected,pending_contextual_families=[pending],latest_pending_contextual_family=FAMILY,latest_contextual_manuscript=str(DOCS[0]),coverage_note=note)
    for unit in ledger['coverage_units']:
        if unit['id']=='all-route-scenes':unit.update(reviewed_route_records=4003,completed_route_records=3974,next=NEXT)
    ledger['coverage_units'].append({**pending,'status':manuscripts[0]['status'],'full_goal_complete':False})
    ledger['formatting_watchlist']['lil_B167_v4136']=dict(status='native-approved;pending-relocation-scene-choices-release',approval=str(APPROVAL),approval_sha256=sha(APPROVAL.read_bytes()),row_count_notes=11,all4_speech_and_menu_sheets_viewed=True,actual_selected_B167_IDs=[],new_emulator_runs=0)
    inventory=deepcopy(read(ledger['unfinished_editorial_scope_v4114']['path']))
    inventory.update(incomplete_route_source_prose_groups=[dict(family=FAMILY,file_path='/data/SC2.DK4',blocks=[167],count=29,record_IDs=[r['id'] for r in rows])],incomplete_route_source_prose_count=29,next_focus=NEXT)
    inventory['B167_fresh_context_review_checkpoint_v4136']=pending
    inventory['remaining_B168_B180_unreviewed_uncredited']=dict(physical_speeches=321,typed_choice_command_leads=0,not_full_Lil_or_project_denominator=True)
    inventory['remaining_B167_B180_inventory_is_historical_at_V4114']=True
    for unit in inventory['broader_coverage_units']:
        if unit['id']=='all-route-scenes':unit.update(reviewed_route_records=4003,completed_route_records=3974,source_prose_pending_records=29,source_prose_pending_family=FAMILY,next=NEXT)
    inv=ROOT/'unfinished_editorial_scope_inventory.json';save(inv,inventory)
    ledger['unfinished_editorial_scope_v4136']=dict(path=str(inv),sha256=sha(inv.read_bytes()),incomplete_COMMON=3,incomplete_route_source_prose=29,remaining_B168_B180_physical_speeches=321,remaining_choice_command_leads=0,canonical_Maria32_pending_uncredited=True,Proof_terminology_consistency_open=True,wider_story_shared_town_random_help_prose_open=True,full_goal_complete=False)
    paths=[PRIOR,APPROVAL,*DOCS,inv,Path(__file__),Path(approval['merged_native_proof'])]
    for key in ['source_context','control_contract','branch_proof','source_entry_proof','whole_exchange_context_notes','effective_current_comparison','native_font_proof','actor_terminology_reconciliation','source_effect_and_predicate_contract','source_nameplate_consumer_proof']:
        p=Path(manuscripts[0][key]);assert sha(p.read_bytes())==manuscripts[0][key+'_sha256'];paths.append(p)
    stable=[Path('translations/release_stack.json'),Path('translations/promoted_build.json'),Path('scripts/build_integrated_release.py')]
    evidence={str(p):sha(p.read_bytes()) for p in paths}
    ledger['lil_B167_scope_reconciliation_v4136']=dict(summary=SUMMARY,evidence=evidence,pending_family=pending,source_prose_reviews_added=29,completion_credit_added=0,full_goal_complete=False)
    ledger['latest_checkpoint']=SUMMARY
    for key in UNCHANGED:assert ledger[key]==before[key],key
    save(lp,ledger)
    section='## V4136: 29 B167 contextual/native reviews; integration pending\n\n'+SUMMARY+'\n\nApproval: '+APPROVAL.as_posix()+'. Unfinished scope: '+inv.as_posix()+'.\n\n'
    for i,p in enumerate(docs):
        first,rest=p.read_text(encoding='utf-8').split('\n',1);p.write_text(('# Current editorial handoff - V4136' if i==0 else first)+'\n\n'+section+rest,encoding='utf-8',newline='\n')
    save(ROOT/'checkpoint_receipt.json',dict(checkpoint='V4136',evidence=evidence,updated_files={str(p):sha(p.read_bytes()) for p in [lp,*docs]},preserved_release_files={str(p):sha(p.read_bytes()) for p in stable},prior_verified_handoff=str(PRIOR),new_source_prose_reviews=29,new_completed_records=0,proposed_revisions=16,justified_retentions=13,fresh_reread=5602,fresh_integrated=5573,fresh_pending=29,source_prose=5605,completed=5573,historical_revised=3551,historical_retained=2022,new_emulator_runs=0,all_jobs_terminal=True,full_goal_complete=False))
    print('V4136:5602 reread/5573 integrated/29 pending;5605 source/prose. V4110 experimental/V4046 main preserved; full goal active.')
