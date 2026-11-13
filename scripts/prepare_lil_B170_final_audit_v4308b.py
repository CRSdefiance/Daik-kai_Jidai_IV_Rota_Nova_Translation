"""Preserve the stale B169 audit-key failure and inspect the current B170 key."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT = Path('work/analysis/lil_B170_final_audit_tools_v4308b')

if __name__ == '__main__':
    assert not ROOT.exists()
    tool = derive('scripts/verify_editorial_handoff_v4308.py','scripts/verify_editorial_handoff_v4308b.py',{
        'editorial_handoff_verification_v4308':'editorial_handoff_verification_v4308b',
        'actual_source_event169_selected':'actual_source_event170_selected',
    })
    ROOT.mkdir(parents=True)
    save(ROOT/'source_derivation.json',dict(tool=tool,
        correction='The copied auditor retained the predecessor event169 field name. Final B170 records correctly contain actual_source_event170_selected=False. Preserve the failed auditor;its successor reads that current field and retains the no-natural-activation gate.',
        no_ROM_registry_ledger_orcredit_change=True,full_goal_complete=False))
