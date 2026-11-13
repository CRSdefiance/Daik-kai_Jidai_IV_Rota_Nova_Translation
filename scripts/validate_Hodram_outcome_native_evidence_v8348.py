"""Positive independent production-native validation against immutable reviewed outcome artifacts."""
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.hodram_outcome_references_v1 import require
from dk4tool.patch.hodram_outcomes_native_evidence_v1 import check_native_models
from scripts.Hodram_outcomes_release_paths_v8347 import DOC,PARENT,proofs
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Hodram_outcome_native_evidence_v8348')
if __name__=='__main__':
    assert not ROOT.exists();data={k:read(p) for k,p in proofs().items()};doc=read(DOC)
    result=check_native_models(data,doc['records'],NdsImage.open(PARENT),read,require)
    ROOT.mkdir(parents=True);save(ROOT/'twelve_complete_native_body_pages_one_Lil_nameplane_recomputed.json',dict(result=result['summary'],no_saved_producer_script_oractual_scene_replayed=True,
        independent_actual_FE_VRAM_comparison_controls_atomic_andregistered_integration_pending=True,new_credit=0,full_goal_complete=False,
        evidence={str(p):sha(Path(p).read_bytes()) for p in [DOC,Path(__file__),Path('dk4tool/patch/hodram_outcomes_native_evidence_v1.py'),*proofs().values()]}))
    print('Independent productionnative:12complete source/stored bodyplanes andone currentLil style11nameplane recomputed;originalFE indices/geometry/font/bounds/consumption match.No new emulator run orcredit.')
