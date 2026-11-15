"""Prepare sole registered build and current startup for the cumulative one-message reflow."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

if __name__=='__main__':
    root=Path('work/analysis/earlier775_release_tools_v4987');assert not root.exists();tools=[]
    tools.append(derive('scripts/build_lil_B183_v4966.py','scripts/build_earlier775_v4987.py',{
        'lil_B183_build_v4966':'earlier775_build_v4987','combined_v4966':'combined_v4987','lil_B183_registration_v4965':'earlier775_registration_v4986',
        'all-routes-unified-v4966':'all-routes-unified-v4987'}))
    tools.append(derive('scripts/run_lil_B183_startup_v4968.py','scripts/run_earlier775_startup_v4989.py',{
        'lil_B183_runs_v4968':'earlier775_runs_v4989','version=4966':'version=4987','lil_B183_v4968_':'earlier775_v4989_',
        'selected_B183':'selected_recommendation775','selected B183':'selected recommendation775'}))
    tools.append(derive('scripts/verify_lil_B183_startup_v4969.py','scripts/verify_earlier775_startup_v4990.py',{
        'lil_B183_startup_v4969':'earlier775_startup_v4990','lil_B183_runs_v4968':'earlier775_runs_v4989',
        'combined_v4966':'combined_v4987','combined_v4914':'combined_v4966','work/analysis/lil_B182_runs_v4916':'work/analysis/lil_B183_runs_v4968',
        'V4914':'V4966','matchV4914':'matchV4966','Current4966':'Current4987','actual_selected_B183_IDs':'actual_selected_recommendation775_IDs'}))
    tools.append(derive('scripts/record_lil_B183_startup_view_v4969.py','scripts/record_earlier775_startup_view_v4990.py',{
        'lil_B183_startup_v4969':'earlier775_startup_v4990','equal_V4914':'equal_V4966','source_B183_not_selected':'source_recommendation775_not_selected'}))
    root.mkdir(parents=True);save(root/'prepared_tools.json',dict(tools=tools,expected_manifest_batches=566,accepted_layers=114,no_build_or_credit_change_yet=True,full_goal_complete=False))
