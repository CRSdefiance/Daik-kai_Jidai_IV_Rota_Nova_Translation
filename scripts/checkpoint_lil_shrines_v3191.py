"""Record 235 complete contextual reviews without premature release credit."""
from collections import Counter
from copy import deepcopy
from pathlib import Path
from shutil import copy2
from dk4tool.patch.grand_race_menu_release import sha
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read, save

ROOT=Path('work/analysis/lil_Shrines_Temples_checkpoint_v3191')
PRIOR=Path('work/analysis/editorial_handoff_verification_v3166/verified_handoff.json')
MANUSCRIPTS=[Path('translations/lil_shrines_temples_editorial_manuscript_v7.json'),
             Path('translations/lil_shrines_temples_actor_style_manuscript_v5.json'),
             Path('translations/lil_shrines_temples_choice_manuscript_v4.json')]
APPROVAL=Path('work/analysis/lil_Shrines_Temples_font_approval_v3190b/approval_receipt.json')
BLOCKS=list(range(101,111))
FAMILY='Lil-Shrines-Temples-235'
SUMMARY=('V3191 records235 fresh whole-exchange reviews across Lil SC2 B101-B110:164speeches(134ordinary/30FE),56unique stored actor-style alternatives across8source4100objects/64slots,and15labels in5source2200three-option menus. Decisions117revisions/118individually justified retentions;all235have exact clean/current references,fresh glosses,complete exchange notes,comparison against effective current English andallfive review gates. Preserve priest ethical counsel/twoMapKeys,Christian prayer/oldcross humor,Sphinx riddle choices andsix-baby arithmetic,the fictional cult threat anddistinct villager-help alternatives,star-adornment uncertainty,community flight from Muslimrule/faith/ancient lamp/hearsay/earnest OttomanEmpire request,bean-doubling59second solution andLil confidence-to-hunch humor,andleft-hand jug riddle solved byturningright. No invented relationships,ranks,denomination,cause or earned reward. Native207actor/eightvoice catalog anddynamicCF/D0 roles arebound without assigning roles;D0historical fallback151 isnot anactual newscene participant claim. Three raw passages are overridden bythe current registered name catalog;retain their effective Camille wording. Eight item pointers andSantiagoCathedral match clean/current native names. All421commands/114relative spans/1140clean-current skipcases,440speech/style dispatches,16whole4100commands,3312catalog-style getters and21predicates pass;zero eventqueries. All220paragraph native planes/1760logical-compiled macro alignmentcases preserve complete first/final/internalglyphs,source controls,FI substitutions,blankpaper,origins,bounds,fourrows andsinglepage. Thirty FEpanels usecalibrated228x48logical/228x64physical paper;two source-leading-LFcases start Englishfirstline safely. All5three-option menus preservecount3,indices0/1/2,cancel,VMnextcommand andgeometry:15decodeobjects/40VMcases/60complete current-reviewed label styleplanes. Modal inputloop bridged. All33final progressive/FE/menu sheets wereviewed orhashmatch viewed predecessors. Three progressive flow findings resolved locally;3newplanes/24newmacro cases,187planes/1496cases bound-reused;30FEplanes/240cases exactly rebound. The138px tightly fitted denial lost leading-Tpixels;faithful26cell That animal doesn\'t exist passes full156px native check. All failures/drafts/producers preserved. Only54row-count notes;31source/consumer and28formatter negatives pass;no weak-ending,orphan,missingglyph,bounds,pagination orcontrolwaiver. Globalhelpers/runtime/ROM/registry unchanged. Coverage4425reread/4190integrated/235pending;source-prose4428including2598SC2. Completion remains4190=2923historically revised+1267retained;routes2826reviewed/2591completed. Pending:relocate164speeches/8alias-preserving4100objects/5three-option menus,114spanfixups/570relocatedcases,421command/inverse restoration,21predicates/wholetypeddispatch,220finalparityplanes/880macro cases,336wholeloaders/twoparents/threeentrycensuses,representative reconciliation andregistered cumulative release afterfullV3144/exactcleanpatch/currentstartup. V3144remains512manifestbatches/114acceptedlayers withwhole clean-input reconstruction and31currentstartupframe matches. No newemulator run,selected newscene,nameplate,earnedprogress,fullroute orhardware claim. RemainingB111-B119 has182objects;B120alreadycompleted. COMMON750-752callers,everywider untouchedstoryline/sharedshop-town/random/help/playerprose,SourceItems/LocalProduct,fivenamedtargetleads,rawclassification includingB141/SC3B109,separategraphics/all18plaques andlater older-record technical re-audit remainopen. Queued0Dvalidationgap staysforlater withoutassertinganolderruntimedefect. Allcompletedfamilies remaincompleted. Preserve everyROM,translation,executedproducer/proof/failure andclean/canonicalinput. V1492remainspromoted. Fullgoalactive;alljobsterminal.')

if __name__=='__main__':
    assert not ROOT.exists()
    lp=Path('translations/editorial_review_current_v1.json');ledger=read(lp);before=deepcopy(ledger)
    assert sha(lp.read_bytes())==read(PRIOR)['ledger_sha256']
    doc,voice,menu=map(read,MANUSCRIPTS);approval=read(APPROVAL)
    rows=doc['records']+voice['records']+menu['records'];ids=[r['id'] for r in rows]
    assert len(rows)==len(set(ids))==235
    assert Counter(r['editorial_decision'] for r in rows)=={'revise':117,'retain-wording':118}
    assert all(all(r['review'].values()) and r['source_meaning'] and r['context'] and r['localization_note'] for r in rows)
    assert all(r.get('fresh_retained_wording_justification') for r in rows if r['editorial_decision']=='retain-wording')
    assert approval['all235_five_review_gates_true']
    assert all(approval['manuscripts'][str(p)]==sha(p.read_bytes()) for p in MANUSCRIPTS)
    source,control,branch=map(read,[doc['source_context'],doc['control_contract'],doc['branch_proof']])
    assert source['total_editorial_objects']==235 and len(source['records'])==164 and len(source['typed_actor_style_records'])==56 and len(source['typed_choice_records'])==15
    assert [b['block'] for b in source['blocks']]==BLOCKS and sum(len(b['all_clean_native_commands']) for b in source['blocks'])==421
    assert len(branch['cases'])==1140 and len(branch['operands_requiring_adjustment_when_resizing'])==114
    assert len(control['speech_and_stored_alternative_dispatch_cases'])==440 and len(control['whole_original4100_command_cases'])==16
    assert len(control['current_original_predicate_cases'])==21 and control['original_event_queries']==[]
    fresh=ledger['contextual_story_natural_dialogue_pass_v1871']
    assert (fresh['fresh_pass_records_explicitly_reread'],fresh['fresh_pass_records_integrated'],fresh['fresh_pass_records_pending_native_actual_release'])==(4190,4190,0)
    selected=[dict(file_path='/data/SC2.DK4',id=n) for n in ids]
    keys={historical_key(r) for r in fresh['record_keys']}
    assert not {historical_key(r) for r in selected}&keys
    assert {historical_key(r) for g in ledger['completed_editorial_families'] for r in g['records']}==keys
    assert ledger['records_with_source_and_prose_pass']==ledger['records_with_source_prose_drafts']==4193
    assert not any(ledger['reviewed_but_incomplete_route_record_IDs'].values())
    docs=[Path('docs')/n for n in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']]
    assert docs[0].read_text(encoding='utf-8').startswith('# Current editorial handoff - V3165')
    ROOT.mkdir(parents=True)
    for p in [lp,*docs]:copy2(p,ROOT/(p.name+'.before'))
    ledger['records_with_source_and_prose_pass']=ledger['records_with_source_prose_drafts']=4428
    ledger['source_prose_reviewed_counts_by_file']['/data/SC2.DK4']=2598
    ledger['reviewed_but_incomplete_route_record_IDs']['/data/SC2.DK4']=ids
    active=ledger['active_source_prose_drafts']
    for p,d in zip(MANUSCRIPTS,[doc,voice,menu],strict=True):
        active['manuscripts'].append(str(p));active['route_record_subsets_pending'][str(p)]=[r['id'] for r in d['records']]
    active.update(status='3-reviewed-COMMON-incomplete;235-Shrines-Temples-native-reviewed-pending-release',
        note='4425fresh rereads:4190integrated and235pending relocation,representative reconciliation andregistered release. Source/prose4428;COMMON750-752andallwider untouchedprose remainopen.')
    fresh['record_keys'].extend(selected);fresh['record_IDs'].extend(ids)
    pending=dict(id=FAMILY,file_path='/data/SC2.DK4',blocks=BLOCKS,records=235,record_keys=selected,
        manuscripts={str(p):sha(p.read_bytes()) for p in MANUSCRIPTS},
        manuscript=str(MANUSCRIPTS[0]),manuscript_sha256=sha(MANUSCRIPTS[0].read_bytes()),
        actor_styles=str(MANUSCRIPTS[1]),actor_styles_sha256=sha(MANUSCRIPTS[1].read_bytes()),
        choices=str(MANUSCRIPTS[2]),choices_sha256=sha(MANUSCRIPTS[2].read_bytes()),
        proposed_revisions=117,retentions=118,source_prose_reviews_added=235,completion_credit_added=0,
        native_font_proof=doc['native_font_proof'],pending='421commands/114spans/570relocatedcases/21predicates/noqueries/8actor-styleobjects/5three-optionmenus;220finalparityplanes/880macrocases;336wholeloaders/twoparents/threeentrycensuses;representative reconciliation;guarded cumulative release afterfullV3144,exactcleanpatch/currentstartup.',new_emulator_runs=0)
    fresh.update(fresh_pass_records_explicitly_reread=4425,fresh_pass_records_integrated=4190,fresh_pass_records_pending_native_actual_release=235,
        pending_record_keys=selected,pending_contextual_families=[pending],latest_pending_contextual_family=FAMILY,
        latest_contextual_manuscript=str(MANUSCRIPTS[0]),latest_contextual_actor_style_draft=str(MANUSCRIPTS[1]),
        latest_contextual_choice_draft=str(MANUSCRIPTS[2]),coverage_note=active['note'])
    for unit in ledger['coverage_units']:
        if unit['id']=='all-route-scenes':unit.update(reviewed_route_records=2826,completed_route_records=2591,next='Integrate235Shrines/Temples objects;continue remaining182B111-B119 andevery untouched route/sharedshop-town/random/help/playerprose family.')
    ledger['coverage_units'].append({**pending,'status':'source-prose-current-native-format-approved;relocation-representative-release-pending','full_goal_complete':False})
    ledger['formatting_watchlist']['lil_Shrines_Temples_v3191']=dict(
        status='220nativepanels/1760macro cases,60menuplanes/40VMreturns pass;relocation/finalpadding/representative/release pending',
        source_context=doc['source_context'],control_contract=doc['control_contract'],branch_proof=doc['branch_proof'],
        native_font_proof=doc['native_font_proof'],approval=str(APPROVAL),narrow_line_count_notes=54,
        all33_final_sheets_viewed_or_identical=True,source_bound_formatter_global_helpers_unchanged=True,
        no_open_final_target_native_font_finding=True,no_orphan_predicate_or_missing_glyph_waivers=True,
        actual_selected_Shrines_Temples_IDs=[],new_emulator_runs=0)
    requirements=ROOT/'next_registered_integration_requirements.json'
    save(requirements,dict(parent_profile='all-routes-unified-v3144',parent_ROM=doc['current_ROM'],parent_ROM_sha256=doc['current_ROM_sha256'],
        manuscripts={str(p):sha(p.read_bytes()) for p in MANUSCRIPTS},source_context=doc['source_context'],
        control_contract=doc['control_contract'],branch_proof=doc['branch_proof'],native_fonts=doc['native_font_proof'],
        native_formatter_module=doc['native_formatter_module'],native_formatter_module_sha256=doc['native_formatter_module_sha256'],
        blocks=BLOCKS,progressive=190,ordinary_speech=134,actor_style_alternatives=56,FE_panels=30,
        choice_labels=15,typed_menu_objects=5,commands=421,relative_sites=114,original_predicates=21,event_queries=0,
        next='Preserve20byte4100headers andall64style aliases/56bodies;virtualD0excludedfromstoredtext. Preserve8byte2200headers,count3,indices012/cancel. Relocate114relative0100/0200/0300/0400spans;570nativecases,421commandinverse-restoration,21predicates/noqueries,typeddispatch,326otherSC2blocks exact. Prove220finalparityplanes/880macrocases,336wholeloaders/twoparents/threeentrycensuses andsource-boundrepresentative rules. Focus actualtests onconcreteunresolvedrisks. Registerguardedstage afterfullV3144;expected515manifestbatches/114acceptedlayers. BuildregisteredROM/exactcleanpatch/freshstartup before235completion.',
        preserve_every_ROM_translation_profile_accepted114_and_V1492_promotion=True,full_goal_complete=False))
    inventory=deepcopy(read(ledger['unfinished_editorial_scope_v3165']['path']))
    inventory.update(incomplete_route_source_prose_groups=[dict(family=FAMILY,file_path='/data/SC2.DK4',blocks=BLOCKS,count=235,record_IDs=ids)],
        incomplete_route_source_prose_count=235,next_focus='Integrate235reviewed B101-B110objects;then continue182B111-B119objects andevery wideruntouched storyline/sharedshop-town/random/help/playerprose. Preserve graphics separation andlater technical re-audit.')
    inventory['lil_B101_B110_fresh_context_review_checkpoint']=dict(checkpoint='V3191',status='235source-prose-native-reviewed;integration-pending',
        manuscripts=[str(p) for p in MANUSCRIPTS],historical_source_only_lead_v3165_now_reviewed=True,
        remaining_B111_B119_unreviewed_objects=182,no_whole_goal_completion_credit=True)
    for unit in inventory['broader_coverage_units']:
        if unit['id']=='all-route-scenes':unit.update(reviewed_route_records=2826,completed_route_records=2591,source_prose_pending_records=235,source_prose_pending_family=FAMILY,next=inventory['next_focus'])
    inv=ROOT/'unfinished_editorial_scope_inventory.json';save(inv,inventory)
    ledger['unfinished_editorial_scope_v3191']=dict(path=str(inv),sha256=sha(inv.read_bytes()),incomplete_COMMON=3,incomplete_route_source_prose=235,remaining_B111_B119=182,full_goal_complete=False)
    evidence={str(p):sha(p.read_bytes()) for p in [*MANUSCRIPTS,APPROVAL,PRIOR,requirements,inv,
        Path(doc['source_context']),Path(doc['control_contract']),Path(doc['branch_proof']),
        Path(doc['whole_exchange_context_notes']),Path(doc['item_terminology_reconciliation']),
        Path(doc['native_font_proof']),Path(doc['native_formatter_module']),Path(doc['scoped_profile_module']),Path(__file__),
        *[Path(s['path']) for s in approval['all33_review_sheets']]]}
    ledger['lil_Shrines_Temples_source_prose_native_v3191']=dict(summary=SUMMARY,**pending,evidence=evidence,goal_turn_classification='progress',full_goal_complete=False)
    ledger['latest_checkpoint']=SUMMARY
    for key in ['completed_editorial_families','records_editorially_completed','records_revised_and_integrated','retained_wordings_editorially_completed',
        'completed_editorial_record_counts_by_file','current_integrated_candidate','reviewed_but_incomplete_COMMON_IDs','unresolved_graphics_work',
        'older_record_reaudit_after_full_editorial_goal','native_source_universe_inventory_v2701c']:
        assert ledger[key]==before[key],key
    assert len(fresh['record_keys'])==len({historical_key(r) for r in fresh['record_keys']})==4425
    assert len(fresh['integrated_record_keys'])==4190 and ledger['goal_status']=='active' and not ledger['full_goal_complete']
    save(lp,ledger)
    section='## V3191:235 shrine and temple reviews; release pending\n\n'+SUMMARY+'\n\nApproval: '+APPROVAL.as_posix()+'. Integration: '+requirements.as_posix()+'. Unfinished scope: '+inv.as_posix()+'.\n\n'
    for i,p in enumerate(docs):
        first,rest=p.read_text(encoding='utf-8').split('\n',1)
        p.write_text(('# Current editorial handoff - V3191' if i==0 else first)+'\n\n'+section+rest,encoding='utf-8',newline='\n')
    candidate=ledger['current_integrated_candidate']
    save(ROOT/'checkpoint_receipt.json',dict(checkpoint='V3191',summary=SUMMARY,evidence=evidence,
        updated_files={str(p):sha(p.read_bytes()) for p in [lp,*docs]},prior_verified_handoff=str(PRIOR),
        new_completed_records=0,new_source_prose_reviews=235,proposed_revisions=117,justified_retentions=118,
        fresh_reread=4425,fresh_integrated=4190,fresh_pending=235,source_prose=4428,completed=4190,
        historical_revised=2923,historical_retained=1267,incomplete_COMMON=3,incomplete_route=235,
        candidate=candidate['path'],candidate_sha256=candidate['sha256'],patch=candidate['patch'],patch_sha256=candidate['patch_sha256'],
        next_requirements=str(requirements),actual_selected_Shrines_Temples_IDs=[],new_emulator_runs=0,
        goal_turn_classification='progress',all_jobs_terminal=True,full_goal_complete=False))
    print('V3191:235newreviews,117revisions/118retentions;4425reread/4190integrated/235pending;source-prose4428. V3144preserved;fullgoalactive.')
