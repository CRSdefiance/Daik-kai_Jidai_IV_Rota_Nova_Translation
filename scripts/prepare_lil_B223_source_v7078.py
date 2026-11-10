"""Bind17 complete B223 source/current objects under the exact current2b6 runtime."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text,derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B223_source_tools_v7078')
if __name__=='__main__':
    assert not ROOT.exists()
    jobs=[('scripts/lil_B222_source_span_binding_v7037.py','scripts/lil_B223_source_span_binding_v7078.py',{'out/all_routes_combined_v7029_candidate.nds':'out/all_routes_combined_v7067_candidate.nds'}),
    ('scripts/map_lil_B214_source_v6697.py','scripts/map_lil_B223_source_v7078.py',{'B214':'B223','source_v6697':'source_v7078','verification_v6692':'verification_v7073','clean_context_v6695/all17_clean_letter_reaction_and_notice_glosses_before_old_English':'clean_context_v7076/all17_clean_Timur_armor_letter_reaction_and_notice_glosses_before_old_English','current_V6686_native_v6696':'current_V7067_native_v7077','lil_B211_source_span_binding_v6550c':'lil_B223_source_span_binding_v7078','len(known)==6526':'len(known)==6635','blocks[214]':'blocks[223]','block=214':'block=223','len(old)==27':'len(old)==22','(1316,1316,1314,1314) and source[1314:]==target[1314:]==bytes(2)':'(1316,1316,1316,1316) and source[1316:]==target[1316:]==bytes(0)','source_logical_end=1314,current_logical_end=1314,source_tail_bytes=2,current_tail_bytes=2':'source_logical_end=1316,current_logical_end=1316,source_tail_bytes=0,current_tail_bytes=0','source_static_actor_selectors=[2,4,23]':'source_static_actor_selectors=[2,13,21]','source_native_commands=27':'source_native_commands=22','natural_event214_activation':'natural_event223_activation'})]
    for a,b,c in jobs:assert not Path(b).exists();checked_text(Path(a).read_text('utf8'),c)
    rows=[derive(a,b,c) for a,b,c in jobs];ROOT.mkdir(parents=True);save(ROOT/'source_locked_complete_B223_comparison.json',dict(tools=rows,current2b6_runtime_and_every_native_numeric_constant_preserved=True,all17_clean_glosses_before_old_English_comparison=True,all1316_stored_and_logical_source_bytes_no_tail=True,new_credit=0,full_goal_complete=False))
