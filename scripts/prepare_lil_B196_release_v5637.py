"""Prepare registered cumulative build, full clean patch and current startup checks."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B196_release_tools_v5637')
if __name__=='__main__':
    assert not ROOT.exists()
    rows=[derive('scripts/build_lil_B195_v5580.py','scripts/build_lil_B196_v5637.py',{
        'B195':'B196','build_v5580':'build_v5637','combined_v5580':'combined_v5637','registration_v5579':'registration_v5636','all-routes-unified-v5580':'all-routes-unified-v5637'})]
    rows.append(derive('scripts/verify_lil_B195_release_v5581.py','scripts/verify_lil_B196_release_v5638.py',{
        'lil_B195_editorial_v1':'lil_B196_editorial_v3','B195':'B196','release_v5581':'release_v5638','combined_v5580':'combined_v5637','combined_v5531':'combined_v5580',
        'registration_v5579':'registration_v5636','build_v5580':'build_v5637',
        'all-routes-unified-v5580':'all-routes-unified-v5637','all-routes-unified-v5531':'all-routes-unified-v5580',
        "+[normal(conf['manuscript'])]":"+[normal(conf['manuscript']),normal(conf['choices'])]",
        "len(manifest['batches'])==579":"len(manifest['batches'])==581",'reference_v5564':'reference_v5619',
        'all579_manifest_batches':'all581_manifest_batches','V5531':'V5580','manifest_batches=579':'manifest_batches=581'}))
    rows.append(derive('scripts/run_lil_B195_startup_v5582.py','scripts/run_lil_B196_startup_v5639.py',{
        'B195':'B196','runs_v5582':'runs_v5639','_v5582_':'_v5639_','version=5580':'version=5637'}))
    rows.append(derive('scripts/verify_lil_B195_startup_v5583.py','scripts/verify_lil_B196_startup_v5640.py',{
        'work/analysis/lil_B194_runs_v5533':'work/analysis/lil_B195_runs_v5582','B195':'B196','startup_v5583':'startup_v5640','runs_v5582':'runs_v5639',
        'combined_v5580':'combined_v5637','combined_v5531':'combined_v5580','V5531':'V5580','Current5580':'Current5637'}))
    rows.append(derive('scripts/record_lil_B195_startup_view_v5583.py','scripts/record_lil_B196_startup_view_v5640.py',{
        'B195':'B196','startup_v5583':'startup_v5640','V5531':'V5580'}))
    rows.append(derive('scripts/run_lil_B195_regressions_v5580.py','scripts/run_lil_B196_regressions_v5637.py',{'B195':'B196','regressions_v5580':'regressions_v5637'}))
    ROOT.mkdir(parents=True);save(ROOT/'prepared_release_and_startup.json',dict(tools=rows,profile='all-routes-unified-v5637',parent_profile='all-routes-unified-v5580',
        expected_manifest_batches=581,accepted_layers=114,atomic_compiler='dk4tool.patch.lil_B196_editorial_v3',both_companions_required=True,
        main_V4701_preserved=True,full_goal_complete=False))
