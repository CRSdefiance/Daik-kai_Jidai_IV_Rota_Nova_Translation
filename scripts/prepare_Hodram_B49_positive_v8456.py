"""Retain failed first positive;test corrected immutable stage with identical whole-object assertions."""
from scripts.source_locked_derivation_v5118 import derive
if __name__=='__main__':
    derive('scripts/validate_Hodram_B49_atomic_v8449.py','scripts/validate_Hodram_B49_atomic_v8456.py',{
        'hodram_B49_editorial_v1':'hodram_B49_editorial_v2','Hodram_B49_release_paths_v8447':'Hodram_B49_release_paths_v8450','Hodram_B49_atomic_positive_v8449':'Hodram_B49_atomic_positive_v8456',
    })
