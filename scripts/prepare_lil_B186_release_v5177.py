"""Prepare the sole registered builder,exact patch and guarded current startup checks."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B186_release_tools_v5177')
if __name__=='__main__':
    assert not ROOT.exists()
    rows=[derive('scripts/build_lil_B185_v5122.py','scripts/build_lil_B186_v5177.py',{
        'B185':'B186','build_v5122':'build_v5177','combined_v5122':'combined_v5177',
        'registration_v5121':'registration_v5176','all-routes-unified-v5122':'all-routes-unified-v5177',
    })]
    rows.append(derive('scripts/verify_lil_B185_release_v5123.py','scripts/verify_lil_B186_release_v5178.py',{
        'B185':'B186','release_v5123':'release_v5178','combined_v5122':'combined_v5177','combined_v5076':'combined_v5122',
        'registration_v5121':'registration_v5176','build_v5122':'build_v5177',
        'all-routes-unified-v5122':'all-routes-unified-v5177','all-routes-unified-v5076':'all-routes-unified-v5122',
        "len(manifest['batches'])==569":"len(manifest['batches'])==570",
        'reference_v5108':'reference_v5161','all569_manifest_batches':'all570_manifest_batches','V5076':'V5122','manifest_batches=569':'manifest_batches=570',
    }))
    rows.append(derive('scripts/run_lil_B185_startup_v5124.py','scripts/run_lil_B186_startup_v5179.py',{
        'B185':'B186','runs_v5124':'runs_v5179','_v5124_':'_v5179_','version=5122':'version=5177',
    }))
    rows.append(derive('scripts/verify_lil_B185_startup_v5125b.py','scripts/verify_lil_B186_startup_v5180.py',{
        'B185':'B186','startup_v5125b':'startup_v5180','runs_v5124':'runs_v5179',
        'combined_v5122':'combined_v5177','combined_v5076':'combined_v5122',
        'lil_B184_runs_v5078':'lil_B185_runs_v5124','V5076':'V5122','Current5122':'Current5177',
    }))
    rows.append(derive('scripts/record_lil_B185_startup_view_v5125b.py','scripts/record_lil_B186_startup_view_v5180.py',{
        'B185':'B186','startup_v5125b':'startup_v5180','V5076':'V5122',
    }))
    ROOT.mkdir(parents=True);save(ROOT/'prepared_guarded_release_and_startup.json',dict(tools=rows,
        registered_profile='all-routes-unified-v5177',parent_profile='all-routes-unified-v5122',
        expected_manifest_batches=570,accepted_layers=114,main_V4701_preserved=True,
        original_actor_getter_CB184_and_all_native_high_constants_and_multiplicities_preserved=True,
        source_and_disposable_inherited_town_battery_preserved=True,
        new_emulator_runs=0,new_review_credit=0,full_goal_complete=False))
    print('Prepared sole registered V5177 builder,exact clean-input patch and guarded NewGame/town startup checks.')
