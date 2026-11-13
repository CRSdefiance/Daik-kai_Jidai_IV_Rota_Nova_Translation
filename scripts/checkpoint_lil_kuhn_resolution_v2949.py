"""Record 360 fresh reviews, preserving all integration and wider-goal gates."""
from pathlib import Path
from copy import deepcopy
from shutil import copy2
from collections import Counter
from dk4tool.patch.grand_race_menu_release import sha
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_Kuhn_Resolution_checkpoint_v2949')
DOC=Path('translations/lil_kuhn_resolution_editorial_manuscript_v6.json')
CHOICES=Path('translations/lil_kuhn_resolution_choice_manuscript_v2.json')
APPROVAL=Path('work/analysis/lil_Kuhn_Resolution_font_approval_v2948/approval_receipt.json')
PRIOR=Path('work/analysis/editorial_handoff_verification_v2921/verified_handoff.json')
BLOCKS=[57,58,59,60,61,62,63,64,65,66,121]
FAMILY='Lil-Kuhn-Resolution-New-World-Clifford-Camille-360'
SUMMARY=' '.join([
 'V2949 freshly reviews360 objects across eleven complete Lil SC2 exchanges B57/B58/B59/B60/B61/B62/B63/B64/B65/B66/B121:Li aftermath,Clifford letter andhostage betrayal,Maldonado/Escante outcomes,New World relic experiment,andthree distinct Kuhn/Camille family outcomes includingthe false-flag ambush andrescue.',
 'There are358speeches(342progressive/16FE) andtwo typed choice labels:214revisions and146individually justified retentions. Exact clean/current references,fresh glosses,whole-exchange context,localization notes andallfive review gates accompany every object. Preserve source qualifications,knowledge,reported deaths,hostage alternatives,Crown mission,first-person apologies,five hostile ships,withdrawal/battle alternatives andno guaranteed selected outcome. James Clifford andDiogo Escante actor controls are sourcebound;Jam Jack Ludwyan is actor11. ApprovedHodram,Maria,Camille remain intact without invented ranks orromance.',
 'B64requires121andtemporarily entrusts two objects,includingthe later named locket. B65excludes48andhas one unnamed youthful object withmanyyears explicit onlyhere. B66requires48/excludes121andhas four known/unknown bartender alternatives;the Overijssel maternal surname,Marinus Kuhn birthname andlongstanding Camille nickname are distinct. B121requires54;Camille own feminine-name recollection is translated respectfully without invented bullying,identity explanations orfatherly gender-disapproval motives. Mother/Mom register,private thoughts,source greed/Spice Islands backstory,reconciliation banter andHodram/Maria deadpan joke remain characterful andbranch-specific. Camille thanksMariafor telling ME ofthe attack. Maria map-deciphering key remains anactual object distinct fromher metaphorical hope forAsia.',
 'Sixteen FE panels preserve14distinct conditional map/Proof theft notices,Clifford complete letter salutation/signature,andthe unlabeled offscreen FI call beforeCamille reveal. Registered ARM9 item pointers/runtime pool reconcile16names,includingUllr,Aksum,Rigveda,Ceremonial Knife andSun-Crest Sheath;no catalog,UI,font orgraphics edits. Source walking binds936commands,340relative sites/3400clean-current native cases,358complete preambles/716historical dispatcher cases,84original predicates andnine event queries. No state oroutcome is forced.',
 'All358complete native panels and2864logical/compiled macro-alignment cases pass first/interior/final glyph,blank-paper,origin,bounds,four-row andsingle-page checks. FEuses source-derived mode1paper andnull-actor24310,includingtwo FI cases;variadic5473Centryr1is not a layout mode. Thetyped menu preserves optionorder/pointers/count and0/1/cancelreturns in six VMcases,eight native current/reviewed style planes andthree source/current/reviewed decodes. Its inputloop is bridged,not actual selected-battle gameplay. All46final sheets were viewed ormatch viewed predecessors byhash. Local formatter successors resolve concrete phrase/weak-word boundaries;reviewed wording stays intact. Twenty-eight formatter and11source/consumer negatives pass;only104individual source/English row-count notes remain. No weak-ending,orphan,control,overflow,glyph orblank-page waiver. Every failed producer,draft andproof remains preserved;global helpers unchanged.',
 'Fresh coverage is3331 reread /2971 integrated-reconciled /360 pending;source/prose3334including1504SC2. Completion stays2971:2090historically revised and881retained. Routes1732reviewed/1372completed. Relocated references,final padding,whole loaders/entries,representative reconciliation andregistered cumulative release remain pending. V2916 remains503manifest batches/114accepted layers withits exactly reconstructable clean-input patch and31-frame actual coldboot startup proof. No selected Kuhn-resolution activation,new emulator run,new nameplate,earned progress,full-route orhardware claim.',
 'COMMON750-752callers,every wider untouched storyline/shared shop-town/random/player prose family,uncredited Source Items/Local Product andfive named-target leads,raw rejected-object classification includingB141,SC3B109,separate graphics/all18plaques andlater older-record technical re-audit remain open. BothB66/B121 are now freshly reviewed;no wider objective is retired. Preserve every generated ROM,earlier translation,clean/canonical input andexecuted proof. V1492 remains promoted. Full goal active;all jobs terminal.'
])

if __name__=='__main__':
    assert not ROOT.exists();lp=Path('translations/editorial_review_current_v1.json');ledger=read(lp);before=deepcopy(ledger)
    assert sha(lp.read_bytes())==read(PRIOR)['ledger_sha256']
    doc,choice,approval=map(read,[DOC,CHOICES,APPROVAL]);rows=doc['records']+choice['records'];ids=[r['id'] for r in rows]
    source,control,branch=map(read,[doc['source_context'],doc['control_contract'],doc['branch_proof']])
    assert len(rows)==len(set(ids))==360 and Counter(r['editorial_decision'] for r in rows)=={'revise':214,'retain-wording':146}
    assert all(all(r['review'].values()) and r['source_meaning'] and r['context'] and r['localization_note'] for r in rows)
    assert source['total_editorial_objects']==360 and source['progressive_speeches']==342 and source['system_FE_panels']==16 and source['typed_choice_labels']==2
    assert sum(len(b['all_clean_native_commands']) for b in source['blocks'])==936 and [b['block'] for b in source['blocks']]==BLOCKS
    assert len(branch['cases'])==3400 and len(branch['operands_requiring_adjustment_when_resizing'])==340
    assert len(control['dispatch_cases'])==716 and len(control['current_original_predicate_cases'])==84 and len(control['original_event_queries'])==9
    assert approval['manuscript_sha256']==sha(DOC.read_bytes()) and approval['choices_sha256']==sha(CHOICES.read_bytes()) and approval['all360_five_review_gates_true']
    fresh=ledger['contextual_story_natural_dialogue_pass_v1871']
    assert (fresh['fresh_pass_records_explicitly_reread'],fresh['fresh_pass_records_integrated'],fresh['fresh_pass_records_pending_native_actual_release'])==(2971,2971,0)
    selected=[dict(file_path='/data/SC2.DK4',id=n) for n in ids];keys={historical_key(r) for r in fresh['record_keys']}
    assert not {historical_key(r) for r in selected}&keys and {historical_key(r) for g in ledger['completed_editorial_families'] for r in g['records']}==keys
    assert ledger['records_with_source_and_prose_pass']==ledger['records_with_source_prose_drafts']==2974
    assert not any(ledger['reviewed_but_incomplete_route_record_IDs'].values())
    docs=[Path('docs')/n for n in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']]
    assert docs[0].read_text(encoding='utf8').startswith('# Current editorial handoff - V2920')
    ROOT.mkdir(parents=True)
    for p in [lp,*docs]:copy2(p,ROOT/(p.name+'.before'))
    ledger['records_with_source_and_prose_pass']=ledger['records_with_source_prose_drafts']=3334
    ledger['source_prose_reviewed_counts_by_file']['/data/SC2.DK4']=1504
    ledger['reviewed_but_incomplete_route_record_IDs']['/data/SC2.DK4']=ids
    active=ledger['active_source_prose_drafts']
    for p,rs in [(DOC,doc['records']),(CHOICES,choice['records'])]:
        active['manuscripts'].append(str(p));active['route_record_subsets_pending'][str(p)]=[r['id'] for r in rs]
    active.update(status='3-reviewed-COMMON-incomplete;360-Kuhn-resolution-native-reviewed-pending-release',note='3331 fresh rereads:2971 integrated/reconciled and360 pending reference,representative andregistered-release gates. Source/prose3334;COMMON750-752andall wider untouched prose remain open.')
    fresh['record_keys'].extend(selected);fresh['record_IDs'].extend(ids)
    pending=dict(id=FAMILY,file_path='/data/SC2.DK4',blocks=BLOCKS,records=360,record_keys=selected,manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),choices=str(CHOICES),choices_sha256=sha(CHOICES.read_bytes()),proposed_revisions=214,retentions=146,source_prose_reviews_added=360,completion_credit_added=0,native_font_proof=doc['native_font_proof'],pending='936commands/340relative sites/1700relocated cases/84predicates/ninequeries/one menu;358final parity planes/1432macro cases;336wholeloaders/twoparents/entrycensus;representative reconciliation;guarded cumulative release afterfullV2916,exactclean patch/currentstartup.',new_emulator_runs=0)
    fresh.update(fresh_pass_records_explicitly_reread=3331,fresh_pass_records_integrated=2971,fresh_pass_records_pending_native_actual_release=360,pending_record_keys=selected,pending_contextual_families=[pending],latest_pending_contextual_family=FAMILY,latest_contextual_manuscript=str(DOC),latest_contextual_choice_draft=str(CHOICES),coverage_note=active['note'])
    for unit in ledger['coverage_units']:
        if unit['id']=='all-route-scenes':unit.update(reviewed_route_records=1732,completed_route_records=1372,next='Integrate360 reviewed Kuhn-resolution objects;continue every untouched storyline/shared shop-town/random/player prose family.')
    ledger['coverage_units'].append(dict(**pending,status='source-prose-current-native-format-approved;reference-representative-release-pending',full_goal_complete=False))
    ledger['formatting_watchlist']['lil_Kuhn_Resolution_v2949']=dict(status='358native panels/2864macro cases,8menu planes/6VMreturns pass;reference/final-padding/release pending',source_context=doc['source_context'],control_contract=doc['control_contract'],branch_proof=doc['branch_proof'],native_font_proof=doc['native_font_proof'],approval=str(APPROVAL),narrow_line_count_notes=104,all46_final_sheets_viewed_or_identical=True,source_bound_formatter_global_helpers_unchanged=True,no_open_final_target_native_font_finding=True,no_orphan_predicate_or_missing_glyph_waivers=True,actual_selected_Kuhn_Resolution_IDs=[],new_emulator_runs=0)
    requirements=ROOT/'next_registered_integration_requirements.json'
    save(requirements,dict(parent_profile='all-routes-unified-v2916',parent_ROM=doc['current_ROM'],parent_ROM_sha256=doc['current_ROM_sha256'],manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),choices=str(CHOICES),choices_sha256=sha(CHOICES.read_bytes()),source_context=doc['source_context'],control_contract=doc['control_contract'],branch_proof=doc['branch_proof'],native_fonts=doc['native_font_proof'],native_formatter_module=doc['native_formatter_module'],native_formatter_module_sha256=doc['native_formatter_module_sha256'],blocks=BLOCKS,progressive=342,FE_panels=16,choice_labels=2,typed_menu_objects=1,commands=936,relative_sites=340,original_predicates=84,event_queries=9,
        next='Compile through source-bound localv3encoder/QA. Preserve936commands/340spans/1700relocated cases/84predicates/ninequeries withmappedcursor/source-owned alignment scratch,one2100menu andallopaque bytes via inverse restoration. Prove336wholeblock loaders/twoparents/fullshippedentrycensus;325otherblocks exact. Check358final parityplanes/1432macroalignments/pagination,including16nullFE/twoFI. Reconcile sharedprogressive/FE/menuactualrules byexactruntime/font/owner hashes;noindividualconditional/speaker visit withoutconcrete risk. Registeroneoptional guardedstage afterfullV2916;expected505batches/114accepted layers. BuildcumulativeROM/exactcleanpatch/currentstartup beforecompletion360.',preserve_every_ROM_translation_profile_accepted114_and_V1492_promotion=True,current_COMMON_parser='dk4tool.patch.surrender_advice_contextual_v1.current_entries',current_context='scripts/current_common_native_context_v2677.py',full_goal_complete=False))
    inventory=deepcopy(read(ledger['unfinished_editorial_scope_v2920']['path']))
    inventory.update(incomplete_route_source_prose_groups=[dict(family=FAMILY,file_path='/data/SC2.DK4',blocks=BLOCKS,count=360,record_IDs=ids)],incomplete_route_source_prose_count=360,next_focus='Integrate360 Kuhn-resolution reviews;then continue all untouched storyline/shared shop/town/random/player prose. BothB66/B121 now freshly reviewed;COMMON750-752callers,raw rejected-object classification,SourceItems/LocalProduct,five named-target leads,SC3B109,separate graphics andlater older-record re-audit remain open.')
    inventory['lil_B66_B121_fresh_context_review_checkpoint']=dict(checkpoint='V2949',status='source-prose-native-reviewed;integration-pending',manuscript=str(DOC),no_whole_goal_completion_credit=True)
    for unit in inventory['broader_coverage_units']:
        if unit['id']=='all-route-scenes':unit.update(reviewed_route_records=1732,completed_route_records=1372,source_prose_pending_records=360,source_prose_pending_family=FAMILY,next=inventory['next_focus'])
    inv=ROOT/'unfinished_editorial_scope_inventory.json';save(inv,inventory)
    ledger['unfinished_editorial_scope_v2949']=dict(path=str(inv),sha256=sha(inv.read_bytes()),incomplete_COMMON=3,incomplete_route_source_prose=360,full_goal_complete=False)
    evidence={str(p):sha(p.read_bytes()) for p in [DOC,CHOICES,APPROVAL,PRIOR,requirements,inv,Path(doc['source_context']),Path(doc['control_contract']),Path(doc['branch_proof']),Path(doc['whole_exchange_context_notes']),Path(doc['item_terminology_reconciliation']),Path(doc['native_font_proof']),Path(doc['native_formatter_module']),Path(doc['scoped_profile_module']),Path(__file__),*[Path(s['path']) for s in approval['all46_review_sheets']]]}
    ledger['lil_Kuhn_Resolution_source_prose_native_v2949']=dict(summary=SUMMARY,**pending,evidence=evidence,goal_turn_classification='progress',full_goal_complete=False);ledger['latest_checkpoint']=SUMMARY
    for key in ['completed_editorial_families','records_editorially_completed','records_revised_and_integrated','retained_wordings_editorially_completed','completed_editorial_record_counts_by_file','current_integrated_candidate','reviewed_but_incomplete_COMMON_IDs','unresolved_graphics_work','older_record_reaudit_after_full_editorial_goal','native_source_universe_inventory_v2701c']:
        assert ledger[key]==before[key],key
    assert len(fresh['record_keys'])==len({historical_key(r) for r in fresh['record_keys']})==3331 and len(fresh['integrated_record_keys'])==2971
    assert ledger['goal_status']=='active' and not ledger['full_goal_complete'];save(lp,ledger)
    section='## V2949:360 Kuhn-resolution reviews; release pending\n\n'+SUMMARY+'\n\nManuscript: '+DOC.as_posix()+'. Choices: '+CHOICES.as_posix()+'. Approval: '+APPROVAL.as_posix()+'. Next integration: '+requirements.as_posix()+'. Unfinished scope: '+inv.as_posix()+'.\n\n'
    for i,p in enumerate(docs):
        first,rest=p.read_text(encoding='utf8').split('\n',1);p.write_text(('# Current editorial handoff - V2949' if i==0 else first)+'\n\n'+section+rest,encoding='utf8',newline='\n')
    candidate=ledger['current_integrated_candidate']
    save(ROOT/'checkpoint_receipt.json',dict(checkpoint='V2949',summary=SUMMARY,evidence=evidence,updated_files={str(p):sha(p.read_bytes()) for p in [lp,*docs]},new_completed_records=0,new_source_prose_reviews=360,proposed_revisions=214,justified_retentions=146,fresh_reread=3331,fresh_integrated=2971,fresh_pending=360,source_prose=3334,completed=2971,historical_revised=2090,historical_retained=881,incomplete_COMMON=3,incomplete_route=360,candidate=candidate['path'],candidate_sha256=candidate['sha256'],patch=candidate['patch'],patch_sha256=candidate['patch_sha256'],next_requirements=str(requirements),actual_selected_Kuhn_Resolution_IDs=[],new_emulator_runs=0,goal_turn_classification='progress',all_jobs_terminal=True,full_goal_complete=False))
    print('V2949:360 new reviews,214revisions/146retentions.3331reread/2971integrated/360pending;source-prose3334. V2916 preserved;full goal active.')
