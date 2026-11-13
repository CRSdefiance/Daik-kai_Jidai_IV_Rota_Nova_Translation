"""Stage fourteen native-approved B179 reviews once; deep independent apply remains required."""
from copy import deepcopy
from pathlib import Path
from shutil import copy2
from dk4tool.patch.grand_race_menu_release import sha
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.lil_B179_checkpoint_text_v4727 import NEXT,SUMMARY
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B179_checkpoint_v4727')
PRIOR=Path('work/analysis/promotion_v4725b/promotion_receipt.json')
APPROVAL=Path('work/analysis/lil_B179_native_approval_v4726/approval_receipt.json')
DOC=Path('translations/lil_B179_editorial_manuscript_v3.json')
FAMILY='Lil-B179-Barkeep-Patron-Sailor-wine-trial-three-gulps-joining-order-and-prospective-Sao-Jorge14'

if __name__=='__main__':
    assert not ROOT.exists()
    lp=Path('translations/editorial_review_current_v1.json');ledger=read(lp)
    assert sha(lp.read_bytes())==read(PRIOR)['ledger_sha256']
    approval,doc=read(APPROVAL),read(DOC);rows=doc['records']
    assert approval['manuscripts']=={str(DOC):sha(DOC.read_bytes())}
    assert len(rows)==14 and all(all(r['review'].values()) for r in rows)
    fresh=ledger['contextual_story_natural_dialogue_pass_v1871']
    assert tuple(fresh[k] for k in ['fresh_pass_records_explicitly_reread','fresh_pass_records_integrated',
        'fresh_pass_records_pending_native_actual_release'])==(5898,5898,0)
    selected=[dict(file_path='/data/SC2.DK4',id=r['id']) for r in rows]
    assert len({historical_key(r) for r in selected})==14
    assert not {historical_key(r) for r in selected}&{historical_key(r) for r in fresh['record_keys']}
    assert ledger['records_with_source_and_prose_pass']==5901 and ledger['source_prose_reviewed_counts_by_file']['/data/SC2.DK4']==4045
    inventory_source=read('work/analysis/lil_B161_B180_clean_scope_v3910/complete_clean_B161_B180_next_exchange_inventory.json')
    remaining=[r for r in inventory_source['blocks'] if r['block']==180]
    assert len(remaining)==1 and sum(r['speeches'] for r in remaining)==11 and sum(r['typed_menu_2100_commands'] for r in remaining)==0
    docs=[Path('docs')/n for n in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']]
    assert docs[0].read_text(encoding='utf-8').startswith('# Current editorial handoff - V4725')
    ROOT.mkdir(parents=True)
    for p in [lp,*docs]:copy2(p,ROOT/(p.name+'.before'))
    ledger['records_with_source_and_prose_pass']=ledger['records_with_source_prose_drafts']=5915
    ledger['source_prose_reviewed_counts_by_file']['/data/SC2.DK4']=4059
    ledger['reviewed_but_incomplete_route_record_IDs']['/data/SC2.DK4']=[r['id'] for r in rows]
    active=ledger['active_source_prose_drafts'];assert str(DOC) not in active['manuscripts']
    active['manuscripts'].append(str(DOC));active['route_record_subsets_pending'][str(DOC)]=[r['id'] for r in rows]
    note='5912 fresh rereads:5898 integrated/14 pending;source/prose5915. B179 credited once as pending;no completion or actual scene credit.'
    active.update(status='3-reviewed-COMMON-incomplete;14-Lil-B179-native-approved-pending-release',note=note)
    pending=dict(id=FAMILY,file_path='/data/SC2.DK4',blocks=[179],records=14,record_keys=selected,
        manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),manuscripts=approval['manuscripts'],
        proposed_revisions=8,retentions=6,source_prose_reviews_added=14,completion_credit_added=0,
        pending=NEXT,new_emulator_runs=0,actual_selected_B179_IDs=[])
    fresh['record_keys'].extend(selected);fresh['record_IDs'].extend(r['id'] for r in rows)
    fresh.update(fresh_pass_records_explicitly_reread=5912,fresh_pass_records_integrated=5898,
        fresh_pass_records_pending_native_actual_release=14,pending_record_keys=selected,pending_contextual_families=[pending],
        latest_pending_contextual_family=FAMILY,latest_contextual_manuscript=str(DOC),coverage_note=note)
    for unit in ledger['coverage_units']:
        if unit['id']=='all-route-scenes':unit.update(reviewed_route_records=4313,completed_route_records=4299,next=NEXT)
    ledger['coverage_units'].append({**pending,'status':doc['status'],'full_goal_complete':False})
    ledger['formatting_watchlist']['lil_B179_v4727']=dict(status='native-approved;pending-relocation-representative-release',
        approval=str(APPROVAL),approval_sha256=sha(APPROVAL.read_bytes()),row_count_notes=4,
        all2_mixed_speech_sheets_viewed=True,actual_selected_B179_IDs=[],new_emulator_runs=0)
    previous=ledger['unfinished_editorial_scope_v4725']
    inventory=deepcopy(previous)
    inventory.update(incomplete_route_source_prose_groups=[dict(family=FAMILY,file_path='/data/SC2.DK4',blocks=[179],count=14,record_IDs=[r['id'] for r in rows])],
        incomplete_route_source_prose_count=14,next_focus=NEXT)
    inventory['B179_fresh_context_review_checkpoint_v4727']=pending
    inventory['remaining_B180_unreviewed_uncredited']=dict(physical_speeches=11,typed_choice_command_leads=0,not_full_Lil_or_project_denominator=True)
    inventory['earlier_B179_uncredited_leads_are_historical_after_V4727']=True
    for unit in inventory['broader_coverage_units']:
        if unit['id']=='all-route-scenes':unit.update(reviewed_route_records=4313,completed_route_records=4299,source_prose_pending_records=14,source_prose_pending_family=FAMILY,next=NEXT)
    inv=ROOT/'unfinished_editorial_scope_inventory.json';save(inv,inventory)
    ledger['unfinished_editorial_scope_v4727']=dict(path=str(inv),sha256=sha(inv.read_bytes()),incomplete_COMMON=3,incomplete_route_source_prose=14,
        remaining_B180_physical_speeches=11,remaining_choice_command_leads=0,canonical_Maria32_pending_uncredited=True,
        Proof_terminology_consistency_open=True,wider_story_shared_town_random_help_prose_open=True,full_goal_complete=False)
    paths=[PRIOR,APPROVAL,DOC,inv,Path(__file__),Path(approval['merged_native_proof'])]
    for key in ['source_context','control_contract','branch_proof','source_entry_proof','whole_exchange_context_notes','effective_current_comparison',
        'native_font_proof','actor_terminology_reconciliation','source_effect_and_predicate_contract','source_nameplate_consumer_proof','separate_untranslated_city_alias_lead']:
        p=Path(doc[key]);assert sha(p.read_bytes())==doc[key+'_sha256'];paths.append(p)
    evidence={str(p):sha(p.read_bytes()) for p in paths}
    ledger['lil_B179_scope_reconciliation_v4727']=dict(summary=SUMMARY,evidence=evidence,pending_family=pending,
        source_prose_reviews_added=14,completion_credit_added=0,full_goal_complete=False)
    ledger['latest_checkpoint']=SUMMARY;planned={lp:encode_ledger(ledger)}
    assert len(planned[lp])<100*1024*1024
    section='## V4727:14 B179 contextual/native reviews;integration pending\n\n'+SUMMARY+'\n\nApproval: '+APPROVAL.as_posix()+'. Unfinished scope: '+inv.as_posix()+'.\n\nNext: '+NEXT+'\n\n'
    for i,p in enumerate(docs):
        first,rest=p.read_text(encoding='utf-8').split('\n',1)
        planned[p]=(('# Current editorial handoff - V4727' if i==0 else first)+'\n\n'+section+rest).encode('utf-8')
    staged=ROOT/'staged';staged.mkdir();plan=[]
    for i,(p,data) in enumerate(planned.items()):
        out=staged/f'{i}.planned';out.write_bytes(data)
        plan.append(dict(target=str(p.resolve()),before_sha256=sha(p.read_bytes()),planned=str(out.resolve()),planned_sha256=sha(data)))
    save(ROOT/'mutation_plan.json',plan)
    stable=['translations/release_stack.json','translations/promoted_build.json','scripts/build_integrated_release.py','translations/rom_retention_pins.json']
    save(ROOT/'staged_receipt.json',dict(checkpoint='V4727',evidence=evidence,preserved_release_files={p:sha(Path(p).read_bytes()) for p in stable},
        prior_verified_handoff=str(PRIOR),new_source_prose_reviews=14,new_completed_records=0,proposed_revisions=8,justified_retentions=6,
        fresh_reread=5912,fresh_integrated=5898,fresh_pending=14,source_prose=5915,completed=5898,
        historical_revised=3740,historical_retained=2158,new_emulator_runs=0,all_jobs_terminal=True,full_goal_complete=False))
    print('V4727 staged:5912 reread/5898 completed/14 pending;5915 source/prose. Deep independent audit required before metadata writes.')
