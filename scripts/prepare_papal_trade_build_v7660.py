"""Prepare the unchanged registered builder runner and existing meaningful regression set."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/papal_trade_build_tools_v7660')
if __name__=='__main__':
    assert not ROOT.exists()
    a=derive('scripts/build_lil_B234_v7611.py','scripts/build_papal_trade_v7660.py',{'lil_B234_build_v7611':'papal_trade_build_v7660','all_routes_combined_v7611_candidate':'all_routes_combined_v7660_candidate','lil_B234_registration_v7610':'papal_trade_registration_v7659','all-routes-unified-v7611':'all-routes-unified-v7660'})
    b=derive('scripts/run_lil_B234_regressions_v7611.py','scripts/run_papal_trade_regressions_v7660.py',{'lil_B234_regressions_v7611':'papal_trade_regressions_v7660'})
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_registered_build_andregressions.json',dict(tools=[a,b],full_V7611_plus_two_sealed_manuscripts_expected628_batches=True,existing110_meaningful_release_dialogue_regressions_unchanged=True,no_separate_test_package_orpromotion=True,new_credit=0,full_goal_complete=False))
