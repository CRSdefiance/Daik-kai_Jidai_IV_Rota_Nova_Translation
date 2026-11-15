"""Prepare frozen successors without changing native constants or historical tools."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B207_release_tools_v6379')
if __name__=='__main__':
    assert not ROOT.exists();rows=[]
    rows.append(derive('scripts/build_lil_B206_v6327.py','scripts/build_lil_B207_v6380.py',{'B206':'B207','build_v6327':'build_v6380','combined_v6327':'combined_v6380','registration_v6326':'registration_v6379','all-routes-unified-v6327':'all-routes-unified-v6380'}))
    rows.append(derive('scripts/run_lil_B206_regressions_v6327.py','scripts/run_lil_B207_regressions_v6380.py',{'B206':'B207','regressions_v6327':'regressions_v6380'}))
    rows.append(derive('scripts/run_lil_B206_startup_v6330.py','scripts/run_lil_B207_startup_v6383.py',{'B206':'B207','runs_v6330':'runs_v6383','_v6330_':'_v6383_','version=6327':'version=6380'}))
    rows.append(derive('scripts/verify_lil_B206_startup_v6331.py','scripts/verify_lil_B207_startup_v6384.py',{'B206':'B207','startup_v6331':'startup_v6384','runs_v6330':'runs_v6383','combined_v6327':'combined_v6380','combined_v6270':'combined_v6327','shady_man_runs_v6272':'lil_B206_runs_v6330','V6270':'V6327','Current6327':'Current6380'}))
    rows.append(derive('scripts/record_lil_B206_startup_view_v6331.py','scripts/record_lil_B207_startup_view_v6384.py',{'B206':'B207','startup_v6331':'startup_v6384','V6270':'V6327'}))
    rows.append(derive('scripts/verify_lil_B206_release_v6328.py','scripts/verify_lil_B207_release_v6381.py',{'lil_B206_editorial_v1':'lil_B207_editorial_v4','B206':'B207','release_v6328':'release_v6381','combined_v6327':'combined_v6380','combined_v6270':'combined_v6327','registration_v6326':'registration_v6379','build_v6327':'build_v6380','all-routes-unified-v6327':'all-routes-unified-v6380','all-routes-unified-v6270':'all-routes-unified-v6327',"['manuscript','choice_manuscript']":"['manuscript']",'==597':'==598','manifest_batches=597':'manifest_batches=598','all597_':'all598_',"profile_config.get('shady_man_label')":"profile_config.get('lil_B206_editorial')",'out/lil_B206_reference_v6307_RESEARCH_ONLY.nds':'out/lil_B207_reference_v6367_RESEARCH_ONLY.nds','V6270':'V6327'}))
    rows.append(derive('scripts/pin_lil_B206_v6329.py','scripts/pin_lil_B207_v6382.py',{'B206':'B207','retention_v6329':'retention_v6382','release_v6328':'release_v6381','V6327':'V6380'}))
    ROOT.mkdir(parents=True);save(ROOT/'prepared_tools.json',dict(tools=rows,full_goal_complete=False));print('Seven B207 build/release/startup successors prepared with native constants preserved.')
