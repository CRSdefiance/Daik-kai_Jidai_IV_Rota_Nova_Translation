"""Rebind the unchanged original SC1 loader checks to the independently rebuilt B49 reference."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

if __name__=='__main__':
    root=Path('work/analysis/Hodram_B49_loader_tools_v8404');assert not root.exists()
    result=derive('scripts/verify_Hodram_outcome_loaders_v8330.py','scripts/verify_Hodram_B49_loaders_v8404.py',{
        'six-speech Hodram research image':'fourteen-speech/two-choice B49 research image',
        'scripts.create_Hodram_outcomes_reference_v8329':'scripts.create_Hodram_B49_reference_v8403',
        'Hodram_outcome_loaders_v8330':'Hodram_B49_loaders_v8404',
        'Hodram_outcome_reference_v8329':'Hodram_B49_reference_v8403',
        'exact_B47_B48_headers_andall_mapped_targets_fit_original_0x2400_cache':'exact_B49_header_andall_mapped_targets_fit_original_0x2400_cache',
    })
    root.mkdir(parents=True);save(root/'derivation.json',dict(derivation=result,all_original_SC1_load_cache_parent_modes_andnative_addresses_unchanged=True,no_ROM_registration_orcredit_change=True))
