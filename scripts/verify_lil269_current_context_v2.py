"""Bind explicit plan paths while preserving all current-ROM snapshot/getter guards."""
from scripts.verify_lil269_current_context_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text
source=checked_text(previous, {
    'from scripts.prepare_lil269_current_context_v1 import ROOT, RELEASE, PRIOR':
        "ROOT=Path('work/Lil269_B243_B282_clean_20261110/current_context_v1')\nRELEASE=Path('work/lil382_residual_A_release_v1/registered_release_verification.json')\nPRIOR=Path('work/analysis/retrospective_Lil_context_runs_v7836/route2/run_plan.json')",
})
if __name__=='__main__':
    exec(compile(source,__file__+'::same-own-ROM-snapshot-andoriginal-getter-contract','exec'),globals())
