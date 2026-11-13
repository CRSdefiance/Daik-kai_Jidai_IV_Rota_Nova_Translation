"""Prepare registered build,exact patch and current startup verification."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B187_release_tools_v5219')
if __name__=='__main__':
    assert not ROOT.exists()
    rows=[derive('scripts/build_lil_B186_v5177.py','scripts/build_lil_B187_v5219.py',{
        'B186':'B187','build_v5177':'build_v5219','combined_v5177':'combined_v5219',
        'registration_v5176':'registration_v5218','all-routes-unified-v5177':'all-routes-unified-v5219'})]
    rows.append(derive('scripts/verify_lil_B186_release_v5178.py','scripts/verify_lil_B187_release_v5220.py',{
        'B186':'B187','release_v5178':'release_v5220','combined_v5177':'combined_v5219','combined_v5122':'combined_v5177',
        'registration_v5176':'registration_v5218','build_v5177':'build_v5219','all-routes-unified-v5177':'all-routes-unified-v5219',
        'all-routes-unified-v5122':'all-routes-unified-v5177',"len(manifest['batches'])==570":"len(manifest['batches'])==571",
        'reference_v5161':'reference_v5205','all570_manifest_batches':'all571_manifest_batches','V5122':'V5177','manifest_batches=570':'manifest_batches=571'}))
    rows.append(derive('scripts/run_lil_B186_startup_v5179.py','scripts/run_lil_B187_startup_v5221.py',{
        'B186':'B187','runs_v5179':'runs_v5221','_v5179_':'_v5221_','version=5177':'version=5219'}))
    rows.append(derive('scripts/verify_lil_B186_startup_v5180.py','scripts/verify_lil_B187_startup_v5222.py',{
        'B186':'B187','startup_v5180':'startup_v5222','runs_v5179':'runs_v5221',
        'combined_v5177':'combined_v5219','combined_v5122':'combined_v5177','lil_B185_runs_v5124':'lil_B186_runs_v5179',
        'V5122':'V5177','Current5177':'Current5219'}))
    rows.append(derive('scripts/record_lil_B186_startup_view_v5180.py','scripts/record_lil_B187_startup_view_v5222.py',{
        'B186':'B187','startup_v5180':'startup_v5222','V5122':'V5177'}))
    rows.append(derive('scripts/pin_lil_B186_v5181.py','scripts/pin_lil_B187_v5223.py',{
        'B186':'B187','retention_v5181':'retention_v5223','release_v5178':'release_v5220','reference_v5161':'reference_v5205',
        'display_v5166':'display_v5210','V5177':'V5219'}))
    rows.append(derive('scripts/run_lil_B186_regressions_v5177b.py','scripts/run_lil_B187_regressions_v5219.py',{
        'B186':'B187','regressions_v5177b':'regressions_v5219',
        "    prior=Path('work/analysis/lil_B186_regressions_v5177/terminal.json')\n    assert read(prior)['terminal'] and read(prior)['returncode']==1\n":'',
        "        previous_wrong_unittest_runner_receipt=str(prior),previous_wrong_unittest_runner_receipt_sha256=sha(prior.read_bytes()),\n        previous_wrong_runner_not_counted_as_executed_pytest_checks=True,no_ROM_or_ledger_mutation_by_runner=True,":
        '        no_ROM_or_ledger_mutation_by_runner=True,'}))
    ROOT.mkdir(parents=True);save(ROOT/'prepared_guarded_release_and_startup.json',dict(tools=rows,
        registered_profile='all-routes-unified-v5219',parent_profile='all-routes-unified-v5177',expected_manifest_batches=571,accepted_layers=114,
        main_V4701_preserved=True,original_actor_getter_CB184_and_all_native_high_constants_and_multiplicities_preserved=True,
        source_and_disposable_inherited_town_battery_preserved=True,new_emulator_runs=0,new_review_credit=0,full_goal_complete=False))
