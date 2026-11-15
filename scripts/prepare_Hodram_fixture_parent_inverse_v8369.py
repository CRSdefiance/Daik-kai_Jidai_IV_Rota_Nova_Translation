"""Preserve the rejected builder's reader; bind the fixture inverse to validated in-memory predecessor bytes."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/Hodram_fixture_parent_inverse_tools_v8369');assert not root.exists()
    d=derive('dk4tool/patch/hodram_outcomes_actual_evidence_v1.py','dk4tool/patch/hodram_outcomes_actual_evidence_v2.py',{'parent.source.read_bytes()':'bytes(parent.rom.save())'})
    root.mkdir(parents=True);save(root/'whole_fixture_inverse_validated_inmemory_parent_not_original_disk_path.json',dict(derivation=d,failed_registered_profile='all-routes-unified-v8362',failed_build_terminal='work/analysis/Hodram_outcomes_build_v8362/build_terminal.json',no_candidate_ROM_orcompletion_credit_created=True,no_native_actual_pixel_control_orother_guard_changed=True,new_credit=0,full_goal_complete=False))
