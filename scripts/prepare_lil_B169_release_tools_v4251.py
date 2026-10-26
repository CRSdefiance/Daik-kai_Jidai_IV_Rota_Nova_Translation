"""Prepare the cumulative V4251 builder, exact patch and registered startup checks."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT = Path('work/analysis/lil_B169_release_tools_v4251')
if __name__ == '__main__':
    assert not ROOT.exists()
    tools = [derive('scripts/build_lil_B168_v4204.py','scripts/build_lil_B169_v4251.py',{
        'lil_B168_build_v4204':'lil_B169_build_v4251',
        'all_routes_combined_v4204':'all_routes_combined_v4251',
        'lil_B168_registration_v4203':'lil_B169_registration_v4250b',
        'all-routes-unified-v4204':'all-routes-unified-v4251',
    })]
    tools.append(derive('scripts/verify_lil_B168_release_v4205.py','scripts/verify_lil_B169_release_v4252.py',{
        'lil_B168_editorial_v1':'lil_B169_editorial_v2',
        'lil_B168_release_v4205':'lil_B169_release_v4252',
        'all_routes_combined_v4204':'all_routes_combined_v4251',
        'all_routes_combined_v4160':'all_routes_combined_v4204',
        'lil_B168_registration_v4203':'lil_B169_registration_v4250b',
        'all-routes-unified-v4204':'all-routes-unified-v4251',
        'all-routes-unified-v4160':'all-routes-unified-v4204',
        'lil_B168_editorial':'lil_B169_editorial',
        "len(manifest['batches'])==544":"len(manifest['batches'])==545",
        'lil_mikhail':'lil_proof',
        'all544_manifest_batches_and114_accepted_layers_present':'all545_manifest_batches_and114_accepted_layers_present',
        'all_earlier_profiles_and_V4160_promotion_unchanged':'all_earlier_profiles_and_V4204_promotion_unchanged',
        'every_other_file_font_graphic_route_ARM9_ARM7_and_component_exact_to_V4160':'every_other_file_font_graphic_route_ARM9_ARM7_and_component_exact_to_V4204',
        'manifest_batches=544':'manifest_batches=545',
    }))
    tools.append(derive('scripts/run_lil_B168_startup_v4206.py','scripts/run_lil_B169_startup_v4253.py',{
        'lil_B168_runs_v4206':'lil_B169_runs_v4253','lil_B168_v4206':'lil_B169_v4253',
        'version=4204':'version=4251','B168':'B169',
    }))
    tools.append(derive('scripts/verify_lil_B168_startup_v4207.py','scripts/verify_lil_B169_startup_v4254.py',{
        'lil_B168_startup_v4207':'lil_B169_startup_v4254',
        'lil_B168_runs_v4206':'lil_B169_runs_v4253',
        'all_routes_combined_v4204':'all_routes_combined_v4251',
        'all_routes_combined_v4160':'all_routes_combined_v4204',
        'lil_B167_runs_v4162':'lil_B168_runs_v4206',
        'V4160':'V4204','Current4204':'Current4251','B168':'B169',
    }))
    tools.append(derive('scripts/record_lil_B168_startup_view_v4207.py','scripts/record_lil_B169_startup_view_v4254.py',{
        'lil_B168_startup_v4207':'lil_B169_startup_v4254','V4160':'V4204','B168':'B169',
    }))
    ROOT.mkdir(parents=True)
    save(ROOT/'source_derivation.json',dict(tools=tools,expected_manifest_batches=545,accepted_layers=114,
        existing_V4204_promotion_preserved=True,no_build_patch_or_startup_claim_yet=True))
    print('V4251 cumulative build/patch/startup tools prepared;545 batches expected,V4204 remains main.')
