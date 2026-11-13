"""Prepare registered cumulative build,clean patch,fresh startup and existing regression suite."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B194_release_tools_v5531')
if __name__=='__main__':
    assert not ROOT.exists()
    rows=[derive('scripts/build_lil_B193_v5478.py','scripts/build_lil_B194_v5531.py',{
        'B193':'B194','build_v5478':'build_v5531','combined_v5478':'combined_v5531','registration_v5477':'registration_v5530','all-routes-unified-v5478':'all-routes-unified-v5531'})]
    rows.append(derive('scripts/verify_lil_B193_release_v5479.py','scripts/verify_lil_B194_release_v5532.py',{
        'B193':'B194','release_v5479':'release_v5532','combined_v5478':'combined_v5531','combined_v5437':'combined_v5478',
        'registration_v5477':'registration_v5530','build_v5478':'build_v5531','all-routes-unified-v5478':'all-routes-unified-v5531',
        'all-routes-unified-v5437':'all-routes-unified-v5478',"len(manifest['batches'])==577":"len(manifest['batches'])==578",
        'reference_v5464':'reference_v5509','all577_manifest_batches':'all578_manifest_batches','V5437':'V5478','manifest_batches=577':'manifest_batches=578'}))
    rows.append(derive('scripts/run_lil_B193_startup_v5480.py','scripts/run_lil_B194_startup_v5533.py',{
        'B193':'B194','runs_v5480':'runs_v5533','_v5480_':'_v5533_','version=5478':'version=5531'}))
    rows.append(derive('scripts/verify_lil_B193_startup_v5481.py','scripts/verify_lil_B194_startup_v5534.py',{
        'B193':'B194','startup_v5481':'startup_v5534','runs_v5480':'runs_v5533','combined_v5478':'combined_v5531','combined_v5437':'combined_v5478',
        'lil_B192_runs_v5439':'lil_B193_runs_v5480','V5437':'V5478','Current5478':'Current5531'}))
    rows.append(derive('scripts/record_lil_B193_startup_view_v5481.py','scripts/record_lil_B194_startup_view_v5534.py',{
        'B193':'B194','startup_v5481':'startup_v5534','V5437':'V5478'}))
    rows.append(derive('scripts/run_lil_B193_regressions_v5478.py','scripts/run_lil_B194_regressions_v5531.py',{
        'B193':'B194','regressions_v5478':'regressions_v5531'}))
    ROOT.mkdir(parents=True);save(ROOT/'prepared_guarded_release_and_startup.json',dict(tools=rows,
        registered_profile='all-routes-unified-v5531',parent_profile='all-routes-unified-v5478',
        expected_manifest_batches=578,accepted_layers=114,main_V4701_preserved=True,
        atomic_conditional_compiler_v1_and93_negatives_required=True,source_and_disposable_town_battery_preserved=True,
        new_emulator_runs=0,new_review_credit=0,full_goal_complete=False))
