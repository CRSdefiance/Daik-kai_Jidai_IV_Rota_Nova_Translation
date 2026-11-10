"""Preserve the passing v1 stage and add independent dispatch/query/terminal associations in v2."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/Gerhard_atomic_tools_v8255')
if __name__=='__main__':
    assert not ROOT.exists()
    receipts=[]
    receipts.append(derive('dk4tool/patch/gerhard_surname_editorial_v1.py','dk4tool/patch/gerhard_surname_editorial_v2.py',{
        "CONFIG='translations/gerhard_surname_editorial_release_v1.json'":"CONFIG='translations/gerhard_surname_editorial_release_v2.json'",
        'from dk4tool.patch.gerhard_surname_risk_v1 import check_bounded_risk':'from dk4tool.patch.gerhard_surname_risk_v1 import check_bounded_risk\nfrom dk4tool.patch.gerhard_surname_native_associations_v1 import check_final_native_associations',
        '    check_controls(data,result,sourcegroups,require)':'    check_final_native_associations(data,result,sourcegroups,load,require)\n    check_controls(data,result,sourcegroups,require)',
    }))
    receipts.append(derive('scripts/pin_Gerhard_production_v8253.py','scripts/pin_Gerhard_production_v8255.py',{
        'Gerhard_production_tools_v8253':'Gerhard_production_tools_v8255',
        'gerhard_surname_editorial_release_v1.json':'gerhard_surname_editorial_release_v2.json',
        "'gerhard_surname_editorial_v1.py'":"'gerhard_surname_editorial_v2.py','gerhard_surname_native_associations_v1.py'",
    }))
    receipts.append(derive('scripts/validate_Gerhard_atomic_positive_v8254.py','scripts/validate_Gerhard_atomic_positive_v8256.py',{
        'gerhard_surname_editorial_v1':'gerhard_surname_editorial_v2','Gerhard_atomic_positive_v8254':'Gerhard_atomic_positive_v8256',
    }))
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_successors.json',dict(derivations=receipts,all_original_native_literals_guards_andprose_preserved=True,new_credit=0,full_goal_complete=False))
