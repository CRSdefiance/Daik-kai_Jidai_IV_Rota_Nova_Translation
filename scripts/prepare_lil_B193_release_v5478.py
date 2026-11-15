"""Prepare registered cumulative build,clean patch and fresh startup checks."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B193_release_tools_v5478')
if __name__=='__main__':
    assert not ROOT.exists()
    rows=[derive('scripts/build_lil_B192_v5437.py','scripts/build_lil_B193_v5478.py',{
        'B192':'B193','build_v5437':'build_v5478','combined_v5437':'combined_v5478','registration_v5436':'registration_v5477','all-routes-unified-v5437':'all-routes-unified-v5478'})]
    rows.append(derive('scripts/verify_lil_B192_release_v5438.py','scripts/verify_lil_B193_release_v5479.py',{
        'B192':'B193','release_v5438':'release_v5479','combined_v5437':'combined_v5478','combined_v5396':'combined_v5437','registration_v5436':'registration_v5477','build_v5437':'build_v5478',
        'all-routes-unified-v5437':'all-routes-unified-v5478','all-routes-unified-v5396':'all-routes-unified-v5437',"len(manifest['batches'])==576":"len(manifest['batches'])==577",'reference_v5423':'reference_v5464','all576_manifest_batches':'all577_manifest_batches','V5396':'V5437','manifest_batches=576':'manifest_batches=577'}))
    rows.append(derive('scripts/run_lil_B192_startup_v5439.py','scripts/run_lil_B193_startup_v5480.py',{
        'B192':'B193','runs_v5439':'runs_v5480','_v5439_':'_v5480_','version=5437':'version=5478'}))
    rows.append(derive('scripts/verify_lil_B192_startup_v5440.py','scripts/verify_lil_B193_startup_v5481.py',{
        'B192':'B193','startup_v5440':'startup_v5481','runs_v5439':'runs_v5480','combined_v5437':'combined_v5478','combined_v5396':'combined_v5437',
        'lil_B191_runs_v5398':'lil_B192_runs_v5439','V5396':'V5437','Current5437':'Current5478'}))
    rows.append(derive('scripts/record_lil_B192_startup_view_v5440.py','scripts/record_lil_B193_startup_view_v5481.py',{'B192':'B193','startup_v5440':'startup_v5481','V5396':'V5437'}))
    rows.append(derive('scripts/pin_lil_B192_v5441.py','scripts/pin_lil_B193_v5482.py',{
        'B192':'B193','retention_v5441':'retention_v5482','release_v5438':'release_v5479','reference_v5423':'reference_v5464','display_v5428':'display_v5469','V5437':'V5478'}))
    rows.append(derive('scripts/run_lil_B192_regressions_v5437.py','scripts/run_lil_B193_regressions_v5478.py',{'B192':'B193','regressions_v5437':'regressions_v5478'}))
    ROOT.mkdir(parents=True);save(ROOT/'prepared_guarded_release_and_startup.json',dict(tools=rows,registered_profile='all-routes-unified-v5478',parent_profile='all-routes-unified-v5437',
        expected_manifest_batches=577,accepted_layers=114,main_V4701_preserved=True,native_high_constants_and_multiplicities_preserved=True,atomic_linear_compiler_v1_required=True,
        source_and_disposable_inherited_town_battery_preserved=True,new_emulator_runs=0,new_review_credit=0,full_goal_complete=False))
