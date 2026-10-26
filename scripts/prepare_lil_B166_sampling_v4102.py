"""Derive the cold-boot sampler, retaining actual menu input and read-only observation."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save
ROOT = Path('work/analysis/lil_B166_sampling_tools_v4102')
if __name__ == '__main__':
    assert not ROOT.exists()
    pair = derive('scripts/run_lil_B164_display_fixture_v3993.py', 'scripts/run_lil_B166_display_fixture_v4103.py', {
        'lil_B164_display_fixture_v3992': 'lil_B166_display_fixture_v4101',
        'lil_B164_display_run_v3993': 'lil_B166_display_run_v4103',
        'lil_B164_display_v3993': 'lil_B166_display_v4103',
        "'native_script_observation.json'": "'commands.json'",
        'source_event164_not_selected': 'source_event166_not_selected',
        "displayed_original_source_block':164": "displayed_original_source_block':166",
        'B164-retained-choice-content-fixture': 'B166-retained-choice-content-fixture',
    })
    ROOT.mkdir(parents=True)
    save(ROOT / 'source_derivation.json', dict(tool=pair, actual_source_membership_and_choice_containers_preserved=True,
        source_event166_not_selected=True, four_paired_cold_boots_planned_not_yet_claimed=True))
    print('B166 paired actual-menu runner created;four planned cold boots,no current gameplay claim.')
