"""Derive cumulative V4204 build, clean patch and fresh registered startup checks."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT = Path('work/analysis/lil_B168_release_tools_v4204')
if __name__ == '__main__':
    assert not ROOT.exists()
    tools = []
    tools.append(derive('scripts/build_lil_B167_v4160.py', 'scripts/build_lil_B168_v4204.py', {
        'lil_B167_build_v4160': 'lil_B168_build_v4204', 'all_routes_combined_v4160': 'all_routes_combined_v4204',
        'lil_B167_registration_v4159b': 'lil_B168_registration_v4203', 'all-routes-unified-v4160': 'all-routes-unified-v4204',
    }))
    tools.append(derive('scripts/verify_lil_B167_release_v4161.py', 'scripts/verify_lil_B168_release_v4205.py', {
        'lil_B167_editorial_v2': 'lil_B168_editorial_v1', 'lil_B167_release_v4161': 'lil_B168_release_v4205',
        'all_routes_combined_v4160': 'all_routes_combined_v4204', 'all_routes_combined_v4110': 'all_routes_combined_v4160',
        'lil_B167_registration_v4159b': 'lil_B168_registration_v4203', 'all-routes-unified-v4160': 'all-routes-unified-v4204',
        "registry['profiles']['all-routes-unified-v4110']": "registry['profiles']['all-routes-unified-v4160']",
        'lil_B167_editorial': 'lil_B168_editorial', "len(manifest['batches'])==543": "len(manifest['batches'])==544",
        "[normal(conf['manuscript']),normal(conf['choices'])]": "[normal(conf['manuscript'])]",
        "registry['latest_promoted_build']['profile']=='all-routes-unified-v4046'": "registry['latest_promoted_build']['profile']=='all-routes-unified-v4160'",
        'lil_sail_lesson': 'lil_mikhail', 'all543_manifest_batches_and114_accepted_layers_present': 'all544_manifest_batches_and114_accepted_layers_present',
        'all_earlier_profiles_and_V4046_promotion_unchanged': 'all_earlier_profiles_and_V4160_promotion_unchanged',
        'every_other_file_font_graphic_route_ARM9_ARM7_and_component_exact_to_V4110': 'every_other_file_font_graphic_route_ARM9_ARM7_and_component_exact_to_V4160',
        'manifest_batches=543': 'manifest_batches=544',
    }))
    tools.append(derive('scripts/run_lil_B167_startup_v4162.py', 'scripts/run_lil_B168_startup_v4206.py', {
        'lil_B167_runs_v4162': 'lil_B168_runs_v4206', 'lil_B167_v4162': 'lil_B168_v4206', 'version=4160': 'version=4204', 'B167': 'B168',
    }))
    tools.append(derive('scripts/verify_lil_B167_startup_v4163.py', 'scripts/verify_lil_B168_startup_v4207.py', {
        'lil_B167_startup_v4163': 'lil_B168_startup_v4207', 'lil_B167_runs_v4162': 'lil_B168_runs_v4206',
        'all_routes_combined_v4160': 'all_routes_combined_v4204', 'all_routes_combined_v4110': 'all_routes_combined_v4160',
        'lil_B166_runs_v4112': 'lil_B167_runs_v4162', 'V4110': 'V4160', 'Current4160': 'Current4204', 'B167': 'B168',
    }))
    tools.append(derive('scripts/record_lil_B167_startup_view_v4163.py', 'scripts/record_lil_B168_startup_view_v4207.py', {
        'lil_B167_startup_v4163': 'lil_B168_startup_v4207', 'V4110': 'V4160', 'B167': 'B168',
    }))
    ROOT.mkdir(parents=True)
    save(ROOT / 'source_derivation.json', dict(tools=tools, expected_manifest_batches=544, accepted_layers=114,
        existing_V4160_promotion_preserved=True, no_build_patch_or_startup_claim_yet=True))
    print('V4204 registered build/release/startup tools prepared;544 batches expected,V4160 stays main.')
