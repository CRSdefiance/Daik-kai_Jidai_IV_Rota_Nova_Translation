"""Stage a shared late hook and namespace-only compatibility; do not edit the live builder."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive,checked_text
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.hodram_outcomes_builder_guard_v7 import STAGE_V7,STAGE_B49_V4,STAGE_B50_V2,STAGE_B51
from dk4tool.patch.hodram_outcomes_builder_guard_v8 import BUILDER,STAGE_V8,STAGE_B49_V5,STAGE_B50_V3,STAGE_B51_V2,BUILDER_STAGE,validate_builder_bytes

ROOT=Path('work/analysis/Hodram_B52_builder_support_v8694')
SPECS=[
    ('dialogue','profile',7,8,{'hodram_outcomes_builder_guard_v7':'hodram_outcomes_builder_guard_v8'}),
    ('dialogue','layout',7,8,{'hodram_outcomes_profile_v7':'hodram_outcomes_profile_v8'}),
    ('dialogue','names',7,8,{'hodram_outcomes_profile_v7':'hodram_outcomes_profile_v8'}),
    ('patch','native_guards',7,8,{'hodram_outcomes_profile_v7':'hodram_outcomes_profile_v8'}),
    ('patch','native_evidence',8,9,{'hodram_outcomes_native_guards_v7':'hodram_outcomes_native_guards_v8'}),
    ('patch','controls',7,8,{'hodram_outcomes_profile_v7':'hodram_outcomes_profile_v8','hodram_outcomes_native_guards_v7':'hodram_outcomes_native_guards_v8'}),
    ('patch','editorial',7,8,{'hodram_outcomes_profile_v7':'hodram_outcomes_profile_v8',
        'hodram_outcomes_layout_v7':'hodram_outcomes_layout_v8','hodram_outcomes_names_v7':'hodram_outcomes_names_v8',
        'hodram_outcomes_native_evidence_v8':'hodram_outcomes_native_evidence_v9','hodram_outcomes_controls_v7':'hodram_outcomes_controls_v8',
        'hodram_outcomes_builder_guard_v7':'hodram_outcomes_builder_guard_v8','hodram_outcomes_editorial_release_v7':'hodram_outcomes_editorial_release_v8'}),
]

if __name__=='__main__':
    assert not ROOT.exists()
    current=BUILDER.read_bytes();source=BUILDER.read_text(encoding='utf-8');assert source.encode()==current
    changes={STAGE_V7:STAGE_V8,STAGE_B49_V4:STAGE_B49_V5,STAGE_B50_V2:STAGE_B50_V3,STAGE_B51:STAGE_B51_V2,
             '    # Lexically valid "% o"':BUILDER_STAGE+'    # Lexically valid "% o"'}
    planned=checked_text(source,changes).encode()
    inverse=planned.replace(BUILDER_STAGE.encode(),b'',1)
    for new,old in [(STAGE_V8,STAGE_V7),(STAGE_B49_V5,STAGE_B49_V4),(STAGE_B50_V3,STAGE_B50_V2),(STAGE_B51_V2,STAGE_B51)]:inverse=inverse.replace(new.encode(),old.encode(),1)
    assert inverse==current
    previous_config=read('translations/hodram_B51_editorial_release_v1.json')
    original_digest=previous_config['dependencies'][str(BUILDER)]
    assert validate_builder_bytes(current,original_digest)['whole_original_builder_inverse_preserved']
    assert validate_builder_bytes(planned,original_digest)['shared_late_editorial_hook_present']
    modules=[Path('dk4tool/patch/hodram_outcomes_builder_guard_v8.py'),Path('dk4tool/patch/late_editorial_extensions_v1.py')]
    derivations=[]
    for area,name,before,after,delta in SPECS:
        src=f'dk4tool/{area}/hodram_outcomes_{name}_v{before}.py';dst=f'dk4tool/{area}/hodram_outcomes_{name}_v{after}.py'
        derivations.append(derive(src,dst,delta));modules.append(Path(dst))
    for name,before,after in [('B49',4,5),('B50',2,3),('B51',1,2)]:
        src=f'dk4tool/patch/hodram_{name}_editorial_v{before}.py';dst=f'dk4tool/patch/hodram_{name}_editorial_v{after}.py'
        derivations.append(derive(src,dst,{'hodram_outcomes_builder_guard_v7':'hodram_outcomes_builder_guard_v8'}));modules.append(Path(dst))

    def extend(oldpath,newpath,inherited=None):
        oldpath,newpath=Path(oldpath),Path(newpath);assert not newpath.exists()
        old=read(oldpath);new=read(oldpath)
        if inherited:
            for path,digest in inherited.items():assert path not in new['dependencies'] or new['dependencies'][path]==digest;new['dependencies'][path]=digest
        for p in [oldpath,Path(__file__),*modules]:
            path,digest=str(p.resolve()),sha(p.read_bytes());assert path not in new['dependencies'] or new['dependencies'][path]==digest;new['dependencies'][path]=digest
        assert all(new['dependencies'][p]==h for p,h in old['dependencies'].items())
        assert {k:v for k,v in old.items() if k!='dependencies'}=={k:v for k,v in new.items() if k!='dependencies'}
        save(newpath,new)
        return new,dict(old_configuration=str(oldpath),old_configuration_sha256=sha(oldpath.read_bytes()),
             new_configuration=str(newpath),new_configuration_sha256=sha(newpath.read_bytes()),prior_dependencies=len(old['dependencies']),new_dependencies=len(new['dependencies']),
             every_original_dependency_entry_andall_other_configuration_values_preserved=True)

    records=[];inherited=None
    for old,new in [('hodram_outcomes_editorial_release_v7','hodram_outcomes_editorial_release_v8'),
                    ('hodram_B49_editorial_release_v5','hodram_B49_editorial_release_v6'),
                    ('hodram_B50_editorial_release_v2','hodram_B50_editorial_release_v3'),
                    ('hodram_B51_editorial_release_v1','hodram_B51_editorial_release_v2')]:
        conf,row=extend('translations/'+old+'.json','translations/'+new+'.json',inherited);inherited=conf['dependencies'];records.append(row)
    assert BUILDER.read_bytes()==current
    ROOT.mkdir(parents=True)
    (ROOT/'builder.before.py').write_bytes(current);(ROOT/'builder.planned.py').write_bytes(planned)
    save(ROOT/'source_equivalence.json',dict(derivations=derivations,namespace_only_outcomes_derivations=derivations[:7],
         B49_B50_B51_guard_import_only_derivations=derivations[7:],configurations=records,
         full_current_builder_inverse_byte_exact=True,builder_before_sha256=sha(current),builder_planned_sha256=sha(planned),original_frozen_builder_digest=original_digest,
         shared_hook_after_complete_B51_before_final_percent_andgraphics_guards=True,
         all_original_native_high_integer_constants_andmultiplicity_preserved=True,
         unchanged_frozen_native_contracts={str(p):sha(p.read_bytes()) for p in [Path('translations')/n for n in ['hodram_outcomes_native_contract_v1.json','hodram_B49_native_contract_v2.json','hodram_B50_native_contract_v2.json','hodram_B51_native_contract_v1.json','hodram_B52_native_contract_v1.json']]},
         exact_builder_changedinput_tests_andwhole_V8609_prefix_verification_pending=True,
         no_live_builder_registry_ROM_orcompletion_credit_change=True,full_goal_complete=False))
    print('Staged shared late hook andnamespace-only compatibility;entire old builder inverse andall original config dependency entries preserved. Live builder/registry/ROM unchanged.')
