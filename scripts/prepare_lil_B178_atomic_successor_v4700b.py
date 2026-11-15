"""Correct an inherited ten-dispatch guard;preserve both failed registration inputs."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B178_atomic_successor_v4700b');assert not ROOT.exists()
compiler=derive('dk4tool/patch/lil_B178_editorial_v1.py','dk4tool/patch/lil_B178_editorial_v2.py',{
    "len(controls['relocated_dispatch_cases'])==10":"len(controls['relocated_dispatch_cases'])==13",
})
registration=derive('scripts/register_lil_B178_v4700.py','scripts/register_lil_B178_v4700b.py',{
    'lil_B178_editorial_v1':'lil_B178_editorial_v2',
    'lil_B178_registration_v4700':'lil_B178_registration_v4700b',
    'build_integrated_release_v4700.tmp':'build_integrated_release_v4700b.tmp',
})
ROOT.mkdir(parents=True)
save(ROOT/'source_derivation.json',dict(compiler=compiler,registration=registration,
    failure='Inherited dispatch count10 rejected correct13-dispatch B178 evidence during read-only positive compilation.',
    no_ROM_image_mutation_or_registry_builder_config_change_before_failure=True,
    failed_positive_config_and_producers_preserved=True,no_new_emulator_run_orcredit=True,full_goal_complete=False))
print('Prepared thirteen-dispatch compiler/registration successor;failed positive input and producers preserved.')
