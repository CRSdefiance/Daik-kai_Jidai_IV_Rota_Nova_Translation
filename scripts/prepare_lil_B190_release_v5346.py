"""Prepare the registered cumulative build,exact patch and current startup gates."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B190_release_tools_v5346')
if __name__=='__main__':
    assert not ROOT.exists()
    rows=[derive('scripts/build_lil_B189_v5304.py','scripts/build_lil_B190_v5346.py',{
        'B189':'B190','build_v5304':'build_v5346','combined_v5304':'combined_v5346','registration_v5303':'registration_v5345','all-routes-unified-v5304':'all-routes-unified-v5346'})]
    rows.append(derive('scripts/verify_lil_B189_release_v5305.py','scripts/verify_lil_B190_release_v5347.py',{
        'B189':'B190','release_v5305':'release_v5347','combined_v5304':'combined_v5346','combined_v5263':'combined_v5304',
        'registration_v5303':'registration_v5345','build_v5304':'build_v5346','all-routes-unified-v5304':'all-routes-unified-v5346','all-routes-unified-v5263':'all-routes-unified-v5304',
        "len(manifest['batches'])==573":"len(manifest['batches'])==574",'reference_v5290':'reference_v5332','all573_manifest_batches':'all574_manifest_batches','V5263':'V5304','manifest_batches=573':'manifest_batches=574'}))
    rows.append(derive('scripts/run_lil_B189_startup_v5306.py','scripts/run_lil_B190_startup_v5348.py',{
        'B189':'B190','runs_v5306':'runs_v5348','_v5306_':'_v5348_','version=5304':'version=5346'}))
    rows.append(derive('scripts/verify_lil_B189_startup_v5307.py','scripts/verify_lil_B190_startup_v5349.py',{
        'B189':'B190','startup_v5307':'startup_v5349','runs_v5306':'runs_v5348','combined_v5304':'combined_v5346','combined_v5263':'combined_v5304',
        'lil_B188_runs_v5265':'lil_B189_runs_v5306','V5263':'V5304','Current5304':'Current5346'}))
    rows.append(derive('scripts/record_lil_B189_startup_view_v5307.py','scripts/record_lil_B190_startup_view_v5349.py',{
        'B189':'B190','startup_v5307':'startup_v5349','V5263':'V5304'}))
    rows.append(derive('scripts/pin_lil_B189_v5308.py','scripts/pin_lil_B190_v5350.py',{
        'B189':'B190','retention_v5308':'retention_v5350','release_v5305':'release_v5347','reference_v5290':'reference_v5332','display_v5295':'display_v5337','V5304':'V5346'}))
    rows.append(derive('scripts/run_lil_B189_regressions_v5304.py','scripts/run_lil_B190_regressions_v5346.py',{
        'B189':'B190','regressions_v5304':'regressions_v5346'}))
    ROOT.mkdir(parents=True);save(ROOT/'prepared_registered_release_and_startup.json',dict(tools=rows,
        registered_profile='all-routes-unified-v5346',parent_profile='all-routes-unified-v5304',expected_manifest_batches=574,accepted_layers=114,
        all_native_high_constants_and_multiplicities_preserved=True,main_V4701_and_every_ROM_preserved=True,no_credit=True,full_goal_complete=False))
