"""Prepare registered build,exact clean patch,current startup and existing release regressions."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B198_release_tools_v5756')
if __name__=='__main__':
    assert not ROOT.exists()
    rows=[derive('scripts/build_lil_B197_v5692.py','scripts/build_lil_B198_v5756.py',{
        'B197':'B198','build_v5692':'build_v5756','combined_v5692':'combined_v5756',
        'registration_v5691':'registration_v5755','all-routes-unified-v5692':'all-routes-unified-v5756'})]
    rows.append(derive('scripts/verify_lil_B197_release_v5693.py','scripts/verify_lil_B198_release_v5757.py',{
        'B197':'B198','lil_B197_editorial_v1':'lil_B198_editorial_v2','release_v5693':'release_v5757',
        'combined_v5692':'combined_v5756','combined_v5637':'combined_v5692',
        'registration_v5691':'registration_v5755','build_v5692':'build_v5756',
        'all-routes-unified-v5692':'all-routes-unified-v5756','all-routes-unified-v5637':'all-routes-unified-v5692',
        "[normal(conf['manuscript']),normal(conf['choices'])]":"[normal(conf['manuscript'])]",
        "len(manifest['batches'])==583":"len(manifest['batches'])==584",'all583_manifest_batches':'all584_manifest_batches',
        'reference_v5677':'reference_v5733','V5637':'V5692','manifest_batches=583':'manifest_batches=584'}))
    rows.append(derive('scripts/run_lil_B197_startup_v5694.py','scripts/run_lil_B198_startup_v5758.py',{
        'B197':'B198','runs_v5694':'runs_v5758','_v5694_':'_v5758_','version=5692':'version=5756'}))
    rows.append(derive('scripts/verify_lil_B197_startup_v5695.py','scripts/verify_lil_B198_startup_v5759.py',{
        'B197':'B198','startup_v5695':'startup_v5759','runs_v5694':'runs_v5758',
        'combined_v5692':'combined_v5756','combined_v5637':'combined_v5692',
        'lil_B196_runs_v5639':'lil_B197_runs_v5694','V5637':'V5692','Current5692':'Current5756'}))
    rows.append(derive('scripts/record_lil_B197_startup_view_v5695.py','scripts/record_lil_B198_startup_view_v5759.py',{
        'B197':'B198','startup_v5695':'startup_v5759','V5637':'V5692'}))
    rows.append(derive('scripts/run_lil_B197_regressions_v5692.py','scripts/run_lil_B198_regressions_v5756.py',{
        'B197':'B198','regressions_v5692':'regressions_v5756'}))
    ROOT.mkdir(parents=True);save(ROOT/'prepared_guarded_release_and_current_startup.json',dict(tools=rows,
        profile='all-routes-unified-v5756',parent_profile='all-routes-unified-v5692',expected_manifest_batches=584,
        accepted_layers=114,promoted_main_V4701_preserved=True,source_correct_native_style11_is_test_reference_not_runtime_change=True,
        all_generated_ROMs_and_source_disposable_town_batteries_preserved=True,new_review_credit=0,full_goal_complete=False))
    print('Prepared registered V5756 build/exact clean patch/two current startup cases/existing release regressions.584 batches expected;main preserved.')
