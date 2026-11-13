"""Derive registered cumulative build, clean-patch and scoped startup tools."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save
ROOT = Path('work/analysis/lil_B166_release_tools_v4110')
if __name__ == '__main__':
    assert not ROOT.exists()
    tools = []
    tools.append(derive('scripts/build_lil_B165_v4046.py','scripts/build_lil_B166_v4110.py',{
        'lil_B165_build_v4046':'lil_B166_build_v4110','all_routes_combined_v4046':'all_routes_combined_v4110',
        'lil_B165_registration_v4045':'lil_B166_registration_v4109','all-routes-unified-v4046':'all-routes-unified-v4110'}))
    tools.append(derive('scripts/verify_lil_B165_release_v4047.py','scripts/verify_lil_B166_release_v4111.py',{
        'lil_B165_editorial_v1':'lil_B166_editorial_v1','lil_B165_release_v4047':'lil_B166_release_v4111',
        'all_routes_combined_v4046':'all_routes_combined_v4110','all_routes_combined_v4002':'all_routes_combined_v4046',
        'lil_B165_registration_v4045':'lil_B166_registration_v4109','all-routes-unified-v4046':'all-routes-unified-v4110',
        'all-routes-unified-v4002':'all-routes-unified-v4046','lil_B165_editorial':'lil_B166_editorial',
        "+[normal(conf['manuscript'])]":"+[normal(conf['manuscript']),normal(conf['choices'])]",
        "len(manifest['batches'])==539":"len(manifest['batches'])==541",
        "registry['latest_promoted_build']['profile']=='all-routes-unified-v1492'":"registry['latest_promoted_build']['profile']=='all-routes-unified-v4046'",
        'lil_julio_argument':'lil_manuel_advice',
        'all539_manifest_batches_and114_accepted_layers_present':'all541_manifest_batches_and114_accepted_layers_present',
        'all_earlier_profiles_and_V1492_promotion_unchanged':'all_earlier_profiles_and_V4046_promotion_unchanged',
        'every_other_file_font_graphic_route_ARM9_ARM7_and_component_exact_to_V4002':'every_other_file_font_graphic_route_ARM9_ARM7_and_component_exact_to_V4046',
        'manifest_batches=539':'manifest_batches=541'}))
    tools.append(derive('scripts/run_lil_B165_startup_v4048.py','scripts/run_lil_B166_startup_v4112.py',{
        'lil_B165_runs_v4048':'lil_B166_runs_v4112','lil_B165_v4048':'lil_B166_v4112',
        'version=4046':'version=4110','B165':'B166'}))
    tools.append(derive('scripts/verify_lil_B165_startup_v4049.py','scripts/verify_lil_B166_startup_v4113.py',{
        'lil_B165_startup_v4049':'lil_B166_startup_v4113','lil_B165_runs_v4048':'lil_B166_runs_v4112',
        'all_routes_combined_v4046':'all_routes_combined_v4110','all_routes_combined_v4002':'all_routes_combined_v4046',
        'lil_B164_runs_v4004':'lil_B165_runs_v4048','V4002':'V4046','Current4046':'Current4110','B165':'B166'}))
    tools.append(derive('scripts/record_lil_B165_startup_view_v4049.py','scripts/record_lil_B166_startup_view_v4113.py',{
        'lil_B165_startup_v4049':'lil_B166_startup_v4113','V4002':'V4046','B165':'B166'}))
    ROOT.mkdir(parents=True)
    save(ROOT/'source_derivation.json',dict(tools=tools,expected_manifest_batches=541,accepted_layers=114,
        existing_V4046_promotion_to_remain=True,no_build_or_release_or_startup_claim_yet=True))
    print('Registered V4110 build/release/startup successors created;541 cumulative manuscripts expected,V4046 remains main.')
