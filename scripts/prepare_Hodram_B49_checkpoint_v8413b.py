"""Correct overlapping textual metadata substitutions before staging authoritative progress."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

if __name__=='__main__':
    root=Path('work/analysis/Hodram_B49_checkpoint_tools_v8413b');assert not root.exists()
    result=derive('scripts/checkpoint_Hodram_B49_v8413.py','scripts/checkpoint_Hodram_B49_v8413b.py',{
        'new_emulator_runs=2,new_actual_frames=0,new_research_ROMs=0':'new_emulator_runs=2,new_actual_frames=20002,new_research_ROMs=3',
    })
    root.mkdir(parents=True);save(root/'derivation.json',dict(derivation=result,unexecuted_predecessor_preserved=True,only_verified_handoff_actual_coverage_metadata_corrected=True,no_native_ROM_ledger_counter_orprose_change=True))
