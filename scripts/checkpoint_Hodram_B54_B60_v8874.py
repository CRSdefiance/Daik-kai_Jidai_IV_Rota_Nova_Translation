"""Additive verified handoff:82 five-gate decisions,14 captures;production/release pending."""
import json,sys
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/Hodram_B54_B60_checkpoint_v8874')
LEDGER=Path('translations/editorial_review_current_v1.json')
KEY='Hodram_SC1B54_B60_82_atomic_shared_registered_build_live_next224_inventory44_meanings_v8874'
SCOPE='unfinished_editorial_scope_v8874'
DOC=Path('translations/hodram_B54_B60_editorial_manuscript_v4.json')
NAMES=Path('translations/hodram_B54_B60_speaker_name_review_v2.json')
FORMAT=Path('work/analysis/Hodram_B54_B60_format_v8826/formatting_approval.json')
REVIEW=Path('work/analysis/Hodram_B54_B60_actual_review_v8825/qualified_actual_review.json')
EVIDENCE=[str(DOC),str(NAMES),str(FORMAT),str(REVIEW),
 'work/analysis/Hodram_B54_B60_compiled_v8808/compiled_body_bindings.json',
 'work/analysis/Hodram_B54_B60_relocation_v8809/reconstruction.json',
 'work/analysis/Hodram_B54_B60_independent_v8810/independent_reconstruction.json',
 'work/analysis/Hodram_B54_B60_stored_v8811/stored_pages_controls_andreferences.json',
 'work/analysis/Hodram_B54_B60_reference_v8812/research_image_receipt.json',
 'work/analysis/Hodram_B54_B60_loaders_v8813/325_loads14fresh636reused_parent_modes.json',
 'work/analysis/Hodram_B54_B60_references_v8814/references.json',
 'work/analysis/Hodram_B54_B60_fixtures_v8815/twelve_whole_scripts.json',
 'work/analysis/Hodram_B54_B60_models_v8817/native_models.json',
 'work/analysis/Hodram_B56_FE_binding_v8819b/two_original_FE_paint_snapshots_six_exact_bitmap_palette_RGB_holds.json',
 'work/analysis/Hodram_B54_B60_comparison_v8821/paired_selected_path_comparison.json',
 'work/analysis/Hodram_B60_focus_actual_v8823/B60/paired_actual_dialogue_headers_flow_returns.json',
 'work/analysis/Hodram_B60_focus_comparison_v8824/paired_selected_path_comparison.json',
]
TEXT="V8874 continues from verified V8861. All 82 Hodram SC1 B54-B60 decisions have passed production, atomic and shared integration checks. Both direct-current and canonical-source/full-current-memory lifecycles produced value-equal reports, exactly one final whole-NDS commit and the complete reviewed reference image. Three wrong-memory inputs, four genuine semantic changes and the shared late-target mismatch were rejected with zero commits and unchanged original objects. The four semantic injections bypassed only the outer digest layer; frozen native, editorial and semantic guards remained active. All nine production groups and 886 changed-input rejections remain passed. No gameplay or native source/display/capture producer was replayed.\n\nFinal release configuration v2 preserves all 3,562 sealed dependency entries and adds 11 integration dependencies, for 3,573 total. It retains every frozen batch and complete prior B31/B53 release dependency. Registered experimental profile all-routes-unified-v8865 appends the new extension after the complete V8778 prefix, including unchanged B52 and B31/B53 extensions. Every prior profile, all 114 accepted layers, Main V4701, canonical baseline and every builder byte remain unchanged. The registration preserves a complete registry inverse. Expected manifest: 648 batches, 18 release checks and 110 regressions. All 110 pytest regressions passed.\n\nThe registered builder is live under exec session 29114, producer PID 62552 and child PID 55424, confirmed by authoritative process observation in work/analysis/Hodram_B54_B60_build_observation_v8874/authoritative_process_observation.json. Quiet buffered output is not a failure. Re-poll this exact handle or current process/terminal state; do not restart solely because an observation times out or the log is quiet. The current verified cumulative ROM remains V8778. V8865 build completion, manifest/whole-reference verification, exact clean-input patch reconstruction and its own startup/direct view remain pending. Prepared release verifier8866, capture8867, current-context binding8868 and startup review8869 retain the original guards. Completion8870/auditor8871 are prepared, not applied. The auditor preparer's numeric-leading receipt identifiers caused a preserved SyntaxError; qualified8871b corrects only metadata names and retains original source-lock guards. A later qualified completion successor must use this V8874 ledger/handoff as its prior state.\n\nClean source inventory8872 adds 224 uncredited candidate speeches from complete SC1 B61-B70 blocks, with complete commands, preambles and EV1 metadata, no typed menu and zero completed overlap. Exact B65 clean context is associated with its earlier source-only inventory, without duplicate credit. First-meaning packet8873 covers all 44 speeches in complete B61/B62 exchanges before consulting existing English. All 68 clean B142 context speeches were read for the callback. B61 distinguishes the uncomprehended question about destruction of Sera's country from her later confirmation of soldiers attacking her home. B62 preserves vocabulary clarification, an unfinished thought about her town, conditional permission to stay and specific cooking praise. Her recollection of Hodram's earlier objection about a civilian woman aboard does not become a universal historical naval rule. Preserve respectful language learning, unnamed language, source uncertainty and no invented romance or family bond. The other 180 candidate speeches are not glossed. New source/native/name/macro/context/localization/formatting/gameplay/release gates remain pending; these notes add no source-prose or completion credit.\n\nCounts remain 7,237 completed / 7,240 credited source-prose and drafts / 4,492 integrated revisions / 2,745 retentions. The pending 82 decisions comprise 46 revisions and 36 justified retentions. Existing evidence remains 14 initialized saved runs, 130,014 frames, 676 complete holds, 150 page occurrences, 63 unique observed utterances and 19 offline-only utterances. Preserve every main/focused timing, decoded-length, RNG, RGB, following-command and long B60 actor difference. Focused7001 equality is bounded; RNG and all11 later RGBpairs still differ. No immediate-return mainRAM, causal diagnosis, future-equivalence, natural activation, earned chronology, fullroute or hardware claim. Ten progressive names remain scoped; all207/fullcatalogue/customnames, wider role contexts and Geronimo/Alonso sharedデ full-name ownership/deployment/consumers remain open. Preserve Rafael, Hodram, Joakim, Maria and Camille.\n\nNext: finish this exact registered build without replay, run release/patch verification and own startup, view the new startup sheet, then independently stage/audit/apply once-only 82-record completion. Current completion counters must not increase before those gates pass. Continue the full four-storyline, earlier translated dialogue, shared town/shop, random scenes, Help/remaining prose, speaker-name and retrospective premature-break objective. Every previous unfinished-scope key/value/lead and document byte is preserved. Preserve every ROM, translation, draft, producer, proof and failure. Graphics/all18 plaques and the later older-record technical re-audit remain separate. Roughly20,000 remaining is a planning estimate, not an audited denominator. No promotion, separate user package, pruning, commit or push. The full goal remains active and incomplete.\n"

PRODUCTION={'policy': 'work/analysis/Hodram_B54_B60_policy_validation_v8831b/policy_validation.json', 'reconstruction': 'work/analysis/Hodram_B54_B60_reconstruction_validation_v8833/independent_reconstruction_validation.json', 'references': 'work/analysis/Hodram_B54_B60_reference_validation_v8836/independent_reference_validation.json', 'native': 'work/analysis/Hodram_B54_B60_native_validation_v8838/independent_native_validation.json', 'controls': 'work/analysis/Hodram_B54_B60_controls_validation_v8840/independent_controls_validation.json', 'loaders': 'work/analysis/Hodram_B54_B60_loader_validation_v8842/independent_loader_validation.json'}
EVIDENCE += list(PRODUCTION.values()) + ['translations/hodram_B54_B60_native_contract_v1.json','work/analysis/Hodram_B54_B60_metadata_v8829/explicit_route_binding.json','work/analysis/Hodram_B54_B60_policy_count_v8834/terminal_failure_and_count_qualification.json','work/analysis/Hodram_B54_B60_native_tools_v8837b/source_locked_native_evidence.json']

PRODUCTION.update({'actual': 'work/analysis/Hodram_B54_B60_actual_validation_v8847/independent_actual_validation.json', 'comparison': 'work/analysis/Hodram_B54_B60_comparison_validation_v8849/independent_comparison_validation.json', 'FE_actual': 'work/analysis/Hodram_B56_FE_production_validation_v8851b/independent_FE_actual_validation.json'})
EVIDENCE += list(PRODUCTION.values()) + ['translations/hodram_B54_B60_editorial_release_v1.json','work/analysis/Hodram_B54_B60_release_seal_v8855/reference_seal.json','work/analysis/Hodram_B54_B60_release_seal_v8855/configuration_receipt.json','work/analysis/Hodram_B54_B60_wrong_memory_v8858/wrong_memory_rejections.json','work/analysis/Hodram_B56_FE_JSON_qualification_v8852/JSON_tuple_array_qualification.json']

EVIDENCE += ['translations/hodram_B54_B60_editorial_release_v2.json', 'work/analysis/Hodram_B54_B60_integration_binding_v8863/integration_binding.json', 'work/analysis/Hodram_B54_B60_registration_v8864/registration_receipt.json', 'work/analysis/Hodram_B54_B60_atomic_positive_v8857/atomic_positive.json', 'work/analysis/Hodram_B54_B60_atomic_challenges_v8859/semantic_rejections.json', 'work/analysis/Hodram_B54_B60_shared_extension_v8860/shared_extension_validation.json', 'work/analysis/Hodram_B54_B60_regressions_v8865/terminal.json', 'work/analysis/Hodram_B54_B60_build_v8865/build_plan.json', 'work/analysis/Hodram_B54_B60_build_observation_v8874/authoritative_process_observation.json', 'work/analysis/Hodram_next_clean_v8872/complete_clean_SC1_B61_B70_EV1_andcoverage_before_current_English.json', 'work/analysis/Hodram_B61_B62_clean_gloss_v8873/44_first_meanings_with_country_question_vocabulary_andnaval_callback_context.json', 'work/analysis/Hodram_B54_B60_completion_audit_syntax_v8871b/preserved_syntax_failure_andqualified_preparer.json']

if __name__=='__main__':
    mode=sys.argv[1]
    if mode=='stage':
        assert not ROOT.exists();old=read(LEDGER);doc,names,approval,review=map(read,[DOC,NAMES,FORMAT,REVIEW])
        assert old['records_editorially_completed']==7237 and old['goal_status']=='active' and not old['full_goal_complete'] and KEY not in old and SCOPE not in old
        assert approval['all82_five_gates_true'] and approval['standard_natural_dialogue_v2_validation_pass'] and len(names['records'])==10
        assert (review['total_runs'],review['total_frames'],review['total_holds'])==(14,130014,676)
        ROOT.mkdir(parents=True);(ROOT/'ledger_before.json').write_bytes(LEDGER.read_bytes())
        pending=dict(status='82-fivegate-allproduction-atomic-shared-semantic-pass-registered-build-live-uncredited',production_proofs=PRODUCTION,production_negative_count=886,previous_goal_turn_progress_verified_by_V8862=True,
            manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),names=str(NAMES),names_sha256=sha(NAMES.read_bytes()),formatting=str(FORMAT),formatting_sha256=sha(FORMAT.read_bytes()),
            actual_review=str(REVIEW),actual_review_sha256=sha(REVIEW.read_bytes()),records=[{k:r[k] for k in ['id','file_path','block','source_record_index','source_reference','source_hex','current_reference','current_hex','final_reference','final_hex','english','compiled_hex','decision','finding','localization_note','retention_reason','review','actual_observation_status','formatting_approval_reason']} for r in doc['records']],
            total=82,revisions=46,retentions=36,actual_unique=63,offline_only=19,actual_runs=14,actual_frames=130014,actual_holds=676,
            supersedes_only_pending_state_of='Hodram_SC1B54_B60_82_allnine_production_groups_sealed_pending_atomic_registered_v8861',
            all_long_andfocused_scope_limits_preserved=True,Geronimo_Alonso_shared_de_fullname_lead_open=True,
            new_credit=0,new_registered_ROM=False,research_ROMs_preserved=13,full_goal_complete=False,
            evidence={p:sha(Path(p).read_bytes()) for p in EVIDENCE})
        new=deepcopy(old);new['latest_checkpoint']=TEXT;new[KEY]=pending
        scope_before=Path(old['unfinished_editorial_scope_v8861']['path']);scope=read(scope_before);(ROOT/'scope_before.json').write_bytes(scope_before.read_bytes())
        scope[KEY]=deepcopy(pending);save(ROOT/'unfinished_editorial_scope_inventory.json',scope)
        new[SCOPE]=dict(path=str(ROOT/'unfinished_editorial_scope_inventory.json'),sha256=sha((ROOT/'unfinished_editorial_scope_inventory.json').read_bytes()),all_prior_leads_families_history_andfull_four_storyline_objective_preserved=True,new_completion_credit=0,full_goal_complete=False)
        new['research_checkpoints'].append(dict(id='V8874-Hodram-B54-B60-atomic-shared-pass-registered-build-live-next224-first44',documentation='docs/editorial_Hodram_B54_B60_v8874.md',manuscript=str(DOC),
            actual_review=str(REVIEW),new_editorially_completed=0,new_registered_ROM=False,research_ROMs=13,actual_runs=14,actual_frames=130014))
        save(ROOT/'ledger_staged.json',new);changes=[]
        for path,header in [('docs/editorial_handoff_current.md','# Current editorial handoff - V8874; V8778 current\n\n## B54-B60:atomic/shared pass;registered build live;next224 clean candidates/first44 meanings\n\n'),('docs/known_issues.md','## V8874: Hodram B54-B60 stored/actual/format checkpoint\n\n'),('docs/todo.md','## V8874 active editorial continuation\n\n')]:
            p=Path(path);before=p.read_bytes();backup=ROOT/(p.name+'.before');backup.write_bytes(before);staged=ROOT/(p.name+'.staged');prefix=(header+TEXT+'\n').encode('utf-8');staged.write_bytes(prefix+before)
            changes.append(dict(path=path,before=str(backup),before_sha256=sha(before),staged=str(staged),staged_sha256=sha(staged.read_bytes()),prefix_bytes=len(prefix)))
        checkpoint=ROOT/'editorial_Hodram_B54_B60_v8874.md';checkpoint.write_text('# Hodram B54-B60 stored andactual checkpoint V8874\n\n'+TEXT,encoding='utf-8')
        protected=[Path('translations/release_stack.json'),Path('scripts/build_integrated_release.py'),Path(old['current_integrated_candidate']['path']),Path(old['current_integrated_candidate']['patch']),Path('out/raphael_natural_v2_accepted_base.nds'),Path('work/clean.nds'),Path('translations/rom_retention_pins.json')]
        save(ROOT/'stage_manifest.json',dict(ledger_before_sha256=sha(LEDGER.read_bytes()),ledger_staged_sha256=sha((ROOT/'ledger_staged.json').read_bytes()),scope_before_path=str(scope_before),scope_before_sha256=sha(scope_before.read_bytes()),
            documents=changes,checkpoint_doc=str(checkpoint),checkpoint_doc_sha256=sha(checkpoint.read_bytes()),protected_files={str(p):sha(p.read_bytes()) for p in protected},evidence=pending['evidence'],
            previous_goal_turn_was_progress_verified_by_V8862_andnew_atomic_shared_registration_source_meaning_work_completed=True,new_credit=0,full_goal_complete=False))
        print('Staged V8874:82fivegate reviews/14actualruns;all counts andregistered artifacts unchanged.Independent audit required.')
    elif mode=='apply':
        m=read(ROOT/'stage_manifest.json');a=read(ROOT/'independent_staged_audit.json');assert a['pass'] and a['stage_manifest_sha256']==sha((ROOT/'stage_manifest.json').read_bytes())
        assert sha(LEDGER.read_bytes())==m['ledger_before_sha256']
        for r in m['documents']:assert sha(Path(r['path']).read_bytes())==r['before_sha256'] and sha(Path(r['staged']).read_bytes())==r['staged_sha256']
        for p,h in {**m['protected_files'],**m['evidence']}.items():assert sha(Path(p).read_bytes())==h
        checkpoint=Path('docs/editorial_Hodram_B54_B60_v8874.md');assert not checkpoint.exists()
        LEDGER.write_bytes((ROOT/'ledger_staged.json').read_bytes())
        for r in m['documents']:Path(r['path']).write_bytes(Path(r['staged']).read_bytes())
        checkpoint.write_bytes(Path(m['checkpoint_doc']).read_bytes())
        save(ROOT/'applied.json',dict(ledger_sha256=sha(LEDGER.read_bytes()),stage_manifest_sha256=sha((ROOT/'stage_manifest.json').read_bytes()),new_credit=0,full_goal_complete=False));print('Applied audited checkpoint;verification required.')
    else:raise ValueError(mode)
