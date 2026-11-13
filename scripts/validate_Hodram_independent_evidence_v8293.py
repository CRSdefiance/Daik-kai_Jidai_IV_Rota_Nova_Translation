"""Validate the production native/actual helper against existing immutable observations."""
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.hodram_three_blocks_references_v1 import reconstruct_and_bind,require
from dk4tool.patch.hodram_three_blocks_evidence_v1 import check_evidence
from scripts.Hodram_three_blocks_release_paths_v8290 import PARENT,ROM,DOC,proofs
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Hodram_independent_evidence_v8293')
if __name__=='__main__':
    assert not ROOT.exists();paths=proofs();data={k:read(p) for k,p in paths.items()};doc=read(DOC)
    parent,reference,clean=[NdsImage.open(p) for p in [PARENT,ROM,Path('work/clean.nds')]]
    rebuilt=reconstruct_and_bind(parent,clean,doc,data['relocation'],data['current'])
    result=check_evidence(data,doc['records'],parent,reference,rebuilt,read,require)
    ROOT.mkdir(parents=True);save(ROOT/'native56_body6_name_masks_six_fixture_traces262_actual_holds_recomputed.json',dict(result=result,
        no_saved_producer_script_replayed_no_emulator_orROM_mutation=True,
        atomic_stage_controls_comparison_corruption_tests_andregistered_release_pending=True,new_credit=0,full_goal_complete=False,
        evidence={str(p):sha(Path(p).read_bytes()) for p in [DOC,PARENT,ROM,Path(__file__),Path('dk4tool/patch/hodram_three_blocks_evidence_v1.py'),*map(Path,paths.values())]}))
    print('Independent native/actual:Hodram56bodypages/six names/six wholefixture traces/262complete body-name holds match. No new emulation orcredit.')
