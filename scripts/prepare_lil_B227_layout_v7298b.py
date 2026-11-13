"""Bind the planner to the reviewed sentence successor; preserve every native rule."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B227_layout_tools_v7298b')
if __name__=='__main__':
    assert not ROOT.exists()
    r=derive('scripts/plan_lil_B227_layout_v7298.py','scripts/plan_lil_B227_layout_v7298b.py',{'manuscript_v1.json':'manuscript_v1b.json','layout_v7298':'layout_v7298b'})
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_reviewed_prose_planner.json',r)
