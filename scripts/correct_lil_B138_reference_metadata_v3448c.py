"""Correct one inherited map label through immutable successors and a full audit chain."""
from copy import deepcopy
from pathlib import Path
from shutil import copy2
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B138_reference_metadata_repair_v3448')
OLDMAP=Path('translations/lil_B138_editorial_relocation_map_v1.json')
NEWMAP=Path('translations/lil_B138_editorial_relocation_map_v2.json')
OLDDOC=Path('translations/lil_B138_editorial_manuscript_v7.json')
NEWDOC=Path('translations/lil_B138_editorial_manuscript_v8.json')
OLDAPP=Path('work/analysis/lil_B138_reference_approval_v3446/approval_receipt.json')
NEWAPP=Path('work/analysis/lil_B138_reference_approval_v3446c/approval_receipt.json')
if __name__=='__main__':
    assert not ROOT.exists() and not NEWAPP.exists()
    oldkey='all12_relocated_predicate_pairs_preserve_source_operands_results_and_unowned_RAM';newkey='all10_predicates_and1_query_current_relocated_results_and_source_operands_equal'
    mapping=read(OLDMAP);assert mapping.pop(oldkey) is True and newkey not in mapping
    control=read(mapping['relocated_control_proof']);assert len(control['relocated_predicate_pairs'])==11 and sum(c['word']==0x8000 for c in control['relocated_predicate_pairs'])==10 and len(control['original_event_queries'])==1
    mapping[newkey]=True;mapping.update(previous_reference_map=str(OLDMAP),previous_reference_map_sha256=sha(OLDMAP.read_bytes()),metadata_correction='The proven scope is ten predicates and one query,not twelve predicates. No mapped command,operand,target byte orapproval gate is changed.')
    if NEWMAP.exists():assert read(NEWMAP)==mapping
    else:save(NEWMAP,mapping)
    doc=read(OLDDOC);doc.update(previous_manuscript=str(OLDDOC),previous_manuscript_sha256=sha(OLDDOC.read_bytes()),reference_map=str(NEWMAP),reference_map_sha256=sha(NEWMAP.read_bytes()))
    if NEWDOC.exists():assert read(NEWDOC)==doc
    else:save(NEWDOC,doc)
    approval=read(OLDAPP);hashes={p:d for p,d in approval['hashes'].items() if Path(p) not in [OLDDOC,OLDMAP]};hashes.update({str(p):sha(p.read_bytes()) for p in [NEWDOC,NEWMAP,OLDDOC,OLDMAP,OLDAPP,Path(__file__)]})
    approval.update(manuscript=str(NEWDOC),reference_map=str(NEWMAP),hashes=hashes,previous_approval=str(OLDAPP),previous_approval_sha256=sha(OLDAPP.read_bytes()),inherited_count_label_corrected_without_repeating_native_checks=True,producer_sha256=sha(Path(__file__).read_bytes()));NEWAPP.parent.mkdir(parents=True);save(NEWAPP,approval)
    lp=Path('translations/editorial_review_current_v1.json');ledger=read(lp);intermediate=Path('work/analysis/lil_B138_reference_checkpoint_v3447/checkpoint_receipt.json');previous=read(intermediate)
    assert sha(lp.read_bytes())==previous['updated_files'][str(lp)] and ledger['contextual_story_natural_dialogue_pass_v1871']['latest_contextual_manuscript']==str(OLDDOC)
    documents=[Path('docs')/n for n in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']];assert documents[0].read_text(encoding='utf-8').startswith('# Current editorial handoff - V3447');ROOT.mkdir(parents=True)
    for p in [lp,*documents]:copy2(p,ROOT/(p.name+'.before'))
    correction=dict(previous_map=str(OLDMAP),previous_map_sha256=sha(OLDMAP.read_bytes()),corrected_map=str(NEWMAP),corrected_map_sha256=sha(NEWMAP.read_bytes()),incorrect_key=oldkey,correct_key=newkey,actual_predicates=10,actual_queries=1,actual_conditional_pairs=11,no_prose_compiled_bytes_source_operands_or_test_results_changed=True,original_failed_auditor='scripts/verify_editorial_handoff_v3447b.py',original_failed_auditor_sha256=sha(Path('scripts/verify_editorial_handoff_v3447b.py').read_bytes()),all_prior_artifacts_preserved=True)
    correction['failed_preparer_preserved']='scripts/correct_lil_B138_reference_metadata_v3448.py';correction['partial_map2_and_manuscript8_reused_only_after_exact_dict_equality']=True
    proof=ROOT/'reference_metadata_successors.json';save(proof,correction)
    originalreq=Path(ledger['lil_B138_reference_approval_v3447']['requirements']);requirements=read(originalreq);requirements.update(manuscript=str(NEWDOC),reference_map=str(NEWMAP));req=ROOT/'next_registered_integration_requirements.json';save(req,requirements)
    summary=ledger['latest_checkpoint'].replace('V3447','V3448')+'\n\nIndependent review caught an inherited map-key label claiming twelve predicate pairs. The tested scope is ten predicates and one query. The map v2/manuscript v8/approval successor correct only that metadata label; all source,prose,compiled target bytes,reference mappings andnative results remain unchanged. The failed map v1,manuscript v7,approval and first auditor remain preserved. Registered integration/exact patch/startup remain pending;full goal active.'
    fresh=ledger['contextual_story_natural_dialogue_pass_v1871'];fresh['latest_contextual_manuscript']=str(NEWDOC)
    for p in fresh['pending_contextual_families']:p.update(manuscript=str(NEWDOC),manuscript_sha256=sha(NEWDOC.read_bytes()),reference_map=str(NEWMAP))
    active=ledger['active_source_prose_drafts'];active['manuscripts'].append(str(NEWDOC));active['route_record_subsets_pending'][str(NEWDOC)]=[r['id'] for r in doc['records']]
    for u in ledger['coverage_units']:
        if u['id']=='Lil-B138-44':u.update(manuscript=str(NEWDOC),manuscript_sha256=sha(NEWDOC.read_bytes()),reference_map=str(NEWMAP))
    evidence={**ledger['lil_B138_reference_approval_v3447']['evidence'],**{str(p):sha(p.read_bytes()) for p in [NEWDOC,NEWMAP,NEWAPP,proof,intermediate,req,Path(__file__)]}}
    lead=deepcopy(ledger['lil_B138_reference_approval_v3447']);lead.update(summary=summary,manuscript=str(NEWDOC),manuscript_sha256=sha(NEWDOC.read_bytes()),evidence=evidence,requirements=str(req),requirements_sha256=sha(req.read_bytes()),metadata_repair=str(proof));ledger['lil_B138_reference_approval_v3447']=lead
    inventory=deepcopy(read(ledger['unfinished_editorial_scope_v3447']['path']));inventory['B138_references_ready_v3447']=lead;inventory['B138_reference_metadata_repair_v3448']=correction
    inv=ROOT/'unfinished_editorial_scope_inventory.json';save(inv,inventory);ledger['unfinished_editorial_scope_v3447'].update(path=str(inv),sha256=sha(inv.read_bytes()),latest_repair='V3448')
    ledger['lil_B138_reference_metadata_repair_v3448']=dict(proof=str(proof),proof_sha256=sha(proof.read_bytes()),new_source_prose_reviews=0,new_completed_records=0,full_goal_complete=False)
    ledger['formatting_watchlist']['lil_B138_v3439'].update(reference_approval=str(NEWAPP),reference_metadata_repair=str(proof));ledger['latest_checkpoint']=summary;save(lp,ledger)
    section='## V3448: B138 reference count label corrected; registered integration pending\n\n'+summary+'\n\nCorrected approval: '+NEWAPP.as_posix()+'. Requirements: '+req.as_posix()+'.\n\n'
    for i,p in enumerate(documents):
        first,rest=p.read_text(encoding='utf-8').split('\n',1);p.write_text(('# Current editorial handoff - V3448' if i==0 else first)+'\n\n'+section+rest,encoding='utf-8',newline='\n')
    save(ROOT/'repair_receipt.json',dict(checkpoint='V3448',evidence={**evidence,str(inv):sha(inv.read_bytes())},updated_files={str(p):sha(p.read_bytes()) for p in [lp,*documents]},prior_verified_handoff=previous['prior_verified_handoff'],intermediate_checkpoint_receipt=str(intermediate),intermediate_checkpoint_receipt_sha256=sha(intermediate.read_bytes()),intermediate_before_directory=str(ROOT),next_requirements=str(req),fresh_reread=4924,fresh_integrated=4880,fresh_pending=44,source_prose=4927,new_source_prose_reviews=0,new_completed_records=0,all_jobs_terminal=True,full_goal_complete=False))
    a=Path('scripts/verify_editorial_handoff_v3447b.py');b=Path('scripts/verify_editorial_handoff_v3448b.py');assert not b.exists();t=a.read_text(encoding='utf-8')
    t=t.replace("ROOT=Path('work/analysis/editorial_handoff_verification_v3447b')","ROOT=Path('work/analysis/editorial_handoff_verification_v3448b')")
    t=t.replace("rp=CHECKPOINT/'checkpoint_receipt.json'","rp=Path('work/analysis/lil_B138_reference_metadata_repair_v3448/repair_receipt.json')")
    t=t.replace("'latest_checkpoint'}","'latest_checkpoint','lil_B138_reference_metadata_repair_v3448'}")
    t=t.replace("{'lil_B138_reference_approval_v3447','unfinished_editorial_scope_v3447'}","{'lil_B138_reference_approval_v3447','unfinished_editorial_scope_v3447','lil_B138_reference_metadata_repair_v3448'}")
    t=t.replace("approval=read('work/analysis/lil_B138_reference_approval_v3446/approval_receipt.json')","approval=read('work/analysis/lil_B138_reference_approval_v3446c/approval_receipt.json')")
    t=t.replace('# Current editorial handoff - V3447','# Current editorial handoff - V3448').replace("checkpoint='V3447'","checkpoint='V3448'").replace('Independent V3447 audit','Independent V3448 audit')
    marker="    changed={'contextual_story_natural_dialogue_pass_v1871'";at=t.index(marker)
    extra="""    intermediate=read(receipt['intermediate_checkpoint_receipt']);assert sha(Path(receipt['intermediate_checkpoint_receipt']).read_bytes())==receipt['intermediate_checkpoint_receipt_sha256']
    for p,digest in intermediate['updated_files'].items():assert sha((Path(receipt['intermediate_before_directory'])/(Path(p).name+'.before')).read_bytes())==digest
    oldmap=read('translations/lil_B138_editorial_relocation_map_v1.json');newmap=read('translations/lil_B138_editorial_relocation_map_v2.json')
    oldkey='all12_relocated_predicate_pairs_preserve_source_operands_results_and_unowned_RAM';assert oldmap.pop(oldkey) is True
    newcopy=deepcopy(newmap)
    for k in ['all10_predicates_and1_query_current_relocated_results_and_source_operands_equal','previous_reference_map','previous_reference_map_sha256','metadata_correction']:newcopy.pop(k)
    assert oldmap==newcopy and oldkey not in newmap
"""
    t=t[:at]+extra+t[at:];compile(t,str(b),'exec');b.write_text(t,encoding='utf-8')
    print('V3448 corrects the inherited reference label through preserved map/document/approval successors. Counts and ROM bytes unchanged;independent audit pending.')
