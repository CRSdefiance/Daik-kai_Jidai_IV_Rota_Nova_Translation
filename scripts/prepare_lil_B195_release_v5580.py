"""Prepare the registered cumulative build,exact clean patch and fresh startup."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B195_release_tools_v5580')
if __name__=='__main__':
    assert not ROOT.exists()
    rows=[derive('scripts/build_lil_B193_v5478.py','scripts/build_lil_B195_v5580.py',{
        'B193':'B195','build_v5478':'build_v5580','combined_v5478':'combined_v5580','registration_v5477':'registration_v5579','all-routes-unified-v5478':'all-routes-unified-v5580'})]
    rows.append(derive('scripts/verify_lil_B193_release_v5479.py','scripts/verify_lil_B195_release_v5581.py',{
        'B193':'B195','release_v5479':'release_v5581','combined_v5478':'combined_v5580','combined_v5437':'combined_v5531',
        'registration_v5477':'registration_v5579','build_v5478':'build_v5580',
        'all-routes-unified-v5478':'all-routes-unified-v5580','all-routes-unified-v5437':'all-routes-unified-v5531',
        "len(manifest['batches'])==577":"len(manifest['batches'])==579",'reference_v5464':'reference_v5564',
        'all577_manifest_batches':'all579_manifest_batches','V5437':'V5531','manifest_batches=577':'manifest_batches=579'}))
    rows.append(derive('scripts/run_lil_B193_startup_v5480.py','scripts/run_lil_B195_startup_v5582.py',{
        'B193':'B195','runs_v5480':'runs_v5582','_v5480_':'_v5582_','version=5478':'version=5580'}))
    rows.append(derive('scripts/verify_lil_B193_startup_v5481.py','scripts/verify_lil_B195_startup_v5583.py',{
        'B193':'B195','startup_v5481':'startup_v5583','runs_v5480':'runs_v5582','combined_v5478':'combined_v5580',
        'combined_v5437':'combined_v5531','lil_B192_runs_v5439':'lil_B194_runs_v5533','V5437':'V5531','Current5478':'Current5580'}))
    rows.append(derive('scripts/record_lil_B193_startup_view_v5481.py','scripts/record_lil_B195_startup_view_v5583.py',{
        'B193':'B195','startup_v5481':'startup_v5583','V5437':'V5531'}))
    rows.append(derive('scripts/pin_lil_B193_v5482.py','scripts/pin_lil_B195_v5584.py',{
        'B193':'B195','retention_v5482':'retention_v5584','release_v5479':'release_v5581','reference_v5464':'reference_v5564',
        'display_v5469':'display_v5569','V5478':'V5580'}))
    rows.append(derive('scripts/run_lil_B193_regressions_v5478.py','scripts/run_lil_B195_regressions_v5580.py',{
        'B193':'B195','regressions_v5478':'regressions_v5580'}))
    ROOT.mkdir(parents=True);save(ROOT/'prepared_guarded_release_and_startup.json',dict(tools=rows,
        registered_profile='all-routes-unified-v5580',parent_profile='all-routes-unified-v5531',expected_manifest_batches=579,
        accepted_layers=114,main_V4701_preserved=True,native_high_constants_and_multiplicities_preserved=True,
        atomic_linear_compiler_v1_and_R17_guarded_row_retention_required=True,
        source_and_disposable_inherited_town_battery_preserved=True,new_emulator_runs=0,new_review_credit=0,full_goal_complete=False))
