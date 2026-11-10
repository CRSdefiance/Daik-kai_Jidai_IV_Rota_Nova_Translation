"""Retain the three prepared producers and qualify the unchanged pytest runner's actual schema."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/Hodram_B31_B53_integration_tools_v8776b');assert not root.exists()
    existing=[Path('scripts')/p for p in ['bind_Hodram_B31_B53_integration_v8776.py','register_Hodram_B31_B53_v8777.py','build_Hodram_B31_B53_v8778.py']]
    assert all(p.exists() for p in existing)
    regression=derive('scripts/run_Hodram_B52_regressions_v8704.py','scripts/run_Hodram_B31_B53_regressions_v8778.py',{
        'Hodram_B52_regressions_v8704':'Hodram_B31_B53_regressions_v8778',
    })
    root.mkdir(parents=True);save(root/'derivation.json',dict(regression=regression,existing_derived_outputs={str(p):sha(p.read_bytes()) for p in existing},
        stopped_preparer='scripts/prepare_Hodram_B31_B53_registered_integration_v8776.py',
        stopped_preparer_sha256=sha(Path('scripts/prepare_Hodram_B31_B53_registered_integration_v8776.py').read_bytes()),
        original_runner_has_no_ROM_orprofile_arguments_andall110_repository_tests_preserved=True,
        no_prepared_producer_overwritten_orreexecuted=True,no_registry_ROM_orcredit_change=True,full_goal_complete=False))
