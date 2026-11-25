"""Prepare source-locked registered build/regression/reconstruction/retention/town tools."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/square_shopkeeper_release_tools_v7028')
if __name__=='__main__':
    assert not ROOT.exists()
    rows=[derive('scripts/build_lil_B221_v7011.py','scripts/build_square_shopkeeper_v7029.py',{
        'lil_B221_build_v7011':'square_shopkeeper_build_v7029','combined_v7011':'combined_v7029','lil_B221_registration_v7010':'square_shopkeeper_registration_v7028','all-routes-unified-v7011':'all-routes-unified-v7029'})]
    rows.append(derive('scripts/run_lil_B221_regressions_v7011.py','scripts/run_square_shopkeeper_regressions_v7029.py',{'lil_B221_regressions_v7011':'square_shopkeeper_regressions_v7029'}))
    rows.append(derive('scripts/verify_lil_B221_release_v7012.py','scripts/verify_square_shopkeeper_release_v7030.py',{
        'lil_B221_editorial_v1':'square_shopkeeper_label_release_v2','lil_B221_release_v7012':'square_shopkeeper_release_v7030',
        'combined_v7011':'combined_v7029','combined_v6956':'combined_v7011','lil_B221_registration_v7010':'square_shopkeeper_registration_v7028',
        'lil_B221_build_v7011':'square_shopkeeper_build_v7029','all-routes-unified-v7011':'all-routes-unified-v7029','all-routes-unified-v6956':'all-routes-unified-v7011',
        "['manuscript','choice_manuscript']":"['manuscript']",'613':'614',
        "file_changes==[owned.PATH] and component_changes==[]":"file_changes==[] and component_changes==[owned.PATH]",
        "conf['required_runtime_arm9_sha256']":"conf['target_ARM9_sha256']",
        "profile_config.get('lil_B220_editorial')":"profile_config.get('lil_B221_editorial')",'lil_B221_editorial':'square_shopkeeper_labels',
        'out/lil_B221_reference_v6997_RESEARCH_ONLY.nds':'out/square_shopkeeper_v7018_RESEARCH_ONLY.nds',
        'every_other_file_font_graphic_route_ARM9_ARM7_and_component_exact_to_V6956':'every_other_file_font_graphic_route_ARM7_code_and_unowned_ARM9_bytes_exact_to_V7011'}))
    rows.append(derive('scripts/pin_lil_B221_v7013.py','scripts/pin_square_shopkeeper_v7031.py',{
        'lil_B221_retention_v7013':'square_shopkeeper_retention_v7031','lil_B221_release_v7012':'square_shopkeeper_release_v7030','B221':'ten Shopkeeper labels','V7011':'V7029'}))
    rows.append(derive('scripts/run_lil_B221_startup_v7014.py','scripts/run_square_shopkeeper_town_v7032.py',{
        'lil_B221_runs_v7014':'square_shopkeeper_runs_v7032','lil_B221_v7014_':'square_shopkeeper_v7032_','version=7011':'version=7029'}))
    ROOT.mkdir(parents=True);save(ROOT/'prepared_release_tools.json',dict(tools=rows,whole_ROM_identical_target_NewGame7019_reuse_planned_not_new_gameplay=True,
        fresh_registered_town_run_required=True,new_review_credit=0,full_goal_complete=False))
    print('Five source-locked Shopkeeper release tools prepared;exact target NewGame can be reused after whole-ROM reconstruction.',flush=True)
