"""Derive exact existing complete-bank load/cache and original parent-mode checks."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/Hodram_B31_B53_loader_tools_v8737');assert not root.exists()
    receipt=derive('scripts/verify_Hodram_B52_loaders_v8646.py','scripts/verify_Hodram_B31_B53_loaders_v8737.py',{
        'scripts.create_Hodram_B52_reference_v8645':'scripts.create_Hodram_B31_B53_reference_v8736',
        'Hodram_B52_loaders_v8646':'Hodram_B31_B53_loaders_v8737','Hodram_B52_reference_v8645':'Hodram_B31_B53_reference_v8736',
        'exact_B52_header_andall_mapped_targets_fit_original_0x2400_cache':'exact_B31_B53_headers_andall_mapped_targets_fit_original_0x2400_cache',
        'three-speech/two-choice/four-relative B52':'three-speech/two-block/four-relative B31/B53',
    })
    root.mkdir(parents=True);save(root/'derivation.json',dict(tool=receipt,all_native_high_integer_constants_andmultiplicity_preserved=True,
        all_original_complete_payload_cache_parentmode_neighbor_ABI_andinstruction_guards_unchanged=True,
        controlled_native_route_inputs_not_ordinary_event_activation=True,no_ROM_registry_orcredit_change=True,new_credit=0,new_emulator_runs=0,full_goal_complete=False))
