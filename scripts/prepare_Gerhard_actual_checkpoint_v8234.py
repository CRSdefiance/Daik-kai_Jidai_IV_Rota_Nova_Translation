"""Reversible zero-credit checkpoint for five approved surname formats and fully scoped actual evidence."""
import ast
from pathlib import Path
from scripts import checkpoint_Gerhard_reference_v8220 as previous
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/Gerhard_actual_checkpoint_tools_v8234')
PROOFS={**previous.PROOFS,
 'manuscript':'translations/gerhard_surname_consistency_manuscript_v2.json',
 'prior_manuscript':'translations/gerhard_surname_consistency_manuscript_v1.json',
 'native_loaders':'work/analysis/Gerhard_loaders_v8222/336_whole_native_loads_cache_hits672_initial_parent_modes.json',
 'caller_census':'work/analysis/Gerhard_reference_census_v8223/all225_commands44_relative_sites_five_revisions_EV2_entries_shipped_callers.json',
 'whole_fixtures':'work/analysis/Gerhard_scene_fixtures_v8224/four_complete_parent_revised_SC2_scripts_original_Lil_prelude_fixtures.json',
 'actual_models':'work/analysis/Gerhard_actual_models_v8226/five_previous_body_planes_revised_exact_reuses_three_header_consumers.json',
 'intro_fixtures':'work/analysis/Gerhard_intro_display_fixtures_v8227/two_focused_parent_revised_eight_speech_intro_display_fixtures.json',
 'actual':'work/analysis/Gerhard_actual_v8229/six_paired_runs_actual_five_surname_bodies_headers_conditions_andnormal_returns.json',
 'actual_comparison':'work/analysis/Gerhard_actual_comparison_v8230b/three_actual_pairs_scene_timing_RNG_final_components_later_RGB_scope.json',
 'actual_focus':'work/analysis/Gerhard_intro_actual_focus_v8232/exact_intro_replay8_RAM_phases_bounded_later_state_andRNG_differences.json',
 'actual_approval':'work/analysis/Gerhard_actual_approval_v8233/scoped_actual_format_approval.json',
}
SUMMARY=(
 'Registered cumulative V8172 and main V4701 are unchanged. Counts remain 7171 completed,7174 source/prose and drafts,4455 integrated revisions and2716 retentions;SC0 368,SC1 91,SC2 4915,SC3 197,COMMON1600 complete/1603 source-prose,route subset5571. '
 'V8172 retains639 manifest batches/114 accepted layers/18 release checks/110 regressions,full-reference equality,exact clean-input patch andown-startup evidence. The full editorial goal remains active. No separate unified test package,promotion,pruning,commit orpush.\n\n'
 'Gerhard Adernkatz source/context decision andfull295-speech clean exchanges,14 existing consistent consumers andsix inconsistent consumers are verified from8196-8203. Onlyone currently owned12-byte ARM9 surname andfive previously completed SC2 speeches are planned tochange. '
 'The original20-byte Japanese allocation nowcontains a separately referenced8-byte Blades string after the name. Preserve Blades,allpointer fields,andallbytes outside thecurrent12-byte name span;full inverse andliteral-pointer census pass,without arbitrary dynamic-alias claims. '
 'All other prose is individually retained with source/context reasons. No officialLatin canon,historicalidentity,newrank orbiography isclaimed. ApprovedHodram/Joakim/Camille remain. '
 'The pinned research reference8215 changesonlythat12-byte name span andfive SC2 bodies;all20 Latin consumers becomeAdernkatz,334 otherSC2 blocks/125 otherparagraphs/everyotherfile/component areexact,andfullparentROM inverse passes. It isnot a registered handoff ornewparent.\n\n'
 'Reuse logical8204/privateLil216px-fourrow plan8205/native5pages20alignments8206/view8207/sparse8208b/stored8209/owned targetname8210c/view8211/finalcontrols8214/reference8215/ownresearchstartup8217-8219. '
 'Lil defaults remain3/5/9,sourceFI1/noFAFO,selectors01/09/10,fullpreambles,bodyNUL/phase/guard rules andfonts unchanged. One line-break-count info andzero warnings remain;no waiver ormanualwrap/shortening. '
 'Sparse B27/B74 reconstruction preserves225 commands,130 complete preambles,44 relative sites,all opaque effects,the prior reviewed typedchoice,andcomplete four-byte ends/separate storage tails. '
 'Native relative cases220clean+220current+220target pass;storedoneparitytail uses4fresh alignments andfour unchanged bodies reuse16,allfive viewedinkplanes exact. Final5dispatches/51nonrelative controls/30rawevaluations/150seeded value-carry ends pass. '
 'Research own4001-frame startup has6wholeRGBpairs/wholeactors/captain2 and8fresh namegetters,exact targetARM9/12-byte inverse/Blades/COMMON/directory/123264pool guards. Do not reuse this captain2 context forHodramcaptain1.\n\n'
 'Fresh8222 whole SC2 native proof passes336 loads/cachehits and672 original entry modes. Two fresh decoded caller censuses8223 bind225commands/44relatives/twoEV2 index-based entries,withonlyoriginal24070 interpretercall andno literalalias. '
 'Onlydecoded-unit difference is theowned surname data;full ARM9 inverse proves everyotherbyte exact. Allsource-relative/opaque/menu/end maps remainbound toresearchimage. Preserve8222 failedpreparer and8222b/c exact-key correction.\n\n'
 'Paired actual tests8225 keepfull original B27/B74 scripts behind the original9-command/48-byte Lil prelude,with identical ordinary inputs andreadonly observers. All4whole-script fixtures arepinned andunregistered. '
 'WholeB27 selects35of51 speeches and82commands including9initializers,normal[0,0]at12415 bothversions;16conditional speeches,includingGerhardintro,areunvisited. '
 'Its later initialized tail entersSC0B44 withcaptain0/party0 inbothversions. It doesnot prove normalLilroutecontinuity,naturalStockholmactivation,originallocation orearnedprogress. '
 'WholeB74 selects75of79 speeches and114commands including9initializers;allthree corrected surnamebodies and30Gerhard speaking entries appear. Originaltypedchoice selectsoption0 andreturns[2,0],withnormal[0,0]at22255 bothversions. '
 'FourB74 speechobjects andindividualoption1 selection remainunvisited. Preservealloriginal conditions;do notcall theunvisited branches completed gameplay.\n\n'
 'Additional8227/8228 B27 eight-speech introduction display fixtures cover bothcorrectedB27 bodies withoriginalunaltered speeches,closingzero-skip andnormalend. '
 'The original outercondition andremaining B27effects areexplicitly NOTexecuted bythis focused display slice. Its normalreturns5695previous/5694revised aremeasured. '
 'No runtimeflags,results,roster,roles,funds,RNG,controllerretiming,battery orsavestate forcing. These6 initialruns total152006frames. '
 'Actual8229 audit finds all5 correctedsinglepages complete,30complete bodyholds and262relevant complete nameholds acrossbefore/after pairs,withzero unresolved masks. '
 'Allselectedresults,textmemberships,choice andUIrequestwords agree. Gerhard namewidth includingnativeflush changes120px to108px asintended;Hodram/Camille labelsstayexact. Fivebefore/aftercrop sheetswere directlyviewed.\n\n'
 'Measured8230b scene/portrait upperRGB pairs117 (34wholeB27,75wholeB74,8intro) allmatch;onewholeB27 speech hasno common heldshot. Unchanged testedheaders match. '
 'Commandcomparison/duration-difference counts are1/0 wholeB27,74/19 wholeB74 and8/2 intro. All rawvalues andsourceoffsets arepreserved;do notclaim identicaltiming orRNGphase. '
 'WholeB27 later328RGBsamples andwholeB74 later164RGBsamples allmatch;finalfivequeried components,wholeactors andPRNGseeds match perpair. WholeB27 captain0 remains acontextlimit. '
 'Intro later29of106RGBsamples differ;finalstate/tasks/calendar equal,butmodels/persistentobjects/wholeactors/RNG differ. Preserve8230 initial failedfinal-captain2 assumption and8230b measuredscope successor.\n\n'
 'Focused exactreplays8231/8232 add24002frames/8readonlyRAMsamples perversion. Everyobserverrow exceptoutputpaths,all8 selectedPNG/framebuffers andfinalwholeRAM reproduceexactly perversion. TotalGerhardscene testing176008frames/eightterminal-reapedruns. '
 'First7sampled phases3970/4330/4810/5770/6310/9730/10510 have equalqueried state/models/persistentobjects/tasks/calendar/wholeactors;RNGvalues differat9730and10510. '
 'At12000:2fleetbytes,150actorbytes and54townbytes differ;rawcalendar535/[0,11,7]previous versus534/[0,11,6]revised. Final12001 rawcalendar both535/[0,11,7]. Do not interpretthese dates. '
 'These arebounded fixtureobservations,not everyframecausality,futureoutcomes orfullsimulationequivalence. Alltiming/RNG/component/byte/calendar/RGB/fixture limits remainforlaterolder-record technicalre-audit.\n\n'
 'Scoped actualapproval8233 creates translations/gerhard_surname_consistency_manuscript_v2.json:five per-record natural-dialogue-v2 gates true forfive previously completed speeches andoneownednameasset. '
 'Allprose exceptsurname andallindividualretentionreasons areexact;11sheets directlyviewed (2nativecomparison,5actualbodies,3laterpairs,1focusedphase). All5 wraps areautomatic216px/fourrows,singlepages,fullfirst/internal/finalglyphs complete. '
 'No concrete editedname clipping,droppedglyph,unintendedpage,changedoriginalchoice/control ornormal-return defect remains intested scope. Frozenpolicy/independentatomicproduction/registeredcumulative/exactcleanpatch/regressions/ownregisteredstartup remainpending. '
 'This revisit addszeroduplicate source/prose/completed/revised/retained credit. RegisteredV8172/mainV4701 stillhave theoldname pending explicitintegration. '
 'The28 HodramEnglishbodies remainunconsulted/uncredited;source/context/nativecontrols/item/pathproofs8183/8187-8192 andnameprosev2 remainverified. Theirformatting/actual/releasegates arenotgranted bythis Lil evidence. Fullgoal andallpriorunfinished families/leads remainintact.'
)
NEXT=(
 'Continue from verifiedV8235/currentregisteredV8172. Reuse allGerhard proofs through scopedactualapproval8233/manuscriptv2;do not repeatcompleted native/loader/actual/replay checks without anewchange orconcreterisk. '
 'Nextfreeze a dedicated natural-dialogue-v2 source/prose/layout/name contract forfive sparseSC2 records plusoneARM9 owned12-byte field. Bind exact source/current/compiled/stored refs,allfivegates,sourceFI1/Lil3-Argot5-ArgotCo9,216px/fourrows/6pxASCII/12pxCP932,fullpreambles,zeroNULbody,phase/guard rules,zero warnings/oneinfo. '
 'Bind name9letters+NUL+2zeros within12,protectedBlades8/pointers/nointeriorliteralalias/fullARM9inverse,all14 existingconsistentconsumers andall20finalLatinoccurrences. PreserveapprovedHodram/Joakim/Camille andallothernamefields. '
 'Policy mustreject actual-changing prose/facts/rank/relationship/macros/source/preamble/profile/name-span/neighbor mutations withoutweakened globalguards. Then independentlyseal fullreference/relocation/source controls/actualscope includingalllaterlimits. '
 'Implement independent atomicstage forARM9+SC2 afterfullV8172 stack:validate bothchanges completely beforeone finalNDS-object commit (ARM9component andfiles list). Do not claimonefile-listcommit whenchanginganARM9component too. '
 'Positive exactfull-reference test andmeaningful precommit semanticproof-corruption tests withdeliberate digestbypass/committraps/trustedcontractrevalidation are required. '
 'Thenregisterexperimental cumulative profile inheritingallV8172 layers,build throughbuild_integrated_release.py,requireexactapprovedreference/clean-inputpatch/appropriate release regressions andownregisteredstartup. '
 'No newdialoguecreditforfive alreadycompleted revisions. MainV4701unchanged;no separateunifiedtestpackage,promotion,pruning,commit orpush.\n\n'
 'KeepfullB27 initializedactual35of51 andcaptain0laterSC0B44 tail distinctfromnormalLilroutecoverage. WholeB74actual75of79 includesall3editedbodies/defaultmenuoption0;introdisplay8covers2editedB27bodies butoutercondition/remainingeffects areunexecuted. '
 'Retain152006initial+24002replayframes,30completebodyholds,262nameholds,117sceneRGBpairs,allUI/results same,command/timingdifferences1/0,74/19,8/2,andthefullrecordedRNG/component/byte/calendar/RGB/fixturelimits. '
 'FullB27later328 andB74later164RGBpairs/finalfivecomponents/actors/seeds equal;intro29of106laterRGBdiffs andfinalmodels/persistent/actors/RNGdifferences staybounded,notbroadsimulationequivalence. '
 'First7focused RAMcomponentsets equal;12000diff2fleet/150actor/54townbytes andonecalendar-tick/dateoffsetbeforefinalcalendarconvergence;rawdatesuninterpreted. Preserveallfailureproducers/artifacts andexecutedfiles.\n\n'
 'Return to28clean-first HodramSC1B137/B45/B46 currentbodymapping/effectivecomparison andwhole-exchange English review;thismayproceed independently whileH1integrationmustincludeexplicitregisteredAdernkatz dependency. '
 'Reuse28glosses8183,owncaptain1input8187,controls8188,4800RedDye/layout0proof8190b,paths8191,names8192 andsix-nameprosev2. PreserveHodramrestraint,Camillehesitation,Charlesbluntness,Gerhardpracticalfleetadvice,Lilfinancialcompetitivebravado andmapkeyconfusion. '
 'No inventedrank,kinship,romance,guaranteedrecruitment,completedroutes,mapgift/ownership oraccepted/woncontest. NewH1route-awarelayout/nativeglyphs/all60controls/8relatives/2rawevaluators/valuecarry/distinct4800layout0-hide4700/silences/representativeactual/policy/registeredrelease remainpending.\n\n'
 +previous.NEXT[previous.NEXT.index('Keepfullobjective'):]
)
if __name__=='__main__':
    assert not ROOT.exists();source=Path(previous.__file__).read_text('utf8');tree=ast.parse(source)
    assignments={n.targets[0].id:ast.get_source_segment(source,n) for n in tree.body if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Name)}
    gates_old=next(ast.get_source_segment(source,n) for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='gates')
    key="all(all(r['review'][k] for k in ['source','context','localization','naturalness']) and not r['review']['formatting'] for r in doc['records'])"
    assert gates_old.count(key)==1
    gates_new=gates_old.replace(key,"all(all(r['review'][k] is True for k in ['source','context','localization','naturalness','formatting']) for r in doc['records'])")
    extra='''    assert all(doc['name_records'][0]['review'].values()) and data['actual_approval']['manuscript_sha256']==sha(DOC.read_bytes())
    assert data['actual_approval']['individual_five_gate_body_records']==5 and data['actual_approval']['individual_five_gate_owned_name_records']==1
    actual=data['actual'];assert not actual['unresolved'] and actual['complete_body_holds']==30 and actual['relevant_name_holds']==262
    assert actual['new_actual_frames']==int('152006') and len(actual['groups'])==6
    assert sorted(actual['complete_changed_body_IDs_revised'])==sorted(r['id'] for r in doc['records'])
    assert data['native_loaders']['fresh_native_whole_loads_andcache_hits']==336 and data['native_loaders']['fresh_initial_parent_modes']==672
    assert data['caller_census']['all225_source_current_target_commands44_relative_sites_bound_to_research_ROM'] and data['caller_census']['fresh_caller_censuses']==2
    comparison=data['actual_comparison'];assert comparison['actual_sha256']==sha(Path(PROOFS['actual']).read_bytes())
    assert sum(len(g['selected_scene_andportrait_pairs']) for g in comparison['groups'])==117 and all(g['all_UI_request_words_equal'] for g in comparison['groups'])
    assert [len(g['duration_differences']) for g in comparison['groups']]==[0,19,2]
    assert [len(g['later_RGB_differences']) for g in comparison['groups']]==[0,0,29]
    assert [g['later_sample_count'] for g in comparison['groups']]==[328,164,106]
    focus=data['actual_focus'];assert focus['total_Gerhard_scene_frames_including_replay']==int('176008') and focus['new_actual_frames']==24002
    assert focus['all_same_ROM_input_horizon_observer_rows_selected_framebuffers_andfinal_RAM_reproduce_exactly_perversion']
    assert len(data['actual_approval']['directly_viewed_sheets'])==11 and all(s['directly_viewed'] for s in data['actual_approval']['directly_viewed_sheets'])
    for group in actual['groups']:
        terminal=read(group['terminal']);assert terminal['terminal'] and terminal['all_callbacks_readonly_andhost_slots_restored']
        assert sha(Path(terminal['report']).read_bytes())==terminal['report_sha256'] and sha(Path(terminal['observer']).read_bytes())==terminal['observer_sha256']
        for speech in group['speeches']:
            for hold in speech.get('complete_holds',[]):assert sha(Path(hold['capture']).read_bytes())==hold['sha256']
    for group in focus['groups']:
        terminal=read(group['terminal']);assert terminal['terminal'] and terminal['frames']==12001 and terminal['all_callbacks_readonly_andhost_slots_restored']
    return prior,data'''
    gates_new=gates_new.replace('    return prior,data',extra);assert gates_new!=gates_old
    pending_old=source[source.index('        pending=dict('):source.index('        inventory[KEY]=')]
    pending_new=pending_old.replace('pending-loaders-callers-actual-registered-release','scoped-actual-approved-pending-frozen-policy-atomic-registered-release')
    pending_new=pending_new.replace('new_credit=0,new_emulator_runs=1,new_actual_frames=4001,new_optional_scene_runs=0',
        "all5_body_andone_owned_name_formatting_gates_true=True,actual_complete_body_holds=30,actual_relevant_name_holds=262,\n            actual_fullB27_selected35_of51_intro_unvisited=True,actual_fullB74_selected75_of79_three_edited_bodies=True,actual_intro_display8_outercondition_not_executed=True,\n            fullB27_later_captain0_SC0B44_fixture_limit=True,exact_focused_replay8RAMphases=True,policy_atomic_registered_integration_pending=True,\n            new_credit=0,new_emulator_runs=8,new_actual_frames=int('176008'),new_research_ROMs=6,new_natural_optional_scene_runs=0")
    assert pending_new!=pending_old
    verify_old=source[source.index('            verified=deepcopy(prior);'):source.index('            VERIFY.mkdir')]
    verify_new='''            verified=deepcopy(prior);verified.update(ledger_sha256=sha(LEDGER.read_bytes()),previous_verified_handoff=str(PRIOR),
                previous_verified_handoff_sha256=sha(PRIOR.read_bytes()),next_required=NEXT,unfinished_scope=SCOPE,pending_source_batch=KEY,
                strict_own_Lil_current_input=PROOFS['Lil_input'],strict_own_Gerhard_research_input=PROOFS['research_input'],
                new_credit=0,new_emulator_runs=8,new_actual_frames=int('176008'),new_research_ROMs=6,all_sessions_terminal_andreaped=True,
                all_prior_roots_families_records_andcounts_recover_exactly=True,full_goal_active=True,full_goal_complete=False,producer_sha256=sha(Path(__file__).read_bytes()))
            details=verified['Gerhard_surname_correction_checkpoint'];details.pop('loaders_callers_actual_andregistered_release_pending',None)
            details.update(approved_manuscript=str(DOC),approved_manuscript_sha256=sha(DOC.read_bytes()),all5_body_andone_owned_name_formatting_gates_true=True,
                native_archive_loads=336,native_parent_modes=672,fresh_shipped_caller_censuses=2,actual_complete_body_holds=30,actual_relevant_name_holds=262,
                fullB27_actual35of51_latercaptain0_fixture_limit=True,fullB74_actual75of79_defaultchoice0=True,
                focusedB27_intro8speeches_not_original_outercondition=True,exact_focused_replay8RAMphases=True,
                scene_frames_including_replay=int('176008'),scoped_actual_approval=PROOFS['actual_approval'],frozen_policy_atomic_andregistered_release_pending=True)
            verified['Hodram_source_native_checkpoint'].update(name_surname_concern_pending=False,surname_registered_asset_pending=True,current_dialogue_English_unconsulted=True)
'''
    values={'ROOT':"Path('work/analysis/Gerhard_actual_checkpoint_v8234')",'VERIFY':"Path('work/analysis/editorial_handoff_verification_v8235')",
        'PRIOR':"Path('work/analysis/editorial_handoff_verification_v8221/verified_handoff.json')",'DOC':"Path('translations/gerhard_surname_consistency_manuscript_v2.json')",
        'KEY':repr('Gerhard_Adernkatz_scoped_actual_format_approved_pending_policy_atomic_registered_andHodram28_v8234'),
        'OLD_KEY':repr(previous.KEY),'SCOPE':repr('unfinished_editorial_scope_v8234'),'PROOFS':repr(PROOFS),'SUMMARY':repr(SUMMARY),'NEXT':repr(NEXT)}
    changes={assignments[k]:k+'='+v for k,v in values.items()}
    changes.update({gates_old:gates_new,pending_old:pending_new,verify_old:verify_new,
        'Gerhard_fullreference_controls_andown_research_startup_now_pass=True,loaders_callers_actual_registered_andHodram_bodyEnglish_pending=True':
        'Gerhard_source_native_loaders_andscoped_actual_formatting_now_pass=True,frozen_policy_atomic_registered_andHodram_bodyEnglish_pending=True',
        '## V8220: Gerhard isolated reference andown startup verified; focused scenes andregistered correction pending':
        '## V8234: Gerhard five surname passages andowned name format approved; frozen policy andregistered correction pending',
        '# Current editorial handoff - V8220; V8172 current':'# Current editorial handoff - V8234; V8172 current',
        'Gerhard research-reference/own-startup checkpoint staged;six targets,zero credit.Deep inverse audit next.':'Gerhard scoped-actual/format-approval checkpoint staged;six targets,zero credit.Deep inverse audit next.',
        'Gerhard research-reference/own-startup checkpoint applied;currentV8172 andallcompletion counts unchanged.Full goal active.':'Gerhard scoped-actual/format-approval checkpoint applied;currentV8172 andallcompletion counts unchanged.Full goal active.',
        'VerifiedV8221/currentV8172:7171completed;Gerhard pinned fullreference/finalcontrols/own4001frame startup/6RGBpairs/8getters pass.Focused scenes/registered correction/Hodram28 prose pending.Full goal active.':
        'VerifiedV8235/currentV8172:7171completed;Gerhard5body+1nameformat gates/30actualbodyholds/262nameholds/native archive-caller proofs/scoped actualrisk pass.Frozenpolicy/atomic/registered andHodram28 prose pending.Full goal active.',
    })
    result=derive(str(Path(previous.__file__)),'scripts/checkpoint_Gerhard_actual_v8234.py',changes)
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_derivation.json',result)
    print('Prepared scoped-actual/format checkpoint;zero duplicate credit,all prior scope/candidate/values reversible.')
