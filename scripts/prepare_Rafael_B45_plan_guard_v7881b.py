"""Replace an unnecessary dead preparatory assertion; the real current-ARM9 binding stays intact."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/Rafael_B45_plan_guard_tools_v7881b');assert not root.exists()
    result=derive('scripts/plan_Rafael_B45_layout_v7881.py','scripts/plan_Rafael_B45_layout_v7881b.py',{
        'work/analysis/Rafael_B45_layout_v7881':'work/analysis/Rafael_B45_layout_v7881b',
        "assert len(measured['cases'])==32 and measured['ARM9_sha256']==bound_ARM9 if False else True":
        "assert len(measured['cases'])==32",
    })
    root.mkdir(parents=True);save(root/'provenance.json',dict(derivation=result,
        real_ARM9_binding_below_source_load_unchanged=True,actual32_measurement_count_now_checked_atboth_points=True,
        no_prose_layout_native_orQA_change=True,prior_producer_andoutputs_preserved=True,new_credit=0,full_goal_complete=False))
