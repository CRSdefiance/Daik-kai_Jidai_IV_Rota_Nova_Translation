"""Publish the already completed14 rejection results after the duplicate-key receipt failure; no rerun."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B215_atomic_v6773b');POS=Path('work/analysis/lil_B215_atomic_v6772/positive_receipt.json');CASES=Path('work/analysis/lil_B215_atomic_v6773/negative_cases.json')
if __name__=='__main__':
    assert not ROOT.exists();positive=read(POS);cases=read(CASES);conf=read(positive['config']);assert len(cases)==len({r['case'] for r in cases})==14 and all(r['rejected'] and r['archive_writes']==0 for r in cases) and sha(Path(positive['config']).read_bytes())==positive['config_sha256'] and sha(Path(positive['parent_ROM']).read_bytes())==positive['parent_ROM_sha256']
    for p,h in conf['dependencies'].items():assert sha(Path(p).read_bytes())==h
    receipt=deepcopy(positive);receipt.update(negative_cases=str(CASES),negative_cases_sha256=sha(CASES.read_bytes()),negative_count=14,all_negatives_reject_before_mutation=True,virtual_JSON_separately_tests_semantics_behind_valid_physical_hashes=True,three_warning_decisions_and_measured_later_world_limits_bound=True,all14_checks_already_finished_before_original_publication_failure=True,no_positive_native_rejection_or_gameplay_checks_replayed=True,publication_failure='dict(**positive,...,full_goal_complete=False) repeated an existing key after all14 cases and source-hash checks passed; preserve original producer and saved cases.',failed_producer_sha256=sha(Path('scripts/challenge_lil_B215_atomic_v6773.py').read_bytes()),new_ROMs=0,new_credit=0,full_goal_complete=False);ROOT.mkdir(parents=True);save(ROOT/'atomic_validation_receipt.json',receipt);print('Recovered publication of14 completed zero-write rejections; no checks or emulator runs repeated.')
