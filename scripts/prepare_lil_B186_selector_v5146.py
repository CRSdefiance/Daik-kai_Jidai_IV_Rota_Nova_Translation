"""Bind the planner's explicit source selector guard to Owner174 and Cook175."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B186_selector_guard_v5146')
if __name__=='__main__':
    assert not ROOT.exists()
    rows=[derive('dk4tool/dialogue/lil_B186_layout_v1.py','dk4tool/dialogue/lil_B186_layout_v2.py',{'frozenset({164,165})':'frozenset({174,175})'})]
    rows.append(derive('scripts/plan_lil_B186_layout_v5144.py','scripts/plan_lil_B186_layout_v5147.py',{'lil_B186_layout_v1':'lil_B186_layout_v2','lil_B186_layout_v5144':'lil_B186_layout_v5147'}))
    rows.append(derive('scripts/verify_lil_B186_fonts_v5145.py','scripts/verify_lil_B186_fonts_v5148.py',{'lil_B186_layout_v1':'lil_B186_layout_v2','lil_B186_fonts_v5145':'lil_B186_fonts_v5148'}))
    ROOT.mkdir(parents=True);save(ROOT/'exact_source_selector_guard_successors.json',dict(derivations=rows,
        stopped_v5144_and_v1_preserved=True,reason='The inherited planner guard rejected all11 progressive speeches because it retained164/165. Source/name/dispatch proofs require174/175. FE254 already passed. Only the explicit guard identities change;all prose,metrics,controls and native constants stay exact.',
        no_wider_selector_acceptance=True,new_review_credit=0,full_goal_complete=False))
    print('Prepared exact174/175 guard successor;no prose,width,font or wrapping-cost change.')
