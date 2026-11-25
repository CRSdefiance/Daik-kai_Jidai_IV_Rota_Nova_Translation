"""Re-pin the exact builder-inverse successor, preserving the original configuration and positive."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/Hodram_outcome_production_successor_tools_v8359d');assert not root.exists();results=[]
    results.append(derive('scripts/pin_Hodram_outcomes_production_v8354.py','scripts/pin_Hodram_outcomes_production_v8359d.py',{
        'hodram_outcomes_profile_v1':'hodram_outcomes_profile_v2','hodram_outcomes_editorial_v1':'hodram_outcomes_editorial_v2','Hodram_outcomes_production_v8354':'Hodram_outcomes_production_v8359d',
        '    for path in deps:assert path.is_file()':'''    deps.update(Path(p) for p in read('translations/hodram_outcomes_editorial_release_v1.json')['dependencies'])
    deps.add(Path('work/analysis/Hodram_outcome_builder_successor_tools_v8359b/original_frozen_contract_andall_semantic_validators_preserved_exact_builder_inverse_successors.json').resolve())
    deps.add(Path('work/analysis/Hodram_builder_inverse_validation_v8359c/exact_owned_builder_stage_full_inverse_two_positives_eight_changed_builder_rejections.json').resolve())
    # The frozen417 native contract still binds the original builder by exact owned-stage inverse.
    deps.discard(Path('scripts/build_integrated_release.py').resolve())
    for path in deps:assert path.is_file()''',
    }))
    results.append(derive('scripts/validate_Hodram_outcome_atomic_positive_v8355.py','scripts/validate_Hodram_outcome_atomic_positive_v8359e.py',{'hodram_outcomes_editorial_v1':'hodram_outcomes_editorial_v2','Hodram_outcome_atomic_positive_v8355':'Hodram_outcome_atomic_positive_v8359e'}))
    root.mkdir(parents=True);save(root/'source_locked_builder_inverse_production_positive_tools.json',dict(derivations=results,original_config_andpositive_preserved=True,only_exact_additive_builder_stage_normalized_all_semantic_gates_unchanged=True,new_credit=0,full_goal_complete=False))
