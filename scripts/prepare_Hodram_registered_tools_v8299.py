"""Source-lock sole-builder and regressions to the complete registered Hodram profile."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/Hodram_registered_tools_v8299')
if __name__=='__main__':
    assert not ROOT.exists();results=[]
    results.append(derive('scripts/build_Gerhard_surname_v8259.py','scripts/build_Hodram_three_blocks_v8300.py',{
        'Gerhard_surname_build_v8259':'Hodram_three_blocks_build_v8300','all_routes_combined_v8259':'all_routes_combined_v8300',
        'Gerhard_surname_registration_v8258':'Hodram_three_blocks_registration_v8299','all-routes-unified-v8259':'all-routes-unified-v8300',
    }))
    results.append(derive('scripts/run_Gerhard_surname_regressions_v8259.py','scripts/run_Hodram_three_blocks_regressions_v8300.py',{
        'Gerhard_surname_regressions_v8259':'Hodram_three_blocks_regressions_v8300',
    }))
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_registered_runners.json',dict(derivations=results,
        no_builder_orregistry_changed_bythis_preparer=True,new_credit=0,full_goal_complete=False))
