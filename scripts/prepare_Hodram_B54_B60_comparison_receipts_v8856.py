"""Add incremental receipts to the not-yet-executed comparison validator, retaining every guard."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/Hodram_B54_B60_comparison_receipt_tools_v8856');assert not root.exists()
    result=derive('scripts/validate_Hodram_B54_B60_comparison_v8849.py','scripts/validate_Hodram_B54_B60_comparison_v8849b.py',{
        '    cases=[]':"    ROOT.mkdir(parents=True)\n    save(ROOT/'partial_comparison_validation.json',dict(comparison_summary=result,negative_cases=[],terminal=False,new_credit=0,full_goal_complete=False))\n    print('All14 saved final snapshots/335RGBpairs/81prefixcallbacks independently pass;starting16 changed-input cases.',flush=True)\n    cases=[]",
        "cases.append(dict(label=label,actual_changed_input=True,rejected=True,diagnostic=message))":"cases.append(dict(label=label,actual_changed_input=True,rejected=True,diagnostic=message))\n            save(ROOT/'partial_comparison_validation.json',dict(comparison_summary=result,negative_cases=cases,terminal=False,new_credit=0,full_goal_complete=False))\n            print('COMPARISON_REJECT',len(cases),label,flush=True)",
        "ROOT.mkdir(parents=True);save(ROOT/'independent_comparison_validation.json'":"save(ROOT/'independent_comparison_validation.json'",
    })
    root.mkdir(parents=True);save(root/'source_locked_receipts.json',dict(derivation=result,all_existing_semantic_andprotected_file_guards_preserved=True,only_incremental_console_andimmutable_result_receipts_added=True,no_validator_replay=True,new_credit=0,full_goal_complete=False))
