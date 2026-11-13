"""Stage thirteen native-approved B178 reviews once; deep independent apply remains required."""
from copy import deepcopy
from pathlib import Path
from shutil import copy2
from dk4tool.patch.grand_race_menu_release import sha
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.lil_B178_checkpoint_text_v4679 import NEXT,SUMMARY
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B178_checkpoint_v4679')
PRIOR=Path('work/analysis/editorial_handoff_verification_v4674/verified_handoff.json')
APPROVAL=Path('work/analysis/lil_B178_native_approval_v4678/approval_receipt.json')
DOC=Path('translations/lil_B178_editorial_manuscript_v3.json')
FAMILY='Lil-B178-home-baking-three-Ladies-husband-corner-bakery-teaching-ingredients-and-prospective-Amsterdam-wheat13'

if __name__=='__main__':
    assert not ROOT.exists()
    lp=Path('translations/editorial_review_current_v1.json');ledger=read(lp)
    assert sha(lp.read_bytes())==read(PRIOR)['ledger_sha256']
    approval,doc=read(APPROVAL),read(DOC);rows=doc['records']
    assert approval['manuscripts']=={str(DOC):sha(DOC.read_bytes())}
    assert len(rows)==13 and all(all(r['review'].values()) for r in rows)
    fresh=ledger['contextual_story_natural_dialogue_pass_v1871']
    assert tuple(fresh[k] for k in ['fresh_pass_records_explicitly_reread','fresh_pass_records_integrated',
        'fresh_pass_records_pending_native_actual_release'])==(5885,5885,0)
    selected=[dict(file_path='/data/SC2.DK4',id=r['id']) for r in rows]
    assert len({historical_key(r) for r in selected})==13
    assert not {historical_key(r) for r in selected}&{historical_key(r) for r in fresh['record_keys']}
    assert ledger['records_with_source_and_prose_pass']==5888 and ledger['source_prose_reviewed_counts_by_file']['/data/SC2.DK4']==4032
    inventory_source=read('work/analysis/lil_B161_B180_clean_scope_v3910/complete_clean_B161_B180_next_exchange_inventory.json')
    remaining=[r for r in inventory_source['blocks'] if r['block'] in [179,180]]
    assert len(remaining)==2 and sum(r['speeches'] for r in remaining)==25 and sum(r['typed_menu_2100_commands'] for r in remaining)==0
    docs=[Path('docs')/n for n in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']]
    assert docs[0].read_text(encoding='utf-8').startswith('# Current editorial handoff - V4673')
    ROOT.mkdir(parents=True)
    for p in [lp,*docs]:copy2(p,ROOT/(p.name+'.before'))
    ledger['records_with_source_and_prose_pass']=ledger['records_with_source_prose_drafts']=5901
    ledger['source_prose_reviewed_counts_by_file']['/data/SC2.DK4']=4045
    ledger['reviewed_but_incomplete_route_record_IDs']['/data/SC2.DK4']=[r['id'] for r in rows]
    active=ledger['active_source_prose_drafts'];assert str(DOC) not in active['manuscripts']
    active['manuscripts'].append(str(DOC));active['route_record_subsets_pending'][str(DOC)]=[r['id'] for r in rows]
    note='5898 fresh rereads:5885 integrated/13 pending;source/prose5901. B178 credited once as pending;no completion or actual scene credit.'
    active.update(status='3-reviewed-COMMON-incomplete;13-Lil-B178-native-approved-pending-release',note=note)
    pending=dict(id=FAMILY,file_path='/data/SC2.DK4',blocks=[178],records=13,record_keys=selected,
        manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),manuscripts=approval['manuscripts'],
        proposed_revisions=2,retentions=11,source_prose_reviews_added=13,completion_credit_added=0,
        pending=NEXT,new_emulator_runs=0,actual_selected_B178_IDs=[])
    fresh['record_keys'].extend(selected);fresh['record_IDs'].extend(r['id'] for r in rows)
    fresh.update(fresh_pass_records_explicitly_reread=5898,fresh_pass_records_integrated=5885,
        fresh_pass_records_pending_native_actual_release=13,pending_record_keys=selected,pending_contextual_families=[pending],
        latest_pending_contextual_family=FAMILY,latest_contextual_manuscript=str(DOC),coverage_note=note)
    for unit in ledger['coverage_units']:
        if unit['id']=='all-route-scenes':unit.update(reviewed_route_records=4299,completed_route_records=4286,next=NEXT)
    ledger['coverage_units'].append({**pending,'status':doc['status'],'full_goal_complete':False})
    ledger['formatting_watchlist']['lil_B178_v4679']=dict(status='native-approved;pending-relocation-representative-release',
        approval=str(APPROVAL),approval_sha256=sha(APPROVAL.read_bytes()),row_count_notes=5,
        all2_mixed_speech_sheets_viewed=True,actual_selected_B178_IDs=[],new_emulator_runs=0)
    previous=ledger['unfinished_editorial_scope_v4659'];assert sha(Path(previous['path']).read_bytes())==previous['sha256']
    inventory=deepcopy(read(previous['path']))
    inventory.update(incomplete_route_source_prose_groups=[dict(family=FAMILY,file_path='/data/SC2.DK4',blocks=[178],count=13,record_IDs=[r['id'] for r in rows])],
        incomplete_route_source_prose_count=13,next_focus=NEXT)
    inventory['B178_fresh_context_review_checkpoint_v4679']=pending
    inventory['remaining_B179_B180_unreviewed_uncredited']=dict(physical_speeches=25,typed_choice_command_leads=0,not_full_Lil_or_project_denominator=True)
    inventory['earlier_B178_uncredited_leads_are_historical_after_V4679']=True
    for unit in inventory['broader_coverage_units']:
        if unit['id']=='all-route-scenes':unit.update(reviewed_route_records=4299,completed_route_records=4286,source_prose_pending_records=13,source_prose_pending_family=FAMILY,next=NEXT)
    inv=ROOT/'unfinished_editorial_scope_inventory.json';save(inv,inventory)
    ledger['unfinished_editorial_scope_v4679']=dict(path=str(inv),sha256=sha(inv.read_bytes()),incomplete_COMMON=3,incomplete_route_source_prose=13,
        remaining_B179_B180_physical_speeches=25,remaining_choice_command_leads=0,canonical_Maria32_pending_uncredited=True,
        Proof_terminology_consistency_open=True,wider_story_shared_town_random_help_prose_open=True,full_goal_complete=False)
    paths=[PRIOR,APPROVAL,DOC,inv,Path(__file__),Path(approval['merged_native_proof'])]
    for key in ['source_context','control_contract','branch_proof','source_entry_proof','whole_exchange_context_notes','effective_current_comparison',
        'native_font_proof','actor_terminology_reconciliation','source_effect_and_predicate_contract','source_nameplate_consumer_proof']:
        p=Path(doc[key]);assert sha(p.read_bytes())==doc[key+'_sha256'];paths.append(p)
    evidence={str(p):sha(p.read_bytes()) for p in paths}
    ledger['lil_B178_scope_reconciliation_v4679']=dict(summary=SUMMARY,evidence=evidence,pending_family=pending,
        source_prose_reviews_added=13,completion_credit_added=0,full_goal_complete=False)
    ledger['latest_checkpoint']=SUMMARY;planned={lp:encode_ledger(ledger)}
    assert len(planned[lp])<100*1024*1024
    section='## V4679:13 B178 contextual/native reviews;integration pending\n\n'+SUMMARY+'\n\nApproval: '+APPROVAL.as_posix()+'. Unfinished scope: '+inv.as_posix()+'.\n\nNext: '+NEXT+'\n\n'
    for i,p in enumerate(docs):
        first,rest=p.read_text(encoding='utf-8').split('\n',1)
        planned[p]=(('# Current editorial handoff - V4679' if i==0 else first)+'\n\n'+section+rest).encode('utf-8')
    staged=ROOT/'staged';staged.mkdir();plan=[]
    for i,(p,data) in enumerate(planned.items()):
        out=staged/f'{i}.planned';out.write_bytes(data)
        plan.append(dict(target=str(p.resolve()),before_sha256=sha(p.read_bytes()),planned=str(out.resolve()),planned_sha256=sha(data)))
    save(ROOT/'mutation_plan.json',plan)
    stable=['translations/release_stack.json','translations/promoted_build.json','scripts/build_integrated_release.py','translations/rom_retention_pins.json']
    save(ROOT/'staged_receipt.json',dict(checkpoint='V4679',evidence=evidence,preserved_release_files={p:sha(Path(p).read_bytes()) for p in stable},
        prior_verified_handoff=str(PRIOR),new_source_prose_reviews=13,new_completed_records=0,proposed_revisions=2,justified_retentions=11,
        fresh_reread=5898,fresh_integrated=5885,fresh_pending=13,source_prose=5901,completed=5885,
        historical_revised=3738,historical_retained=2147,new_emulator_runs=0,all_jobs_terminal=True,full_goal_complete=False))
    print('V4679 staged:5898 reread/5885 completed/13 pending;5901 source/prose. Deep independent audit required before metadata writes.')
