"""Preserve the stale-derivation-key failure; useonly the actual verified v3 predecessor."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/maria_B36_production_repair_tools_v7818b');assert not root.exists()
    result=derive('scripts/prepare_Maria_B36_production_v7818.py','scripts/prepare_Maria_B36_production_fixed_v7818b.py',{
        "        'expected=[(34,[6295,6295],7,0,0,163),(108,[11336,11575],37,14,75,75),(35,[11335,11334],35,8,60,79)]':\n        'expected=[(36,[8213,8216],18,6,108,131)]',\n":"",
        'maria_B36_production_tools_v7818':'maria_B36_production_tools_v7818b',
        'validate_Maria_B36_atomic_v7818.py':'validate_Maria_B36_atomic_v7818b.py',
        'maria_B36_atomic_v7818':'maria_B36_atomic_v7818b',
    })
    root.mkdir(parents=True);save(root/'provenance.json',dict(derivation=result,
        stale_v2_expected_table_key_removed_only_actual_v3_table_is_transformed=True,
        original_7818_failed_before_any_production_output_ROM_registry_orledger_write=True,
        all_native_numeric_constants_source_andatomic_guards_preserved=True,new_credit=0,full_goal_complete=False))
