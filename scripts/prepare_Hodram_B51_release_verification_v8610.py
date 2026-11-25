"""Derive complete cumulative B51 manifest/reference/inverse/clean-patch verification."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

if __name__=='__main__':
    root=Path('work/analysis/Hodram_B51_release_tools_v8610');assert not root.exists()
    source=Path('scripts/verify_Hodram_B50_release_v8544.py').read_text(encoding='utf-8')
    a=source.index("    assert newprofile.pop('hodram_B50_editorial')");b=source.index('    norm=',a)
    profiles="""    assert newprofile.pop('hodram_B51_editorial')==str(owned.CONFIG)
    for key,oldpath,newpath in [('hodram_B50_editorial','translations/hodram_B50_editorial_release_v1.json','translations/hodram_B50_editorial_release_v2.json'),('hodram_B49_editorial','translations/hodram_B49_editorial_release_v4.json','translations/hodram_B49_editorial_release_v5.json'),('hodram_outcomes_editorial','translations/hodram_outcomes_editorial_release_v6.json','translations/hodram_outcomes_editorial_release_v7.json')]:
        assert Path(newprofile.pop(key)).as_posix()==newpath and Path(oldprofile.pop(key)).as_posix()==oldpath
    assert newprofile==oldprofile
"""
    c=source.index('    assert builder.count(');d=source.index("    clean=Path(conf['clean_ROM'])",c)
    builder="""    stages=[STAGE_V7,STAGE_B49_V4,STAGE_B50_V2,STAGE_B51]
    assert all(builder.count(s.encode())==1 for s in stages)
    assert builder.replace(STAGE_B51.encode(),b'',1).replace(STAGE_V7.encode(),STAGE_V6.encode(),1).replace(STAGE_B49_V4.encode(),STAGE_B49_V3.encode(),1).replace(STAGE_B50_V2.encode(),STAGE_B50.encode(),1)==oldbuilder
    assert validate_builder_bytes(builder,guard['full_original_source_inverse_sha256'])['B51_additive_stage_present']
    assert all(builder.index(a.encode())+len(a.encode())==builder.index(b.encode()) for a,b in zip(stages,stages[1:]))
    assert builder.index(STAGE_B51.encode())+len(STAGE_B51.encode())==builder.index(b'    # Lexically valid "% o"')
"""
    result=derive('scripts/verify_Hodram_B50_release_v8544.py','scripts/verify_Hodram_B51_release_v8610.py',{
        source[a:b]:profiles,source[c:d]:builder,
        'hodram_B50_editorial_v1':'hodram_B51_editorial_v1',
        'from dk4tool.patch.hodram_outcomes_builder_guard_v6 import STAGE_V5,STAGE_B49_V2,STAGE_V6,STAGE_B49_V3,STAGE_B50,validate_builder_bytes':'from dk4tool.patch.hodram_outcomes_builder_guard_v7 import STAGE_V6,STAGE_B49_V3,STAGE_B50,STAGE_V7,STAGE_B49_V4,STAGE_B50_V2,STAGE_B51,validate_builder_bytes',
        'Hodram_B50_release_v8544':'Hodram_B51_release_v8610',
        'all_routes_combined_v8543_candidate':'all_routes_combined_v8609_candidate',
        'all_routes_combined_v8475_candidate':'all_routes_combined_v8543_candidate',
        'Hodram_B50_registration_v8542':'Hodram_B51_registration_v8608',
        'Hodram_B50_atomic_positive_v8539':'Hodram_B51_atomic_positive_v8604',
        'Hodram_B50_build_v8543':'Hodram_B51_build_v8609','Hodram_B50_regressions_v8543':'Hodram_B51_regressions_v8609',
        'all-routes-unified-v8543':'all-routes-unified-v8609',
        "registry['profiles']['all-routes-unified-v8475']":"registry['profiles']['all-routes-unified-v8543']",
        "len(proof['changed_records'])==3":"len(proof['changed_records'])==5",
        "['hodram_B50_editorial']":"['hodram_B51_editorial']",
        'if a!=b]==[50]':'if a!=b]==[51]',
        'Hodram_B50_builder_validation_v8535':'Hodram_B51_builder_validation_v8596',
        '==644':'==645','manifest_batches=644':'manifest_batches=645','batches=644':'batches=645',
        'all644_manifest_batches_and114_accepted_layers_present':'all645_manifest_batches_and114_accepted_layers_present',
        'only_SC1_B50_change_324_otherblocks_andall_other_files_components_exact':'only_SC1_B51_change_324_otherblocks_andall_other_files_components_exact',
        'Registered cumulative B50 aftercompleteV8475;644manifest':'Registered cumulative B51 aftercompleteV8543;645manifest',
        'registered V8543':'registered V8609','registered B50 output':'registered B51 output',
    })
    regressions=derive('scripts/run_Hodram_B50_regressions_v8543.py','scripts/run_Hodram_B51_regressions_v8609.py',{'Hodram_B50_regressions_v8543':'Hodram_B51_regressions_v8609'})
    root.mkdir(parents=True);save(root/'derivation.json',dict(tool=result,regressions=regressions,all_native_numbers_manifest_accepted_checks_reference_unowned_bytes_payload_andclean_patch_guards_preserved=True,all_prior_profiles_builder_registry_values_ROMs_andpins_must_survive=True,no_promotion_pruning_orcredit=True,new_credit=0,full_goal_complete=False))
