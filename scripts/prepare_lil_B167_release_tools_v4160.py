"""Derive the registered cumulative build, exact patch and current startup verification."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B167_release_tools_v4160')
if __name__=='__main__':
    assert not ROOT.exists();tools=[]
    tools.append(derive('scripts/build_lil_B166_v4110.py','scripts/build_lil_B167_v4160.py',{
        'lil_B166_build_v4110':'lil_B167_build_v4160','all_routes_combined_v4110':'all_routes_combined_v4160',
        'lil_B166_registration_v4109':'lil_B167_registration_v4159b','all-routes-unified-v4110':'all-routes-unified-v4160'}))
    tools.append(derive('scripts/verify_lil_B166_release_v4111.py','scripts/verify_lil_B167_release_v4161.py',{
        'lil_B166_editorial_v1':'lil_B167_editorial_v2','lil_B166_release_v4111':'lil_B167_release_v4161',
        'all_routes_combined_v4110':'all_routes_combined_v4160','all_routes_combined_v4046':'all_routes_combined_v4110',
        'lil_B166_registration_v4109':'lil_B167_registration_v4159b','all-routes-unified-v4110':'all-routes-unified-v4160',
        "registry['profiles']['all-routes-unified-v4046']":"registry['profiles']['all-routes-unified-v4110']",
        'lil_B166_editorial':'lil_B167_editorial',"len(manifest['batches'])==541":"len(manifest['batches'])==543",
        'lil_manuel_advice':'lil_sail_lesson','all541_manifest_batches_and114_accepted_layers_present':'all543_manifest_batches_and114_accepted_layers_present',
        'every_other_file_font_graphic_route_ARM9_ARM7_and_component_exact_to_V4046':'every_other_file_font_graphic_route_ARM9_ARM7_and_component_exact_to_V4110',
        'manifest_batches=541':'manifest_batches=543'}))
    tools.append(derive('scripts/run_lil_B166_startup_v4112.py','scripts/run_lil_B167_startup_v4162.py',{
        'lil_B166_runs_v4112':'lil_B167_runs_v4162','lil_B166_v4112':'lil_B167_v4162','version=4110':'version=4160','B166':'B167'}))
    tools.append(derive('scripts/verify_lil_B166_startup_v4113.py','scripts/verify_lil_B167_startup_v4163.py',{
        'lil_B166_startup_v4113':'lil_B167_startup_v4163','lil_B166_runs_v4112':'lil_B167_runs_v4162',
        'all_routes_combined_v4110':'all_routes_combined_v4160','all_routes_combined_v4046':'all_routes_combined_v4110',
        'lil_B165_runs_v4048':'lil_B166_runs_v4112','V4046':'V4110','Current4110':'Current4160','B166':'B167'}))
    tools.append(derive('scripts/record_lil_B166_startup_view_v4113.py','scripts/record_lil_B167_startup_view_v4163.py',{
        'lil_B166_startup_v4113':'lil_B167_startup_v4163','V4046':'V4110','B166':'B167'}))
    ROOT.mkdir(parents=True);save(ROOT/'source_derivation.json',dict(tools=tools,expected_manifest_batches=543,accepted_layers=114,existing_V4046_promotion_preserved=True,no_build_patch_or_startup_claim_yet=True))
    print('V4160 cumulative registered build/release/startup tools created;543 manuscript batches expected,V4046 stays main.')
