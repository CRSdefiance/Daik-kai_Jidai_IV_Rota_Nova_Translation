"""Bind both typed commands to their measured D0 selector; preserve the rejected assertion."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B209_clean_tools_v6447b')
if __name__=='__main__':
    assert not ROOT.exists()
    r=derive('scripts/expand_lil_B209_clean_v6447.py','scripts/expand_lil_B209_clean_v6447b.py',{
        "==[208,0]":"==[208,208]",
        'clean_v6447\')':'clean_v6447b\')',
        'current_actor_selector0_andD0_roles':'current_actor_selectorD0_role',
    })
    ROOT.mkdir(parents=True);save(ROOT/'source_selector_correction.json',dict(tool=r,prior_rejected_assertion='Expected [208,0];actual source headers at8/702 both end00d0. No output or shared mutation occurred before rejection.',source_bound_selectors=[208,208],all_original_getters_and_guards_unchanged=True,full_goal_complete=False))
