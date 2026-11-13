"""Credit 150 fresh reviews without claiming integration or Maria-copy completion."""
from collections import Counter
from copy import deepcopy
from pathlib import Path
from shutil import copy2
from dk4tool.patch.grand_race_menu_release import sha
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B111_B119_checkpoint_v3237')
PRIOR=Path('work/analysis/editorial_handoff_verification_v3215/verified_handoff.json')
MANUSCRIPTS=[Path('translations/lil_B111_B119_editorial_manuscript_v5.json'),Path('translations/lil_B111_B119_actor_style_manuscript_v4.json')]
APPROVAL=Path('work/analysis/lil_B111_B119_font_approval_v3236/approval_receipt.json')
MARIA=Path('work/analysis/lil_B111_B119_source_v3217/canonical_Maria32_deferred_source_lead.json')
BLOCKS=list(range(111,120));FAMILY='Lil-B111-B119-150'
SUMMARY='''V3237 records 150 fresh contextual reviews across Lil SC2 B111-B119: 116 speeches (115 ordinary and one FE gold notice) and 34 stored actor-style alternatives in six 4100 objects with 48 slots. Decisions are 47 revisions and 103 individually justified retentions. Each target has exact clean/current references, a fresh gloss, complete exchange context, effective-current comparison and all five review gates. Preserve the Buddhist rice offering and courtesy joke; one cargo hold; the grandfather-boy rescue and keepsake without Lil kinship; jade valuation and inferred building importance; reduced underground slave/drug trade and cacao; tablet/mosque material inference; Benazir's India map tip; possible figurehead reuse; tribal spiritual significance and exact 24,000 gold; and trend profits, smiles, food/casino humor and alternate Guild reporters. Current native actor19 is Carlo; the provisional Manuel note is superseded only for this new batch. No invented rank, relationship, sect, romance, place, cause or earned progress.

The original physical 182-object packet is now classified as 150 reachable Lil targets plus 32 appended Maria-copy speeches. Twelve original VM returns and conservative prefix graphs show ordinary SC0/SC1/SC2 entries return before their appended copies. The exact clean Japanese counterpart is reached at canonical SC3 B97; all 32 remain queued in the full editorial goal, without Lil macro dispatch or completion credit. Preserve the current SC2 B115 appended bytes exactly as unowned data during relocation. All 305 physical commands, 148 physical speeches and 64 relative spans remain mapped, including the copy. The native actor catalog, eight voices, CF/D0/D1/D6/D7/DC roles, 300 dispatch cases, 12 whole 4100 commands, 2,484 catalog pointers, 15 predicates and event319 query are bound without forcing roles, flags, outcomes or eligibility. The five actual virtual prefixes must stay out of stored alternative bodies; preserve real 20-byte headers and all 48 aliases.

All 149 progressive planes and one FE plane pass complete first/final/internal glyph, blank-paper, origin, bounds and single-page checks with 1,200 logical/compiled macro alignment cases. All 20 final sheets were viewed or hash-match viewed predecessors. One sharp-tongue wrap finding was resolved by a local successor formatter with all words retained: one new plane/eight new macro cases, 148 progressive planes/1,184 cases reused by exact bindings, and one FE plane/eight cases rebound unchanged. Forty-three source/consumer and 28 formatter negatives pass. Only 46 row-count notes remain; no weak-ending, orphan, control, glyph, alias, event-query, bounds or pagination waiver. The failed Windows path-spelling comparison and all producers/proofs are preserved; its successor normalizes path identity while keeping content-hash guards. Global helpers/runtime/ROM/registry remain unchanged.

Coverage is 4,575 fresh rereads, 4,425 integrated/completed and 150 pending integration; source/prose 4,578 including 2,748 SC2, with 2,976 reviewed route objects and 2,826 completed. Completion remains 3,040 historically revised plus 1,385 retained. Pending are 305-command inverse restoration, 64 span fixups/320 relocated native cases, 116 speech/six typed objects, unchanged unowned copy, 15 predicates/one event query, 150 final native planes/600 macro cases, 336 loaders/two parents/three entry censuses, representative reconciliation and a guarded registered cumulative release after full V3204 with an exact clean-input patch and fresh startup checks. Expected manifest is 517 batches/114 accepted layers. V3204 remains the registered experimental candidate with 515 batches, exact clean patch and 31 current opening/town framebuffer matches. V1492 remains promoted.

No new emulator run, selected B111-B119 scene, nameplate, earned reward/progress, full-route or hardware claim. All completed families remain completed. COMMON750-752 callers, canonical Maria32, every wider untouched storyline/shared shop-town/random/help/player prose, SourceItems/LocalProduct, five named-target leads and raw B141/SC3B109 classification remain open. Keep graphics/all18 plaques separate and retain the later older-record technical re-audit and queued0D validation-gap lead without asserting an older runtime defect. Preserve every ROM, earlier translation, executed producer/proof/failure and clean/canonical input. Full goal active; all jobs terminal.'''

if __name__=='__main__':
    assert not ROOT.exists()
    lp=Path('translations/editorial_review_current_v1.json');ledger=read(lp);before=deepcopy(ledger)
    assert sha(lp.read_bytes())==read(PRIOR)['ledger_sha256']
    doc,voice=map(read,MANUSCRIPTS);approval=read(APPROVAL);rows=doc['records']+voice['records'];ids=[r['id'] for r in rows]
    assert len(rows)==len(set(ids))==150 and Counter(r['editorial_decision'] for r in rows)=={'revise':47,'retain-wording':103}
    assert all(all(r['review'].values()) and r['source_meaning'] and r['context'] and r['localization_note'] for r in rows)
    assert all(r.get('fresh_retained_wording_justification') for r in rows if r['editorial_decision']=='retain-wording')
    assert approval['all150_five_review_gates_true'] and all(approval['manuscripts'][str(p)]==sha(p.read_bytes()) for p in MANUSCRIPTS)
    source,control,branch=map(read,[doc['source_context'],doc['control_contract'],doc['branch_proof']])
    assert source['total_editorial_objects']==150 and len(source['records'])==116 and len(source['typed_actor_style_records'])==34 and not source['typed_choice_records']
    assert [b['block'] for b in source['blocks']]==BLOCKS and sum(len(b['all_clean_native_commands']) for b in source['blocks'])==305
    assert source['total_stored_physical_speeches_including_unreachable_copies']==148 and len(source['unowned_appended_Maria_copy_records'])==32
    assert len(branch['cases'])==640 and len(branch['operands_requiring_adjustment_when_resizing'])==64
    assert len(control['speech_and_stored_alternative_dispatch_cases'])==300 and len(control['whole_original4100_command_cases'])==12
    assert len(control['current_original_predicate_cases'])==16 and len(control['original_event_queries'])==1
    fresh=ledger['contextual_story_natural_dialogue_pass_v1871']
    assert (fresh['fresh_pass_records_explicitly_reread'],fresh['fresh_pass_records_integrated'],fresh['fresh_pass_records_pending_native_actual_release'])==(4425,4425,0)
    selected=[dict(file_path='/data/SC2.DK4',id=n) for n in ids];keys={historical_key(r) for r in fresh['record_keys']}
    assert not {historical_key(r) for r in selected}&keys
    assert {historical_key(r) for g in ledger['completed_editorial_families'] for r in g['records']}==keys
    assert ledger['records_with_source_and_prose_pass']==ledger['records_with_source_prose_drafts']==4428
    assert not any(ledger['reviewed_but_incomplete_route_record_IDs'].values())
    docs=[Path('docs')/n for n in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']]
    assert docs[0].read_text(encoding='utf-8').startswith('# Current editorial handoff - V3214')
    ROOT.mkdir(parents=True)
    for p in [lp,*docs]:copy2(p,ROOT/(p.name+'.before'))
    ledger['records_with_source_and_prose_pass']=ledger['records_with_source_prose_drafts']=4578
    ledger['source_prose_reviewed_counts_by_file']['/data/SC2.DK4']=2748
    ledger['reviewed_but_incomplete_route_record_IDs']['/data/SC2.DK4']=ids
    active=ledger['active_source_prose_drafts']
    for p,d in zip(MANUSCRIPTS,[doc,voice],strict=True):
        active['manuscripts'].append(str(p));active['route_record_subsets_pending'][str(p)]=[r['id'] for r in d['records']]
    active.update(status='3-reviewed-COMMON-incomplete;150-Lil-B111-B119-native-reviewed-pending-release',note='4575 fresh rereads:4425 integrated and150 pending relocation, representative reconciliation and registered release. Source/prose4578; canonical Maria32, COMMON750-752 and every wider untouched prose family remain open.')
    fresh['record_keys'].extend(selected);fresh['record_IDs'].extend(ids)
    pending=dict(id=FAMILY,file_path='/data/SC2.DK4',blocks=BLOCKS,records=150,record_keys=selected,manuscripts={str(p):sha(p.read_bytes()) for p in MANUSCRIPTS},manuscript=str(MANUSCRIPTS[0]),manuscript_sha256=sha(MANUSCRIPTS[0].read_bytes()),actor_styles=str(MANUSCRIPTS[1]),actor_styles_sha256=sha(MANUSCRIPTS[1].read_bytes()),proposed_revisions=47,retentions=103,source_prose_reviews_added=150,completion_credit_added=0,native_font_proof=doc['native_font_proof'],pending='305physical commands/64spans/320relocatedcases;116active speech+6whole4100/34unique/48slots;32unowned copy speeches byte-exact;15predicates+1query;150finalplanes/600macrocases;336loaders/twoparents/threeentrycensuses;representative reconciliation and guarded registered release afterfullV3204/exactcleanpatch/currentstartup.',new_emulator_runs=0)
    fresh.update(fresh_pass_records_explicitly_reread=4575,fresh_pass_records_integrated=4425,fresh_pass_records_pending_native_actual_release=150,pending_record_keys=selected,pending_contextual_families=[pending],latest_pending_contextual_family=FAMILY,latest_contextual_manuscript=str(MANUSCRIPTS[0]),latest_contextual_actor_style_draft=str(MANUSCRIPTS[1]),coverage_note=active['note'])
    for u in ledger['coverage_units']:
        if u['id']=='all-route-scenes':u.update(reviewed_route_records=2976,completed_route_records=2826,next='Integrate150 reviewed B111-B119 Lil targets; canonical32 Maria SC3B97 and every wider untouched route/shared shop-town/random/help/player prose family remain open.')
    ledger['coverage_units'].append({**pending,'status':'source-prose-current-native-format-approved;relocation-representative-release-pending','full_goal_complete':False})
    ledger['formatting_watchlist']['lil_B111_B119_v3237']=dict(status='150native planes/1200macro cases pass;relocation/finalpadding/representative/release pending',source_context=doc['source_context'],control_contract=doc['control_contract'],branch_proof=doc['branch_proof'],native_font_proof=doc['native_font_proof'],approval=str(APPROVAL),narrow_line_count_notes=46,all20_final_sheets_viewed_or_identical=True,no_open_final_target_native_font_finding=True,no_orphan_predicate_query_or_missing_glyph_waivers=True,actual_selected_B111_B119_IDs=[],new_emulator_runs=0)
    requirements=ROOT/'next_registered_integration_requirements.json'
    save(requirements,dict(parent_profile='all-routes-unified-v3204',parent_ROM=doc['current_ROM'],parent_ROM_sha256=doc['current_ROM_sha256'],manuscripts={str(p):sha(p.read_bytes()) for p in MANUSCRIPTS},source_context=doc['source_context'],control_contract=doc['control_contract'],branch_proof=doc['branch_proof'],native_fonts=doc['native_font_proof'],classification=doc['appended_copy_classification'],native_formatter_module=doc['native_formatter_module'],native_formatter_module_sha256=doc['native_formatter_module_sha256'],blocks=BLOCKS,progressive=149,ordinary_speech=115,actor_style_alternatives=34,actor_style_objects=6,actor_style_slots=48,FE_panels=1,choice_labels=0,commands=305,physical_speeches=148,active_editorial_speeches=116,unowned_Maria_copy_speeches=32,relative_sites=64,relocated_skip_cases=320,original_predicates=15,event_queries=1,next=pending['pending'],expected_manifest_batches=517,expected_accepted_layers=114,preserve_all5_actual_virtual_prefixes_and20byte_headers=True,preserve_unowned_current_B115_tail_exact_while_moving=True,canonical_Maria32_still_queued=True,preserve_every_ROM_translation_profile_accepted114_and_V1492_promotion=True,full_goal_complete=False))
    inventory=deepcopy(read(ledger['unfinished_editorial_scope_v3214']['path']))
    inventory.update(incomplete_route_source_prose_groups=[dict(family=FAMILY,file_path='/data/SC2.DK4',blocks=BLOCKS,count=150,record_IDs=ids)],incomplete_route_source_prose_count=150,next_focus='Integrate150 reviewed B111-B119 Lil targets, then continue every untouched route/shared shop-town/random/help/player prose family, including canonical32 Maria SC3B97. Keep graphics separate and retain later technical re-audit.')
    inventory['lil_B111_B119_fresh_context_review_checkpoint']=dict(checkpoint='V3237',status='150source-prose-native-reviewed;integration-pending',manuscripts=[str(p) for p in MANUSCRIPTS],historical182_physical_lead_classified=True,reachable_Lil_targets=150,canonical_Maria32_pending_source_lead=str(MARIA),canonical_Maria32_pending_source_lead_sha256=sha(MARIA.read_bytes()),unowned32_copy_not_completed_or_discarded=True,no_whole_goal_completion_credit=True)
    inventory['canonical_Maria_SC3_B97_uncredited32_source_lead']=dict(path=str(MARIA),sha256=sha(MARIA.read_bytes()),records=32,all_editorial_Maria_binding_and_release_gates_pending=True,source_prose_or_completion_credit_added=0)
    for u in inventory['broader_coverage_units']:
        if u['id']=='all-route-scenes':u.update(reviewed_route_records=2976,completed_route_records=2826,source_prose_pending_records=150,source_prose_pending_family=FAMILY,next=inventory['next_focus'])
    inv=ROOT/'unfinished_editorial_scope_inventory.json';save(inv,inventory)
    ledger['unfinished_editorial_scope_v3237']=dict(path=str(inv),sha256=sha(inv.read_bytes()),incomplete_COMMON=3,incomplete_route_source_prose=150,canonical_Maria32_still_uncredited=True,full_goal_complete=False)
    ledger['lil_B111_B119_scope_reconciliation_v3237']=dict(historical182_source_lead_preserved=True,reachable_reviewed_Lil_targets=150,unowned_appended_Maria_copy_speeches=32,canonical_Maria_source_lead=str(MARIA),canonical_Maria_source_lead_sha256=sha(MARIA.read_bytes()),classification=doc['appended_copy_classification'],classification_sha256=doc['appended_copy_classification_sha256'],no_Lil_company_dispatch_or_completion_credit_for_Maria32=True)
    evidence={str(p):sha(p.read_bytes()) for p in [*MANUSCRIPTS,APPROVAL,PRIOR,MARIA,requirements,inv,Path(doc['source_context']),Path(doc['control_contract']),Path(doc['branch_proof']),Path(doc['whole_exchange_context_notes']),Path(doc['item_terminology_reconciliation']),Path(doc['actor_voice_contract']),Path(doc['effective_current_comparison']),Path(doc['appended_copy_classification']),Path(doc['native_font_proof']),Path(doc['native_formatter_module']),Path(doc['scoped_profile_module']),Path(__file__),*[Path(s['path']) for s in approval['all20_review_sheets']]]}
    ledger['lil_B111_B119_source_prose_native_v3237']=dict(summary=SUMMARY,**pending,evidence=evidence,goal_turn_classification='progress',full_goal_complete=False)
    ledger['latest_checkpoint']=SUMMARY
    for k in ['completed_editorial_families','records_editorially_completed','records_revised_and_integrated','retained_wordings_editorially_completed','completed_editorial_record_counts_by_file','current_integrated_candidate','reviewed_but_incomplete_COMMON_IDs','unresolved_graphics_work','older_record_reaudit_after_full_editorial_goal','native_source_universe_inventory_v2701c','lil_B111_B119_next_source_lead_v3214']:
        assert ledger[k]==before[k],k
    assert len(fresh['record_keys'])==len({historical_key(r) for r in fresh['record_keys']})==4575
    assert len(fresh['integrated_record_keys'])==4425 and ledger['goal_status']=='active' and not ledger['full_goal_complete']
    save(lp,ledger)
    section='## V3237: 150 Lil reviews; canonical Maria32 queued; integration pending\n\n'+SUMMARY+'\n\nApproval: '+APPROVAL.as_posix()+'. Integration: '+requirements.as_posix()+'. Unfinished scope: '+inv.as_posix()+'.\n\n'
    for i,p in enumerate(docs):
        first,rest=p.read_text(encoding='utf-8').split('\n',1)
        p.write_text(('# Current editorial handoff - V3237' if i==0 else first)+'\n\n'+section+rest,encoding='utf-8',newline='\n')
    candidate=ledger['current_integrated_candidate']
    save(ROOT/'checkpoint_receipt.json',dict(checkpoint='V3237',summary=SUMMARY,evidence=evidence,updated_files={str(p):sha(p.read_bytes()) for p in [lp,*docs]},prior_verified_handoff=str(PRIOR),new_completed_records=0,new_source_prose_reviews=150,proposed_revisions=47,justified_retentions=103,fresh_reread=4575,fresh_integrated=4425,fresh_pending=150,source_prose=4578,completed=4425,historical_revised=3040,historical_retained=1385,incomplete_COMMON=3,incomplete_route=150,canonical_Maria32_pending=True,candidate=candidate['path'],candidate_sha256=candidate['sha256'],patch=candidate['patch'],patch_sha256=candidate['patch_sha256'],next_requirements=str(requirements),actual_selected_B111_B119_IDs=[],new_emulator_runs=0,goal_turn_classification='progress',all_jobs_terminal=True,full_goal_complete=False))
    print('V3237:150new reviews,47revisions/103retentions;4575reread/4425integrated/150pending;source-prose4578. CanonicalMaria32queued;V3204 preserved;fullgoalactive.')
