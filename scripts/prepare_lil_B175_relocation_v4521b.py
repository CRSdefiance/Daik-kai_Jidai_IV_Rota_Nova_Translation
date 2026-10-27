"""Correct inherited summary metadata before executing the mixed-consumer relocation."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

if __name__=='__main__':
    tool=derive('scripts/research_lil_B175_relocation_v4521.py','scripts/research_lil_B175_relocation_v4521b.py',{
        'source_FE_system_objects=0':'source_FE_system_objects=9',
        'predicates_typed_dispatch_final_parity_fonts_external_references_and_sampling_pending':
            'final_parity_fonts_external_references_and_sampling_pending',
    })
    save(Path('work/analysis/lil_B175_relocation_tools_v4521/corrected_mixed_consumer_summary_derivation.json'),dict(
        tool=tool,initial_unexecuted_producer_preserved=True,no_prose_or_relocation_algorithm_change=True,full_goal_complete=False))
    print('Prepared corrected B175 relocation metadata: nine FE, no nonexistent predicate/typed tests.')
