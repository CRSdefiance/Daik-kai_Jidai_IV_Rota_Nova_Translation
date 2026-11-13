"""Bind the actual B221 current control-case label; preserve the first partial producer."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B221_control_binding_tools_v7000b')
if __name__=='__main__':
    assert not ROOT.exists()
    row=derive('scripts/prove_lil_B221_relocated_controls_v7000.py','scripts/prove_lil_B221_relocated_controls_v7000b.py',{
        'relocated_controls_v7000':'relocated_controls_v7000b',
        "r['version']=='current-English'":"r['version']=='current'"})
    ROOT.mkdir(parents=True)
    save(ROOT/'source_control_case_label_binding.json',dict(derivation=row,
        failure='Original B221 source/current control proof labels its second case current, rather than current-English.',
        original_producer_and_partial_context_preserved=True,
        exact_source_control_bytes_native_addresses_and_all_checks_unchanged=True,
        no_ROM_change_or_credit=True,full_goal_complete=False))
