"""Preserve interrupted test; distinguish tuple/list inputs in challenge receipts."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

if __name__ == '__main__':
    root = Path('work/analysis/Hodram_B52_policy_tools_v8664b')
    assert not root.exists()
    receipt = derive('scripts/validate_Hodram_B52_policy_v8664.py', 'scripts/validate_Hodram_B52_policy_v8664b.py', {
        'work/analysis/Hodram_B52_policy_validation_v8664': 'work/analysis/Hodram_B52_policy_validation_v8664b',
        "json.dumps(value, ensure_ascii=False, sort_keys=True, default=repr)": "json.dumps([type(value).__name__, value], ensure_ascii=False, sort_keys=True, default=repr)",
    })
    root.mkdir(parents=True)
    save(root / 'derivation.json', dict(derivation=receipt,
         failure='Challenge recorder serialized a tuple and list identically and stopped before calling the not-list rejection. Preserve input types in receipt hashes; compiler and all frozen guards remain unchanged.',
         original_executed_runner_andpartial_stdout_preserved=True,
         no_completed_policy_receipt_exists_so_successor_finishes_validation=True,
         no_native_CPU_probe_oractual_capture_replay=True))
