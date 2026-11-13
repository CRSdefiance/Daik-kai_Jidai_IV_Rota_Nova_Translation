"""Carry all preceding semantics andthe exact v3 registered-config alias into guarded corrected B49 stage."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/Hodram_B49_predecessor_tools_v8451')
OLD=Path('translations/hodram_outcomes_editorial_release_v4.json')
NEW=Path('translations/hodram_outcomes_editorial_release_v5.json')
SPECS=[
 ('dialogue','profile',4,5,{'hodram_outcomes_builder_guard_v4':'hodram_outcomes_builder_guard_v5'}),
 ('dialogue','layout',4,5,{'hodram_outcomes_profile_v4':'hodram_outcomes_profile_v5'}),
 ('dialogue','names',4,5,{'hodram_outcomes_profile_v4':'hodram_outcomes_profile_v5'}),
 ('patch','native_guards',4,5,{'hodram_outcomes_profile_v4':'hodram_outcomes_profile_v5'}),
 ('patch','native_evidence',5,6,{'hodram_outcomes_native_guards_v4':'hodram_outcomes_native_guards_v5'}),
 ('patch','controls',4,5,{'hodram_outcomes_profile_v4':'hodram_outcomes_profile_v5','hodram_outcomes_native_guards_v4':'hodram_outcomes_native_guards_v5'}),
 ('patch','editorial',4,5,{'hodram_outcomes_profile_v4':'hodram_outcomes_profile_v5','hodram_outcomes_layout_v4':'hodram_outcomes_layout_v5','hodram_outcomes_names_v4':'hodram_outcomes_names_v5','hodram_outcomes_native_evidence_v5':'hodram_outcomes_native_evidence_v6','hodram_outcomes_controls_v4':'hodram_outcomes_controls_v5','hodram_outcomes_builder_guard_v4':'hodram_outcomes_builder_guard_v5','hodram_outcomes_editorial_release_v4':'hodram_outcomes_editorial_release_v5'}),
]
if __name__=='__main__':
    assert not ROOT.exists() and not NEW.exists();results=[];paths=[]
    for area,name,old,new,changes in SPECS:
        source=Path(f'dk4tool/{area}/hodram_outcomes_{name}_v{old}.py');target=Path(f'dk4tool/{area}/hodram_outcomes_{name}_v{new}.py');assert not target.exists()
        results.append(derive(source,target,changes));paths.append(target)
    conf=read(OLD);olddeps=dict(conf['dependencies'])
    for path in [OLD,Path('dk4tool/patch/hodram_outcomes_builder_guard_v5.py'),*paths]:conf['dependencies'][str(path.resolve())]=sha(path.read_bytes())
    assert all(conf['dependencies'][p]==h for p,h in olddeps.items());save(NEW,conf);ROOT.mkdir(parents=True)
    save(ROOT/'source_equivalence.json',dict(derivations=results,old_configuration=str(OLD),old_configuration_sha256=sha(OLD.read_bytes()),new_configuration=str(NEW),new_configuration_sha256=sha(NEW.read_bytes()),prior_dependencies=len(olddeps),new_dependencies=len(conf['dependencies']),every_prior_dependency_retained_exact=True,only_explicit_import_guard_config_namespace_bindings_changed=True,all_prior_semantic_bodies_native_addresses_andmultiplicity_preserved=True,no_builder_registry_ROM_orcredit_change=True,new_credit=0,full_goal_complete=False))
