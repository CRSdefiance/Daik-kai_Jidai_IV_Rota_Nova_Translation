"""Require B229's actual no-tail source, preserving the rejected B228-tail inheritance."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B229_fixture_tail_repair_v7387b')
if __name__=='__main__':
    assert not ROOT.exists() and not Path('out/lil_B229_source_v7387_clean_Japanese_RESEARCH_ONLY.nds').exists()
    r=derive('scripts/research_lil_B229_source_fixture_v7387.py','scripts/research_lil_B229_source_fixture_v7387b.py',{'jp[end:]==bytes(2)':'jp[end:]==bytes(0)'});ROOT.mkdir(parents=True);save(ROOT/'source_locked_B229_no_tail.json',dict(tool=r,source944_logical944_tail0_bound=True,first_fixture_rejected_before_ROM_archive_orpin_write=True,no_dialogue_runtime_orinput_change=True,new_credit=0,full_goal_complete=False))
