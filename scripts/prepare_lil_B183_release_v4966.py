"""Prepare the sole registered build, exact patch and current startup evidence."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B183_release_tools_v4966')
if __name__=='__main__':
    assert not ROOT.exists();tools=[]
    tools.append(derive('scripts/build_lil_B182_v4914.py','scripts/build_lil_B183_v4966.py',{
        'B182':'B183','build_v4914':'build_v4966','combined_v4914':'combined_v4966','registration_v4913':'registration_v4965','all-routes-unified-v4914':'all-routes-unified-v4966'}))
    tools.append(derive('scripts/verify_lil_B182_release_v4915.py','scripts/verify_lil_B183_release_v4967.py',{
        'B182':'B183','release_v4915':'release_v4967','combined_v4914':'combined_v4966','combined_v4867':'combined_v4914',
        'registration_v4913':'registration_v4965','build_v4914':'build_v4966','all-routes-unified-v4914':'all-routes-unified-v4966',
        'all-routes-unified-v4867':'all-routes-unified-v4914',"len(manifest['batches'])==564":"len(manifest['batches'])==565",
        'out/lil_B182_reference_v4898_RESEARCH_ONLY.nds':'out/lil_B183_reference_v4950_RESEARCH_ONLY.nds',
        'all564_manifest_batches':'all565_manifest_batches','exact_to_V4867':'exact_to_V4914','manifest_batches=564':'manifest_batches=565'}))
    tools.append(derive('scripts/run_lil_B182_startup_v4916.py','scripts/run_lil_B183_startup_v4968.py',{
        'B182':'B183','runs_v4916':'runs_v4968','version=4914':'version=4966','v4916_':'v4968_'}))
    tools.append(derive('scripts/verify_lil_B182_startup_v4917.py','scripts/verify_lil_B183_startup_v4969.py',{
        'B182':'B183','startup_v4917':'startup_v4969','runs_v4916':'runs_v4968','combined_v4914':'combined_v4966','combined_v4867':'combined_v4914',
        'work/analysis/lil_B181_runs_v4869':'work/analysis/lil_B182_runs_v4916','V4867':'V4914','matchV4867':'matchV4914','Current4914':'Current4966'}))
    tools.append(derive('scripts/record_lil_B182_startup_view_v4917.py','scripts/record_lil_B183_startup_view_v4969.py',{
        'B182':'B183','startup_v4917':'startup_v4969','equal_V4867':'equal_V4914'}))
    tools.append(derive('scripts/pin_lil_B182_v4918.py','scripts/pin_lil_B183_v4970.py',{
        'B182':'B183','retention_v4918':'retention_v4970','release_v4915':'release_v4967','reference_v4898':'reference_v4950','display_v4903':'display_v4957','V4914':'V4966'}))
    ROOT.mkdir(parents=True);save(ROOT/'prepared_tools.json',dict(tools=tools,profile='all-routes-unified-v4966',expected_manifest_batches=565,accepted_layers=114,
        prior_exact_font_startup_controls_reused_without_new_parent_runs=True,new_ROM_or_emulator_or_credit_change=False,full_goal_complete=False))
