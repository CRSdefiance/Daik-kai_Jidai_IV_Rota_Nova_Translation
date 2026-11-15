"""Positive independent production validation of the complete six-record control/loader scope."""
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.hodram_outcome_references_v1 import reconstruct_and_bind,require
from dk4tool.patch.hodram_outcomes_native_evidence_v2 import check_native_models
from dk4tool.patch.hodram_outcomes_controls_v1 import check_controls,check_loaders_and_census
from scripts.Hodram_outcomes_release_paths_v8347 import DOC,PARENT,ROM,proofs
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Hodram_outcome_controls_validation_v8353')
if __name__=='__main__':
    assert not ROOT.exists();data={k:read(p) for k,p in proofs().items()};doc=read(DOC);parent=NdsImage.open(PARENT);reference=NdsImage.open(ROM);clean=NdsImage.open('work/clean.nds')
    rebuilt=reconstruct_and_bind(parent,clean,doc,data['relocation'],data['current']);native=check_native_models(data,doc['records'],parent,read,require)
    control=check_controls(data,doc['records'],parent,reference,rebuilt,native,read,require);loader=check_loaders_and_census(data,parent,reference,rebuilt,read,require)
    ROOT.mkdir(parents=True);save(ROOT/'six_dispatches_two_EV1_entries100_endcases14_opaque_decodes325_loads650_modes_recomputed.json',dict(controls=control,loaders=loader,all_existing_actual_capture_evidence_reused_no_emulator_runs=True,atomic_challenges_registered_integration_andonce_only_credit_pending=True,new_credit=0,full_goal_complete=False,
        evidence={str(p):sha(Path(p).read_bytes()) for p in [DOC,Path(__file__),Path('dk4tool/patch/hodram_outcomes_controls_v1.py'),Path('dk4tool/patch/hodram_outcomes_loaders_v1.py'),*proofs().values()]}))
    print('Independent controls:6dispatches/2EV1entries/100ends/14opaque decodes;325loads-cache/650modes/326actions/census bound.No ROMwrite orcredit.')
