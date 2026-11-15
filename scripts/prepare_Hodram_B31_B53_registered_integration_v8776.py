"""Prepare additive dependency binding and registration; preserve the unchanged shared builder."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/Hodram_B31_B53_integration_tools_v8776');assert not root.exists()
    binding=derive('scripts/bind_Hodram_B52_integration_v8699.py','scripts/bind_Hodram_B31_B53_integration_v8776.py',{
        'hodram_B52_editorial_v2':'hodram_B31_B53_editorial_v2',
        'Hodram_B52_release_paths_v8693':'Hodram_B31_B53_release_paths_v8767',
        'Hodram_B52_integration_binding_v8699':'Hodram_B31_B53_integration_binding_v8776',
        "FINAL=Path('translations/hodram_B52_editorial_release_v3.json')":"FINAL=Path('translations/hodram_B31_B53_editorial_release_v2.json')",
        'Hodram_B52_atomic_positive_v8690b/atomic_positive.json':'Hodram_B31_B53_atomic_positive_v8770/atomic_positive.json',
        'Hodram_B52_wrong_memory_v8691b/wrong_memory_rejections.json':'Hodram_B31_B53_wrong_memory_v8771/wrong_memory_rejections.json',
        'Hodram_B52_atomic_challenges_v8692/semantic_rejections.json':'Hodram_B31_B53_atomic_challenges_v8772/semantic_rejections.json',
        'Hodram_B52_shared_extension_v8697/shared_extension_validation.json':'Hodram_B31_B53_shared_extension_v8773c/shared_extension_validation.json',
        'Hodram_B52_predecessor_positive_v8696/whole_V8609_byte_exact.json':'Hodram_B52_release_v8705/registered_release_verification.json',
        "data['semantic']['negative_count']==16":"data['semantic']['negative_count']==4",
        "data['shared']['negative_count']==6":"data['shared']['negative_count']==1",
        "data['prefix']['whole_registered_V8609_ROM_byte_exact'] and data['prefix']['current_V8609_sha256']==sha(PARENT.read_bytes())":"data['prefix']['whole_ROM_equals_pinned_approved_reference'] and data['prefix']['candidate_sha256']==sha(PARENT.read_bytes()) and data['prefix']['manifest_batches']==646 and data['prefix']['accepted_layers']==114",
        "data['prefix']['all_native_source_editorial_semantic_andproduction_guards_enabled']":"data['prefix']['all18_registered_release_checks_pass'] and data['prefix']['all110_release_dialogue_regressions_pass'] and data['prefix']['whole_clean_input_ROM_reconstruction_byte_exact']",
        'translations/hodram_B51_editorial_release_v2.json':'translations/hodram_B52_editorial_release_v3.json',
        'dk4tool/patch/hodram_b52_extension_v2.py':'dk4tool/patch/hodram_b31_b53_extension_v2.py',
        'scripts/validate_Hodram_B52_atomic_v8690b.py':'scripts/validate_Hodram_B31_B53_atomic_v8770.py',
        'scripts/validate_Hodram_B52_wrong_memory_v8691b.py':'scripts/validate_Hodram_B31_B53_wrong_memory_v8771.py',
        'scripts/challenge_Hodram_B52_atomic_v8692.py':'scripts/challenge_Hodram_B31_B53_atomic_v8772.py',
        'scripts/validate_Hodram_B52_shared_extension_v8697.py':'scripts/validate_Hodram_B31_B53_shared_v8773c.py',
        'all_original998_entries_andall_compatible_prefix_dependencies_retained_exact':'all_original1424_entries_andentire_registered_V8704_dependencies_retained_exact',
        'semantic_zero_commit_cases=16,shared_zero_commit_cases=6,builder_changed_input_cases=29':'semantic_zero_commit_cases=4,shared_zero_commit_cases=1,unchanged_builder_changed_input_cases_reused=29',
        'whole_registered_V8609_prefix_reproduced_withall_guards':'entire_verified_registered_V8704_prefix_preserved',
        "'B52 integration bound:equal lifecycle reports/3wrong-memory/16semantic/6shared failures/29builder failures/fullV8609 prefix. Final dependencies'":"'B31/B53 bound:equal lifecycle reports/3wrong-memory/4semantic/1late-target failures;unchanged builder tests andwhole verifiedV8704 prefix reused. Final dependencies'",
        "';all998 prior entries retained. No ROM/credit.'":"';all1424 prior entries retained. No ROM/credit.'",
    })
    source=Path('scripts/register_Hodram_B52_v8703.py').read_text('utf-8')
    a=source.index('    profile.update(');z=source.index('    updated=deepcopy(registry)',a)
    newprofile="""    old_extensions=deepcopy(profile['late_editorial_extensions'])
    profile.update(status='experimental',late_editorial_extensions=old_extensions+[spec],
        description='Complete V8704 plus clean-Japanese contextual Hodram SC1 B31/B53: three revisions, preserving speaker agency and wanted-status meaning.',
        note=profile.get('note','')+' B31/B53: natural-dialogue-v2 en-US; all five individual gates, full216px automatic pages2/4/3rows, zero warnings orwaivers. Preserve all18 original commands/3preambles/4relatives/1rawquery/8opaquecontrols/2normalends. Source52->31->53 dependencies do not establish continuity, location, earned chronology, B52choice effects orunnamed-man identity. Retain scoped Barbarossa Hayreddin/Fazul components and Port Worker role without invented ranks, kinship orhistory. Four whole-block coldboots24004frames/76body-name holds/fourpages observe long B31 andB53warning;short B31 remains offline-only. Normal returns[0,1]/[0,0] preserve existing resultword independently ofr3mode1. Three decodedlength differences retained;duration/UI/boundaryRNG/followingcommands, five finalcomponents/actors/captain1/calendar/seed3325064553 and68laterRGBpairs match inbounded fixtures. No natural activation/fullcatalogue/all207/customnames/future simulation/fullroute/hardware claim. All364 production negatives, both atomiclifecycles,3wrongmemory,4representative semantic andlate shared target failure pass. Every prior profile, accepted layer, builder byte, ROM andtranslation preserved;full editorial objective active,graphics/laterolder-record audit separate.')
    assert all(profile[k]==v for k,v in registry['profiles']['all-routes-unified-v8704'].items() if k not in ['status','late_editorial_extensions','description','note'])
    assert profile['late_editorial_extensions'][:-1]==registry['profiles']['all-routes-unified-v8704']['late_editorial_extensions']
"""
    b=source.index("    source=read(SUPPORT/'source_equivalence.json')");e=source.index("    rp=Path('translations/release_stack.json')",b)
    builder="""    source=read(SUPPORT/'source_equivalence.json');before=BUILDER.read_bytes();after=before
    assert before==(SUPPORT/'builder.planned.py').read_bytes() and sha(before)==source['builder_planned_sha256']
    assert validate_builder_bytes(before,source['original_frozen_builder_digest'])['shared_late_editorial_hook_present']
"""
    mutation="    temporary=BUILDER.with_name('build_integrated_release_v8703.tmp');assert not temporary.exists();temporary.write_bytes(after);os.replace(temporary,BUILDER)\n"
    registration=derive('scripts/register_Hodram_B52_v8703.py','scripts/register_Hodram_B31_B53_v8777.py',{
        source[a:z]:newprofile,source[b:e]:builder,mutation:'',
        'hodram_B52_editorial_v2':'hodram_B31_B53_editorial_v2',
        'Hodram_B52_release_paths_v8693':'Hodram_B31_B53_release_paths_v8767',
        'Hodram_B52_registration_v8703':'Hodram_B31_B53_registration_v8777',
        "PROFILE='all-routes-unified-v8704'":"PROFILE='all-routes-unified-v8778'",
        "CONFIG=Path('translations/hodram_B52_editorial_release_v3.json')":"CONFIG=Path('translations/hodram_B31_B53_editorial_release_v2.json')",
        'Hodram_B52_integration_binding_v8699':'Hodram_B31_B53_integration_binding_v8776',
        'whole_registered_V8609_prefix_reproduced_withall_guards':'entire_verified_registered_V8704_prefix_preserved',
        "binding['builder_changed_input_cases']":"binding['unchanged_builder_changed_input_cases_reused']",
        '==(3,16,6,29)':'==(3,4,1,29)',
        'editorial_handoff_verification_v8687':'editorial_handoff_verification_v8775',
        "['batches'])==645":"['batches'])==646",
        'dk4tool/patch/hodram_b52_extension_v2.py':'dk4tool/patch/hodram_b31_b53_extension_v2.py',
        "id='hodram-b52',module='dk4tool.patch.hodram_b52_extension_v2'":"id='hodram-b31-b53',module='dk4tool.patch.hodram_b31_b53_extension_v2'",
        "registry['profiles']['all-routes-unified-v8609']":"registry['profiles']['all-routes-unified-v8704']",
        "assert not profile.get('late_editorial_extensions')":"assert len(profile['late_editorial_extensions'])==1 and profile['late_editorial_extensions'][0]['target_ROM_sha256']==sha(PARENT.read_bytes())",
        "parent_profile='all-routes-unified-v8609'":"parent_profile='all-routes-unified-v8704'",
        'expected_manifest_batches=646':'expected_manifest_batches=647',
        "'Registered experimentalV8704 afterwholeV8609 through shared late hook;646batches/114accepted expected. Full oldbuilder/registry inverse retained. No ROMbuild/promotion/credit yet.'":"'Registered experimentalV8778 aftercompleteV8704;647batches/114accepted expected. Prior B52 extension andevery builder byte unchanged;whole registry inverse retained. No ROMbuild/promotion/credit yet.'",
    })
    build=derive('scripts/build_Hodram_B52_v8704.py','scripts/build_Hodram_B31_B53_v8778.py',{
        'Hodram_B52_build_v8704':'Hodram_B31_B53_build_v8778',
        'all_routes_combined_v8704_candidate':'all_routes_combined_v8778_candidate',
        'Hodram_B52_registration_v8703':'Hodram_B31_B53_registration_v8777',
        'all-routes-unified-v8704':'all-routes-unified-v8778',
    })
    regression=derive('scripts/run_Hodram_B52_regressions_v8704.py','scripts/run_Hodram_B31_B53_regressions_v8778.py',{
        'Hodram_B52_regressions_v8704':'Hodram_B31_B53_regressions_v8778',
        'all_routes_combined_v8704_candidate':'all_routes_combined_v8778_candidate',
        'all-routes-unified-v8704':'all-routes-unified-v8778',
    })
    root.mkdir(parents=True);save(root/'derivation.json',dict(binding=binding,registration=registration,build=build,regression=regression,
        all_original1424_dependencies_preserved_additive_closure_only=True,unchanged_builder_andprevious_complete_prefix_tests_reused_not_replayed=True,
        prior_B52_extension_preserved_exact_before_new_extension=True,original_registry_inverse_all_profiles_accepted_andmain4701_preserved=True,
        no_registry_ROM_orcredit_change_by_preparer=True,full_goal_complete=False))
