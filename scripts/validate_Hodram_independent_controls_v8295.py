"""Check complete source-qualified controls, loader handoffs and caller census without scene replay."""
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.hodram_three_blocks_references_v1 import reconstruct_and_bind,require
from dk4tool.patch.hodram_three_blocks_controls_v1 import check_controls,check_loaders_and_census
from scripts.Hodram_three_blocks_release_paths_v8290 import PARENT,ROM,DOC,proofs
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Hodram_independent_controls_v8295')
if __name__=='__main__':
    assert not ROOT.exists();paths=proofs();data={k:read(p) for k,p in paths.items()};doc=read(DOC)
    parent,reference,clean=[NdsImage.open(p) for p in [PARENT,ROM,Path('work/clean.nds')]]
    rebuilt=reconstruct_and_bind(parent,clean,doc,data['relocation'],data['current'])
    controls=check_controls(data,doc['records'],parent,reference,rebuilt,read,require)
    entries=check_loaders_and_census(data,parent,reference,rebuilt,read,require)
    ROOT.mkdir(parents=True);save(ROOT/'28_dispatches24_controls40_relatives6_queries150_reused_ends325_loads650_modes_census_bound.json',dict(controls=controls,entries=entries,
        sourcequalified_original_effects_4800_layout0_4700_andall_full_terminals_preserved=True,
        native_boundary_evidence_not_full_scene_execution_orattainability_scope=True,
        atomic_production_corruption_tests_andregistered_release_pending=True,new_credit=0,new_emulator_runs=0,full_goal_complete=False,
        evidence={str(p):sha(Path(p).read_bytes()) for p in [DOC,PARENT,ROM,Path(__file__),Path('dk4tool/patch/hodram_three_blocks_controls_v1.py'),*map(Path,paths.values())]}))
    print('Independent controls:28dispatches/24controls/40relatives/6queries/150reused ends,325loads650modes/allEV1actions/shippedcaller census bound;no scene replay orcredit.')
