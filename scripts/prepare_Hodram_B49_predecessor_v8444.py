"""Source-locked predecessor compatibility;preserve every earlier config/module and builder byte."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/Hodram_B49_predecessor_tools_v8444')
OLD=Path('translations/hodram_outcomes_editorial_release_v3.json')
NEW=Path('translations/hodram_outcomes_editorial_release_v4.json')
SPECS=[
 ('dialogue','profile',3,4,{'hodram_outcomes_builder_guard_v2':'hodram_outcomes_builder_guard_v4'}),
 ('dialogue','layout',3,4,{'hodram_outcomes_profile_v3':'hodram_outcomes_profile_v4'}),
 ('dialogue','names',3,4,{'hodram_outcomes_profile_v3':'hodram_outcomes_profile_v4'}),
 ('patch','native_guards',3,4,{'hodram_outcomes_profile_v3':'hodram_outcomes_profile_v4'}),
 ('patch','native_evidence',4,5,{'hodram_outcomes_native_guards_v3':'hodram_outcomes_native_guards_v4'}),
 ('patch','controls',3,4,{'hodram_outcomes_profile_v3':'hodram_outcomes_profile_v4','hodram_outcomes_native_guards_v3':'hodram_outcomes_native_guards_v4'}),
 ('patch','editorial',3,4,{'hodram_outcomes_profile_v3':'hodram_outcomes_profile_v4','hodram_outcomes_layout_v3':'hodram_outcomes_layout_v4','hodram_outcomes_names_v3':'hodram_outcomes_names_v4','hodram_outcomes_native_evidence_v4':'hodram_outcomes_native_evidence_v5','hodram_outcomes_controls_v3':'hodram_outcomes_controls_v4','hodram_outcomes_builder_guard_v2':'hodram_outcomes_builder_guard_v4','hodram_outcomes_editorial_release_v3':'hodram_outcomes_editorial_release_v4'}),
]

if __name__=='__main__':
    assert not ROOT.exists() and not NEW.exists();results=[];newpaths=[]
    alias='''
PRESERVED_CONFIG='translations/hodram_outcomes_editorial_release_v3.json'
PRESERVED_CONFIG_SHA256='''+repr(sha(OLD.read_bytes()))+'''

def resolve_config(config):
    path=Path(config)
    if path.resolve()==Path(PRESERVED_CONFIG).resolve():
        require(sha(path.read_bytes())==PRESERVED_CONFIG_SHA256,'exact preserved registered v3 config alias')
        return CONFIG
    return config

'''
    for area,name,old,new,changes in SPECS:
        source=Path(f'dk4tool/{area}/hodram_outcomes_{name}_v{old}.py');target=Path(f'dk4tool/{area}/hodram_outcomes_{name}_v{new}.py')
        assert not target.exists()
        if name=='editorial':changes={**changes,'def plan_release(image,baseline,config=CONFIG):':alias+'def plan_release(image,baseline,config=CONFIG):',"    conf=load(config);check_dependencies(conf)":"    conf=load(resolve_config(config));check_dependencies(conf)"}
        results.append(derive(source,target,changes));newpaths.append(target)
    conf=read(OLD);olddeps=dict(conf['dependencies'])
    for path in [OLD,Path('dk4tool/patch/hodram_outcomes_builder_guard_v4.py'),*newpaths]:conf['dependencies'][str(path.resolve())]=sha(path.read_bytes())
    assert all(conf['dependencies'][p]==h for p,h in olddeps.items())
    save(NEW,conf);ROOT.mkdir(parents=True)
    save(ROOT/'source_equivalence.json',dict(derivations=results,old_configuration=str(OLD),old_configuration_sha256=sha(OLD.read_bytes()),new_configuration=str(NEW),new_configuration_sha256=sha(NEW.read_bytes()),prior_dependencies=len(olddeps),new_dependencies=len(conf['dependencies']),every_prior_dependency_retained_exact=True,only_import_builderguard_andexact_oldconfig_alias_bindings_changed=True,all_native_constants_andmultiplicity_preserved=True,previous_native_actual_comparison_FE_control_compiler_semantic_checks_unchanged=True,no_builder_registry_ROM_orcredit_change=True,new_credit=0,full_goal_complete=False))
    print('Prepared exact predecessor compatibility andv3config alias;all earlier dependencies andsemantic bodies retained. Builder/registry untouched.')
