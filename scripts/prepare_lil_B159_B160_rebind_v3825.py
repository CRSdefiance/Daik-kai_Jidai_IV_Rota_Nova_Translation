"""Derive the remaining63 exact-byte source/current binding after verified V3819."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save
from dk4tool.patch.grand_race_menu_release import sha
if __name__=='__main__':
    row=derive('scripts/rebind_lil_B158_B160_source_v3786.py','scripts/rebind_lil_B159_B160_source_v3825.py',{
        'lil_B158_B160_source_v3786':'lil_B159_B160_source_v3825','editorial_handoff_verification_v3785':'editorial_handoff_verification_v3824',
        'lil_B157_B160_source_v3744':'lil_B158_B160_source_v3786','all157_clean_current_complete_context':'all82_clean_current_complete_context','reused314_dispatches_and84_source_exact_control_leaves':'reused164_dispatches_and57_source_exact_control_leaves',
        "158<=g['block']<=160":"159<=g['block']<=160","158<=c['block']<=160":"159<=c['block']<=160",'len(rows)==82':'len(rows)==63',"for g in groups)==207":"for g in groups)==142",'len(cases)==164 and len(leaves)==57':'len(cases)==126 and len(leaves)==35',
        "{'FI':6,'FA':0,'FO':0}":"{'FI':5,'FA':0,'FO':0}","source_selector']==254 for r in rows)==4":"source_selector']==254 for r in rows)==0",
        'total_editorial_objects=82,speech_objects=82,ordinary_source_speeches=78,system_FE_panels=4':'total_editorial_objects=63,speech_objects=63,ordinary_source_speeches=63,system_FE_panels=0',
        'source_native_commands=207,source_relative_sites=68':'source_native_commands=142,source_relative_sites=44',
        'historical_snapshot_is_Lil_London_not_selected_B158_B160=True':'historical_snapshot_is_Lil_London_not_selected_B159_B160=True','historical_snapshot_is_Lil_London_not_selected_B157_B160':'historical_snapshot_is_Lil_London_not_selected_B158_B160',
        'all82_clean_current_complete_context.json':'all63_clean_current_complete_context.json','reused164_dispatches_and57_source_exact_control_leaves.json':'reused126_dispatches_and35_source_exact_control_leaves.json',
        'exact164_calls_reused_not_reexecuted':'exact126_calls_reused_not_reexecuted','all57_nonrelative_control_leaves_exact':'all35_nonrelative_control_leaves_exact','source_FE4_nullactor_consumer_separately_preserved':'no_source_FE_consumer_in_remaining63',
        'rebound=82,progressive=78,FE=4,commands=207,relative_sites=68':'rebound=63,progressive=63,FE=0,commands=142,relative_sites=44','exact_dispatch_reuses=164,exact_leaves=57':'exact_dispatch_reuses=126,exact_leaves=35','Bind82 untouched speeches to V3778':'Bind63 untouched speeches to V3819'})
    root=Path('work/analysis/lil_B159_B160_rebind_tools_v3825');assert not root.exists();root.mkdir(parents=True);save(root/'source_derivation.json',dict(tool=row,no_new_native_calls_or_source_prose_credit=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
