"""Prepare source-locked B221 build, regression, release and startup tools."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B221_release_tools_v7010')
if __name__=='__main__':
    assert not ROOT.exists()
    rows=[derive('scripts/build_lil_B220_v6956.py','scripts/build_lil_B221_v7011.py',{
        'B220':'B221','build_v6956':'build_v7011','combined_v6956':'combined_v7011','registration_v6955':'registration_v7010','all-routes-unified-v6956':'all-routes-unified-v7011'})]
    rows.append(derive('scripts/run_lil_B220_regressions_v6956.py','scripts/run_lil_B221_regressions_v7011.py',{'B220':'B221','regressions_v6956':'regressions_v7011'}))
    rows.append(derive('scripts/verify_lil_B220_release_v6957.py','scripts/verify_lil_B221_release_v7012.py',{
        'B220':'B221','release_v6957':'release_v7012','combined_v6956':'combined_v7011','combined_v6910':'combined_v6956',
        'registration_v6955':'registration_v7010','build_v6956':'build_v7011','all-routes-unified-v6956':'all-routes-unified-v7011',
        'all-routes-unified-v6910':'all-routes-unified-v6956',"['manuscript']":"['manuscript','choice_manuscript']",'611':'613',
        "profile_config.get('lil_B218_editorial')":"profile_config.get('lil_B220_editorial')",'reference_v6942':'reference_v6997','V6910':'V6956'}))
    rows.append(derive('scripts/run_lil_B220_startup_v6959.py','scripts/run_lil_B221_startup_v7014.py',{
        'B220':'B221','runs_v6959':'runs_v7014','_v6959_':'_v7014_','version=6956':'version=7011'}))
    rows.append(derive('scripts/verify_lil_B220_startup_v6960.py','scripts/verify_lil_B221_startup_v7015.py',{
        'B220':'B221','startup_v6960':'startup_v7015','lil_B220_runs_v6959':'lil_B221_runs_v7014',
        'combined_v6956':'combined_v7011','combined_v6910':'combined_v6956','lil_B218_runs_v6913':'lil_B220_runs_v6959','V6910':'V6956','Current6956':'Current7011'}))
    rows.append(derive('scripts/record_lil_B220_startup_view_v6960.py','scripts/record_lil_B221_startup_view_v7015.py',{'B220':'B221','startup_v6960':'startup_v7015','V6910':'V6956'}))
    ROOT.mkdir(parents=True);save(ROOT/'prepared_tools.json',dict(tools=rows,full_goal_complete=False))
    print('Six source-locked release/build/regression/startup tools prepared.',flush=True)
