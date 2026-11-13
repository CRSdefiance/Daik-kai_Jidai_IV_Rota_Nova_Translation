"""Preserve8317 syntax attempt; remove only the unmatched metadata-assembly parenthesis."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/Hodram_current_tools_v8317b');assert not root.exists()
    result=derive('scripts/map_Hodram_B47_B48_current_v8317.py','scripts/map_Hodram_B47_B48_current_v8317b.py',{
        'Hodram_B47_B48_current_v8317':'Hodram_B47_B48_current_v8317b',
        'source_prose_orcompletion_credit_added=False,prose_formatting_actual_effects_andregistered_release_pending=True))':'source_prose_orcompletion_credit_added=False,prose_formatting_actual_effects_andregistered_release_pending=True)',
    })
    root.mkdir(parents=True);save(root/'syntax_only_successor.json',dict(derivation=result,failed_syntax_producer_preserved=True,no_native_guard_orinput_change=True,new_credit=0))
