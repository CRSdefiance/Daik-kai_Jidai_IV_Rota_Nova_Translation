"""Prepare the sole cumulative builder,exact patch and fresh startup checks."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B188_release_tools_v5263')
if __name__=='__main__':
    assert not ROOT.exists()
    rows=[derive('scripts/build_lil_B187_v5219.py','scripts/build_lil_B188_v5263.py',{
        'B187':'B188','build_v5219':'build_v5263','combined_v5219':'combined_v5263','registration_v5218':'registration_v5262b','all-routes-unified-v5219':'all-routes-unified-v5263'})]
    rows.append(derive('scripts/verify_lil_B187_release_v5220.py','scripts/verify_lil_B188_release_v5264.py',{
        'B187':'B188','lil_B187_editorial_v1':'lil_B188_editorial_v2','release_v5220':'release_v5264','combined_v5219':'combined_v5263','combined_v5177':'combined_v5219',
        'registration_v5218':'registration_v5262b','build_v5219':'build_v5263','all-routes-unified-v5219':'all-routes-unified-v5263','all-routes-unified-v5177':'all-routes-unified-v5219',
        "len(manifest['batches'])==571":"len(manifest['batches'])==572",'reference_v5205':'reference_v5249','all571_manifest_batches':'all572_manifest_batches','V5177':'V5219','manifest_batches=571':'manifest_batches=572'}))
    rows.append(derive('scripts/run_lil_B187_startup_v5221.py','scripts/run_lil_B188_startup_v5265.py',{
        'B187':'B188','runs_v5221':'runs_v5265','_v5221_':'_v5265_','version=5219':'version=5263'}))
    rows.append(derive('scripts/verify_lil_B187_startup_v5222.py','scripts/verify_lil_B188_startup_v5266.py',{
        'B187':'B188','startup_v5222':'startup_v5266','runs_v5221':'runs_v5265','combined_v5219':'combined_v5263','combined_v5177':'combined_v5219',
        'lil_B186_runs_v5179':'lil_B187_runs_v5221','V5177':'V5219','Current5219':'Current5263'}))
    rows.append(derive('scripts/record_lil_B187_startup_view_v5222.py','scripts/record_lil_B188_startup_view_v5266.py',{
        'B187':'B188','startup_v5222':'startup_v5266','V5177':'V5219'}))
    rows.append(derive('scripts/pin_lil_B187_v5223.py','scripts/pin_lil_B188_v5267.py',{
        'B187':'B188','retention_v5223':'retention_v5267','release_v5220':'release_v5264','reference_v5205':'reference_v5249','display_v5210':'display_v5254','V5219':'V5263'}))
    rows.append(derive('scripts/run_lil_B187_regressions_v5219.py','scripts/run_lil_B188_regressions_v5263.py',{
        'B187':'B188','regressions_v5219':'regressions_v5263'}))
    ROOT.mkdir(parents=True);save(ROOT/'prepared_guarded_release_and_startup.json',dict(tools=rows,registered_profile='all-routes-unified-v5263',parent_profile='all-routes-unified-v5219',
        expected_manifest_batches=572,accepted_layers=114,main_V4701_preserved=True,original_actor_getter_CB184_and_all_native_high_constants_and_multiplicities_preserved=True,
        compiler_v2_lookup_successor_required=True,source_and_disposable_inherited_town_battery_preserved=True,new_emulator_runs=0,new_review_credit=0,full_goal_complete=False))
