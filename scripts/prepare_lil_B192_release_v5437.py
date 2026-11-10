"""Prepare cumulative build,exact clean-input patch and current startup checks."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B192_release_tools_v5437')
if __name__=='__main__':
    assert not ROOT.exists()
    rows=[derive('scripts/build_lil_B191_v5396.py','scripts/build_lil_B192_v5437.py',{
        'B191':'B192','build_v5396':'build_v5437','combined_v5396':'combined_v5437','registration_v5395':'registration_v5436','all-routes-unified-v5396':'all-routes-unified-v5437'})]
    rows.append(derive('scripts/verify_lil_B191_release_v5397.py','scripts/verify_lil_B192_release_v5438.py',{
        'B191':'B192','release_v5397':'release_v5438','combined_v5396':'combined_v5437','combined_v5346':'combined_v5396',
        'registration_v5395':'registration_v5436','build_v5396':'build_v5437','all-routes-unified-v5396':'all-routes-unified-v5437','all-routes-unified-v5346':'all-routes-unified-v5396',
        "len(manifest['batches'])==575":"len(manifest['batches'])==576",'reference_v5381':'reference_v5423','all575_manifest_batches':'all576_manifest_batches','V5346':'V5396','manifest_batches=575':'manifest_batches=576'}))
    rows.append(derive('scripts/run_lil_B191_startup_v5398.py','scripts/run_lil_B192_startup_v5439.py',{
        'B191':'B192','runs_v5398':'runs_v5439','_v5398_':'_v5439_','version=5396':'version=5437'}))
    rows.append(derive('scripts/verify_lil_B191_startup_v5399.py','scripts/verify_lil_B192_startup_v5440.py',{
        'B191':'B192','startup_v5399':'startup_v5440','runs_v5398':'runs_v5439','combined_v5396':'combined_v5437','combined_v5346':'combined_v5396',
        'lil_B190_runs_v5348':'lil_B191_runs_v5398','V5346':'V5396','Current5396':'Current5437'}))
    rows.append(derive('scripts/record_lil_B191_startup_view_v5399.py','scripts/record_lil_B192_startup_view_v5440.py',{
        'B191':'B192','startup_v5399':'startup_v5440','V5346':'V5396'}))
    rows.append(derive('scripts/pin_lil_B191_v5400.py','scripts/pin_lil_B192_v5441.py',{
        'B191':'B192','retention_v5400':'retention_v5441','release_v5397':'release_v5438','reference_v5381':'reference_v5423','display_v5386':'display_v5428','V5396':'V5437'}))
    rows.append(derive('scripts/run_lil_B191_regressions_v5396.py','scripts/run_lil_B192_regressions_v5437.py',{
        'B191':'B192','regressions_v5396':'regressions_v5437'}))
    ROOT.mkdir(parents=True);save(ROOT/'prepared_guarded_release_and_startup.json',dict(tools=rows,registered_profile='all-routes-unified-v5437',parent_profile='all-routes-unified-v5396',
        expected_manifest_batches=576,accepted_layers=114,main_V4701_preserved=True,native_high_constants_and_multiplicities_preserved=True,
        atomic_linear_compiler_v1_required=True,source_and_disposable_inherited_town_battery_preserved=True,new_emulator_runs=0,new_review_credit=0,full_goal_complete=False))
