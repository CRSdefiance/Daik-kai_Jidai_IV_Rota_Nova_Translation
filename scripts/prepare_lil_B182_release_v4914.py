"""Prepare sole registered build, clean-input reconstruction and exact-current startup."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B182_release_tools_v4914')
if __name__=='__main__':
    assert not ROOT.exists();tools=[]
    tools.append(derive('scripts/build_lil_B181_v4867.py','scripts/build_lil_B182_v4914.py',{
        'B181':'B182','build_v4867':'build_v4914','combined_v4867':'combined_v4914',
        'registration_v4866b':'registration_v4913','all-routes-unified-v4867':'all-routes-unified-v4914'}))
    tools.append(derive('scripts/verify_lil_B181_release_v4868.py','scripts/verify_lil_B182_release_v4915.py',{
        'B181':'B182','editorial_v1 as owned':'editorial_v1 as owned','release_v4868':'release_v4915',
        'combined_v4867':'combined_v4914','combined_v4821':'combined_v4867','registration_v4866b':'registration_v4913',
        'build_v4867':'build_v4914','all-routes-unified-v4867':'all-routes-unified-v4914',
        'all-routes-unified-v4821':'all-routes-unified-v4867',"len(manifest['batches'])==563":"len(manifest['batches'])==564",
        'out/lil_B181_reference_v4852_RESEARCH_ONLY.nds':'out/lil_B182_reference_v4898_RESEARCH_ONLY.nds',
        'all563_manifest_batches':'all564_manifest_batches','exact_to_V4821':'exact_to_V4867','manifest_batches=563':'manifest_batches=564'}))
    tools.append(derive('scripts/run_lil_B181_startup_v4869.py','scripts/run_lil_B182_startup_v4916.py',{
        'B181':'B182','runs_v4869':'runs_v4916','version=4867':'version=4914','v4869_':'v4916_'}))
    tools.append(derive('scripts/verify_lil_B181_startup_v4870.py','scripts/verify_lil_B182_startup_v4917.py',{
        'B181':'B182','startup_v4870':'startup_v4917','runs_v4869':'runs_v4916',
        'combined_v4867':'combined_v4914','combined_v4821':'combined_v4867',
        'work/analysis/lil_B180_runs_v4823':'work/analysis/lil_B181_runs_v4869',
        'V4821':'V4867','matchV4821':'matchV4867','Current4867':'Current4914'}))
    tools.append(derive('scripts/record_lil_B181_startup_view_v4870.py','scripts/record_lil_B182_startup_view_v4917.py',{
        'B181':'B182','startup_v4870':'startup_v4917','equal_V4821':'equal_V4867'}))
    ROOT.mkdir(parents=True);save(ROOT/'prepared_tools.json',dict(tools=tools,profile='all-routes-unified-v4914',
        expected_manifest_batches=564,accepted_layers=114,prior_exact_font_startup_controls_reused_without_new_parent_runs=True,
        new_ROM_or_emulator_or_credit_change=False,full_goal_complete=False))
    print('Prepared registered V4914 build,exact clean-input patch verification and two current startup cold boots.')
