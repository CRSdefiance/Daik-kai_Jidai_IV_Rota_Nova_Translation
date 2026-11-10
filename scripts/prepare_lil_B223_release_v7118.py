"""Prepare registered build, full ancestry, exact patch and retention runners."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive,checked_text
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B223_release_tools_v7118')
if __name__=='__main__':
    assert not ROOT.exists()
    jobs=[('scripts/build_lil_B222_v7067.py','scripts/build_lil_B223_v7118.py',{'B222':'B223','v7067':'v7118','v7066':'v7117'}),
      ('scripts/run_lil_B222_regressions_v7067.py','scripts/run_lil_B223_regressions_v7118.py',{'B222':'B223','v7067':'v7118'}),
      ('scripts/verify_lil_B222_release_v7068.py','scripts/verify_lil_B223_release_v7119.py',{'B222':'B223','lil_B222_editorial_v1':'lil_B223_editorial_v3','v7068':'v7119','v7067':'v7118','v7029':'v7067','V7029':'V7067','v7066':'v7117','reference_v7054':'reference_v7102',"profile_config.get('square_shopkeeper_labels')":"profile_config.get('lil_B222_editorial')","len(manifest['batches'])==615":"len(manifest['batches'])==616",'manifest_batches=615':'manifest_batches=616','all615_manifest_batches':'all616_manifest_batches'}),
      ('scripts/pin_lil_B222_v7069.py','scripts/pin_lil_B223_v7120.py',{'B222':'B223','v7069':'v7120','v7068':'v7119','V7067':'V7118'})]
    for a,b,c in jobs:assert not Path(b).exists();checked_text(Path(a).read_text('utf8'),c)
    rows=[derive(a,b,c) for a,b,c in jobs];ROOT.mkdir(parents=True);save(ROOT/'source_locked_release_runners.json',dict(tools=rows,expected616_batches114_accepted18_checks_and110_regressions=True,exact_clean_input_patch_full_reference_ROM_and_unchanged_components_required=True,all_prior_ROMs_and_pins_preserved=True,new_credit=0,full_goal_complete=False))
