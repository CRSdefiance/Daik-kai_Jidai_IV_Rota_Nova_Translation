"""Source-lock cumulative B50 manifest, exact reference, unowned-byte and clean-patch verification."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

if __name__=='__main__':
    root=Path('work/analysis/Hodram_B50_release_tools_v8544');assert not root.exists()
    source=Path('scripts/verify_Hodram_B49_release_v8460.py').read_text(encoding='utf-8')
    profileline="    assert newprofile.pop('hodram_B49_editorial')==str(owned.CONFIG) and newprofile.pop('hodram_outcomes_editorial')=='translations/hodram_outcomes_editorial_release_v5.json' and oldprofile.pop('hodram_outcomes_editorial')=='translations/hodram_outcomes_editorial_release_v3.json' and newprofile==oldprofile"
    newprofile="""    assert newprofile.pop('hodram_B50_editorial')==str(owned.CONFIG)
    assert Path(newprofile.pop('hodram_B49_editorial')).as_posix()=='translations/hodram_B49_editorial_release_v4.json' and Path(oldprofile.pop('hodram_B49_editorial')).as_posix()=='translations/hodram_B49_editorial_release_v3.json'
    assert Path(newprofile.pop('hodram_outcomes_editorial')).as_posix()=='translations/hodram_outcomes_editorial_release_v6.json' and Path(oldprofile.pop('hodram_outcomes_editorial')).as_posix()=='translations/hodram_outcomes_editorial_release_v5.json' and newprofile==oldprofile"""
    a=source.index("    assert builder.count(STAGE_V5.encode())");b=source.index("    clean=Path(conf['clean_ROM'])",a)
    builder="""    assert builder.count(STAGE_V6.encode())==builder.count(STAGE_B49_V3.encode())==builder.count(STAGE_B50.encode())==1
    assert builder.replace(STAGE_B50.encode(),b'',1).replace(STAGE_V6.encode(),STAGE_V5.encode(),1).replace(STAGE_B49_V3.encode(),STAGE_B49_V2.encode(),1)==oldbuilder
    assert validate_builder_bytes(builder,guard['full_original_source_inverse_sha256'])['B50_additive_stage_present']
    assert builder.index(STAGE_V6.encode())+len(STAGE_V6.encode())==builder.index(STAGE_B49_V3.encode()) and builder.index(STAGE_B49_V3.encode())+len(STAGE_B49_V3.encode())==builder.index(STAGE_B50.encode()) and builder.index(STAGE_B50.encode())+len(STAGE_B50.encode())==builder.index(b'    # Lexically valid "% o"')
"""
    result=derive('scripts/verify_Hodram_B49_release_v8460.py','scripts/verify_Hodram_B50_release_v8544.py',{
        'hodram_B49_editorial_v2':'hodram_B50_editorial_v1',
        'from dk4tool.patch.hodram_outcomes_builder_guard_v4 import STAGE_V3\n':'',
        'from dk4tool.patch.hodram_outcomes_builder_guard_v5 import STAGE_V5,STAGE_B49_V2,validate_builder_bytes':'from dk4tool.patch.hodram_outcomes_builder_guard_v6 import STAGE_V5,STAGE_B49_V2,STAGE_V6,STAGE_B49_V3,STAGE_B50,validate_builder_bytes',
        'Hodram_B49_release_v8460':'Hodram_B50_release_v8544',
        'all_routes_combined_v8459_candidate':'all_routes_combined_v8543_candidate',
        'all_routes_combined_v8377_candidate':'all_routes_combined_v8475_candidate',
        'Hodram_B49_registration_v8458':'Hodram_B50_registration_v8542',
        'Hodram_B49_atomic_positive_v8456':'Hodram_B50_atomic_positive_v8539',
        'Hodram_B49_build_v8459':'Hodram_B50_build_v8543',
        'Hodram_B49_regressions_v8459':'Hodram_B50_regressions_v8543',
        'all-routes-unified-v8459':'all-routes-unified-v8543',
        "registry['profiles']['all-routes-unified-v8377']":"registry['profiles']['all-routes-unified-v8475']",
        profileline:newprofile,
        'positive=read(POSITIVE);proof=positive[\'report\'];assert positive[\'one_complete_NDS_commit\'] and len(proof[\'changed_records\'])==16':"positive=read(POSITIVE);proof=positive['cases'][1]['report'];assert positive['positive_lifecycles']==2 and positive['one_complete_NDS_commit_percase'] and len(proof['changed_records'])==3",
        "['hodram_B49_editorial']":"['hodram_B50_editorial']",
        'if a!=b]==[49]':'if a!=b]==[50]',
        'Hodram_B49_builder_v8452':'Hodram_B50_builder_validation_v8535',
        source[a:b]:builder,
        '==643':'==644','manifest_batches=643':'manifest_batches=644',
        'all643_manifest_batches_and114_accepted_layers_present':'all644_manifest_batches_and114_accepted_layers_present',
        'only_SC1_B49_change_324_otherblocks_andall_other_files_components_exact':'only_SC1_B50_change_324_otherblocks_andall_other_files_components_exact',
        'Registered cumulative B49 aftercompleteV8377;643manifest/114accepted/18checks/110regressions;main4701 unchanged.':'Registered cumulative B50 aftercompleteV8475;644manifest/114accepted/18checks/110regressions;main4701 unchanged.',
        'registered V8459':'registered V8543',
        'batches=643':'batches=644',
        'registered B49 output':'registered B50 output',
    })
    root.mkdir(parents=True);save(root/'derivation.json',dict(tool=result,all_native_high_integer_constants_andmultiplicity_preserved=True,all_prior_manifest_accepted_layers_checks_regressions_reference_exactness_unowned_bytes_payload_andclean_patch_guards_preserved=True,all_prior_profiles_builder_registry_values_ROMs_andpins_must_survive=True,no_promotion_pruning_orcredit=True,new_credit=0,full_goal_complete=False))
