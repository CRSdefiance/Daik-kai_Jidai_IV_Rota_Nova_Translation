"""Audited zero-credit B52 contextual/native-speech/menu checkpoint; full goal intact."""
import argparse
import gzip
import json
import os
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/Hodram_B52_checkpoint_v8670')
VERIFY = Path('work/analysis/editorial_handoff_verification_v8671')
PRIOR = Path('work/analysis/editorial_handoff_verification_v8661/verified_handoff.json')
LEDGER = Path('translations/editorial_review_current_v1.json')
KEY = 'Hodram_SC1B52_contextual_native_speech_menu_review_pending_integration_v8670'
SCOPE = 'unfinished_editorial_scope_v8670'
COUNTERS = ['records_editorially_completed', 'records_with_source_and_prose_pass', 'records_with_source_prose_drafts',
    'records_revised_and_integrated', 'retained_wordings_editorially_completed']
COUNTS = [7229, 7232, 7232, 4487, 2742]
PROOFS = {'clean': 'work/analysis/Hodram_B52_clean_v8616/complete_clean_SC1_B52_EV1_andcoverage_before_current_English.json', 'gloss': 'work/analysis/Hodram_B52_clean_gloss_v8617/three_first_clean_glosses_two_choice_labels_anddistinct_terminal_risks.json', 'source_controls': 'work/analysis/Hodram_B52_source_controls_v8620/source_controls.json', 'source_display': 'work/analysis/Hodram_B52_source_display_v8626/source_display.json', 'source_choice_getters': 'work/analysis/Hodram_B52_choice_source_v8627/source_choice_getters.json', 'source_VM': 'work/analysis/Hodram_B52_source_choice_VM_v8628b/source_menu_provider_andresponse_paths.json', 'source_view_names': 'work/analysis/Hodram_B52_source_names_v8630/three_source_pages_role_andHayreddin_component_review.json', 'current': 'work/analysis/Hodram_B52_current_v8631/current_effective.json', 'prose': 'work/analysis/Hodram_B52_prose_v8632/contextual_review.json', 'manuscript': 'translations/hodram_B52_editorial_manuscript_v3.json', 'names': 'translations/hodram_B52_speaker_name_review_v1.json', 'logical': 'work/analysis/Hodram_B52_logical_v8633/logical_paragraphs.json', 'plan': 'work/analysis/Hodram_B52_layout_v8634/automatic_plans.json', 'pages': 'work/analysis/Hodram_B52_pages_v8635/compiled_native_pages.json', 'menu': 'work/analysis/Hodram_B52_menu_v8636/menu_provider_and_planes.json', 'native_review': 'work/analysis/Hodram_B52_native_review_v8637/native_body_andchoice_review.json', 'qualified_note': 'work/analysis/Hodram_B52_native_note_v8638/qualified_native_review.json', 'release': 'work/analysis/Hodram_B51_release_v8610/registered_release_verification.json', 'own_input': 'work/analysis/current_V8609_Hodram_native_v8612/current_native_input.json', 'startup': 'work/analysis/Hodram_B51_registered_startup_view_v8613/own_registered_startup6_RGBpairs_actor_equal_unchanged_names_direct_view.json', 'prior_completion_audit': 'work/analysis/Hodram_B51_completion_audit_v8625/independent_staged_completion_audit.json', 'actual_review': 'work/analysis/Hodram_B52_actual_review_v8659/qualified_actual_review.json', 'latest_manuscript': 'translations/hodram_B52_editorial_manuscript_v6.json', 'latest_names': 'translations/hodram_B52_speaker_name_review_v4.json', 'actual_review_manuscript': 'translations/hodram_B52_editorial_manuscript_v4.json', 'actual_review_names': 'translations/hodram_B52_speaker_name_review_v2.json', 'format_approval': 'work/analysis/Hodram_B52_format_v8662b/formatting_approval.json', 'frozen_contract': 'work/analysis/Hodram_B52_policy_v8663/frozen_contract.json', 'native_contract': 'translations/hodram_B52_native_contract_v1.json', 'policy': 'work/analysis/Hodram_B52_policy_validation_v8664b/policy_validation.json', 'production_reconstruction': 'work/analysis/Hodram_B52_reconstruction_production_v8666/production_reconstruction.json', 'production_native': 'work/analysis/Hodram_B52_native_production_v8667/native_production_validation.json'}

SUMMARY = "Current verified registered experimental cumulative ROM remains V8609. MainV4701/canonical baseline, every generated ROM, earlier translation, draft, executed producer, proof and failure remain preserved. Counts remain7,229 completed/7,232 credited source-prose and drafts/4,487 integrated revisions/2,742 justified retentions;SC1 149/routes5629. B51 remains credited exactly once. B52 five reviewed decisions are still unintegrated/uncredited:three speeches/two typed choices,two revisions/three individual retentions. Full all-four-storyline/earlier translated dialogue/shared town-shop/random/Help/restprose/all207 propernames-roles-aliases-customnames/retrospective premature-break objective remains active. Roughly20,000 remaining candidates is only a planning estimate,not an audited prose denominator. Graphics/all18plaques andlater older-record technical re-audit stay separate.\n\nV8660/verified8661 preserves the complete B52 clean-first source8616/gloss8617/sourcecontrols8620/sourcepages8626/choicegetters8627/qualifiedVM8628b/names8630/current8631/prose8632/logical8633/plan8634/pages8635/menu8636/nativeview8637/qualifiednote8638/stored8643/independent8644/reference8645/loaders8646/references8647/fixtures8648/actual8649-8658/qualifiedreview8659 history. Reuse these proofs and all six terminal/reaped actual runs without unchanged replay. Three research ROMs remain pinned. No new ROM,registry stage,emulator capture,promotion,separate requested package,pruning,commit orpush is added by this checkpoint.\n\nActual scope remains six initialized whole-script cold boots50,406frames/138 complete body-name holds/12 page occurrences. Main four runs40,004frames/92holds/8pages cover all3unique speeches,both ordinary A/Down choice selections and distinct normal[0,0]/flagged[1,0] end kinds. Two focused runs10,402frames/46holds/4pages use the exact unretimed default input prefix,stopping afterA4480duration5. Twelve existing captured menus/24complete captions verify Japanese/English complete glyphs,constructor-based centering/bounds andselected/unselected backgrounds/highlights,including shared4210blink-off. Live owner-pointer/RAM/VRAM/palette/unowned backing-byte identity andactualB/cancelavailability remain unclaimed;backing bounds are the separate offline menu8636proof. Both fixtures use current registered English names/UI/code/font. Originalevent52requires30/excludes74;originallocation,outereligibility/scheduling,earnedchronology,fullroute andhardware remain unobserved. No savestate,RAMoverlay,forcedflags/predicates/roster/role/funds/RNG/results orper-language retiming.\n\nAll measured limits remain:menu duration229Japanese/231English frames;normalreturns4495/4497 andflagged4494/4496. Longwithdrawal has46/93 differing later RGBpairs,unequal state/models/persistentobjects/calendar/wholeactors,matching tasks,finalseeds2571928604/1941737819 anddifferent rawcalendars. At10001Japanese sails whileEnglish displaysRiga resupply;no harmlessness orcausal explanation is established. Longopposition has13/93laterRGBdifferences,five matching sampled components/wholeactors butdifferent seeds1611048932/1190801271. Focusedwithdrawal matches all5sampled components/wholeactors/captain1/seed613908813/rawcalendar and13laterRGBpairs,withno followingcommands. It supports immediate post-exchange behavior only anddoesnot erase longdivergence orprovefuture simulation/everyframecausality. Preserve all earlier B51/B50/B49/Gerhard/Rafael/Hodram/B48 timing/RNG/RGB/calendar/followingcommand andfixture limitations.\n\nFormattingapproval8662b produces latest manuscript translations/hodram_B52_editorial_manuscript_v6.json andnames translations/hodram_B52_speaker_name_review_v4.json. Allfive individual gates nowtrue for allfive decisions,one scoped PortWorkerrole andone mentionedHayreddin surnamecomponent. Everyapproved word,source/current reference,compiledbyte,nativepage andoriginal QAinfo remains;zero warnings/waivers. Are you planning to make an enemy of Hayreddin's outfit? and You've got a death wish, huh? remain the two revisions;Not at all.,Bring it on.,Then get out before they notice you. remain individually justified retentions. PortWorker doesnot invent kinship/rank;mentionedHayreddin isnot an actualactor34header/fullname/catalogue approval. Wider contexts/all207names remainopen. The original stopped8662approval andpartialnamesv3 remain;its exploratory encoder natural-dialogue was rejected bystandardv2. Successor8662b explicitly binds dialogue-relocatable-v1 withoutaltering validator/prose/bytes.\n\nFrozencontract8663 binds three speechpages,two typedchoices,all14commands/three complete six-byte preambles/four relatives/zeroqueries/four opaquecontrols/both fullendwords,full216px metrics,FI6FA9FO15 withzero source macros,exactsource/current/final references and471 immutabledependencies. Original normal166moves158/carriesvalue;flagged224moves232/returnskind1clearsvalue. Preserve83c2andthreeA000s structurally withoutinvented effectsemantics. Scoped names andactual/offline/longdivergence/focus limits are frozen. The completebuilder is explicitly excluded fromaccidental mutablehashpinning;all earlierdependency locks remainunchanged. Standardv2 speech andchoicevalidation passes.\n\nPolicyvalidation8664b passes3speechcompilers/two choices/scopednames and243 genuinely changed semanticinputrejections withall frozen guardsactive. Cases cover individualgates,approvedprose/source/context/meaning/voices,complete source/current/finalreferences,macros/metrics/guardphase/manualbreaks/padding,sourcefile/block/runtime/consumer,typedcount/order/offsets andname/component scope. Allprotectedfiles/clean/currentROMs/registry/ledger remainhash-exact. Original8664stopped onthe testrecorder serializingtuple/list identically;successor8664b preserves inputtype inreceipt hashes withoutchanging policyorcompiler. No completedpolicyreceipt existed;no nativeprobeoractualcapture wasreplayed.\n\nProductionreconstruction8665/8666 preserves the established sparseinverse algorithm andexplicitly bindsB52's distinctnormal/flagged ends,three speechbodies andwhole32bytetypedmenu. Exact236byteblock/wholearchive matchthe independent14-command-atom reconstruction8644;clean/currentblock andwholearchive inverses pass. Twenty-six actualchanged source/control/preamble/compiledbody/relative/menu/end defects reject. Independent nativeproduction8667 rebinds trusted sourceadapters andchecks sixcomplete Japanese/storedEnglish pages plusonePortWorkerstyle11nameplane,includingfirst/internal/finalglyphs,bounds,consumption,font andpagination. Ten genuinelychanged nativeevidencedefects reject withfrozen guardsactive. These are disposable offline productionchecks,notnewgameplay. No ROMoratomiccommit/completioncredit.\n\nRemaining required work:source-bound production menu/control-flow/loaders-census/references/actual/comparison readers andtheir meaningfulnegativecases;onewhole-NDS atomiccommit inbothdirect-current andcanonical.source/full-current.romlifecycles;genuinelywrong-memory zero-commit checks;solebuilderregisteredcumulative release/exactcleanpatch/ownstartup;thenexactlyfiveonce-onlycompletiondecisions. The full editorial goalisnotcomplete."

NEXT = "Continue from verifiedV8671/current registeredV8609. Latest B52 manuscriptv6/namesv4/contractv1 haveallfiveindividualgatestrue. Policyvalidation work/analysis/Hodram_B52_policy_validation_v8664b/policy_validation.json passes243 semanticnegatives;production reconstruction8666 passes26 andnativeproduction8667 passes10. Reusecompletednative/source/stored/actual/format/compiler/reconstruction checkswithoutunchangedreplay. Preserveoriginalfailed8662/8664,correctedsuccessors,partialnamesv3 andeveryearlierartifact. No livejobsremain;fiveB52decisionsstilluncredited.\n\nNext complete independentproduction menu evidence,source-controlled branch/end/caller-result contracts,325wholeloads/650parentmodes/census identity reuse,exactsource/current/final references,existingactualsource/English body-name/menu/normalandflaggedtrace readers andfullcomparison limits. Existingnative menu/backing CPUevidence andactualvisibleRGBareseparate;donotupgradecapturedRGBtoowner/RAM/VRAM/paletteidentity. Originaleffectsemantics/outereventeligibility/location/cancelavailability/futurecausality remainoutsideobservedcoverage. Preservebothlongwithdrawaldivergence andfocusedimmediateagreement. Noretestingofeveryconditionalorfullnaturalplaythroughisrequired.\n\nInspectsupportedbuilderhooksbeforeaddingastage. The existing late_story_editorial_release hookrequiresfixedallocations/equalblockandarchivelengthsandexecutesbeforethelateB51tail,soitcannotdirectlyapplyB52'srelocated228to236blockafterthecompletecurrentprefix. Preferanappropriatesource-lockedreusablelateextensionifimplemented;retainwholeoriginalbuilderinverseandallpredecessordependencyguards. ThencompleteatomicwholeNDScommitinbothlifecyclesandwrong-memory/semanticzero-commitcases,registeredcumulativebuild/exactclean-inputpatch/ownstartup,once-onlyfive-recordcredit. UseownV8609captain1context scripts/Hodram_B51_registered_route_context_v8612.py;nohistoricalRAMoverlay/captain2.\n\nFullcopiedunfinishedinventoryremainsauthoritative:allfourstories/earliertranslateddialogue/sharedtown-shop/random/Help/restprose/all207names-roles-aliases-customnames/retrospectiveearlybreaks. Preservecontraction/questiontag/unscanned558plans/weak-before-row/COMMON750-752/preLF6435/wideractors104/105/113/147/JanusPasar-Pasha/ceramics17wrap/Cristina-Christina/HansRetzel-Letzel/Samwellmiddle/SourceItem-LocalProduct/Alexandria/AksumGoldSeal/Armadillo-SteelHide/HerophilusMedicine/イギリス/AlShin-AlFeridShin/Sailor151-159-versus-Retainer/oldernormal-end/nineteenth-cell/B47/B48/B50metadataleads. EveryROMandearliertranslationpreserved;noseparatepackage,promotion,pruning,commitorpush. Graphics/all18plaquesandlaterolder-recordtechnicalre-auditremainseparate. Counts7229/7232/4487/2742;fullgoalactive."

def parent_at(value, path):
    for key in path[:-1]:
        value = value[key]
    return value, path[-1]

def restore(value):
    result = deepcopy(value)
    for op in reversed(value[KEY]['inverse_operations']):
        parent, key = parent_at(result, op['path'])
        if op['existed']:
            parent[key] = deepcopy(op['before'])
        else:
            parent.pop(key)
    return result

def gates():
    prior=read(PRIOR);data={k:read(p) for k,p in PROOFS.items()}
    assert [prior[k] for k in ['completed','source_prose','revised','retained']]==[7229,7232,4487,2742]
    assert prior['candidate_sha256']==data['release']['candidate_sha256']==data['own_input']['current_ROM_sha256']==data['startup']['candidate_sha256']==data['current']['current_ROM_sha256']
    assert sha(Path(prior['candidate']).read_bytes())==prior['candidate_sha256'] and prior['Hodram_B51_completed_once']
    doc=data['manuscript'];allrows=doc['records']+doc['typed_choice_records']
    assert len(doc['records'])==3 and len(doc['typed_choice_records'])==2 and doc['revised']==2 and doc['retained']==3
    assert all(all(r['review'][k] is True for k in ['source','context','localization','naturalness']) and r['review']['formatting'] is False for r in allrows)
    assert data['gloss']['all3_clean_utterances_andtwo_choices_glossed_before_current_English'] and data['current']['source_first_glosses_andcomplete_native_page_view_precede_current_English']
    assert data['current']['all5_source_units_uncredited_in_current_ledger'] and data['current']['source_dispatches_and20_native_relative_cases_reused_not_replayed']
    control=data['source_controls'];assert len(control['all_original_source_commands'])==14 and len(control['source_relative_cases'])==4 and len(control['distinct_seeded_ends'])==50 and control['normal166_carries_seed_flagged224_clears_seed_andreturns_kind1']
    assert data['source_display']['complete_native_source_page_count']==3 and data['source_view_names']['all_three_complete_Japanese_speech_pages_andone_reused_role_plane_directly_viewed']
    assert data['source_choice_getters']['native_count_cases']==4 and data['source_choice_getters']['native_label_pointer_cases']==8
    assert data['source_VM']['bridged_modal_return_cases']==6 and len(data['source_VM']['structural_response_paths'])==2 and data['source_VM']['reused_original_kind2_value_forwarding_kind3_carry_cases']==50
    assert data['logical']['fresh_native_alignment_cases']==12 and data['pages']['fresh_compiled_alignment_cases']==12 and len(data['pages']['records'])==3
    assert not data['plan']['failures'] and not any(i['severity'] in ['warning','error'] for r in data['plan']['records'] for i in r['base_QA']['issues'])
    assert data['native_review']['reviewed_body_pages']==3 and len(data['native_review']['original_infos'])==1 and data['native_review']['no_qa_waivers']
    assert data['qualified_note']['manuscript_sha256']==sha(Path(PROOFS['manuscript']).read_bytes()) and data['qualified_note']['all_words_compiled_bytes_source_current_refs_individual_review_gates_native_planes_choice_geometry_andactual_scope_unchanged']
    menu=data['menu'];assert menu['even_alignment_provider_cases']==4 and menu['bridged_modal_return_cases']==12 and len(menu['records'])==8
    assert (menu['current_width_px'],menu['reviewed_width_px'])==(84,72) and menu['current_rectangle']==[70,64,186,128] and menu['reviewed_rectangle']==[76,64,180,128]
    assert menu['menu_shape_changes_due_only_to_three_unspoken_storage_spaces_removed'] and data['native_review']['all_five_formatting_gates_false']
    for sheet in [data['source_view_names']['directly_viewed_sheet'],data['native_review']['directly_viewed_speech_sheet'],data['native_review']['directly_viewed_menu_sheet']]:assert sha(Path(sheet['path']).read_bytes())==sheet['sha256']
    assert data['prior_completion_audit']['five_disjoint_new_keys_only'] and data['prior_completion_audit']['four_observed_speeches_Charles_offline_unvisited_preserved']
    review=data['actual_review']
    assert review['total_runs']==6 and review['total_frames']==50406 and review['total_holds']==138 and review['total_page_occurrences']==12
    assert review['exact_focus_schedule_is_unretimed_default_prefix_before4485'] and review['opposition_schedule_only_adds_ordinary_DOWN4100_duration5']
    assert review['long_withdrawal_later_component_actor_calendar_PRNG_and46_RGB_differences_preserved']
    assert review['focused_withdrawal_all5_components_actors_PRNG_and13_RGB_pairs_match']
    assert review['all_five_formatting_gates_still_false_formal_policy_atomic_registered_release_andcredit_pending']
    assert sha(Path(PROOFS['actual_review_manuscript']).read_bytes())==review['manuscript']['sha256']
    assert sha(Path(PROOFS['actual_review_names']).read_bytes())==review['names']['sha256']
    for path,digest in review['evidence'].items():assert sha(Path(path).read_bytes())==digest
    approval=data['format_approval'];latest=data['latest_manuscript']
    assert approval['all5_five_gates_true'] and approval['manuscript_sha256']==sha(Path(PROOFS['latest_manuscript']).read_bytes()) and approval['names_sha256']==sha(Path(PROOFS['latest_names']).read_bytes())
    assert all(all(r['review'].values()) for r in latest['records']+latest['typed_choice_records'])
    assert data['policy']['negative_count']==243 and data['policy']['all_frozen_dependency_guards_remained_enabled']
    assert data['frozen_contract']['contract_sha256']==sha(Path(PROOFS['native_contract']).read_bytes()) and data['frozen_contract']['dependency_count']==471
    for path,digest in data['native_contract']['dependencies'].items():assert sha(Path(path).read_bytes())==digest
    assert len(data['production_reconstruction']['negative_cases'])==26 and data['production_reconstruction']['complete_clean_current_block_andwhole_archive_inverses_pass']
    assert data['production_native']['negative_count']==10 and data['production_native']['positive_native_pages']==6 and data['production_native']['positive_scoped_nameplanes']==1
    return prior,data

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('phase', choices=['stage', 'audit', 'apply', 'verify'])
    mode = parser.parse_args().phase
    prior, data = gates()
    if mode == 'stage':
        assert not ROOT.exists()
        before = LEDGER.read_bytes()
        old = json.loads(before)
        assert sha(before) == prior['ledger_sha256'] and [old[k] for k in COUNTERS] == COUNTS and old['goal_status'] == 'active'
        new, ops = deepcopy(old), []
        def put(path, value):
            parent, key = parent_at(new, path)
            ops.append(dict(path=path, existed=key in parent, before=deepcopy(parent.get(key))))
            parent[key] = deepcopy(value)
        pending=dict(status='five-all-gate-decisions-frozen-policy243-reconstruction26-native10-negativechecks-pass-production-atomic-registered-pending',file_path='/data/SC1.DK4',blocks=[52],records=5,physical_speeches=3,typed_choice_labels=2,proposed_revisions=2,justified_retentions=3,scoped_role_retentions=1,mentioned_name_component_retentions=1,source_commands=14,source_relative_sites=4,source_query_sites=0,source_FE_panels=0,source_selector_values=[113,113,113],manuscript=PROOFS['latest_manuscript'],names=PROOFS['latest_names'],proofs=PROOFS,records_with_exact_source_current_andcompiled_references=deepcopy(data['latest_manuscript']['records']+data['latest_manuscript']['typed_choice_records']),all_four_prose_gates_true=True,all_five_formatting_gates_true=True,fresh_logical_alignment_cases=12,fresh_compiled_alignment_cases=12,complete_native_English_speech_pages=3,complete_current_target_English_menu_styleplanes=8,source_choice_native_getter_counts=4,source_choice_native_labelpointer_cases=8,source_menu_bridged_returns=6,current_target_menu_bridged_returns=12,source_relative_cases=20,current_relative_cases=20,source_distinct_seeded_end_cases=50,original_caller_result_channel_cases_reused=50,source_opaque_pairs=4,automatic_fullwidth_px=216,line_count_infos=1,warnings=0,waivers=0,menu_width_current84_reviewed72=True,actual_visible_menu_geometry_highlight_controller_bothendpaths_verified=True,actual_live_owner_RAM_VRAM_palette_backing_byteidentity_not_claimed=True,actual_B52_emulator_runs=6,actual_B52_frames=50406,actual_complete_holds=138,actual_page_occurrences=12,stored_relocation_andindependent_reconstruction_verified=True,frozen_policy243_rejections_andindependent_reconstruction26_native10_verified=True,remaining_production_readers_atomic_registered_release_andcredit_pending=True,new_source_prose_counter_credit=0,new_credit=0,full_goal_complete=False)
        oldpending = prior['pending_source_batch']
        marker = dict(checkpoint=KEY, prior_unread_andpending_flags_historical_not_deleted=True, new_credit=0)
        put([oldpending, 'superseded_by_contextual_native_speech_menu_checkpoint'], marker)
        put(['latest_checkpoint'], SUMMARY + '\n\n' + NEXT)
        descriptor = old[prior['unfinished_scope']]
        assert sha(Path(descriptor['path']).read_bytes()) == descriptor['sha256']
        inventory = deepcopy(read(descriptor['path']))
        inventory[KEY] = deepcopy(pending)
        inventory['next_focus'] = NEXT
        if oldpending in inventory:
            inventory[oldpending]['superseded_by_contextual_native_speech_menu_checkpoint'] = marker
        ROOT.mkdir(parents=True)
        scope = ROOT / 'unfinished_editorial_scope_inventory.json'
        save(scope, inventory)
        put([SCOPE], dict(path=str(scope), sha256=sha(scope.read_bytes()),
            all_prior_leads_families_history_andfull_four_storyline_objective_preserved=True,
            five_uncredited_contextual_decisions=5, graphics_andlater_older_record_technical_reaudit_separate=True, full_goal_complete=False))
        evidence = {str(p): sha(Path(p).read_bytes()) for p in [PRIOR, scope, Path(__file__), *map(Path, PROOFS.values())]}
        put([KEY], dict(**pending, summary=SUMMARY, next=NEXT, evidence=evidence, goal_turn_classification='progress', all_new_native_jobs_terminal_andreaped=True))
        new[KEY]['inverse_operations'] = deepcopy(ops)
        assert restore(new) == old and [new[k] for k in COUNTERS] == COUNTS
        assert new['completed_editorial_families'] == old['completed_editorial_families'] and new['current_integrated_candidate'] == old['current_integrated_candidate']
        (ROOT / 'ledger.before.json.gz').write_bytes(gzip.compress(before, mtime=0))
        targets = {LEDGER: encode_ledger(new)}
        for name in ['editorial_handoff_current.md', 'translation_progress.md', 'editorial_review_goal.md', 'todo.md', 'known_issues.md']:
            path = Path('docs') / name
            prefix = ('# Current editorial handoff - V8670; V8609 current\n\n' if name == 'editorial_handoff_current.md' else '')
            prefix += '## V8670: B52 five format gates and frozen policy pass; production and registered integration pending\n\n' + SUMMARY + '\n\n' + NEXT + '\n\n'
            targets[path] = prefix.replace('\n', '\r\n').encode('utf-8') + path.read_bytes()
        files = []
        for index, (path, value) in enumerate(targets.items()):
            planned = ROOT / f'{index:02d}.after'
            planned.write_bytes(value)
            if path != LEDGER:
                (ROOT / f'{index:02d}.before.gz').write_bytes(gzip.compress(path.read_bytes(), mtime=0))
            files.append(dict(target=str(path.resolve()), before_sha256=sha(path.read_bytes()), planned=str(planned.resolve()), planned_sha256=sha(value)))
        save(ROOT / 'staged_checkpoint.json', dict(files=files, evidence=evidence, unchanged_counters=COUNTS, new_credit=0, full_goal_complete=False))
        print('V8670 staged: six targets, five uncredited all-five-gate decisions; frozen policy243/reconstruction26/native10 pass. Exact inverse audit next.')
    else:
        plan = read(ROOT / 'staged_checkpoint.json')
        old = json.loads(gzip.decompress((ROOT / 'ledger.before.json.gz').read_bytes()))
        new = read(plan['files'][0]['planned'])
        assert restore(new) == old and [new[k] for k in COUNTERS] == COUNTS and new['completed_editorial_families'] == old['completed_editorial_families']
        assert new['current_integrated_candidate'] == old['current_integrated_candidate'] and new['goal_status'] == 'active' and not new['full_goal_complete']
        for row in plan['files']:
            assert sha(Path(row['planned']).read_bytes()) == row['planned_sha256']
            assert sha(Path(row['target']).read_bytes()) == row['planned_sha256' if mode == 'verify' else 'before_sha256']
        for path, digest in plan['evidence'].items():
            assert sha(Path(path).read_bytes()) == digest
        if mode == 'audit':
            assert not (ROOT / 'preapplication_audit.json').exists()
            for index, row in enumerate(plan['files'][1:], start=1):
                original = gzip.decompress((ROOT / f'{index:02d}.before.gz').read_bytes())
                assert sha(original) == row['before_sha256'] and Path(row['planned']).read_bytes().endswith(original)
            save(ROOT / 'preapplication_audit.json', dict(staged_plan_sha256=sha((ROOT / 'staged_checkpoint.json').read_bytes()),
                every_prior_value_counter_candidate_andfamily_recovers_exactly=True, every_prior_document_preserved_byte_exact=True, new_credit=0))
            print('V8670 inverse audit passes: every prior ledger value, record, counter, candidate and document preserved.')
        elif mode == 'apply':
            assert not (ROOT / 'application_receipt.json').exists()
            assert read(ROOT / 'preapplication_audit.json')['staged_plan_sha256'] == sha((ROOT / 'staged_checkpoint.json').read_bytes())
            for row in plan['files']:
                target, planned = Path(row['target']), Path(row['planned'])
                assert target.is_relative_to(Path.cwd().resolve()) and planned.is_relative_to(ROOT.resolve())
                with target.open('r+b') as stream:
                    stream.write(planned.read_bytes())
                    stream.truncate()
                    stream.flush()
                    os.fsync(stream.fileno())
                assert sha(target.read_bytes()) == row['planned_sha256']
            save(ROOT / 'application_receipt.json', dict(all_six_targets_hash_exact=True, no_ROM_registry_orcompletion_counter_change=True, new_credit=0, full_goal_complete=False))
            print('V8670 applied; V8609 and all completion counters unchanged. Full goal active.')
        else:
            assert read(ROOT / 'application_receipt.json')['all_six_targets_hash_exact'] and not VERIFY.exists()
            verified = deepcopy(prior)
            verified.update(ledger_sha256=sha(LEDGER.read_bytes()), previous_verified_handoff=str(PRIOR), previous_verified_handoff_sha256=sha(PRIOR.read_bytes()),
                next_required=NEXT, unfinished_scope=SCOPE, pending_source_batch=KEY, next_clean_exchange_not_selected=False,
                Hodram_B52_contextual_native_speech_menu_checkpoint=deepcopy(new[KEY]), new_uncredited_source_positions=5,
                physical_speeches_pending=3, typed_choice_labels_pending=2, new_credit=0, new_emulator_runs=0, new_actual_frames=0, new_research_ROMs=0,
                all_new_native_jobs_terminal_andreaped=True, all_prior_roots_families_records_andcounts_recover_exactly=True,
                full_goal_active=True, full_goal_complete=False, producer_sha256=sha(Path(__file__).read_bytes()))
            VERIFY.mkdir(parents=True)
            save(VERIFY / 'verified_handoff.json', verified)
            print('Verified V8671/current V8609: 7229 completed; B52 all-five-gate/policy243/reconstruction26/native10 pass; remaining production/atomic/registered pending. Full objective active.')
