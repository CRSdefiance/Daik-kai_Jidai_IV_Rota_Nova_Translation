"""Bind exact unchanged predecessor atomic-positive semantics to the compatibility successor."""
from scripts.source_locked_derivation_v5118 import derive
if __name__=='__main__':
    derive('scripts/validate_Hodram_outcome_atomic_positive_v8374b.py','scripts/validate_Hodram_outcome_atomic_positive_v8445.py',{
        'hodram_outcomes_editorial_v3':'hodram_outcomes_editorial_v4',
        'Hodram_outcome_atomic_positive_v8374b':'Hodram_outcome_atomic_positive_v8445',
        'report=owned.apply_release(image,baseline)':'report=owned.apply_release(image,baseline,config=owned.PRESERVED_CONFIG)',
        'canonical_source_path_with_exact_current_parent_memory=True':'canonical_source_path_with_exact_current_parent_memory=True,exact_preserved_registered_v3config_alias_used=True,compatible_v4_configuration=owned.CONFIG',
    })
