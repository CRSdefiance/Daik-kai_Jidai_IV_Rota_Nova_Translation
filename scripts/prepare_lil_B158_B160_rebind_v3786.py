"""Derive the remaining82 exact-byte source/current binding after verified V3778."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save
from dk4tool.patch.grand_race_menu_release import sha
if __name__=='__main__':
    row=derive('scripts/rebind_lil_B157_B160_source_v3744.py','scripts/rebind_lil_B158_B160_source_v3786.py',{
        'lil_B157_B160_source_v3744':'lil_B158_B160_source_v3786','editorial_handoff_verification_v3743':'editorial_handoff_verification_v3785',
        'lil_B156_B160_source_v3698':'lil_B157_B160_source_v3744','all233_clean_current_complete_context':'all157_clean_current_complete_context','reused466_dispatches_and127_source_exact_control_leaves':'reused314_dispatches_and84_source_exact_control_leaves',
        "157<=g['block']<=160":"158<=g['block']<=160","157<=c['block']<=160":"158<=c['block']<=160",'len(rows)==157':'len(rows)==82',"for g in groups)==317":"for g in groups)==207",'len(cases)==314 and len(leaves)==84':'len(cases)==164 and len(leaves)==57',
        "{'FI':8,'FA':0,'FO':0}":"{'FI':6,'FA':0,'FO':0}",'source_selector']==254 for r in rows)==6':'source_selector']==254 for r in rows)==4',
        'total_editorial_objects=157,speech_objects=157,ordinary_source_speeches=151,system_FE_panels=6':'total_editorial_objects=82,speech_objects=82,ordinary_source_speeches=78,system_FE_panels=4',
        'source_native_commands=317,source_relative_sites=76':'source_native_commands=207,source_relative_sites=68',
        'historical_snapshot_is_Lil_London_not_selected_B157_B160=True':'historical_snapshot_is_Lil_London_not_selected_B158_B160=True','historical_snapshot_is_Lil_London_not_selected_B156_B160':'historical_snapshot_is_Lil_London_not_selected_B157_B160',
        'all157_clean_current_complete_context.json':'all82_clean_current_complete_context.json','reused314_dispatches_and84_source_exact_control_leaves.json':'reused164_dispatches_and57_source_exact_control_leaves.json',
        'exact314_calls_reused_not_reexecuted':'exact164_calls_reused_not_reexecuted','all84_nonrelative_control_leaves_exact':'all57_nonrelative_control_leaves_exact','source_FE6_nullactor':'source_FE4_nullactor',
        'rebound=157,progressive=151,FE=6,commands=317,relative_sites=76':'rebound=82,progressive=78,FE=4,commands=207,relative_sites=68','exact_dispatch_reuses=314,exact_leaves=84':'exact_dispatch_reuses=164,exact_leaves=57','Bind157 untouched speeches to V3738':'Bind82 untouched speeches to V3778'})
    root=Path('work/analysis/lil_B158_B160_rebind_tools_v3786');assert not root.exists();root.mkdir(parents=True);save(root/'source_derivation.json',dict(tool=row,no_new_native_calls_or_source_prose_credit=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
