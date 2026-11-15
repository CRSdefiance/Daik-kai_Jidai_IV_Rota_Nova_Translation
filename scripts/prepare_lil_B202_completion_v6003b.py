"""Make historical native-only flags explicit in the final integrated rows."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    proof=derive('scripts/complete_lil_B202_v6003.py','scripts/complete_lil_B202_v6003b.py',{
        "'source_prose_or_completion_credit_added','command_offset']":"'source_prose_or_completion_credit_added','command_offset','current_native_voice_macro_entry_and_context_pending','native_plane_verified_not_actual_English_gameplay']",
        'current_native_voice_macro_entry_controls_and_context_pending=False,':'current_native_voice_macro_entry_controls_and_context_pending=False,current_native_voice_macro_entry_and_context_pending=False,native_plane_verified_not_actual_English_gameplay=False,actual_English_complete_panel_and_native_holds_verified=True,',
    })
    root=Path('work/analysis/lil_B202_completion_preparation_v6003b');root.mkdir(parents=True);save(root/'derivation.json',proof)
