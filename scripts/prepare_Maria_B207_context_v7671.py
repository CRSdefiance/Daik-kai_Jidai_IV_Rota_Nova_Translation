"""Keep all current2b6 native guards; require the separately captured actual Maria captain3."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/maria_B207_context_tools_v7671')
if __name__=='__main__':
    assert not ROOT.exists()
    tool=derive('scripts/square_shopkeeper_exact_native_context_v7020.py','scripts/maria_current_native_context_v7671.py',{'class CurrentContext:':'class MariaCurrentContext:','assert get(0x7F244)==2':'assert get(0x7F244)==3'})
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_strict_Maria_current_context.json',dict(tool=tool,separate_class_requires_actual_own_current_captain3=True,all_original2b6_COMMON_directory123264_payload_executed_instruction_actor_andownership_guards_preserved=True,no_historical_ROM_RAM_overlay_orold_payload_guard_reuse=True,original_Lil_Rafael_Hodram_context_classes_unchanged=True,new_credit=0,full_goal_complete=False))
