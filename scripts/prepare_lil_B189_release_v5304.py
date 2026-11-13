"""Prepare the cumulative registered build,exact patch and fresh startup checks."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B189_release_tools_v5304')
if __name__=='__main__':
    assert not ROOT.exists()
    rows=[derive('scripts/build_lil_B188_v5263.py','scripts/build_lil_B189_v5304.py',{
        'B188':'B189','build_v5263':'build_v5304','combined_v5263':'combined_v5304','registration_v5262b':'registration_v5303','all-routes-unified-v5263':'all-routes-unified-v5304'})]
    rows.append(derive('scripts/verify_lil_B188_release_v5264.py','scripts/verify_lil_B189_release_v5305.py',{
        'B188':'B189','lil_B188_editorial_v2':'lil_B189_editorial_v1','release_v5264':'release_v5305','combined_v5263':'combined_v5304','combined_v5219':'combined_v5263',
        'registration_v5262b':'registration_v5303','build_v5263':'build_v5304','all-routes-unified-v5263':'all-routes-unified-v5304','all-routes-unified-v5219':'all-routes-unified-v5263',
        "len(manifest['batches'])==572":"len(manifest['batches'])==573",'reference_v5249':'reference_v5290','all572_manifest_batches':'all573_manifest_batches','V5219':'V5263','manifest_batches=572':'manifest_batches=573'}))
    rows.append(derive('scripts/run_lil_B188_startup_v5265.py','scripts/run_lil_B189_startup_v5306.py',{
        'B188':'B189','runs_v5265':'runs_v5306','_v5265_':'_v5306_','version=5263':'version=5304'}))
    rows.append(derive('scripts/verify_lil_B188_startup_v5266.py','scripts/verify_lil_B189_startup_v5307.py',{
        'B188':'B189','startup_v5266':'startup_v5307','runs_v5265':'runs_v5306','combined_v5263':'combined_v5304','combined_v5219':'combined_v5263',
        'lil_B187_runs_v5221':'lil_B188_runs_v5265','V5219':'V5263','Current5263':'Current5304'}))
    rows.append(derive('scripts/record_lil_B188_startup_view_v5266.py','scripts/record_lil_B189_startup_view_v5307.py',{
        'B188':'B189','startup_v5266':'startup_v5307','V5219':'V5263'}))
    rows.append(derive('scripts/pin_lil_B188_v5267.py','scripts/pin_lil_B189_v5308.py',{
        'B188':'B189','retention_v5267':'retention_v5308','release_v5264':'release_v5305','reference_v5249':'reference_v5290','display_v5254':'display_v5295','V5263':'V5304'}))
    rows.append(derive('scripts/run_lil_B188_regressions_v5263.py','scripts/run_lil_B189_regressions_v5304.py',{
        'B188':'B189','regressions_v5263':'regressions_v5304'}))
    ROOT.mkdir(parents=True);save(ROOT/'prepared_guarded_release_and_startup.json',dict(tools=rows,registered_profile='all-routes-unified-v5304',parent_profile='all-routes-unified-v5263',
        expected_manifest_batches=573,accepted_layers=114,main_V4701_preserved=True,original_actor_getter_CB184_and_all_native_high_constants_and_multiplicities_preserved=True,
        atomic_four_speaker_compiler_v1_required=True,source_and_disposable_inherited_town_battery_preserved=True,new_emulator_runs=0,new_review_credit=0,full_goal_complete=False))
