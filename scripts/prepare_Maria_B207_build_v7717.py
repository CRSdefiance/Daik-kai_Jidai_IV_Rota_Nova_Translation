"""Prepare the sole cumulative builder runner andrequired unchanged regression set."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/maria_B207_build_tools_v7717')
if __name__=='__main__':
    assert not ROOT.exists()
    build=derive('scripts/build_papal_trade_v7660.py','scripts/build_Maria_B207_v7717.py',{
        'papal_trade_build_v7660':'maria_B207_build_v7717','all_routes_combined_v7660_candidate':'all_routes_combined_v7717_candidate',
        'papal_trade_registration_v7659':'maria_B207_registration_v7716','all-routes-unified-v7660':'all-routes-unified-v7717',
    })
    regression=derive('scripts/run_papal_trade_regressions_v7660.py','scripts/run_Maria_B207_regressions_v7717.py',{
        'papal_trade_regressions_v7660':'maria_B207_regressions_v7717',
    })
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_registered_build_andregressions.json',dict(build=build,regressions=regression,complete_V7660_plusone_sealed_Maria_manuscript_expected629_batches=True,existing110_release_dialogue_regressions_unchanged=True,no_separate_test_package_orpromotion=True,new_credit=0,full_goal_complete=False))
