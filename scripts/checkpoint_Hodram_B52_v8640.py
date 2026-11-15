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

ROOT = Path('work/analysis/Hodram_B52_checkpoint_v8640')
VERIFY = Path('work/analysis/editorial_handoff_verification_v8641')
PRIOR = Path('work/analysis/editorial_handoff_verification_v8624/verified_handoff.json')
LEDGER = Path('translations/editorial_review_current_v1.json')
KEY = 'Hodram_SC1B52_contextual_native_speech_menu_review_pending_integration_v8640'
SCOPE = 'unfinished_editorial_scope_v8640'
COUNTERS = ['records_editorially_completed', 'records_with_source_and_prose_pass', 'records_with_source_prose_drafts',
    'records_revised_and_integrated', 'retained_wordings_editorially_completed']
COUNTS = [7229, 7232, 7232, 4487, 2742]
PROOFS = {'clean': 'work/analysis/Hodram_B52_clean_v8616/complete_clean_SC1_B52_EV1_andcoverage_before_current_English.json', 'gloss': 'work/analysis/Hodram_B52_clean_gloss_v8617/three_first_clean_glosses_two_choice_labels_anddistinct_terminal_risks.json', 'source_controls': 'work/analysis/Hodram_B52_source_controls_v8620/source_controls.json', 'source_display': 'work/analysis/Hodram_B52_source_display_v8626/source_display.json', 'source_choice_getters': 'work/analysis/Hodram_B52_choice_source_v8627/source_choice_getters.json', 'source_VM': 'work/analysis/Hodram_B52_source_choice_VM_v8628b/source_menu_provider_andresponse_paths.json', 'source_view_names': 'work/analysis/Hodram_B52_source_names_v8630/three_source_pages_role_andHayreddin_component_review.json', 'current': 'work/analysis/Hodram_B52_current_v8631/current_effective.json', 'prose': 'work/analysis/Hodram_B52_prose_v8632/contextual_review.json', 'manuscript': 'translations/hodram_B52_editorial_manuscript_v3.json', 'names': 'translations/hodram_B52_speaker_name_review_v1.json', 'logical': 'work/analysis/Hodram_B52_logical_v8633/logical_paragraphs.json', 'plan': 'work/analysis/Hodram_B52_layout_v8634/automatic_plans.json', 'pages': 'work/analysis/Hodram_B52_pages_v8635/compiled_native_pages.json', 'menu': 'work/analysis/Hodram_B52_menu_v8636/menu_provider_and_planes.json', 'native_review': 'work/analysis/Hodram_B52_native_review_v8637/native_body_andchoice_review.json', 'qualified_note': 'work/analysis/Hodram_B52_native_note_v8638/qualified_native_review.json', 'release': 'work/analysis/Hodram_B51_release_v8610/registered_release_verification.json', 'own_input': 'work/analysis/current_V8609_Hodram_native_v8612/current_native_input.json', 'startup': 'work/analysis/Hodram_B51_registered_startup_view_v8613/own_registered_startup6_RGBpairs_actor_equal_unchanged_names_direct_view.json', 'prior_completion_audit': 'work/analysis/Hodram_B51_completion_audit_v8625/independent_staged_completion_audit.json'}

SUMMARY = "Current verified registered experimental cumulative ROM remains V8609;mainV4701/canonical baseline andevery ROM,translation,draft,executed producer,proof andfailure remain preserved. Counts stay7,229 completed/7,232 credited source-prose anddrafts/4,487 integrated revisions/2,742 justified retentions;SC1 149/routes5629. B51 five decisions remain credited exactly once. B52 five decisions are reviewed butunintegrated/uncredited:three speeches/two typed choices,two revisions/three individually justified retentions. No new ROM,emulator run,registry layer,promotion,separate requested package,pruning,commit orpush. Full all-four-storyline/earlier-dialogue/shared town-shop/random/Help/remaining prose/all207names-roles-aliases-customnames/retrospective premature-break objective remains active. Graphics/all18plaques andlater older-record technical re-audit stay separate. Roughly20,000candidate remainder is a planning estimate,not an audited prose denominator.\n\nB52 clean-first source8616/three firstglosses-plus-two-choices8617 precede currentEnglish8631. Sourcecontrols8620 bind14commands/three six-byte71preambles/four relative sites20cases/zeroqueries/one2100/fouropaque structural pairs/50endcases andthree event/dependency getters. Normalend166preserves the carried word;flagged224returns kind1/clears it. Source83c2at164 is retained structurally without invented effect semantics. Event52requires30/excludes74;outer eligibility,scheduling,original location andfullchronology remain unexecuted. Numericadjacency doesnot prove continuity withB51.\n\nSource display8626 executes three dispatches/twelve guarded alignments/three complete Japanese pages in ownV8609 captain1 context. Actor113/voice0 andPortWorker fields are bound;two unchanged getters andone complete style11nameplane are reused only through exact complete currentcode/COMMON/font/wholeactors bindings. The three Japanese pages androleplane were directly viewed in8630. Choicegetters8627 freshly bindfour counts/eight labelpointers atboth evenalignments through clean/current code. SourceVM qualified8628b binds two providers/six bridged0/1/cancelreturns,sourcewidths[14,12]/rectangle[70,64,186,128],andtwo structural response paths using exact originalcaller-span/50reused kind2value-forwarding/kind3carry cases. Choice0 reaches withdrawal/end166;choice1 reaches reckless-boldness/end224. Cancel returns kind0 without claiming a followup path. These are offline/synthetic structural arguments,not actual controller oroptional activation coverage. Original failed8628 producer (wrong caller-span field) remains preserved;8628b changes only that schema binding.\n\nCurrent8631 preserves all14source/current commands,fullpreambles/four relative targets/two distinct ends/opaque bytes andboth typed labels. Three current dispatches/twenty current branch cases are fresh;three source dispatches/twenty source cases are explicitly reused fromexactsource/code/owncontext proofs. Five canonical source IDs areR0006/R0011/R0013/R0021/R0033 withzero historical completed overlap;old typed aliases are preserved. Current literalEnglish had no registeredcatalogue replacement. All exact source/current offsets,bytes,NULrecordindices,typedcommand/optionindices andold padding remain.\n\nContextual manuscript latest translations/hodram_B52_editorial_manuscript_v3.json/namesv1 keeps two revisions: Are you planning to make an enemy of Hayreddin's outfit? and You've got a death wish, huh? The first restores a question about intended opposition anduses an informal group noun ratherthan unsupported family implications;actor34source/current surname-component bytes independently bind established Hayreddin. Earlier reviewed clan terminology in the formal company-capability comparison is kept asidentity/context evidence,not a biological-family claim ornew faction spelling. The final full idiomatic comment preserves dangerous boldness andcasualだねえ,not literal suicidal intent,a threat orpromised outcome. Retain Then get out before they notice you.,Not at all.,Bring it on. with individual whole-exchange reasons. PortWorker is retained in this exact gruff warning;source兄貴 doesnot create kinship/rank,andunusedEurope metadata isnot a personal surname. These scoped role/mentioned-component decisions do not complete wider contexts/all207names. All five records have source/context/localization/naturalness true,formatting false.\n\nLogical8633 andcompiled8635 each pass12 fresh progressive alignments,zero source macros andcomplete literal bytes/ABI/unowned4MiB guards. Automaticplan8634 uses original216px width/fontmetrics/guards/pairphase andunaltered QA. Three complete English singlepages pass independent nativeglyph/bounds/consumption/pagination andwere directly viewed. The question wraps afterenemy;its followingofphrase stays together. One original line-count info remains for the retained withdrawal sentence;zero warnings/waivers. No shortening,authoredordinarybreaks/padding,narrowedviewport orfontchange. Preserve stopped layoutpreparer8633's absent spaced-pattern failure;qualified8633b preserves the already completed logical source/proof without replay. Native review8637 makes manuscriptv2;qualified wrapnote8638/manuscriptv3 removes an unnecessary implied capacity explanation while preserving every word,compiledbyte,ref,gate andplane. Originalv1/v2/review are retained.\n\nMenu8636 compiles retained words as32bytes versus36current/sourcebytes,withnativecount2/order/offsets[0,12]. Four current/target evenalignment providers/twelve bridgedreturns andeight complete English style1/style15 planes pass exact currentinstruction/123264payload guards. Removing three unspoken Notatall storage spaces changes widths[14,12]to[11,12],logicalwidth84to72 andrectangle[70,64,186,128]to[76,64,180,128];both reviewed labels are centered. Both current/target caption sheets were directly viewed. This is a concrete changed-menu geometry/backing/highlight/controller/normal-versus-flagged-end transition risk for actual focused tests,not proof of physical in-game display. SourceJapanese choiceglyphs,stored sparse relocation/control/end/inverses,actual representative scenes,formal frozenpolicy/negativecases,independent production readers,atomic registered integration/cleanpatch/ownstartup andonce-only five-record credit remain pending. No B52 actual scene,controller input,natural activation,earned inventory,customname,fullroute,hardware,everyframe causality orfuture simulation claim is added. Retain all earlier B51/B50/B49/Gerhard/Rafael/Hodram/B48 timing/RNG/RGB/component/calendar/followingcommand andfixture-entry limitations."

NEXT = 'Continue from verifiedV8641/current registeredV8609. Counts7229completed/7232source-prose/4487revised/2742retained remain;B51 credited once,B52 five decisions uncredited. Latest B52 manuscriptv3/namesv1 has two revisions/three individual retentions,four prose gates true/allfive formatting gates false. Reuse completed source/gloss/controls8620/sourcepages8626/getters8627/qualifiedVM8628b/source-names-view8630/current8631/prose8632/logical8633/plan8634/compiledpages8635/menu8636/nativeview8637/qualifiednote8638 without unchanged replay. Keep failed originalVM8628,layoutpreparer8633 andall earlier manuscripts/producers/proofs. No jobs remain live from this checkpoint;no new B52 ROM/capture/credit.\n\nNext independently reconstruct one sparse B52 block/archive withthree compiled speech bodies andthe32byte typedchoice object,keeping all14commands/three fullpreambles/four relative mappings/typedcount/order/opaque83c2plusA000sites/both distinct four-byteends/separate tail. Bind exact clean/current/final refs andcanonical choice IDsR0011/R0013,all324unownedSC1blocks/allotherfiles/components/fullROMinverse;do not freeze old offsets or shorten wording tofit. Native source/current proofs use the documented original structures:sourcecontrols flat fields,distinct_seeded_ends contains50cases forends166/224;normal preserves value,flagged clears it/returns1. Retain every six-word result,caller-value channel,ABI/scratch/unowned4MiB/input-outputcanary guard. Independently check original load/cache/index/callers andnative stored dispatch/wrap/pagination/body/name/typedcaption behavior.\n\nFocused actual tests must address the concrete menuwidth84to72/rectangle shift,complete leading/trailing captions,selectionhighlight,normal dismissal/cancel availability ifsupported,andthe two source/English response/end paths. Bind originalJapanese choiceglyphs andcomplete headers/portraits/backing/VRAM/palette/RGB toactual traces without retiming,observer patches orforcing predicates/roster/RNG/flags. Use disclosed initialized whole-script entryfixtures ifnecessary,not a naturalactivation claim;broad practical capture/representative distinct-risk testing isrequired,exhaustive routes/everyconditional-line visits arenot. Keep measured timing/RNG/RGB/component/calendar/followingcommand differences ratherthan claiming broad future equivalence.\n\nUse ownV8609 captain1 helper scripts/Hodram_B51_registered_route_context_v8612.py with work/analysis/current_V8609_Hodram_native_v8612/current_native_input.json. Never overlay historical initializedRAM orborrow captain2. Freeze a source-qualified natural-dialogue-v2 compiler/nativecontract andallindividualgates onlyafter needed native/stored/actual checks. Preserve old profilemetrics/globalQA;test genuinely changed failures withfrozen guards active. Then independentproduction evidence readers,onewholeNDSatomiccommit inbothdirect-current andcanonical.source/full-current.rom lifecycles,wrong-memory/semanticzero-commit checks,andregistered cumulative release/exactcleanpatch/ownstartup. Inspect existing supported/shared hooks beforeadding a stage;prefer a source-locked reusable extension ifsuitable whilepreserving the whole originalbuilder inverse andevery prior dependency. Do not replace frozen original hashes withmutablebuilder fingerprints. Add exactlyfive source/completion decisions onceonly afternecessarychecks;current credit remainszero.\n\nFull copied unfinished inventory remains authoritative:allfourstories/earliertranslateddialogue/shared town-shop/random/Help/restprose/all207propernames-roles-aliases-customnames/retrospective earlybreaks. Preserve contraction/questiontag/unscanned558plans/weak-before-row/COMMON750-752/preLF6435/wideractors104/105/113/147/JanusPasar-Pasha/ceramics17wrap/Cristina-Christina/HansRetzel-Letzel/Samwellmiddle/SourceItem-LocalProduct/Alexandria/AksumGoldSeal/Armadillo-SteelHide/HerophilusMedicine/イギリス/AlShin-AlFeridShin/Sailor151-159-versus-Retainer andoldernormal-end/nineteenth-cell/B47/B48/B50metadata leads. Preserve all ROMs/earliertranslations/drafts/failedreceipts/mainV4701/canonical baseline. No separatepackage,promotion,pruning,commit orpush. Graphics/all18plaques andlaterolder-recordtechnical re-audit stay separate;roughly20,000candidate remainder isonly aplanning estimate. Full goalactive.'

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
        pending=dict(status='five-whole-exchange-prose-decisions-native-speech-andEnglish-menu-reviewed-relocation-stored-actual-policy-registered-pending',file_path='/data/SC1.DK4',blocks=[52],records=5,physical_speeches=3,typed_choice_labels=2,proposed_revisions=2,justified_retentions=3,scoped_role_retentions=1,mentioned_name_component_retentions=1,source_commands=14,source_relative_sites=4,source_query_sites=0,source_FE_panels=0,source_selector_values=[113,113,113],manuscript=PROOFS['manuscript'],names=PROOFS['names'],proofs=PROOFS,records_with_exact_source_current_andcompiled_references=deepcopy(data['manuscript']['records']+data['manuscript']['typed_choice_records']),all_four_prose_gates_true=True,all_five_formatting_gates_true=False,fresh_logical_alignment_cases=12,fresh_compiled_alignment_cases=12,complete_native_English_speech_pages=3,complete_current_target_English_menu_styleplanes=8,source_choice_native_getter_counts=4,source_choice_native_labelpointer_cases=8,source_menu_bridged_returns=6,current_target_menu_bridged_returns=12,source_relative_cases=20,current_relative_cases=20,source_distinct_seeded_end_cases=50,original_caller_result_channel_cases_reused=50,source_opaque_pairs=4,automatic_fullwidth_px=216,line_count_infos=1,warnings=0,waivers=0,menu_width_current84_reviewed72=True,actual_changed_menu_geometry_backing_highlight_controller_bothendpaths_still_pending=True,actual_B52_emulator_runs=0,actual_B52_frames=0,stored_relocation_independent_readers_frozen_policy_atomic_registered_release_andcredit_pending=True,new_source_prose_counter_credit=0,new_credit=0,full_goal_complete=False)
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
            prefix = ('# Current editorial handoff - V8640; V8609 current\n\n' if name == 'editorial_handoff_current.md' else '')
            prefix += '## V8640: B52 five contextual decisions and native speech/menu review; stored/actual/registered work pending\n\n' + SUMMARY + '\n\n' + NEXT + '\n\n'
            targets[path] = prefix.replace('\n', '\r\n').encode('utf-8') + path.read_bytes()
        files = []
        for index, (path, value) in enumerate(targets.items()):
            planned = ROOT / f'{index:02d}.after'
            planned.write_bytes(value)
            if path != LEDGER:
                (ROOT / f'{index:02d}.before.gz').write_bytes(gzip.compress(path.read_bytes(), mtime=0))
            files.append(dict(target=str(path.resolve()), before_sha256=sha(path.read_bytes()), planned=str(planned.resolve()), planned_sha256=sha(value)))
        save(ROOT / 'staged_checkpoint.json', dict(files=files, evidence=evidence, unchanged_counters=COUNTS, new_credit=0, full_goal_complete=False))
        print('V8640 staged: six targets, five uncredited four-prose-gate decisions; native speech/menu reviewed, formatting false. Exact inverse audit next.')
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
            print('V8640 inverse audit passes: every prior ledger value, record, counter, candidate and document preserved.')
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
            print('V8640 applied; V8609 and all completion counters unchanged. Full goal active.')
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
            print('Verified V8641/current V8609: 7229 completed; B52 two revisions/three retentions/four prose gates/native speeches/menu reviewed; relocation/stored/actual/policy/registered pending. Full objective active.')
