"""Independent positive production validation of actual original FE descriptors/VRAM/palette/RGB."""
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.hodram_outcome_references_v1 import require
from dk4tool.patch.hodram_outcomes_native_evidence_v2 import check_native_models
from dk4tool.patch.hodram_outcomes_FE_evidence_v2 import check_FE_geometry
from scripts.Hodram_outcomes_release_paths_v8347 import DOC,PARENT,proofs
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Hodram_outcome_FE_evidence_v8351b')
if __name__=='__main__':
    assert not ROOT.exists();data={k:read(p) for k,p in proofs().items()};doc=read(DOC);parent=NdsImage.open(PARENT);native=check_native_models(data,doc['records'],parent,read,require);result=check_FE_geometry(data,parent,native,read,require)
    ROOT.mkdir(parents=True);save(ROOT/'two_original_FE_snapshots_four_live_VRAM_palette_RGB_holds_recomputed.json',dict(result=result,no_saved_producer_oractual_capture_replayed=True,independent_controls_atomic_challenges_andregistered_integration_pending=True,new_credit=0,full_goal_complete=False,
        evidence={str(p):sha(Path(p).read_bytes()) for p in [DOC,Path(__file__),Path('dk4tool/patch/hodram_outcomes_FE_evidence_v2.py'),Path('scripts/actual_Hodram_FE_VRAM_v8338b.py'),*proofs().values()]}))
    print('Independent FE:2originalpaint snapshots/4liveVRAM bitmap-palette-RGB holds recomputed;temporary context/persistent view andactualVRAM distinction preserved.No capture replay orcredit.')
