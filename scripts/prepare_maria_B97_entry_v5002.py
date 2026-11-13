"""Prepare original EV3 entry/dependency binding using the fresh current Maria snapshot."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

if __name__=='__main__':
    root=Path('work/analysis/maria_B97_entry_tools_v5002');assert not root.exists()
    tool=derive('scripts/prove_maria_B109_entry_v3501.py','scripts/prove_maria_B97_entry_v5002.py',{
        'B109':'B97','current_common_native_context_v2677':'current_maria_native_context_v4999','maria_B109_entry_v3501':'maria_B97_entry_v5002',
        'maria_B109_source_v3498/all26':'maria_B97_source_v4998/all32',
        'maria_B109_voices_v3499':'maria_B97_voices_v5000',"r['script_block']==109":"r['script_block']==97",
        'source_UI_control_restoration_and_all_editorial_gates_pending':'source_setup_presentation_effect_bindings_and_all_editorial_gates_pending',
    })
    root.mkdir(parents=True);save(root/'prepared_tools.json',dict(tool=tool,no_new_EMU_or_ROM_or_review_credit=True))
