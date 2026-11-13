"""Independently remeasure saved comparisons without any emulator replay or ROM mutation."""
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.gerhard_surname_comparison_v1 import check_comparisons
from scripts.verify_Gerhard_evidence_v8251 import load,require
from scripts.Gerhard_surname_release_paths_v8238 import proofs,PARENT,ROM
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/Gerhard_independent_comparison_v8252')
if __name__=='__main__':
    assert not ROOT.exists();paths=proofs()
    result=check_comparisons(load(paths['actual_comparison']),load(paths['actual']),NdsImage.open(PARENT),NdsImage.open(ROM),load,require)
    ROOT.mkdir(parents=True);save(ROOT/'all_saved_command_RGB_andfinal_native_values_recomputed.json',dict(**result,
        independent_atomic_stage_corruption_suite_andregistered_release_still_pending=True,new_credit=0,new_emulator_runs=0,full_goal_complete=False,
        evidence={str(p):sha(p.read_bytes()) for p in [Path(__file__),Path('dk4tool/patch/gerhard_surname_comparison_v1.py'),Path(paths['actual']),Path(paths['actual_comparison'])]}))
    print('All3 pairs independently remeasured:command/timing/RNG/UI,117scene pairs,598laterRGB pairs,finalnative components;no replay.')
