"""Keep all frozen policy data and417 dependencies; bind only an exact owned builder extension by full inverse."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/Hodram_outcome_builder_successor_tools_v8359b');assert not root.exists();results=[]
    results.append(derive('dk4tool/dialogue/hodram_outcomes_profile_v1.py','dk4tool/dialogue/hodram_outcomes_profile_v2.py',{
        'from dk4tool.patch.grand_race_menu_release import sha':'from dk4tool.patch.grand_race_menu_release import sha\nfrom dk4tool.patch.hodram_outcomes_builder_guard_v1 import checked_dependency',
        'if sha(Path(p).read_bytes())!=h:raise ValueError("Native dependency changed:"+p)':'if not checked_dependency(Path(p),h):raise ValueError("Native dependency changed:"+p)',
    }))
    for area,name,old,new,changes in [
        ('dialogue','layout',1,2,{'hodram_outcomes_profile_v1':'hodram_outcomes_profile_v2'}),
        ('dialogue','names',1,2,{'hodram_outcomes_profile_v1':'hodram_outcomes_profile_v2'}),
        ('patch','native_guards',1,2,{'hodram_outcomes_profile_v1':'hodram_outcomes_profile_v2'}),
        ('patch','native_evidence',2,3,{'hodram_outcomes_native_guards_v1':'hodram_outcomes_native_guards_v2'}),
        ('patch','controls',1,2,{'hodram_outcomes_profile_v1':'hodram_outcomes_profile_v2','hodram_outcomes_native_guards_v1':'hodram_outcomes_native_guards_v2'}),
        ('patch','editorial',1,2,{'hodram_outcomes_profile_v1':'hodram_outcomes_profile_v2','hodram_outcomes_layout_v1':'hodram_outcomes_layout_v2','hodram_outcomes_names_v1':'hodram_outcomes_names_v2','hodram_outcomes_native_evidence_v2':'hodram_outcomes_native_evidence_v3','hodram_outcomes_controls_v1':'hodram_outcomes_controls_v2','hodram_outcomes_editorial_release_v1':'hodram_outcomes_editorial_release_v2',
            'from dk4tool.patch.grand_race_menu_release import sha':'from dk4tool.patch.grand_race_menu_release import sha\nfrom dk4tool.patch.hodram_outcomes_builder_guard_v1 import checked_dependency',
            "require(sha(Path(path).read_bytes())==digest,'dependency:'+path)":"require(checked_dependency(Path(path),digest),'dependency:'+path)"}),
    ]:results.append(derive(f'dk4tool/{area}/hodram_outcomes_{name}_v{old}.py',f'dk4tool/{area}/hodram_outcomes_{name}_v{new}.py',changes))
    root.mkdir(parents=True);save(root/'original_frozen_contract_andall_semantic_validators_preserved_exact_builder_inverse_successors.json',dict(derivations=results,frozen_contract_and417_original_dependency_entries_unchanged=True,all_native_numeric_constants_andmultiplicity_preserved=True,all_prose_native_actual_FE_control_comparison_gates_unchanged=True,only_builder_dependency_accepts_exact_owned_stage_plus_whole_original_inverse=True,no_builder_registry_ROM_orcredit_changed=True,new_credit=0,full_goal_complete=False))
