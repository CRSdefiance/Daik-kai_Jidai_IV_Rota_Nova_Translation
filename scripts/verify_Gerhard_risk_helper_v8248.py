"""Persist the independent eight-phase RAM/replay recomputation; no new gameplay or atomic-stage approval."""
import json
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.gerhard_surname_risk_v1 import check_bounded_risk
from dk4tool.dialogue.gerhard_surname_profile_v1 import contract
from scripts.Gerhard_surname_release_paths_v8238 import proofs
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/Gerhard_risk_helper_v8248')
def load(path):return json.loads(Path(path).read_bytes())
def require(ok,message):
    if not ok:raise ValueError(message)
if __name__=='__main__':
    assert not ROOT.exists();p=proofs();contract()
    result=check_bounded_risk(*[load(p[k]) for k in ['actual_comparison','actual_focus','actual']],load,require,load(p['reference_receipt']))
    contract();ROOT.mkdir(parents=True)
    evidence=[Path(__file__),Path('dk4tool/patch/gerhard_surname_risk_v1.py'),*[Path(p[k]) for k in ['actual_comparison','actual_focus','actual','reference_receipt']]]
    save(ROOT/'independent8phase_RAM_bytes_andexact_replay_recomputation.json',dict(**result,
        helper='dk4tool/patch/gerhard_surname_risk_v1.py',frozen_contract_revalidated_before_andafter=True,
        no_new_emulator_run_orrepeated_natural_playthrough=True,not_independent_atomic_production_approval=True,
        complete_comparison_field_semantics_atomic_stage_corruption_tests_registered_integration_remain_pending=True,
        evidence={str(path):sha(path.read_bytes()) for path in evidence},new_credit=0,new_emulator_runs=0,full_goal_complete=False))
    print('Independent8phase RAM/replay recomputation persisted;atomic production/challenges remainpending;no new gameplay.')
