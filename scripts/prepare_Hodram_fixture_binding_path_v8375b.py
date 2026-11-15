"""Preserve the completed-but-unsaved audit attempt; shorten only its Windows artifact path."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/Hodram_fixture_binding_tools_v8375b');assert not root.exists()
    d=derive('scripts/bind_Hodram_fixture_production_semantics_v8375.py','scripts/bind_Hodram_fixture_production_semantics_v8375b.py',{
        'Hodram_fixture_production_semantic_binding_v8375':'Hodram_fixture_binding_v8375b',
        'prior50_source_equivalence_exact_fixture_inverse_new_canonical_lifecycle_positive_three_precommit_negatives.json':'semantic_binding.json',
    })
    root.mkdir(parents=True);save(root/'short_artifact_path_derivation.json',dict(derivation=d,previous_attempt_passed_all_computations_but_exceeded_Windows_artifact_path_length=True,only_output_path_shortened_no_guard_orsemantic_change=True,new_credit=0,full_goal_complete=False))
