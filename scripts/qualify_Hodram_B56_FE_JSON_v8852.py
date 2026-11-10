"""Compare reconstructed tuples using the original proof's JSON serialization semantics."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/Hodram_B56_FE_JSON_qualification_v8852');assert not root.exists()
    module=derive('dk4tool/patch/hodram_B54_B60_FE_actual_v1.py','dk4tool/patch/hodram_B54_B60_FE_actual_v2.py',{
        'import struct':'import json,struct',"proof['groups']==groups":"proof['groups']==json.loads(json.dumps(groups))",
    })
    validation=derive('scripts/validate_Hodram_B56_FE_production_v8851.py','scripts/validate_Hodram_B56_FE_production_v8851b.py',{
        'hodram_B54_B60_FE_actual_v1':'hodram_B54_B60_FE_actual_v2',
        'Hodram_B56_FE_production_validation_v8851':'Hodram_B56_FE_production_validation_v8851b',
    })
    root.mkdir(parents=True);save(root/'JSON_tuple_array_qualification.json',dict(module=module,validation=validation,preserved_original_terminal_failure='v8851 positive native memory checks passed; complete reconstructed group comparison rejected Python RGB tuples versus JSON arrays',only_comparison_serialization_matches_original_saved_JSON=True,all_native_memory_palette_VRAM_RGB_andreadonly_guards_preserved=True,new_credit=0,full_goal_complete=False))
