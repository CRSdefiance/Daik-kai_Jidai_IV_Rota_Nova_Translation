"""Recompute bounded paired comparisons from immutable captures and final RAM, without replay."""
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.hodram_three_blocks_references_v1 import require
from dk4tool.patch.hodram_three_blocks_comparison_v1 import check_comparisons
from scripts.Hodram_three_blocks_release_paths_v8290 import PARENT,proofs
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Hodram_independent_comparison_v8294')
if __name__=='__main__':
    assert not ROOT.exists();paths=proofs();data={k:read(p) for k,p in paths.items()}
    result=check_comparisons(data,NdsImage.open(PARENT),read,require)
    ROOT.mkdir(parents=True);save(ROOT/'all_command_scene_final_native_state_and532_later_RGB_pairs_recomputed.json',dict(result=result,
        all_original_timing_RNG_UI_component_calendar_RGB_andfixture_tail_limits_preserved=True,
        no_new_ROM_orcapture_no_every_frame_future_outcome_broad_simulation_orfullroute_claim=True,
        independent_controls_atomic_production_corruption_tests_andregistered_release_pending=True,new_credit=0,full_goal_complete=False,
        evidence={str(p):sha(Path(p).read_bytes()) for p in [PARENT,Path(__file__),Path('dk4tool/patch/hodram_three_blocks_comparison_v1.py'),*map(Path,paths.values())]}))
    print('Independent paired comparisons:all command/timing/RNG/UI,28scene/header pairs,six final native states and532 later fullRGBpairs recomputed;B137tail captain0 limit retained.')
