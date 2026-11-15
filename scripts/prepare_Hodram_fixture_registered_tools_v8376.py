"""Register and build the corrected stage while retaining the failed V8362 attempt and exact builder history."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/Hodram_fixture_registered_tools_v8376');assert not root.exists();results=[]
    oldbinding="Path('work/analysis/Hodram_builder_semantic_binding_v8359f/50_prior_semantic_rejections_bound_to_unchanged_gates_new_positive_and8_builder_rejections.json')"
    oldblock='''    anchor='    # Lexically valid "% o"';text=before.decode('utf8');assert text.count(anchor)==1 and "profile_config.get('hodram_outcomes_editorial')" not in text
    after=checked_text(text,{anchor:STAGE+anchor}).encode('utf8');digest=frozen['dependencies'][str(builder.resolve())]
    assert sha(before)==digest and validate_builder_bytes(after,digest)['exact_owned_stage_inverse']'''
    newblock='''    anchor='    # Lexically valid "% o"';text=before.decode('utf8');assert text.count(anchor)==1 and text.count(LEGACY_STAGE)==1 and STAGE not in text
    digest=frozen['dependencies'][str(builder.resolve())];assert validate_builder_bytes(before,digest)['owned_stage_version']=='preserved-v2'
    frozen_builder=before.replace(LEGACY_STAGE.encode(),b'',1);assert sha(frozen_builder)==digest
    after=checked_text(text,{LEGACY_STAGE:STAGE}).encode('utf8')
    assert after.replace(STAGE.encode(),b'',1)==frozen_builder and validate_builder_bytes(after,digest)['owned_stage_version']=='current-v3' '' '
'''.replace("' '' '\n",'\n')
    # Keep the replacement explicit and syntax-checked by derive before writing.
    newblock=newblock.replace("=='current-v3' '' '","=='current-v3'")
    results.append(derive('scripts/register_Hodram_outcomes_v8361.py','scripts/register_Hodram_outcomes_v8376.py',{
        'hodram_outcomes_editorial_v2':'hodram_outcomes_editorial_v3','hodram_outcomes_profile_v2':'hodram_outcomes_profile_v3',
        'from dk4tool.patch.hodram_outcomes_builder_guard_v1 import STAGE,validate_builder_bytes':'from dk4tool.patch.hodram_outcomes_builder_guard_v2 import STAGE,LEGACY_STAGE,validate_builder_bytes',
        'Hodram_outcomes_registration_v8361':'Hodram_outcomes_registration_v8376','all-routes-unified-v8362':'all-routes-unified-v8377','Hodram_outcome_atomic_positive_v8359e':'Hodram_outcome_atomic_positive_v8374b',
        oldbinding:"Path('work/analysis/Hodram_fixture_binding_v8375b/semantic_binding.json')",'editorial_handoff_verification_v8360':'editorial_handoff_verification_v8371',
        "assert binding['prior_semantic_cases']==50 and binding['exact_source_equivalence_ofall_semantic_checks'] and binding['new_builder_guard_negative_count']==8":"assert binding['prior_semantic_cases']==50 and len(binding['derivations'])==7 and binding['new_lifecycle_negative_count']==3 and binding['new_builder_guard_negative_count']==11 and positive['canonical_source_path_with_exact_current_parent_memory']",
        oldblock:newblock,
        "(ROOT/'builder.stage.bin').write_bytes(STAGE.encode());":"(ROOT/'builder.stage.bin').write_bytes(STAGE.encode());(ROOT/'builder.previous_stage.bin').write_bytes(LEGACY_STAGE.encode());(ROOT/'builder.frozen_original.bin').write_bytes(frozen_builder);",
        "builder.read_bytes().replace(STAGE.encode(),b'',1)==before":"builder.read_bytes().replace(STAGE.encode(),LEGACY_STAGE.encode(),1)==before and builder.read_bytes().replace(STAGE.encode(),b'',1)==frozen_builder",
        'build_integrated_release_v8361.tmp':'build_integrated_release_v8376.tmp',
        'newbuilder8negativeguard cases andfresh whole-object positive':'newbuilder11negativeguard cases,3changed-memory lifecycle rejections andfresh canonical-source/current-memory whole-object positive;one tested fixtureinverse correction',
        'all481otherpriorproductiondependencies retained':'all492priorproductiondependencies retained;failedV8362 profile andalllogs preserved',
        'new_builder_negative_cases=8':'new_builder_negative_cases=11,new_canonical_lifecycle_negative_cases=3',
        'Registered experimental V8362':'Registered experimental V8377',
    }))
    results.append(derive('scripts/build_Hodram_outcomes_v8362.py','scripts/build_Hodram_outcomes_v8377.py',{'Hodram_outcomes_build_v8362':'Hodram_outcomes_build_v8377','all_routes_combined_v8362':'all_routes_combined_v8377','Hodram_outcomes_registration_v8361':'Hodram_outcomes_registration_v8376','all-routes-unified-v8362':'all-routes-unified-v8377'}))
    results.append(derive('scripts/run_Hodram_outcomes_regressions_v8362.py','scripts/run_Hodram_outcomes_regressions_v8377.py',{'Hodram_outcomes_regressions_v8362':'Hodram_outcomes_regressions_v8377'}))
    results.append(derive('scripts/verify_Hodram_outcomes_release_v8363.py','scripts/verify_Hodram_outcomes_release_v8378.py',{
        'hodram_outcomes_editorial_v2':'hodram_outcomes_editorial_v3','Hodram_outcomes_release_v8363':'Hodram_outcomes_release_v8378','all_routes_combined_v8362':'all_routes_combined_v8377','Hodram_outcomes_registration_v8361':'Hodram_outcomes_registration_v8376','Hodram_outcome_atomic_positive_v8359e':'Hodram_outcome_atomic_positive_v8374b','Hodram_outcomes_build_v8362':'Hodram_outcomes_build_v8377','Hodram_outcomes_regressions_v8362':'Hodram_outcomes_regressions_v8377','all-routes-unified-v8362':'all-routes-unified-v8377','registered V8362':'registered V8377',
        "builder.replace(stage,b'',1)==(REG/'build_integrated_release.py.before').read_bytes()":"builder.replace(stage,(REG/'builder.previous_stage.bin').read_bytes(),1)==(REG/'build_integrated_release.py.before').read_bytes() and builder.replace(stage,b'',1)==(REG/'builder.frozen_original.bin').read_bytes()",
    }))
    root.mkdir(parents=True);save(root/'registered_corrected_stage_derivations.json',dict(derivations=results,preserved_failed_V8362_registry_profile_andall_artifacts=True,old_V8300_parent_andsame_tested_reference_required=True,expected_manifest_batches=642,accepted_layers=114,no_registry_builder_ROM_orcredit_change_bythis_preparer=True,new_credit=0,full_goal_complete=False))
