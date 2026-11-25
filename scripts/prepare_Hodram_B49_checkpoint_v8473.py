"""Preserve full objective andindependent/atomic progress plus exact failed-registration recovery state."""
from pathlib import Path
from scripts import prepare_Hodram_B49_checkpoint_v8429 as previous
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

PROOFS={**previous.PROOFS,
 'independent_native':'work/analysis/Hodram_B49_independent_native_v8433/independent_native_models.json',
 'independent_actual':'work/analysis/Hodram_B49_independent_actual_v8434b/independent_actual.json',
 'independent_FE':'work/analysis/Hodram_B49_independent_FE_v8436/independent_FE.json',
 'independent_menu':'work/analysis/Hodram_B49_independent_menu_v8437/independent_menu.json',
 'independent_comparison':'work/analysis/Hodram_B49_independent_compare_v8439/independent_comparison.json',
 'independent_controls':'work/analysis/Hodram_B49_independent_controls_v8441b/independent_controls.json',
 'independent_references':'work/analysis/Hodram_B49_independent_refs_v8443/independent_references.json',
 'predecessor_binding':'work/analysis/Hodram_B49_predecessor_binding_v8454/semantic_binding.json',
 'builder_guard':'work/analysis/Hodram_B49_builder_v8452/exact_builder_inverse_cases.json',
 'production_seal':'work/analysis/Hodram_B49_release_seal_v8448/reference_seal.json',
 'compiler_API_fix':'work/analysis/Hodram_B49_atomic_fix_v8450/source_equivalence.json',
 'production_configuration':'translations/hodram_B49_editorial_release_v3.json',
 'atomic_positive_before_pin_fix':'work/analysis/Hodram_B49_atomic_positive_v8456/atomic_positive.json',
 'atomic_positive':'work/analysis/Hodram_B49_atomic_positive_v8465/atomic_positive.json',
 'atomic_semantic_cases':'work/analysis/Hodram_B49_atomic_challenges_v8457/semantic_rejections.json',
 'builder_pin_fix':'work/analysis/Hodram_B49_builder_pin_fix_v8464/pin_correction.json',
 'pin_semantic_binding':'work/analysis/Hodram_B49_pin_semantics_v8465b/semantic_binding.json',
 'failed_registration':'work/analysis/Hodram_B49_registration_v8458/failed_registration_terminal.json',
}

SUMMARY="""Registered cumulative V8377 remains the current verified ROM. Main V4701 and the canonical baseline remain unchanged. Counts stay at 7205 completed, 7208 credited source-prose/drafts, 4474 integrated revisions and 2731 justified retentions; SC0 368, SC1 125, SC2 4915, SC3 197, COMMON 1600 completed/1603 source-prose, route subset 5605. B49 has sixteen approved but uncredited decisions: fourteen speeches and two canonical typed choices, seven revisions and nine justified retentions. Preserve every ROM, translation, draft, executed producer, proof and failed attempt. The full editorial goal remains active.

Independent production readers now pass for all B49 evidence: 28 complete source/stored native pages and both nameplates; six captured groups, 34 page occurrences and 200 complete body/name-or-absent-FE-header holds; four actual menus/twelve owned backing samples/twenty-four visible labels and both selected highlights/results; two original FE paint snapshots/four exact bitmap, palette, VRAM and RGB holds. All 231 later framebuffer pairs are recomputed, retaining all five visible differences, seven command-duration differences and every measured script-boundary/final PRNG, component, actor, raw-calendar and following-command limit. Controls independently execute fourteen dispatches/one null FE/eight relative sites40cases/one raw query/four picture-hide boundaries/25 value-carry ends/two EV1 getters/seven paired opaque structural decodes. All sixteen clean/current/final references, 36 commands, fourteen full preambles, typed menu, full terminal/tails, both clean/current block inverses, whole archive and whole in-memory ROM inverse, 324 unowned blocks and every other file/component bind exactly. All325 load/cache cases,650 parent modes,326 actions and shipped callers are independently bound. Canonical.source with complete V8377.rom also passes. No emulator captures were replayed and no new ROM was written in this checkpoint work.

The B49 atomic stage is hodram_B49_editorial_v2 with explicit release configuration translations/hodram_B49_editorial_release_v3.json. Its complete positive8465 passes every gate, commits exactly one whole NDS object after validation, preserves the original object/files/components/serialized bytes until commit, and produces the exact approved8403 research reference with sixteen manifest IDs. Fourteen actual-changing semantic challenges8457 reject at their expected guards with zero commits and whole input preservation; only the production dependency digest layer was bypassed to reach semantics, while all frozen/native/source gates stayed active. Binding8465b proves those same semantic predicates still apply after the one dependency correction and adds three fresh wrong-memory lifecycle rejections with every guard enabled. The fourteen cases are reused through exact module/config equivalence, not claimed as rerun. All445 B49 frozen entries remain active.

Preserve both stopped attempts. Atomicv1/8449 supplied plain english where the existing compiler requires approved planned_English_markup with its source speaker marker. Source-locked v2 changes only that API field and explicit guard/path namespaces; no approved prose, source/current/final references, native values, layout, QA or independent evidence changed. The registered builder remains the exact planned compatible Hodram-outcomesv5 stage followed by B49v2 before literal-percent safety. The preceding six-record stage still produces byte-exact V8377, with all515 earlier production entries/524 current entries retained; prior50 semantic/four alias challenges are bound by exact source equivalence. Five exact builder forms/sixteen changed builders and preserved older forms pass; full removal of the two owned stages recovers the original417-source builder.

Registration8458 appended experimental profile all-routes-unified-v8459 and wrote the exact planned builder, but its post-registration dependency check stopped before any ROM build. There is no V8459 ROM, manifest, clean patch, release receipt or completion credit. The new config had accidentally collected the mutable complete builder SHA during imported-module discovery. Preserve failed profile8459, its planned registry, backups and failed_registration_terminal.json. Configv3/repair8464 changes exactly that one dependency predicate to the already tested original-source inverse SHA 3becddbd3fb7f5da7ba68b7fde34532aa6e26eed911cc111df0c2a9912804d15, adds the exact old config file as an immutable dependency, and preserves all other entries and metadata. No frozen, native, source or semantic guard is removed. Current configv3 passes with the actual builder;8465 full positive and8465b lifecycle tests verify this recovery. The production module's default configv2 remains historical: pass configv3 explicitly. Do not rerun registration8458 or overwrite executed sources. A fresh successor profile must preserve the failed8459 profile and all old registry values.

All B49 prose, names, five per-record gates, full216px automatic wrapping, two source-qualified ellipses, balanced New World directions, seven source line-count infos and zero warnings/waivers remain unchanged. B49 actual evidence still totals69868frames/eight disclosed initialized whole-script, bounded possession-tail and focusedFE runs. It does not prove natural optional activation, original location, earned inventory/trade eligibility, custom names, full routes, hardware, every-frame causality, future random outcomes or broad simulation. Graphics/all18 plaques and the later older-record technical re-audit remain separate."""

_a=previous.SUMMARY.index('TotalB49actual coverage')
_b=previous.SUMMARY.index('The unchanged standard policy',_a)
SUMMARY+='\n\n'+previous.SUMMARY[_a:_b].strip()
NEXT="""Continue from verifiedV8474/currentregisteredV8377. Use manuscriptv4/namesv2/frozencontractv2, independent readers8433/8434b/8436/8437/8439/8441b/8443, seal8448, atomicmodulev2 with EXPLICIT configuration translations/hodram_B49_editorial_release_v3.json, whole-positive8465 andsemantic/lifecycle binding8465b. Reuse all completed source/prose/layout/native/stored/controls/loaders/callers/actual/menu/FE/comparison/policy/atomic proofs; no unchanged capture or semantic replay is needed. All sixteen decisions remain outside completion/source-prose counters until required registered release checks pass.

Author a fresh successor registration/profile after the complete V8377 stack, preserving failed experimentalV8459 and every earlier registry value. The live builder already contains exactly compatible hodram_outcomes_editorial_v5 then hodram_B49_editorial_v2 before literal-percent safety; do not duplicate either stage or rerun8458. Its exact builder image is work/analysis/Hodram_B49_builder_v8452/planned_builder.bin; preserve both source inverses and full original417 hash. New profile must select hodram_outcomes_editorial_release_v5.json plus explicit hodram_B49_editorial_release_v3.json. Source-lock any successor producers and preserve unexecuted build8459/release8460/startup8461-8463 preparations as earlier artifacts. Expected successor manifest643batches/114accepted/18checks110regressions, unchanged main4701/canonicalbaseline. Bind prior14 semantic tests to8465b rather than repeating them, plus838 policy rejections andthe new3 all-guard lifecycle failures. Build through the sole integrated builder, verify full tested-reference equality, exact clean-input patch, own registered coldboot/startup/native context andall unowned preservation. Only then credit16 once:projected7221completed/7224source-prose/4481revised/2740retained/SC1141/routesubset5621,subjecttofinal arithmetic. No separate user package,promotion,pruning,commit orpush.

Keep the full all-four-story, earlier translated dialogue, shared town/shop/random, Help/remaining prose, all207 names/roles/aliases/custom-name and retrospective premature-wrap objective. Preserve every earlier lead/family/history and actual timing/RNG/component/calendar/RGB/fixture-entry limit in the copied scope inventory. Select the next clean-Japanese whole exchange only after this integration;B50 has not received a new clean-first editorial pass in this checkpoint. Keep graphics andlater older-record technical re-audit separate.

"""+previous.NEXT.rsplit('\n\n',1)[-1]

GATES=previous.GATES.replace('    return prior,data', '''    from dk4tool.patch import hodram_B49_editorial_v2 as owned
    from dk4tool.patch.hodram_outcomes_builder_guard_v5 import BUILDER,validate_builder_bytes
    assert data['independent_native']['independent_native_summary']['native_body_pages_recomputed']==28
    assert data['independent_actual']['actual_summary']['complete_actual_holds']==200 and data['independent_actual']['actual_summary']['unique_speech_IDs']==14
    assert data['independent_menu']['result']['actual_owned_backing_samples_recomputed']==12 and data['independent_menu']['result']['complete_visible_label_samples_recomputed']==24
    assert data['independent_FE']['result']['complete_actual_VRAM_bitmap_palette_RGB_holds_recomputed']==4
    assert data['independent_comparison']['result']['later_full_RGB_pairs_recomputed']==231
    assert data['independent_controls']['result']['native_relative_cases']==40 and data['independent_controls']['result']['normal_seeded_ends']==25
    assert data['independent_references']['canonical_source_withfull_current_ROM_positive'] and data['independent_references']['references']['whole_reference_ROM_equal']
    positive=data['atomic_positive'];assert positive['one_complete_NDS_commit'] and positive['original_object_still_exact_after_commit'] and positive['canonical_source_path_withcomplete_V8377_memory'] and len(positive['report']['changed_records'])==16
    negative=data['atomic_semantic_cases'];assert negative['negative_count']==14 and negative['all_changed_inputs_distinct_andexpected_semantic_guards_match'] and all(c['rejected'] and c['commit_calls']==0 for c in negative['cases'])
    assert data['pin_semantic_binding']['new_lifecycle_rejection_count']==3 and data['pin_semantic_binding']['all_current_protected_files_hash_exact'] and data['pin_semantic_binding']['prior14_semantic_cases_reused_not_rerun']
    assert data['builder_pin_fix']['only_one_dependency_predicate_corrected_all_other_prior_entries_exact'] and data['failed_registration']['terminal'] and data['failed_registration']['returncode']==1
    assert not Path('out/all_routes_combined_v8459_candidate.nds').exists() and not Path('work/analysis/Hodram_B49_registration_v8458/registration_receipt.json').exists()
    assert read('translations/release_stack.json')==read('work/analysis/Hodram_B49_registration_v8458/release_stack.planned.json')
    assert BUILDER.read_bytes()==Path('work/analysis/Hodram_B49_builder_v8452/planned_builder.bin').read_bytes()
    assert validate_builder_bytes(BUILDER.read_bytes(),data['builder_guard']['full_original_source_inverse_sha256'])['corrected_B49_stage_version']==2
    owned.check_dependencies(data['production_configuration'])
    return prior,data''')

if __name__=='__main__':
    root=Path('work/analysis/Hodram_B49_checkpoint_tools_v8473');assert not root.exists();path=Path('scripts/checkpoint_Hodram_B49_v8429.py');source=path.read_text('utf8')
    a=source.index('PROOFS=');b=source.index('\ndef restore');c=source.index('def gates():');d=source.index("if __name__=='__main__':",c);p=source.index('        pending=dict(');q=source.index('        oldpending=',p)
    pending="""        pending=dict(status='B49-all16-fivegates-independent-native-actual-menu-FE-comparison-controls-loaders-whole-atomic-pass-pending-successor-registered-release-after-preserved-V8459-registration-failure',file_path='/data/SC1.DK4',blocks=[49],records=16,physical_speeches=14,typed_choice_labels=2,proposed_revisions=7,justified_retentions=9,manuscript=PROOFS['manuscript'],names=PROOFS['names'],proofs=PROOFS,all_sixteen_five_gates_true=True,exact_source_current_final_references_complete=True,automatic_body_pages=14,source_bound_ellipsis_forms=2,source_macro_counts=dict(FI=0,FA=0,FO=0),line_count_infos=7,warnings=0,waivers=0,relative_sites=8,relocated_relative_cases=40,normal_end_value_carry_cases=25,native_whole_load_cache_paths=325,parent_entry_modes=650,total_actual_frames=69868,actual_emulator_runs=8,complete_actual_holds=200,actual_menu_samples=12,actual_visible_label_samples=24,all_actual_limits_retained=True,policy_changed_input_rejections=838,frozen_dependencies=445,all_independent_production_readers_pass=True,whole_atomic_positive_pass=True,semantic_precommit_rejections=14,semantic_cases_reused_after_one_dependency_correction=True,all_guards_enabled_lifecycle_rejections=3,production_configuration=PROOFS['production_configuration'],explicit_configuration_required=True,preserved_failed_registration_profile='all-routes-unified-v8459',failed_registration_before_any_ROM=True,new_credit=0,full_goal_complete=False)
"""
    result=derive(path,'scripts/checkpoint_Hodram_B49_v8473.py',{
        source[a:b]:'PROOFS='+repr(PROOFS)+'\nSUMMARY='+repr(SUMMARY)+'\nNEXT='+repr(NEXT)+'\n',source[c:d]:GATES,source[p:q]:pending,
        'Hodram_B49_checkpoint_v8429':'Hodram_B49_checkpoint_v8473','editorial_handoff_verification_v8430':'editorial_handoff_verification_v8474','editorial_handoff_verification_v8414':'editorial_handoff_verification_v8430',
        'Hodram_SC1B49_all16_format_policy838_pending_independent_atomic_registered_v8429':'Hodram_SC1B49_independent_atomic_pass_pending_successor_registered_v8473','unfinished_editorial_scope_v8429':'unfinished_editorial_scope_v8473',
        'superseded_by_format_policy_checkpoint':'superseded_by_independent_atomic_checkpoint','Hodram_B49_format_policy_checkpoint':'Hodram_B49_independent_atomic_checkpoint',
        'B49 all16fivegates/nativeactual69868frames/policy838 pass;production next':'B49 independent readers andwhole atomic pass;successor registered release next',
        'new_emulator_runs=6,new_actual_frames=49866,new_research_ROMs=2':'new_emulator_runs=0,new_actual_frames=0,new_research_ROMs=0',
        'B49all16fivegates/838policyrejections/69868actualframes;independentproduction_atomic_registered integration pending.':'B49all16fivegates/independentreaders/14semanticrejections/wholeatomicpass;successor registered integration pending.',
        'V8429':'V8473','V8430':'V8474',
    })
    root.mkdir(parents=True);save(root/'derivation.json',dict(derivation=result,all_prior_scope_leads_families_history_records_counts_currentverifiedROM_andfullobjective_preserved=True,all_native_high_integer_constants_andmultiplicity_preserved=True,no_new_ROM_orcapture_bycheckpoint=True,goal_turn_classification='progress',new_credit=0,full_goal_complete=False))
