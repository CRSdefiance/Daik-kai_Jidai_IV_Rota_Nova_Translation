"""Preserve rejected preflight and bind the actual B228 source-run label before any ROM write."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B228_English_tools_v7358b')
if __name__=='__main__':
    assert not ROOT.exists() and not Path('out/lil_B228_English_v7358_reviewed_English_RESEARCH_ONLY.nds').exists() and not Path('scripts/research_lil_B228_English_fixture_v7358b.py').exists()
    r=derive('scripts/research_lil_B228_English_fixture_v7358.py','scripts/research_lil_B228_English_fixture_v7358b.py',{'source_run_v7246':'source_run_v7341'});ROOT.mkdir(parents=True);save(ROOT/'source_locked_runner_label_repair.json',dict(tool=r,first_fixture_rejected_before_ROM_orarchive_orpin_mutation=True,actual_source_run7341_required=True,no_dialogue_runtime_orinput_change=True,new_credit=0,full_goal_complete=False))
