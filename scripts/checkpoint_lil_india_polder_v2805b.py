"""Record34 fresh source/prose/native reviews; preserve pending release gates."""
from pathlib import Path
from copy import deepcopy
from shutil import copy2
from collections import Counter
from dk4tool.patch.grand_race_menu_release import sha
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_India_Polder_checkpoint_v2805b')
DOC=Path('translations/lil_india_polder_editorial_manuscript_v5.json')
SOURCE=Path('work/analysis/lil_India_Polder_source_v2792/complete119_clean_current_native_context.json')
CONTROL=Path('work/analysis/lil_India_Polder_controls_v2794/source_bound119_preambles_and_original_conditional_predicates.json')
BRANCH=Path('work/analysis/lil_India_Polder_branches_v2793/original_relative_skip_operand_proof.json')
FONTS=Path('work/analysis/lil_India_Polder_fonts_v2803/current_macro_QA_and_progressive_font_proof.json')
APPROVAL=Path('work/analysis/lil_India_Polder_font_approval_v2804/approval_receipt.json')
FAMILY='Lil-India-Camille-Polder-Gift-B37-B38-B39-B40-B129-B130-119'
SUMMARY=' '.join([
    'V2805 freshly reviews119 speeches across six complete Lil exchanges inSC2B37/B38/B39/B40/B129/B130:India poverty andcaste,the moral doubts overprofitable trade,Camille maritime authority argument,the Amsterdam polder introduction,Lelystad gold request/delivery andClifford gift pickup. There are84 proposed revisions and35 individually justified retentions,including punctuation-only reactions andall stored crew/dialogue alternatives. Every object has exact clean/current references,a fresh source gloss,context/localization notes andallfive editorial review gates.',
    'Preserve the characters account ofbirth-assigned social standing without inventing caste groups,ranks ora modern historical explanation. Lil personal wish tohelp isnot limited to aninvented merchant role. Restore her responsibility forthe conflicts,her specific doubts,the Maritime Silk Road image,the desire-versus-profit reasoning,the two peace proposals andthe distinction between recognized authority andmilitary conquest. Established Proof ofConquest terminology isrestored. Do notgrant the artifacts aninvented power tojudge worthiness. The source father relationship stays inits conditional alternative;Camille private parenthesized aside andLil actual scary-dad/sibling analogy remain distinct. No new literal kinship,name orrank isinvented;Camille replaces the legacy Kamil spelling.',
    'The polder student describes coastal dikes,enclosure andpumping,the hope ofhelping the poor,personal naming andabout1000000currencygold asaninitial estimate. Preserve previously sought butinsufficient government aid andhis determination. Later three holds ofcommoditygold andLelystad nearAmsterdam aredistinct fromthat monetary estimate. Do notmove the cargo quantity intoanearlier government quotation,credit anunearned donation,claim who namedLelystad orconvert future office/investment/tradingtown plans intocompleted outcomes. Gift/letter-reading andalready-heard-fromClifford alternatives do notgrant duplicate objects;the key isfordeciphering amap,not aninvented map-screen unlock. ResearchStudent171andBarkeep92remain sourceclasses without inventedunique names.',
    'All193nativecommands,119complete0040ffff00preambles,40relative sites/400clean-current cases and238historical dispatcher contexts are mapped. Ten original current predicates preserve actor/event/roster/RNG andunowned4MiB state;onlysource-owned four-byte alignment scratch02279600maychange andrestoringit recoversall4MiB. Current eventgetter queries bind129inB37,48twiceinB38,130inB129and26inB130. This doesnotprove that48isthefull true-name reveal. The preserved2791/2791bprobes stopped because the first inventory omitted the additional130query;2794bindsallfive queries. Event40requires39;129mustnotfollowcompleted37. Historical catalog getters are notnewobserved nameplates. Native171is executable presentation state,notageneral Shift-Jis stripping rule. UIpreparation andnativepanel bodies are explicitunexecuted boundaries inthe dispatcherprobe. No FEpanels ortypedchoice objects areinthis batch.',
    'A local source/runtime-bound profile andformatter preserve allspeaker controls/macros andglobalhelper/runtime bytes. The initial2796plan found a weak the ending;one faithful paragraph refinement removes repeated locality wording andverbose are living while preserving allsource facts/question. Full native2798planes/952macro cases pass butvisual review finds isolated everything/struggled andawkward phrase boundaries. Successor2800/2801reruns16changed planes/128macro cases andbinds103unchanged planes/824cases. Final2802/2803keeps pretty words andgovernor-office compounds together:three newplanes/24cases and116exact reusedplanes/928cases bindall119completeplanes/952macro cases. All15original sheets,ninechanged successor sheets andthreefinalchanged sheets wereviewed;unchanged finals matchviewed sheets byhash.',
    'Complete first/interior/finalglyphs,blankpaper,origin0,16pxrows,bounds andfour-row singlepage limits pass. Fourteen additional formatter rejection tests and119complete English/control/macro invariants pass. Only39 individually justified ordinaryJapanese/English rowcount notes remain;no weak-ending,orphan,predicate,control,overflow,missingglyph orblankpage waiver isgranted. This iscurrent CPU/font evidence,not newselected-scene gameplay. Complete resized references,40relocated relative sites,tenrelocated predicates,finalparity/pagination,wholeblock loaders/entries,representative reconciliation andguarded registeredrelease remain pending.',
    'Fresh coverage is2581 reread /2462 integrated-reconciled /119 pending. Source/prose is2584,including754SC2. Completion stays2462(1724historically revised,738retained). Route coverage is982reviewed/863completed. Three marketCOMMON750-752remain incomplete. Every wider untouched storyline,shared shop/town dialogue,random scene andremaining player-facing prose remains in scope. Userrepresentativepolicy doesnotrequire individualconditional/speaker/nameplate visits absentaconcrete unresolvedrisk. No selectedIndia/polder activation,newemulatorrun,earnedfunding/delivery,full-route orhardware claim ismade.',
    'Registered cumulative experimentalV2783 remains499batches/114accepted layers withits exactly reconstructable clean-input patch. ROM,registry,builder,manifest,patch,fonts,graphics andglobalruntime are unchanged;V1492remainspromoted. AllROMs,earliertranslations,clean/canonicalinputs andexecuted proofs arepreserved. The previousV2787section heading iscorrected toMediterranean/Africa;its originalbackup andallresults remainpreserved. Five named-target2187-2191leads remainuncredited. Raw rejected-object classification,SC3B109,separategraphics/all18plaques andlater older-record technical re-audit remainopen. Fullgoalactive;alljobsterminal.'
])

if __name__=='__main__':
    assert not ROOT.exists();lp=Path('translations/editorial_review_current_v1.json');ledger=read(lp);before=deepcopy(ledger)
    previous=Path('work/analysis/editorial_handoff_verification_v2788/verified_handoff.json');assert sha(lp.read_bytes())==read(previous)['ledger_sha256']
    doc,source,control,branch,font,approval=map(read,[DOC,SOURCE,CONTROL,BRANCH,FONTS,APPROVAL]);rows=doc['records'];ids=[r['id'] for r in rows]
    assert len(rows)==len(set(ids))==119 and Counter(r['editorial_decision'] for r in rows)=={'revise':84,'retain-wording':35}
    assert all(all(r['review'].values()) and r['source_meaning'] and r['localization_note'] for r in rows)
    assert source['total_editorial_objects']==119 and sum(len(b['all_clean_native_commands']) for b in source['blocks'])==193
    assert len(branch['cases'])==400 and len(branch['operands_requiring_adjustment_when_resizing'])==40
    assert len(control['dispatch_cases'])==238 and len(control['current_original_predicate_cases'])==10 and [(q['block'],q['event']) for q in control['original_event_queries']]==[(37,129),(38,48),(38,48),(129,130),(130,26)]
    assert font['manuscript_sha256']==sha(Path(doc['previous_manuscript']).read_bytes()) and len(font['cases'])==119 and font['current_original_macro_alignment_calls']==952
    assert approval['manuscript_sha256']==sha(DOC.read_bytes()) and approval['all15_review_sheets_viewed'] and approval['narrow_line_count_notes']==39
    fresh=ledger['contextual_story_natural_dialogue_pass_v1871'];assert (fresh['fresh_pass_records_explicitly_reread'],fresh['fresh_pass_records_integrated'],fresh['fresh_pass_records_pending_native_actual_release'])==(2462,2462,0)
    selected=[dict(file_path='/data/SC2.DK4',id=n) for n in ids];keys={(r['file_path'],r['id']) for r in fresh['record_keys']}
    assert not {(r['file_path'],r['id']) for r in selected}&keys
    assert {historical_key(r) for g in ledger['completed_editorial_families'] for r in g['records']}==keys
    assert ledger['records_with_source_and_prose_pass']==ledger['records_with_source_prose_drafts']==2465
    docs=[Path('docs')/n for n in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']]
    assert docs[0].read_text(encoding='utf-8').startswith('# Current editorial handoff - V2787')
    ROOT.mkdir(parents=True)
    for p in [lp,*docs]:copy2(p,ROOT/(p.name+'.before'))
    ledger['records_with_source_and_prose_pass']=ledger['records_with_source_prose_drafts']=2584
    ledger['source_prose_reviewed_counts_by_file']['/data/SC2.DK4']=754
    ledger['reviewed_but_incomplete_route_record_IDs']['/data/SC2.DK4']=ids
    active=ledger['active_source_prose_drafts'];active['manuscripts'].append(str(DOC));active['route_record_subsets_pending'][str(DOC)]=ids
    active.update(status='3-reviewed-COMMON-incomplete;119-post-Seville-Egypt-warning-native-reviewed-pending-release',
        note='2581 fresh rereads:2462 integrated/reconciled and34 India/Camille/polder/gift reviews pending reference,representative and registered-release gates. Source/prose2313; marketCOMMON750-752 and all wider untouched prose remain open.')
    fresh['record_keys'].extend(selected);fresh['record_IDs'].extend(ids)
    pending=dict(id=FAMILY,file_path='/data/SC2.DK4',blocks=[37,38,39,40,129,130],records=119,record_keys=selected,manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),
        proposed_revisions=84,retentions=35,source_prose_reviews_added=119,completion_credit_added=0,native_font_proof=str(FONTS),
        pending='Complete relocation/reference census and all32 resized relative sites; final parity/pagination; whole-script loader/entry proofs; representative shared-rule reconciliation; optional registered cumulative stage afterV2783, exact clean patch and required startup.',
        new_emulator_runs=0)
    fresh.update(fresh_pass_records_explicitly_reread=2581,fresh_pass_records_integrated=2462,fresh_pass_records_pending_native_actual_release=119,
        pending_record_keys=selected,pending_contextual_families=[pending],latest_pending_contextual_family=FAMILY,latest_contextual_manuscript=str(DOC),latest_contextual_choice_draft=None,coverage_note=active['note'])
    for unit in ledger['coverage_units']:
        if unit['id']=='all-route-scenes':unit.update(reviewed_route_records=982,completed_route_records=863,next='Finish34 B37/B38/B39/B40/B129/B130 reference/representative/release gates,then continue every untouched storyline/shared/town/random/player prose family.')
    ledger['coverage_units'].append(dict(**pending,status='source-prose-current-native-formatting-approved;references-representative-release-pending',full_goal_complete=False))
    ledger['formatting_watchlist']['lil_India_Polder_v2805']=dict(status='all119-current-native-fonts-and-full-QA-pass;reference-padding-and-release-pending',
        manuscript=str(DOC),source_context=str(SOURCE),control_contract=str(CONTROL),branch_proof=str(BRANCH),native_font_proof=str(FONTS),
        all15_sheets_viewed_or_exact_previously_viewed=True,source_phrase_flow_findings_resolved=True,narrow_line_count_notes=39,
        no_orphan_predicate_or_missing_glyph_waivers=True,reference_map_pending=True,representative_reconciliation_pending=True,actual_selected_India_Polder_IDs=[],new_emulator_runs=0)
    requirements=ROOT/'next_registered_integration_requirements.json'
    save(requirements,dict(parent_profile='all-routes-unified-v2783',parent_ROM=doc['current_ROM'],parent_ROM_sha256=doc['current_ROM_sha256'],
        manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),source_context=str(SOURCE),control_contract=str(CONTROL),branch_proof=str(BRANCH),native_fonts=str(FONTS),
        blocks=[37,38,39,40,129,130],speeches=119,choices=0,FE_panels=0,commands=193,relative_sites=40,
        next='Compile119 paragraphs through the exact source-bound lil_india_polder_layout_v3 encoder/QA andseven-selector profile. Preserve193nativecommands,allcompletepreambles,40relative sites/200target branchcases,ten relocatedoriginalpredicates andallopaque bytes via inverse restoration. Prove336wholeblock loaders/two parentmodes/full shipped-entry census;330otherblocks exact. Verify119final paritytargets/476additionalmacroalignmentcases/complete nativeplanes/no blankpagination. Bind established actual progressive/shared rules andcurrentV2783startup under exactARM9/COMMON/font/owner hashes;no individual conditional/speaker visits absent concreteunresolvedrisk. Add one optionalguarded stage afterfullV2783stack withsource/runtime/profile/formatter/config/map negativeguards;build registeredcumulativeROM,expected500batches/114acceptedlayers,exactcleanpatch andrequired currentstartup beforecompleting119. PreserveallROMs/translations. B38father referencesremainconditional;B37query129,B38query48twice,B129query130andB130query26 areexact. Do notinfer event48is thefulltrue-name reveal.',
        preserve_every_ROM_translation_profile_accepted114_and_V1492_promotion=True,
        no_actual_selected_India_Polder_or_individual_new_nameplate_claim=True,do_not_require_every_conditional_or_speaker_visit=True,
        current_COMMON_parser_unchanged='dk4tool.patch.surrender_advice_contextual_v1.current_entries',current_context='scripts/current_common_native_context_v2677.py',full_goal_complete=False))
    inventory=deepcopy(read(ledger['unfinished_editorial_scope_v2787']['path']))
    inventory.update(incomplete_route_source_prose_groups=[dict(family=FAMILY,file_path='/data/SC2.DK4',blocks=[37,38,39,40,129,130],count=119,record_IDs=ids)],incomplete_route_source_prose_count=119,
        next_focus='Finish34 reviewed B37/B38/B39/B40/B129/B130 reference/representative/release gates;continue all untouched storyline/shared shop/town/random/player prose. Market750-752 callers,raw rejected-object coverage and five uncredited named-target leads remain open.')
    for unit in inventory['broader_coverage_units']:
        if unit['id']=='all-route-scenes':unit.update(reviewed_route_records=982,completed_route_records=863,source_prose_pending_records=119,source_prose_pending_family=FAMILY,next=inventory['next_focus'])
    inv=ROOT/'unfinished_editorial_scope_inventory.json';save(inv,inventory)
    ledger['unfinished_editorial_scope_v2805']=dict(path=str(inv),sha256=sha(inv.read_bytes()),incomplete_COMMON=3,incomplete_route_source_prose=119,full_goal_complete=False)
    proofpaths=[DOC,SOURCE,CONTROL,BRANCH,FONTS,APPROVAL,requirements,inv,previous,Path(__file__),Path(doc['scoped_profile_module']),
        Path('work/analysis/lil_India_Polder_layout_v2797/all119_layout_and_QA.json'),
        Path('work/analysis/lil_India_Polder_controls_v2791b/original_event_query_diagnostic.json'),
        *[Path(s['path']) for s in font['review_sheets']]]
    evidence={str(p):sha(p.read_bytes()) for p in proofpaths}
    ledger['lil_India_Polder_source_prose_native_v2805']=dict(summary=SUMMARY,**pending,evidence=evidence,goal_turn_classification='progress',full_goal_complete=False)
    ledger['latest_checkpoint']=SUMMARY
    for key in ['completed_editorial_families','records_editorially_completed','records_revised_and_integrated','retained_wordings_editorially_completed','completed_editorial_record_counts_by_file',
        'current_integrated_candidate','reviewed_but_incomplete_COMMON_IDs','unresolved_graphics_work','older_record_reaudit_after_full_editorial_goal']:
        assert ledger[key]==before[key],key
    assert len(fresh['record_keys'])==len({(r['file_path'],r['id']) for r in fresh['record_keys']})==2581 and len(fresh['integrated_record_keys'])==2462
    assert ledger['goal_status']=='active' and not ledger['full_goal_complete'];save(lp,ledger)
    section='## V2805:119 post-Seville and Egypt-warning reviews; reference and release pending\n\n'+SUMMARY+'\n\nManuscript: '+DOC.as_posix()+'. Source: '+SOURCE.as_posix()+'. Native proof: '+FONTS.as_posix()+'. Next integration: '+requirements.as_posix()+'. Unfinished scope: '+inv.as_posix()+'.\n\n'
    for i,p in enumerate(docs):
        first,rest=p.read_text(encoding='utf-8').split('\n',1)
        rest=rest.replace('## V2787:152 post-Seville and Egypt-warning entries completed in V2783','## V2787:152 Mediterranean and Africa reviews completed in V2783')
        p.write_text(('# Current editorial handoff - V2805' if i==0 else first)+'\n\n'+section+rest,encoding='utf-8',newline='\n')
    candidate=ledger['current_integrated_candidate']
    save(ROOT/'checkpoint_receipt.json',dict(checkpoint='V2805',summary=SUMMARY,evidence=evidence,updated_files={str(p):sha(p.read_bytes()) for p in [lp,*docs]},
        new_completed_records=0,new_source_prose_reviews=119,proposed_revisions=84,justified_retentions=35,fresh_reread=2581,fresh_integrated=2462,fresh_pending=119,
        source_prose=2584,completed=2462,historical_revised=1724,historical_retained=738,incomplete_COMMON=3,incomplete_route=119,
        candidate=candidate['path'],candidate_sha256=candidate['sha256'],patch=candidate['patch'],patch_sha256=candidate['patch_sha256'],
        next_requirements=str(requirements),actual_selected_India_Polder_IDs=[],new_emulator_runs=0,goal_turn_classification='progress',all_jobs_terminal=True,full_goal_complete=False))
    print('V2805:119new contextual/native reviews;84revisions/35retentions.2581reread/2462integrated/119pending;source-prose2584. V2783unchanged;full goal active.')
