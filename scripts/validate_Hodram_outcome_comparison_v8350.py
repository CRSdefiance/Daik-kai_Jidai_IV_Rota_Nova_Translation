"""Recompute all bounded actual timing/state/RGB scope including nonzero B48 later differences."""
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.hodram_outcome_references_v1 import require
from dk4tool.patch.hodram_outcomes_comparison_v1 import check_comparisons
from scripts.Hodram_outcomes_release_paths_v8347 import PARENT,proofs
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Hodram_outcome_comparison_validation_v8350')
if __name__=='__main__':
    assert not ROOT.exists();data={k:read(p) for k,p in proofs().items()};result=check_comparisons(data,NdsImage.open(PARENT),read,require)
    ROOT.mkdir(parents=True);save(ROOT/'all_commands_scenes_final_native_states186_RGBpairs_andB48_differences_recomputed.json',dict(result=result,
        original_B48_timing_PRNG_and13later_RGB_differences_preserved=True,no_new_capture_ROM_write_orfull_simulation_claim=True,new_credit=0,full_goal_complete=False,
        evidence={str(p):sha(Path(p).read_bytes()) for p in [Path(__file__),Path('dk4tool/patch/hodram_outcomes_comparison_v1.py'),*proofs().values()]}))
    print('Independent comparison:all command/timing/UI/PRNG/six scene-headerpairs/four finalnative states/186wholeRGBpairs andB48nonzero differences recomputed;no replay orcredit.')
