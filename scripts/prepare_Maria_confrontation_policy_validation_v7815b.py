"""Preserve the schema-key failure;bind the existing plan-adapter key without changing output."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/maria_confrontation_policy_validation_tools_v7815b')
if __name__=='__main__':
    assert not ROOT.exists();results=[]
    results.append(derive('dk4tool/dialogue/maria_B36_plan_v1.py','dk4tool/dialogue/maria_B36_plan_v2.py',{
        "['source_owned_automatic_plan_adapter']":"['source_owned_plan_adapter']",
    }))
    results.append(derive('dk4tool/dialogue/maria_B36_layout_v1.py','dk4tool/dialogue/maria_B36_layout_v2.py',{
        'maria_B36_plan_v1':'maria_B36_plan_v2',
    }))
    results.append(derive('scripts/validate_Maria_confrontation_policy_v7815.py','scripts/validate_Maria_confrontation_policy_v7815b.py',{
        'maria_B36_layout_v1':'maria_B36_layout_v2',
        'from scripts.freeze_Maria_confrontation_policy_v7814 import MANUSCRIPT,CONTRACT,PROFILE,FORMATTER,PLANNER':
        'from scripts.Maria_B36_policy_paths_v7815b import MANUSCRIPT,CONTRACT,PROFILE,FORMATTER,PLANNER',
        'maria_confrontation_policy_validation_v7815':'maria_confrontation_policy_validation_v7815b',
    }))
    ROOT.mkdir(parents=True);save(ROOT/'provenance.json',dict(derivations=results,
        original_7815_KeyError_before_validation_preserved_not_counted_asguard_rejection=True,
        source_owned_plan_adapter_existing_key_bound_no_plan_orcontract_data_changes=True,
        all_original_native_numbers_source_prose_compiled_QA_guards_andsoft_wrap_pairs_preserved=True,
        no_native_font_getter_alignment_oractual_checks_replayed=True,
        no_ROM_registry_ledger_orcredit_change=True,full_goal_complete=False))
