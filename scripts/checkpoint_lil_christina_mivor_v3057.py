"""Record 145 fresh reviews, preserving all integration and wider-goal gates."""
from pathlib import Path
from copy import deepcopy
from shutil import copy2
from collections import Counter
from dk4tool.patch.grand_race_menu_release import sha
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_Christina_Mivor_checkpoint_v3057')
DOC=Path('translations/lil_christina_mivor_editorial_manuscript_v7.json')
APPROVAL=Path('work/analysis/lil_Christina_Mivor_font_approval_v3056/approval_receipt.json')
PRIOR=Path('work/analysis/editorial_handoff_verification_v3034/verified_handoff.json')
BLOCKS=[72,73]
FAMILY='Lil-Christina-Mivor-145'
SUMMARY='V3057 freshly reviews145 speeches in complete LilSC2B72/B73 Christina recruitment andMivor harbor rescue,with130revisions/15individually justified retentions. All have exact clean/current references,fresh glosses,whole-exchange context,localization notes andallfive gates. Julio is explicitly Christina grandfather inthis source;her unwanted parental engagement andcontinued refusal remain firm. Mivor misplaced confidence andtheatrical formality do not establish mutual consent. The rescue doesnot buy romance. Restore the first fear-greater-than-love comparison beforethe later love-wins reversal;keep repeated fear/name cries,unexpected swimming andhis own disbelief without inventing permanent skill orfear cure. Preserve actual swordchallenge/pain andfather-bought rapier without inventedfatal injury orsnappedblade. Mother167 andBoy162 remain source classes;familiar elder-sister/brother addresses establish norescue kinship. Allthree FEpanels retain explicit source Boy labels. Registered current nativecatalog confirms Mivor Genz;provisional Gentz source-packet annotation is corrected inmanuscript metadata,whileexecuted source proof andJapanese bytes remain preserved. Original fullname getter uses32slots of128bytes;failed3039 readonly assumption and3039b write diagnostic remain. Successor3039c bounds only original counter/output writes andrestores them to recover all4MiB;no runtime defect orolder technical audit isclaimed. Event72dependency123/event73dependency158 are historicalsourceeligibility,not earnedcurrent progress. All236commands/145preambles/12relative sites/120clean-current cases/290historicaldispatch cases/threecurrentpredicates pass;noeventqueries orchoices. Complete142ordinary216x64planes plus3labeledFE228x48logical/228x64physicalplanes and1160logical-compiled macro cases preserve allglyphs,blankpaper,origins,bounds,fourrows andsinglepage. Ninechanged ordinaryplanes/72macro cases were reexecuted;133unchanged/1064cases reuse exactEnglish/source/current/runtime/encodedbytes/previewhashes. FEreuse binds exactEnglish/source/controls/encodedbytes across formatterrefinements. All18finalordinary sheets andoneFE sheet viewed. Twenty-eightformatter and13source-consumer negatives pass. Only51row-count notes;no orphan,weakending,control,glyph,bounds orpagination waiver. Allfailedplans,drafts,producers,proofs andROMs preserved. Fresh coverage3791reread/3646integrated/145pending;source-prose3794including1964SC2. Completion remains3646,2512historically revised/1134retained. Routes2192reviewed/2047completed. Relocation/finalpadding/loaders/references/representative/registeredrelease remainpending. V3029 remains507manifestbatches/114acceptedlayers with exactcleanpatch/current31-frame startup proof. OfflineCPU/font work isdistinct fromactualscene gameplay. Allwider untouchedstorylines/sharedshop-town/random/help/playerprose,COMMON750-752callers,SourceItems/LocalProduct,five namedtargetleads,raw rejected-object classification includingB141,SC3B109,separategraphics/all18plaques andlaterolder-record technicalreaudit remainopen. Queued0Dvalidation-gap lead staysforlaterwithoutassertinganolderruntimedefect. BothB66/B121 andB70/B71 staycompleted. V1492remainspromoted;canonical/cleaninputs preserved. Fullgoalactive;alljobsterminal.'

if __name__=='__main__':
    assert not ROOT.exists();lp=Path('translations/editorial_review_current_v1.json');ledger=read(lp);before=deepcopy(ledger)
    assert sha(lp.read_bytes())==read(PRIOR)['ledger_sha256']
    doc,approval=map(read,[DOC,APPROVAL]);rows=doc['records'];ids=[r['id'] for r in rows]
    source,control,branch=map(read,[doc['source_context'],doc['control_contract'],doc['branch_proof']])
    assert len(rows)==len(set(ids))==145 and Counter(r['editorial_decision'] for r in rows)=={'revise':130,'retain-wording':15}
    assert all(all(r['review'].values()) and r['source_meaning'] and r['context'] and r['localization_note'] for r in rows)
    assert source['total_editorial_objects']==145 and source['progressive_speeches']==142 and source['system_FE_panels']==3 and source['typed_choice_labels']==0
    assert sum(len(b['all_clean_native_commands']) for b in source['blocks'])==236 and [b['block'] for b in source['blocks']]==BLOCKS
    assert len(branch['cases'])==120 and len(branch['operands_requiring_adjustment_when_resizing'])==12
    assert len(control['dispatch_cases'])==290 and len(control['current_original_predicate_cases'])==3 and len(control['original_event_queries'])==0
    assert approval['manuscript_sha256']==sha(DOC.read_bytes()) and approval['all145_five_review_gates_true']
    fresh=ledger['contextual_story_natural_dialogue_pass_v1871']
    assert (fresh['fresh_pass_records_explicitly_reread'],fresh['fresh_pass_records_integrated'],fresh['fresh_pass_records_pending_native_actual_release'])==(3646,3646,0)
    selected=[dict(file_path='/data/SC2.DK4',id=n) for n in ids];keys={historical_key(r) for r in fresh['record_keys']}
    assert not {historical_key(r) for r in selected}&keys and {historical_key(r) for g in ledger['completed_editorial_families'] for r in g['records']}==keys
    assert ledger['records_with_source_and_prose_pass']==ledger['records_with_source_prose_drafts']==3649
    assert not any(ledger['reviewed_but_incomplete_route_record_IDs'].values())
    docs=[Path('docs')/n for n in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']]
    assert docs[0].read_text(encoding='utf8').startswith('# Current editorial handoff - V3033')
    ROOT.mkdir(parents=True)
    for p in [lp,*docs]:copy2(p,ROOT/(p.name+'.before'))
    ledger['records_with_source_and_prose_pass']=ledger['records_with_source_prose_drafts']=3794
    ledger['source_prose_reviewed_counts_by_file']['/data/SC2.DK4']=1964
    ledger['reviewed_but_incomplete_route_record_IDs']['/data/SC2.DK4']=ids
    active=ledger['active_source_prose_drafts']
    for p,rs in [(DOC,doc['records'])]:
        active['manuscripts'].append(str(p));active['route_record_subsets_pending'][str(p)]=[r['id'] for r in rs]
    active.update(status='3-reviewed-COMMON-incomplete;145-Christina-Mivor-native-reviewed-pending-release',note='3791 fresh rereads:3646 integrated/reconciled and145 pending reference,representative andregistered-release gates. Source/prose3794;COMMON750-752 andevery wider untouched family remain open.')
    fresh['record_keys'].extend(selected);fresh['record_IDs'].extend(ids)
    pending=dict(id=FAMILY,file_path='/data/SC2.DK4',blocks=BLOCKS,records=145,record_keys=selected,manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),proposed_revisions=130,retentions=15,source_prose_reviews_added=145,completion_credit_added=0,native_font_proof=doc['native_font_proof'],pending='236commands/12relative sites/60relocated cases/3predicates/noqueries/nochoices;145finalparityplanes/580macrocases;336wholeloaders/twoparents/entrycensus;representative reconciliation;guarded cumulative release afterfullV3029,exactcleanpatch/currentstartup',new_emulator_runs=0)
    fresh.update(fresh_pass_records_explicitly_reread=3791,fresh_pass_records_integrated=3646,fresh_pass_records_pending_native_actual_release=145,pending_record_keys=selected,pending_contextual_families=[pending],latest_pending_contextual_family=FAMILY,latest_contextual_manuscript=str(DOC),latest_contextual_choice_draft=None,coverage_note=active['note'])
    for unit in ledger['coverage_units']:
        if unit['id']=='all-route-scenes':unit.update(reviewed_route_records=2192,completed_route_records=2047,next='Integrate145 reviewed Christina/Mivor speeches; continue every untouched storyline/shared shop-town/random/player prose family.')
    ledger['coverage_units'].append(dict(**pending,status='source-prose-current-native-format-approved;reference-representative-release-pending',full_goal_complete=False))
    ledger['formatting_watchlist']['lil_Christina_Mivor_v3057']=dict(status='145native panels/1160macro cases,no choices;reference/final-padding/release pending',source_context=doc['source_context'],control_contract=doc['control_contract'],branch_proof=doc['branch_proof'],native_font_proof=doc['native_font_proof'],approval=str(APPROVAL),narrow_line_count_notes=51,all19_final_sheets_viewed_or_identical=True,source_bound_formatter_global_helpers_unchanged=True,no_open_final_target_native_font_finding=True,no_orphan_predicate_or_missing_glyph_waivers=True,actual_selected_Christina_Mivor_IDs=[],new_emulator_runs=0)
    requirements=ROOT/'next_registered_integration_requirements.json'
    save(requirements,dict(parent_profile='all-routes-unified-v3029',parent_ROM=doc['current_ROM'],parent_ROM_sha256=doc['current_ROM_sha256'],manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),source_context=doc['source_context'],control_contract=doc['control_contract'],branch_proof=doc['branch_proof'],native_fonts=doc['native_font_proof'],native_formatter_module=doc['native_formatter_module'],native_formatter_module_sha256=doc['native_formatter_module_sha256'],blocks=BLOCKS,progressive=142,FE_panels=3,choice_labels=0,typed_menu_objects=0,commands=236,relative_sites=12,original_predicates=3,event_queries=0,
        next='Compile145 with exact source-bound localv3/profile. Preserve236commands/12relative sites/60relocated cases/3predicates/noqueries/nochoices andinverse restore allopaque bytes. Prove336wholeloaders/twoparents/fullentrycensus;334otherblocks exact. Check145finalparityplanes/580macrocases including3 labeledBoyFEpanels. Reconcile shared actualprogressive/FE rules byexact ownedruntime/font/EV2/B74 bytes;individual visits onlyfor concrete risks. Register one guardedoptionalstage afterfullV3029;expected508manifest batches/114acceptedlayers. Build cumulativeROM/exactcleanpatch/freshcurrentstartup before145completion.',preserve_every_ROM_translation_profile_accepted114_and_V1492_promotion=True,current_COMMON_parser='dk4tool.patch.surrender_advice_contextual_v1.current_entries',current_context='scripts/current_common_native_context_v2677.py',full_goal_complete=False))
    inventory=deepcopy(read(ledger['unfinished_editorial_scope_v3033']['path']))
    inventory.update(incomplete_route_source_prose_groups=[dict(family=FAMILY,file_path='/data/SC2.DK4',blocks=BLOCKS,count=145,record_IDs=ids)],incomplete_route_source_prose_count=145,next_focus='Integrate145 Christina/Mivor reviews; continue all untouched storylines/shared shop-town/random/help/player prose. BothB66/B121 remain completed. All inherited unfinished scope and later technical re-audit remain open.')
    gap=Path('work/analysis/lil_Clifford_North_New_World_layout_v2981/source_0D_consumer_validation_gap_and_local_resolution.json')
    inventory['queued_later_source_0D_consumer_reaudit_lead']=dict(path=str(gap),sha256=sha(gap.read_bytes()),status='queued-for-later-older-record-technical-reaudit;no-prior-runtime-defect-or-new-review-credit-asserted')
    for unit in inventory['broader_coverage_units']:
        if unit['id']=='all-route-scenes':unit.update(reviewed_route_records=2192,completed_route_records=2047,source_prose_pending_records=145,source_prose_pending_family=FAMILY,next=inventory['next_focus'])
    inv=ROOT/'unfinished_editorial_scope_inventory.json';save(inv,inventory)
    ledger['unfinished_editorial_scope_v3057']=dict(path=str(inv),sha256=sha(inv.read_bytes()),incomplete_COMMON=3,incomplete_route_source_prose=145,full_goal_complete=False)
    evidence={str(p):sha(p.read_bytes()) for p in [DOC,APPROVAL,PRIOR,requirements,inv,gap,Path(doc['source_context']),Path(doc['control_contract']),Path(doc['branch_proof']),Path(doc['whole_exchange_context_notes']),Path(doc['name_identity_contract']),Path(doc['native_font_proof']),Path(doc['native_formatter_module']),Path(doc['scoped_profile_module']),Path(__file__),*[Path(s['path']) for s in approval['all19_review_sheets']]]}
    ledger['lil_Christina_Mivor_source_prose_native_v3057']=dict(summary=SUMMARY,**pending,evidence=evidence,goal_turn_classification='progress',full_goal_complete=False);ledger['latest_checkpoint']=SUMMARY
    for key in ['completed_editorial_families','records_editorially_completed','records_revised_and_integrated','retained_wordings_editorially_completed','completed_editorial_record_counts_by_file','current_integrated_candidate','reviewed_but_incomplete_COMMON_IDs','unresolved_graphics_work','older_record_reaudit_after_full_editorial_goal','native_source_universe_inventory_v2701c']:
        assert ledger[key]==before[key],key
    assert len(fresh['record_keys'])==len({historical_key(r) for r in fresh['record_keys']})==3791 and len(fresh['integrated_record_keys'])==3646
    assert ledger['goal_status']=='active' and not ledger['full_goal_complete'];save(lp,ledger)
    section='## V3057:145 Christina/Mivor reviews; release pending\n\n'+SUMMARY+'\n\nManuscript: '+DOC.as_posix()+'. Approval: '+APPROVAL.as_posix()+'. Next integration: '+requirements.as_posix()+'. Unfinished scope: '+inv.as_posix()+'.\n\n'
    for i,p in enumerate(docs):
        first,rest=p.read_text(encoding='utf8').split('\n',1);p.write_text(('# Current editorial handoff - V3057' if i==0 else first)+'\n\n'+section+rest,encoding='utf8',newline='\n')
    candidate=ledger['current_integrated_candidate']
    save(ROOT/'checkpoint_receipt.json',dict(checkpoint='V3057',summary=SUMMARY,evidence=evidence,updated_files={str(p):sha(p.read_bytes()) for p in [lp,*docs]},new_completed_records=0,new_source_prose_reviews=145,proposed_revisions=130,justified_retentions=15,fresh_reread=3791,fresh_integrated=3646,fresh_pending=145,source_prose=3794,completed=3646,historical_revised=2512,historical_retained=1134,incomplete_COMMON=3,incomplete_route=145,candidate=candidate['path'],candidate_sha256=candidate['sha256'],patch=candidate['patch'],patch_sha256=candidate['patch_sha256'],next_requirements=str(requirements),actual_selected_Christina_Mivor_IDs=[],new_emulator_runs=0,goal_turn_classification='progress',all_jobs_terminal=True,full_goal_complete=False))
    print('V3057:145newreviews,130revisions/15retentions;3791reread/3646integrated/145pending;source-prose3794. V3029preserved;fullgoalactive.')
