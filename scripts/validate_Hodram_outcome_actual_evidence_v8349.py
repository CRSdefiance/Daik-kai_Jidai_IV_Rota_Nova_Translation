"""Independent production actual-evidence validation without rerunning emulator captures."""
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.hodram_outcome_references_v1 import reconstruct_and_bind,require
from dk4tool.patch.hodram_outcomes_native_evidence_v1 import check_native_models
from dk4tool.patch.hodram_outcomes_actual_evidence_v1 import check_actual
from scripts.Hodram_outcomes_release_paths_v8347 import DOC,PARENT,proofs
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Hodram_outcome_actual_evidence_v8349')
if __name__=='__main__':
    assert not ROOT.exists();data={k:read(p) for k,p in proofs().items()};doc=read(DOC);parent=NdsImage.open(PARENT);clean=NdsImage.open('work/clean.nds')
    rebuilt=reconstruct_and_bind(parent,clean,doc,data['relocation'],data['current']);native=check_native_models(data,doc['records'],parent,read,require);result=check_actual(data,doc['records'],parent,clean,rebuilt,native,read,require)
    ROOT.mkdir(parents=True);save(ROOT/'four_whole_fixtures_all_original_traces_and100_actual_body_name_FE_holds_recomputed.json',dict(result=result,native_summary=native['summary'],no_saved_producer_oractual_emulator_capture_replayed=True,independent_FE_geometry_later_comparisons_controls_atomic_andregistered_integration_pending=True,new_credit=0,full_goal_complete=False,
        evidence={str(p):sha(Path(p).read_bytes()) for p in [DOC,Path(__file__),Path('dk4tool/patch/hodram_outcomes_actual_evidence_v1.py'),Path('dk4tool/patch/hodram_outcomes_native_evidence_v1.py'),*proofs().values()]}))
    print('Independent actual:four whole ROMfixtures/all original commandtraces/100complete nativebody-name orFE-absentheader holds recomputed.No capture rerun orcredit.')
