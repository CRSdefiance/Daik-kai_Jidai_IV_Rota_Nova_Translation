"""Bind all 325 original load/cache paths and650 parent modes to the resized B52 research archive."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

if __name__=='__main__':
    root=Path('work/analysis/Hodram_B52_loader_tools_v8646');assert not root.exists()
    result=derive('scripts/verify_Hodram_B51_loaders_v8571.py','scripts/verify_Hodram_B52_loaders_v8646.py',{
        'scripts.create_Hodram_B51_reference_v8570':'scripts.create_Hodram_B52_reference_v8645','Hodram_B51_loaders_v8571':'Hodram_B52_loaders_v8646','Hodram_B51_reference_v8570':'Hodram_B52_reference_v8645','exact_B51_header':'exact_B52_header','five-speech/eight-relative B51':'three-speech/two-choice/four-relative B52',
    })
    root.mkdir(parents=True);save(root/'derivation.json',dict(tool=result,all_native_high_integer_constants_andmultiplicity_preserved=True,all_original_load_cache_parent_650cases_complete_payload_metadata_neighbor_SP_PC_andABI_guards_preserved=True,source_exact_code_SDK_IO_bridges_only_no_actual_gameplay_claim=True,new_credit=0,full_goal_complete=False))
