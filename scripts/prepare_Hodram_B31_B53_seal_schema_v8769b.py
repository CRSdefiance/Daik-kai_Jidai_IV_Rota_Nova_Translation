"""Qualify the own-current context's actual candidate_sha256 field; preserve stopped preparer."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/Hodram_B31_B53_seal_schema_v8769b');assert not root.exists()
    receipt=derive('scripts/prepare_Hodram_B31_B53_seal_v8769.py','scripts/prepare_Hodram_B31_B53_seal_v8769b.py',{
        'Hodram_B31_B53_seal_tools_v8769':'Hodram_B31_B53_seal_tools_v8769b',
        'current_ROM_sha256':'candidate_sha256',
    })
    root.mkdir(parents=True);save(root/'derivation.json',dict(tool=receipt,source_context_key_exact_from_existing_controls_receipt=True,
        stopped_preparer_preserved_no_partial_seal_orconfig_had_been_written=True,all_previous_guard_logic_preserved=True,new_credit=0,full_goal_complete=False))
