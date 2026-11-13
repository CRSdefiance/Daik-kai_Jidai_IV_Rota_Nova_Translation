"""Pin corrected production and test the actual canonical-source/current-memory builder lifecycle."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/Hodram_fixture_production_positive_tools_v8374');assert not root.exists();results=[]
    results.append(derive('scripts/pin_Hodram_outcomes_production_v8359d.py','scripts/pin_Hodram_outcomes_production_v8374.py',{
        'hodram_outcomes_profile_v2':'hodram_outcomes_profile_v3','hodram_outcomes_editorial_v2':'hodram_outcomes_editorial_v3','Hodram_outcomes_production_v8359d':'Hodram_outcomes_production_v8374',
        "read('translations/hodram_outcomes_editorial_release_v1.json')['dependencies']":"read('translations/hodram_outcomes_editorial_release_v2.json')['dependencies']",
        '    for path in deps:assert path.is_file()':'''    deps.update(Path(p).resolve() for p in [
        'work/analysis/Hodram_outcome_fixture_production_tools_v8372/source_locked_production_fixture_inverse_andtwo_exact_owned_builder_stages.json',
        'work/analysis/Hodram_builder_fixture_successor_validation_v8373/three_exact_builder_forms_eleven_changed_builder_rejections_full_source_inverse.json',
        'work/analysis/Hodram_fixture_parent_inverse_validation_v8369/canonical_source_path_complete_V8300_memory_original_failure_reproduced_corrected100holds_pass.json',
        'work/analysis/Hodram_fixture_parent_inverse_tools_v8369/whole_fixture_inverse_validated_inmemory_parent_not_original_disk_path.json'])
    for path in deps:assert path.is_file()''',
    }))
    results.append(derive('scripts/validate_Hodram_outcome_atomic_positive_v8359e.py','scripts/validate_Hodram_outcome_atomic_positive_v8374b.py',{
        'from pathlib import Path':'from pathlib import Path\nfrom copy import deepcopy',
        'hodram_outcomes_editorial_v2':'hodram_outcomes_editorial_v3','Hodram_outcome_atomic_positive_v8359e':'Hodram_outcome_atomic_positive_v8374b',
        'image=NdsImage.open(PARENT);baseline=':'parent=NdsImage.open(PARENT);image=NdsImage(owned.CANONICAL,deepcopy(parent.rom));baseline=',
        'candidate_before_sha256=sha(before),':'candidate_before_sha256=sha(before),image_source_path=str(image.source),canonical_source_path_with_exact_current_parent_memory=True,',
    }))
    root.mkdir(parents=True);save(root/'source_locked_current_memory_canonical_source_positive_tools.json',dict(derivations=results,all_previous_configurations_andpositives_preserved=True,no_credit_before_full_registered_release_andstartup=True,new_credit=0,full_goal_complete=False))
