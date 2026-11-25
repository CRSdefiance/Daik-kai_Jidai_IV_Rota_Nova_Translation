"""Checkpoint clean Hodram/source/current-native/name concern proofs without newcredit;full goalactive."""
import argparse,gzip,json,os
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.complete_B210_Ferid_v6547 import parent_at
from scripts.complete_Rafael_B50_v8184 import COUNTERS,AFTER
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Gerhard_actual_checkpoint_v8234')
VERIFY=Path('work/analysis/editorial_handoff_verification_v8235')
PRIOR=Path('work/analysis/editorial_handoff_verification_v8221/verified_handoff.json')
LEDGER=Path('translations/editorial_review_current_v1.json')
DOC=Path('translations/gerhard_surname_consistency_manuscript_v2.json')
NAMES=Path('translations/hodram_B137_B45_B46_speaker_name_review_v2.json')
KEY='Gerhard_Adernkatz_scoped_actual_format_approved_pending_policy_atomic_registered_andHodram28_v8234'
OLD_KEY='Gerhard_Adernkatz_reference_ownstartup_pending_actual_registered_andHodram28_v8220'
SCOPE='unfinished_editorial_scope_v8234'
PROOFS={'source137': 'work/analysis/Hodram_B137_clean_context_v8180/complete_clean_SC1_B137_EV1_andcoverage_before_current_English.json', 'source45': 'work/analysis/Hodram_next_clean_v8178/complete_clean_SC1_B45_EV1_andcoverage_before_current_English.json', 'source46': 'work/analysis/Hodram_B46_clean_context_v8179/complete_clean_SC1_B46_EV1_andcoverage_before_current_English.json', 'clean_names': 'work/analysis/Hodram_B137_B45_B46_clean_names_v8182/six_clean_static_identity_fields_before_current_English.json', 'gloss': 'work/analysis/Hodram_B137_B45_B46_clean_gloss_v8183/28_first_clean_glosses_six_identities_explicit_prerequisite_graph_before_current_English.json', 'prior_B44': 'work/analysis/Hodram_B137_B45_B46_clean_gloss_v8183/27_prior_clean_B44_source_refs_exact_no_new_credit.json', 'current_input': 'work/analysis/current_V8172_Hodram_native_v8187/current_native_input.json', 'startup': 'work/analysis/Hodram_current_binding_v8187/own_Hodram_startup_andstrict_captain1_context.json', 'startup_view': 'work/analysis/Hodram_current_startup_view_v8189/own_Hodram_startup_sheet_viewed.json', 'controls': 'work/analysis/Hodram_B137_B45_B46_source_controls_v8188/three_EV1_entries60_commands28_speeches_native_relative_predicate_and75_seeded_ends.json', 'picture': 'work/analysis/Hodram_B46_pigment_v8190b/original4800_descriptor181_clean_current_Red_Dye_andbounded_consumer_path.json', 'paths': 'work/analysis/Hodram_B137_B45_B46_source_paths_v8191/11_structural_compositions_all60_commands28_source_memberships.json', 'native_names': 'work/analysis/Hodram_B137_B45_B46_names_v8192/six_static_speakers12_getters_clean_fields24_synthetic_macro_alignments.json', 'names': 'translations/hodram_B137_B45_B46_speaker_name_review_v2.json', 'surname_source': 'work/analysis/Hodram_B137_B45_B46_name_review_v8193/five_clean_surname_mentions_selfintro_andprior_name_decision.json', 'consumers': 'work/analysis/Gerhard_surname_consumers_v8196/all20_current_Latin_occurrences_five_whole_clean_exchanges.json', 'Lil_input': 'work/analysis/current_V8172_Lil_native_v8198/current_native_input.json', 'Lil_startup': 'work/analysis/Lil_Gerhard_current_binding_v8198/own_Lil_startup_andstrict_captain2_context.json', 'five_refs': 'work/analysis/Gerhard_surname_five_v8199/five_prior_completed_source_current_refs_andwhole295_source_context_receipt.json', 'before_names': 'work/analysis/Gerhard_before_names_v8200/four_identities8_getters3_source_voices16_synthetic_Lil_alignments.json', 'effective': 'work/analysis/Gerhard_surname_effective_v8201/all5_effective_English_templates10_original_dispatches_no_FE.json', 'manuscript': 'translations/gerhard_surname_consistency_manuscript_v2.json', 'ownership': 'work/analysis/Gerhard_name_ownership_v8203/current12_byte_surname_owned_original20_contains_protected_Blades.json', 'logical': 'work/analysis/Gerhard_logical_v8204/5_logical_paragraphs20_original_native_alignments.json', 'plan': 'work/analysis/Gerhard_layout_v8205/5_automatic_Lil_plans_full_native_width.json', 'pages': 'work/analysis/Gerhard_pages_v8206/5_complete_native_paragraphs5_pages20_compiled_alignments.json', 'page_view': 'work/analysis/Gerhard_native_review_v8207/five_native_pages_directly_viewed_one_info_zero_warnings.json', 'relocation': 'work/analysis/Gerhard_sparse_relocation_v8208b/two_blocks_five_sparse_revisions_all_commands_native_relative_cases_full_predecessor_inverse.json', 'stored': 'work/analysis/Gerhard_stored_v8209/5_stored_bodies4_fresh16_reused_alignments5_exact_viewed_pages.json', 'target_name': 'work/analysis/Gerhard_target_name_v8210c/owned12byte_input8_getters4_complete_name_planes_Blades_protected.json', 'target_name_view': 'work/analysis/Gerhard_name_view_v8211/four_name_planes_directly_viewed_research_input_only.json', 'final_controls': 'work/analysis/Gerhard_final_controls_v8214/5_final_dispatches51_controls30_raw_evaluations150_seeded_ends.json', 'research_reference': 'work/analysis/Gerhard_reference_v8215/research_image_receipt.json', 'research_input': 'work/analysis/Gerhard_reference8215_own_native_v8218/current_native_input.json', 'research_binding': 'work/analysis/Gerhard_research_binding_v8218/own_research_startup_andstrict_captain2_context.json', 'research_startup_view': 'work/analysis/Gerhard_research_startup_view_v8219/own_research_startup6_RGBpairs_actor_equal8_fresh_getters_direct_view.json', 'prior_manuscript': 'translations/gerhard_surname_consistency_manuscript_v1.json', 'native_loaders': 'work/analysis/Gerhard_loaders_v8222/336_whole_native_loads_cache_hits672_initial_parent_modes.json', 'caller_census': 'work/analysis/Gerhard_reference_census_v8223/all225_commands44_relative_sites_five_revisions_EV2_entries_shipped_callers.json', 'whole_fixtures': 'work/analysis/Gerhard_scene_fixtures_v8224/four_complete_parent_revised_SC2_scripts_original_Lil_prelude_fixtures.json', 'actual_models': 'work/analysis/Gerhard_actual_models_v8226/five_previous_body_planes_revised_exact_reuses_three_header_consumers.json', 'intro_fixtures': 'work/analysis/Gerhard_intro_display_fixtures_v8227/two_focused_parent_revised_eight_speech_intro_display_fixtures.json', 'actual': 'work/analysis/Gerhard_actual_v8229/six_paired_runs_actual_five_surname_bodies_headers_conditions_andnormal_returns.json', 'actual_comparison': 'work/analysis/Gerhard_actual_comparison_v8230b/three_actual_pairs_scene_timing_RNG_final_components_later_RGB_scope.json', 'actual_focus': 'work/analysis/Gerhard_intro_actual_focus_v8232/exact_intro_replay8_RAM_phases_bounded_later_state_andRNG_differences.json', 'actual_approval': 'work/analysis/Gerhard_actual_approval_v8233/scoped_actual_format_approval.json'}
SUMMARY='Registered cumulative V8172 and main V4701 are unchanged. Counts remain 7171 completed,7174 source/prose and drafts,4455 integrated revisions and2716 retentions;SC0 368,SC1 91,SC2 4915,SC3 197,COMMON1600 complete/1603 source-prose,route subset5571. V8172 retains639 manifest batches/114 accepted layers/18 release checks/110 regressions,full-reference equality,exact clean-input patch andown-startup evidence. The full editorial goal remains active. No separate unified test package,promotion,pruning,commit orpush.\n\nGerhard Adernkatz source/context decision andfull295-speech clean exchanges,14 existing consistent consumers andsix inconsistent consumers are verified from8196-8203. Onlyone currently owned12-byte ARM9 surname andfive previously completed SC2 speeches are planned tochange. The original20-byte Japanese allocation nowcontains a separately referenced8-byte Blades string after the name. Preserve Blades,allpointer fields,andallbytes outside thecurrent12-byte name span;full inverse andliteral-pointer census pass,without arbitrary dynamic-alias claims. All other prose is individually retained with source/context reasons. No officialLatin canon,historicalidentity,newrank orbiography isclaimed. ApprovedHodram/Joakim/Camille remain. The pinned research reference8215 changesonlythat12-byte name span andfive SC2 bodies;all20 Latin consumers becomeAdernkatz,334 otherSC2 blocks/125 otherparagraphs/everyotherfile/component areexact,andfullparentROM inverse passes. It isnot a registered handoff ornewparent.\n\nReuse logical8204/privateLil216px-fourrow plan8205/native5pages20alignments8206/view8207/sparse8208b/stored8209/owned targetname8210c/view8211/finalcontrols8214/reference8215/ownresearchstartup8217-8219. Lil defaults remain3/5/9,sourceFI1/noFAFO,selectors01/09/10,fullpreambles,bodyNUL/phase/guard rules andfonts unchanged. One line-break-count info andzero warnings remain;no waiver ormanualwrap/shortening. Sparse B27/B74 reconstruction preserves225 commands,130 complete preambles,44 relative sites,all opaque effects,the prior reviewed typedchoice,andcomplete four-byte ends/separate storage tails. Native relative cases220clean+220current+220target pass;storedoneparitytail uses4fresh alignments andfour unchanged bodies reuse16,allfive viewedinkplanes exact. Final5dispatches/51nonrelative controls/30rawevaluations/150seeded value-carry ends pass. Research own4001-frame startup has6wholeRGBpairs/wholeactors/captain2 and8fresh namegetters,exact targetARM9/12-byte inverse/Blades/COMMON/directory/123264pool guards. Do not reuse this captain2 context forHodramcaptain1.\n\nFresh8222 whole SC2 native proof passes336 loads/cachehits and672 original entry modes. Two fresh decoded caller censuses8223 bind225commands/44relatives/twoEV2 index-based entries,withonlyoriginal24070 interpretercall andno literalalias. Onlydecoded-unit difference is theowned surname data;full ARM9 inverse proves everyotherbyte exact. Allsource-relative/opaque/menu/end maps remainbound toresearchimage. Preserve8222 failedpreparer and8222b/c exact-key correction.\n\nPaired actual tests8225 keepfull original B27/B74 scripts behind the original9-command/48-byte Lil prelude,with identical ordinary inputs andreadonly observers. All4whole-script fixtures arepinned andunregistered. WholeB27 selects35of51 speeches and82commands including9initializers,normal[0,0]at12415 bothversions;16conditional speeches,includingGerhardintro,areunvisited. Its later initialized tail entersSC0B44 withcaptain0/party0 inbothversions. It doesnot prove normalLilroutecontinuity,naturalStockholmactivation,originallocation orearnedprogress. WholeB74 selects75of79 speeches and114commands including9initializers;allthree corrected surnamebodies and30Gerhard speaking entries appear. Originaltypedchoice selectsoption0 andreturns[2,0],withnormal[0,0]at22255 bothversions. FourB74 speechobjects andindividualoption1 selection remainunvisited. Preservealloriginal conditions;do notcall theunvisited branches completed gameplay.\n\nAdditional8227/8228 B27 eight-speech introduction display fixtures cover bothcorrectedB27 bodies withoriginalunaltered speeches,closingzero-skip andnormalend. The original outercondition andremaining B27effects areexplicitly NOTexecuted bythis focused display slice. Its normalreturns5695previous/5694revised aremeasured. No runtimeflags,results,roster,roles,funds,RNG,controllerretiming,battery orsavestate forcing. These6 initialruns total152006frames. Actual8229 audit finds all5 correctedsinglepages complete,30complete bodyholds and262relevant complete nameholds acrossbefore/after pairs,withzero unresolved masks. Allselectedresults,textmemberships,choice andUIrequestwords agree. Gerhard namewidth includingnativeflush changes120px to108px asintended;Hodram/Camille labelsstayexact. Fivebefore/aftercrop sheetswere directlyviewed.\n\nMeasured8230b scene/portrait upperRGB pairs117 (34wholeB27,75wholeB74,8intro) allmatch;onewholeB27 speech hasno common heldshot. Unchanged testedheaders match. Commandcomparison/duration-difference counts are1/0 wholeB27,74/19 wholeB74 and8/2 intro. All rawvalues andsourceoffsets arepreserved;do notclaim identicaltiming orRNGphase. WholeB27 later328RGBsamples andwholeB74 later164RGBsamples allmatch;finalfivequeried components,wholeactors andPRNGseeds match perpair. WholeB27 captain0 remains acontextlimit. Intro later29of106RGBsamples differ;finalstate/tasks/calendar equal,butmodels/persistentobjects/wholeactors/RNG differ. Preserve8230 initial failedfinal-captain2 assumption and8230b measuredscope successor.\n\nFocused exactreplays8231/8232 add24002frames/8readonlyRAMsamples perversion. Everyobserverrow exceptoutputpaths,all8 selectedPNG/framebuffers andfinalwholeRAM reproduceexactly perversion. TotalGerhardscene testing176008frames/eightterminal-reapedruns. First7sampled phases3970/4330/4810/5770/6310/9730/10510 have equalqueried state/models/persistentobjects/tasks/calendar/wholeactors;RNGvalues differat9730and10510. At12000:2fleetbytes,150actorbytes and54townbytes differ;rawcalendar535/[0,11,7]previous versus534/[0,11,6]revised. Final12001 rawcalendar both535/[0,11,7]. Do not interpretthese dates. These arebounded fixtureobservations,not everyframecausality,futureoutcomes orfullsimulationequivalence. Alltiming/RNG/component/byte/calendar/RGB/fixture limits remainforlaterolder-record technicalre-audit.\n\nScoped actualapproval8233 creates translations/gerhard_surname_consistency_manuscript_v2.json:five per-record natural-dialogue-v2 gates true forfive previously completed speeches andoneownednameasset. Allprose exceptsurname andallindividualretentionreasons areexact;11sheets directlyviewed (2nativecomparison,5actualbodies,3laterpairs,1focusedphase). All5 wraps areautomatic216px/fourrows,singlepages,fullfirst/internal/finalglyphs complete. No concrete editedname clipping,droppedglyph,unintendedpage,changedoriginalchoice/control ornormal-return defect remains intested scope. Frozenpolicy/independentatomicproduction/registeredcumulative/exactcleanpatch/regressions/ownregisteredstartup remainpending. This revisit addszeroduplicate source/prose/completed/revised/retained credit. RegisteredV8172/mainV4701 stillhave theoldname pending explicitintegration. The28 HodramEnglishbodies remainunconsulted/uncredited;source/context/nativecontrols/item/pathproofs8183/8187-8192 andnameprosev2 remainverified. Theirformatting/actual/releasegates arenotgranted bythis Lil evidence. Fullgoal andallpriorunfinished families/leads remainintact.'
NEXT='Continue from verifiedV8235/currentregisteredV8172. Reuse allGerhard proofs through scopedactualapproval8233/manuscriptv2;do not repeatcompleted native/loader/actual/replay checks without anewchange orconcreterisk. Nextfreeze a dedicated natural-dialogue-v2 source/prose/layout/name contract forfive sparseSC2 records plusoneARM9 owned12-byte field. Bind exact source/current/compiled/stored refs,allfivegates,sourceFI1/Lil3-Argot5-ArgotCo9,216px/fourrows/6pxASCII/12pxCP932,fullpreambles,zeroNULbody,phase/guard rules,zero warnings/oneinfo. Bind name9letters+NUL+2zeros within12,protectedBlades8/pointers/nointeriorliteralalias/fullARM9inverse,all14 existingconsistentconsumers andall20finalLatinoccurrences. PreserveapprovedHodram/Joakim/Camille andallothernamefields. Policy mustreject actual-changing prose/facts/rank/relationship/macros/source/preamble/profile/name-span/neighbor mutations withoutweakened globalguards. Then independentlyseal fullreference/relocation/source controls/actualscope includingalllaterlimits. Implement independent atomicstage forARM9+SC2 afterfullV8172 stack:validate bothchanges completely beforeone finalNDS-object commit (ARM9component andfiles list). Do not claimonefile-listcommit whenchanginganARM9component too. Positive exactfull-reference test andmeaningful precommit semanticproof-corruption tests withdeliberate digestbypass/committraps/trustedcontractrevalidation are required. Thenregisterexperimental cumulative profile inheritingallV8172 layers,build throughbuild_integrated_release.py,requireexactapprovedreference/clean-inputpatch/appropriate release regressions andownregisteredstartup. No newdialoguecreditforfive alreadycompleted revisions. MainV4701unchanged;no separateunifiedtestpackage,promotion,pruning,commit orpush.\n\nKeepfullB27 initializedactual35of51 andcaptain0laterSC0B44 tail distinctfromnormalLilroutecoverage. WholeB74actual75of79 includesall3editedbodies/defaultmenuoption0;introdisplay8covers2editedB27bodies butoutercondition/remainingeffects areunexecuted. Retain152006initial+24002replayframes,30completebodyholds,262nameholds,117sceneRGBpairs,allUI/results same,command/timingdifferences1/0,74/19,8/2,andthefullrecordedRNG/component/byte/calendar/RGB/fixturelimits. FullB27later328 andB74later164RGBpairs/finalfivecomponents/actors/seeds equal;intro29of106laterRGBdiffs andfinalmodels/persistent/actors/RNGdifferences staybounded,notbroadsimulationequivalence. First7focused RAMcomponentsets equal;12000diff2fleet/150actor/54townbytes andonecalendar-tick/dateoffsetbeforefinalcalendarconvergence;rawdatesuninterpreted. Preserveallfailureproducers/artifacts andexecutedfiles.\n\nReturn to28clean-first HodramSC1B137/B45/B46 currentbodymapping/effectivecomparison andwhole-exchange English review;thismayproceed independently whileH1integrationmustincludeexplicitregisteredAdernkatz dependency. Reuse28glosses8183,owncaptain1input8187,controls8188,4800RedDye/layout0proof8190b,paths8191,names8192 andsix-nameprosev2. PreserveHodramrestraint,Camillehesitation,Charlesbluntness,Gerhardpracticalfleetadvice,Lilfinancialcompetitivebravado andmapkeyconfusion. No inventedrank,kinship,romance,guaranteedrecruitment,completedroutes,mapgift/ownership oraccepted/woncontest. NewH1route-awarelayout/nativeglyphs/all60controls/8relatives/2rawevaluators/valuecarry/distinct4800layout0-hide4700/silences/representativeactual/policy/registeredrelease remainpending.\n\nKeepfullobjectiveallfourstories/earliertranslateddialogue/sharedshops-towns/random/Help/remainingprose/all207names-roles-aliases/retrospectiveearlybreaks. Preserveeverypriorunfinishedinventory,12contraction/questiontagleads,unscannedbeyond558plans,weak-before-row/page-before-readability/phrasecoherence. KeepPasardistinctfromPasha,Cristina/Christina,HansRetzel/Letzel,Trader/PortWorker/Guildmaster,Sailor151-159versusRetainerconsumers,COMMON750-752,preLF6435,ArmadilloHide/SteelHide,HerophilusMedicine,AksumGoldSeal,AlShin/AlFeridShin,イギリス andallrecordeditem/counterpart/displayleads. Graphics/all18plaques andlaterolder-recordtechnicalre-audit separate:normalendcarry,B35R65/B48R129source19thcells,B48stalerelocationlabel,B47correctedregistrationreceipt,B50checkpoint8149blocklabelcompanion,andalltiming/highlight/RNG/component/byte/calendar/RGB/fixture-reentrylimits. PreserveallROMs/translations/drafts/failures/executedproducers/proofs. MainV4701unchanged;no separateunifiedpackage,promotion,pruning,commit orpush. Fullgoalactive.'

def restore(value):
    result=deepcopy(value);entry=result.pop(KEY)
    for op in reversed(entry['inverse_operations']):
        parent,key=parent_at(result,op['path'])
        if op['existed']:parent[key]=deepcopy(op['before'])
        else:parent.pop(key)
    return result
def gates():
    prior,doc,names=map(read,[PRIOR,DOC,NAMES]);data={k:read(p) for k,p in PROOFS.items()}
    assert prior['completed']==7171 and prior['manifest_batches']==639
    assert sha(Path(prior['candidate']).read_bytes())==prior['candidate_sha256']==data['Lil_input']['current_ROM_sha256']
    assert sha(Path(prior['patch']).read_bytes())==prior['patch_sha256']
    assert len(doc['records'])==5 and all(r['already_editorially_completed'] and r['previous_credit_classification']=='revised-and-integrated' for r in doc['records'])
    assert all(all(r['review'][k] is True for k in ['source','context','localization','naturalness','formatting']) for r in doc['records'])
    assert len(names['records'])==6 and sum(r['decision']=='retention' for r in names['records'])==5 and sum(r['decision']=='revision' for r in names['records'])==1
    assert all(all(r['review'][k] for k in ['source','context','localization','naturalness']) and not r['review']['formatting'] for r in names['records'])
    assert data['five_refs']['all295_clean_records_reviewed_for_name_identity_context_not_full_new_prose_credit']
    assert data['five_refs']['current_Hodram_B137_B45_B46_body_English_still_unconsulted']
    assert data['Lil_startup']['actual_original_captain_ID']==2 and data['Lil_startup']['actual_frames']==4001
    assert data['Lil_startup']['all_strict2b6_COMMON_directory_and123264_payload_guards_pass']
    assert data['before_names']['measured_default_macro_lengths']==dict(FI=3,FA=5,FO=9)
    assert len(data['effective']['effective_current_records'])==5 and len(data['effective']['source_current_dispatches'])==10
    assert data['ownership']['current_owned_name_span']['bytes']==12 and data['ownership']['protected_neighbor']['text']=='Blades'
    assert not data['ownership']['interior_name_literal_pointer_references'] and data['ownership']['whole_ARM9_inverse_recovers_exact_current']
    assert data['logical']['total_bound_alignment_cases']==20 and data['logical']['source_macro_totals']==dict(FI=1,FA=0,FO=0)
    assert len(data['plan']['records'])==5 and not data['plan']['failures']
    assert sum(i['severity']=='info' for r in data['plan']['records'] for i in r['base_QA']['issues'])==1
    assert not any(i['severity'] in ['warning','error'] for r in data['plan']['records'] for i in r['base_QA']['issues'])
    assert data['pages']['complete_progressive_pages']==5 and data['pages']['fresh_compiled_alignment_cases']==20
    assert data['page_view']['all_five_complete_bodies_visually_read'] and data['page_view']['pages_sha256']==sha(Path(PROOFS['pages']).read_bytes())
    rel=data['relocation'];assert len(rel['groups'])==2 and rel['source_relative_sites']==44
    assert rel['clean_native_skip_cases']==rel['current_native_skip_cases']==rel['target_native_skip_cases']==220
    assert sum(len(g['all_target_commands']) for g in rel['groups'])==225 and rel['all125_other_speeches_unchanged'] and rel['other_archive_blocks_exact']==334
    assert rel['all_full_predecessor_archive_bytes_reconstructed_exactly']
    assert sha(Path(rel['target_archive']).read_bytes())==rel['target_archive_sha256']
    stored=data['stored'];assert len(stored['records'])==5 and stored['fresh_native_alignment_cases']==4 and stored['exact_reused_native_alignment_cases']==16
    target=data['target_name'];assert len(target['native_eight_getters']['rows'])==8 and len(target['planes'])==4
    assert target['CPU_only_owned_data_input_not_current_ROM_change_actual_scene_ornew_ROM_startup'] and target['protected_Blades_bytes_andall_other_RAM_exact']
    assert data['target_name_view']['viewed'] and data['target_name_view']['name_proof_sha256']==sha(Path(PROOFS['target_name']).read_bytes())
    assert len(data['gloss']['records'])==28 and all(r['current_English_body_not_yet_consulted'] for r in data['gloss']['records'])
    registry=read('translations/release_stack.json');assert len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v4701'
    ref=data['research_reference'];assert not ref['registered_candidate'] and ref['full_ROM_inverse_recovers_every_parent_byte']
    assert ref['parent_sha256']==prior['candidate_sha256'] and sha(Path(ref['research_ROM']).read_bytes())==ref['research_ROM_sha256']
    assert len(ref['all20_Adernkatz_consumers'])==20 and ref['no_Ardelknatts_orArdelnkatts_remaining_in_image']
    assert ref['every_ARM9_byte_outside_owned12_andBlades_pointer_andtext_exact']
    controls=data['final_controls'];assert len(controls['final_dispatches'])==5 and len(controls['original_nontext_control_maps'])==51
    assert controls['raw_native_evaluations']==30 and controls['normal_seeded_end_cases']==150
    startup=data['research_startup_view'];assert startup['viewed'] and len(startup['six_whole_RGB_pairs'])==6 and startup['fresh_ordinary_research_coldboot_frames']==4001
    assert startup['research_ROM_sha256']==ref['research_ROM_sha256'] and startup['target_family_bytes_andprotected_Blades_measured_inactual_coldboot_RAM']
    assert len(startup['native_eight_getters_from_actual_own_research_snapshot']['rows'])==8 and startup['optional_Stockholm_Hamburg_surname_body_andGerhard_header_actual_UI_not_visited']
    assert data['research_binding']['all_strict_targetARM9_inverse_COMMON_directory_and123264_payload_guards_pass']
    assert data['research_input']['current_ROM_sha256']==ref['research_ROM_sha256'] and not data['research_input']['registered_candidate']
    assert all(doc['name_records'][0]['review'].values()) and data['actual_approval']['manuscript_sha256']==sha(DOC.read_bytes())
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
    return prior,data

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('phase',choices=['stage','audit','apply','verify']);mode=ap.parse_args().phase
    prior,data=gates()
    if mode=='stage':
        assert not ROOT.exists();before=LEDGER.read_bytes();old=json.loads(before)
        assert sha(before)==prior['ledger_sha256'] and tuple(old[k] for k in COUNTERS)==AFTER
        assert old['goal_status']=='active' and not old['full_goal_complete'] and KEY not in old and SCOPE not in old and OLD_KEY in old
        new=deepcopy(old);ops=[]
        def put(path,value):
            parent,key=parent_at(new,path);exists=key in parent
            ops.append(dict(path=path,existed=exists,before=deepcopy(parent[key]) if exists else None));parent[key]=deepcopy(value)
        previous_scope=old[prior['unfinished_scope']]
        assert sha(Path(previous_scope['path']).read_bytes())==previous_scope['sha256']
        inventory=deepcopy(read(previous_scope['path']));inventory['next_focus']=NEXT
        evidence={str(p):sha(Path(p).read_bytes()) for p in [PRIOR,DOC,NAMES,Path(__file__),*map(Path,PROOFS.values())]}
        pending=dict(status='Adernkatz-source-localization-five-native-pages-sparse-relocation-andstored-pass-fullreference-own-startup-pass-scoped-actual-approved-pending-frozen-policy-atomic-registered-release',
            manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),names=str(NAMES),names_sha256=sha(NAMES.read_bytes()),
            corrected_name_target='Gerhard Adernkatz',registered_name_asset_not_yet_changed=True,
            corrected_five_existing_body_records=5,file_path='/data/SC2.DK4',blocks=[27,74],
            prior_completed_revisions_revisited_no_duplicate_credit=True,complete_clean_name_context_speeches=295,
            logical_alignments=20,compiled_alignments=20,native_complete_pages=5,source_relative_sites=44,
            clean_current_target_native_structural_cases=660,all125_other_speeches_andtyped_choice_preserved=True,
            stored_fresh_alignments=4,stored_exact_reused_alignments=16,
            owned_ARM9_name_span_bytes=12,protected_neighbor='Blades',CPU_only_target_getters=8,complete_name_input_planes=4,
            owned_CPU_input_not_current_ROM_oractual_scene=True,
            source_Hodram_pending_reference='Hodram_SC1B137_B45_B46_source_native_pending_surname_current_prose_release_v8194',Hodram_blocks=[137,45,46],Hodram_objects=28,Hodram_current_body_English_unconsulted=True,
            research_ROM=data['research_reference']['research_ROM'],research_ROM_sha256=data['research_reference']['research_ROM_sha256'],
            research_input=PROOFS['research_input'],research_startup_proof=PROOFS['research_startup_view'],research_whole_RGB_pairs=6,own_research_native_getters=8,
            final_raw_evaluations=30,seeded_normal_end_cases=150,own_Lil_native_input=PROOFS['Lil_input'],all_proofs=PROOFS,current_ROM=prior['candidate'],current_ROM_sha256=prior['candidate_sha256'],
            all5_body_andone_owned_name_formatting_gates_true=True,actual_complete_body_holds=30,actual_relevant_name_holds=262,
            actual_fullB27_selected35_of51_intro_unvisited=True,actual_fullB74_selected75_of79_three_edited_bodies=True,actual_intro_display8_outercondition_not_executed=True,
            fullB27_later_captain0_SC0B44_fixture_limit=True,exact_focused_replay8RAMphases=True,policy_atomic_registered_integration_pending=True,
            new_credit=0,new_emulator_runs=8,new_actual_frames=int('176008'),new_research_ROMs=6,new_natural_optional_scene_runs=0,full_goal_complete=False)
        inventory[KEY]=deepcopy(pending)
        if OLD_KEY in inventory:inventory[OLD_KEY]['superseded_by']=dict(checkpoint=KEY,Gerhard_source_native_loaders_andscoped_actual_formatting_now_pass=True,frozen_policy_atomic_registered_andHodram_bodyEnglish_pending=True,new_credit=0)
        ROOT.mkdir(parents=True);scope=ROOT/'unfinished_editorial_scope_inventory.json';save(scope,inventory)
        put([SCOPE],dict(path=str(scope),sha256=sha(scope.read_bytes()),all_prior_leads_families_history_andfull_four_storyline_objective_preserved=True,
            incomplete_COMMON=3,incomplete_credited_route_drafts=0,graphics_andlater_older_record_technical_reaudit_separate=True,full_goal_complete=False))
        put([OLD_KEY,'superseded_by'],dict(checkpoint=KEY,Gerhard_source_native_loaders_andscoped_actual_formatting_now_pass=True,frozen_policy_atomic_registered_andHodram_bodyEnglish_pending=True,new_credit=0))
        put(['latest_checkpoint'],SUMMARY+'\n\n'+NEXT)
        new[KEY]=dict(**pending,summary=SUMMARY,next=NEXT,evidence=evidence,inverse_operations=ops,goal_turn_classification='progress',all_sessions_terminal_andreaped=True)
        assert restore(new)==old and tuple(new[k] for k in COUNTERS)==AFTER and new['current_integrated_candidate']==old['current_integrated_candidate']
        (ROOT/'ledger.before.json.gz').write_bytes(gzip.compress(before,mtime=0));targets={LEDGER:encode_ledger(new)}
        section='## V8234: Gerhard five surname passages andowned name format approved; frozen policy andregistered correction pending\n\n'+SUMMARY+'\n\n'+NEXT+'\n\n'
        for name in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']:
            path=Path('docs')/name
            prefix=('# Current editorial handoff - V8234; V8172 current\n\n' if name=='editorial_handoff_current.md' else '')+section
            targets[path]=prefix.replace('\n','\r\n').encode()+path.read_bytes()
        files=[]
        for i,(path,value) in enumerate(targets.items()):
            planned=ROOT/f'{i:02d}.after';planned.write_bytes(value)
            if path!=LEDGER:(ROOT/f'{i:02d}.before.gz').write_bytes(gzip.compress(path.read_bytes(),mtime=0))
            files.append(dict(target=str(path.resolve()),before_sha256=sha(path.read_bytes()),planned=str(planned.resolve()),planned_sha256=sha(value)))
        save(ROOT/'staged_checkpoint.json',dict(files=files,evidence=evidence,unchanged_counters=list(AFTER),new_credit=0,full_goal_complete=False))
        print('Gerhard scoped-actual/format-approval checkpoint staged;six targets,zero credit.Deep inverse audit next.')
    else:
        plan=read(ROOT/'staged_checkpoint.json');old=json.loads(gzip.decompress((ROOT/'ledger.before.json.gz').read_bytes()));new=read(plan['files'][0]['planned'])
        assert restore(new)==old and tuple(new[k] for k in COUNTERS)==AFTER and new['goal_status']=='active' and not new['full_goal_complete']
        for entry in plan['files']:
            assert sha(Path(entry['planned']).read_bytes())==entry['planned_sha256']
            assert sha(Path(entry['target']).read_bytes())==entry['planned_sha256' if mode=='verify' else 'before_sha256']
        for path,digest in plan['evidence'].items():assert sha(Path(path).read_bytes())==digest
        if mode=='audit':
            assert not (ROOT/'preapplication_audit.json').exists()
            save(ROOT/'preapplication_audit.json',dict(staged_plan_sha256=sha((ROOT/'staged_checkpoint.json').read_bytes()),
                deep_inverse_recovers_every_prior_root_family_record_counter_andcandidate=True,
                full_goal_all_prior_leads_andnew_native_stored_limits_preserved=True,new_credit=0,full_goal_complete=False))
            print('Deep inverse passes;every prior ledger value,candidate,count andunfinished lead recovers exactly.')
        elif mode=='apply':
            assert not (ROOT/'application_receipt.json').exists() and read(ROOT/'preapplication_audit.json')['staged_plan_sha256']==sha((ROOT/'staged_checkpoint.json').read_bytes())
            for entry in plan['files']:
                assert Path(entry['target']).is_relative_to(Path.cwd().resolve()) and Path(entry['planned']).is_relative_to(ROOT.resolve())
                with Path(entry['target']).open('r+b') as stream:stream.write(Path(entry['planned']).read_bytes());stream.truncate();stream.flush();os.fsync(stream.fileno())
                assert sha(Path(entry['target']).read_bytes())==entry['planned_sha256']
            save(ROOT/'application_receipt.json',dict(all_six_targets_hash_exact=True,all_prior_values_reversible=True,new_credit=0,full_goal_complete=False))
            print('Gerhard scoped-actual/format-approval checkpoint applied;currentV8172 andallcompletion counts unchanged.Full goal active.')
        else:
            assert read(ROOT/'application_receipt.json')['all_six_targets_hash_exact'] and not VERIFY.exists()
            verified=deepcopy(prior);verified.update(ledger_sha256=sha(LEDGER.read_bytes()),previous_verified_handoff=str(PRIOR),
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
            VERIFY.mkdir(parents=True);save(VERIFY/'verified_handoff.json',verified)
            print('VerifiedV8235/currentV8172:7171completed;Gerhard5body+1nameformat gates/30actualbodyholds/262nameholds/native archive-caller proofs/scoped actualrisk pass.Frozenpolicy/atomic/registered andHodram28 prose pending.Full goal active.')
