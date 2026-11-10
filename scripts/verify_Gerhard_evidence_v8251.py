"""Positive independent production-evidence check; no changes to a ROM, registry or ledger."""
import json
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.gerhard_surname_rebuild_v1 import rebuild
from dk4tool.patch.gerhard_surname_evidence_v1 import check_evidence
from dk4tool.dialogue.gerhard_surname_profile_v1 import validate_approved_batch
from scripts.Gerhard_surname_release_paths_v8238 import proofs,APPROVED,PARENT,ROM
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/Gerhard_independent_evidence_v8251')
def load(p):return json.loads(Path(p).read_bytes())
def require(ok,message):
    if not ok:raise ValueError('Gerhard independent evidence: '+message)
if __name__=='__main__':
    assert not ROOT.exists();doc=load(APPROVED);validate_approved_batch(doc)
    parent,reference=map(NdsImage.open,[PARENT,ROM]);data={k:load(p) for k,p in proofs().items()}
    result=rebuild(parent.read_file('/data/SC2.DK4'),parent.read_file('/__arm9__.bin'),doc['records'])
    proof=check_evidence(data,doc['records'],parent,reference,result,load,require)
    ROOT.mkdir(parents=True);save(ROOT/'native_models_actual_masks_commands_andfixtures_independently_revalidated.json',dict(**proof,
        manuscript=str(APPROVED),manuscript_sha256=sha(APPROVED.read_bytes()),new_credit=0,new_emulator_runs=0,
        independent_atomic_stage_corruption_suite_andregistered_release_still_pending=True,full_goal_complete=False,
        evidence={str(p):sha(p.read_bytes()) for p in [Path(__file__),Path('dk4tool/patch/gerhard_surname_evidence_v1.py'),APPROVED]}))
    print('Independent actual/native evidence passes:30body/262name masks,all selected source/results/RNG/UI/timing;no replay orROM commit.')
