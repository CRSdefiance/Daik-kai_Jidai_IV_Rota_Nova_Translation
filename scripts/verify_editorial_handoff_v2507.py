"""Final20-row audit,distinct-duel contracts and corrected historical name binding."""
from pathlib import Path
OLD=Path('scripts/verify_editorial_handoff_v2483.py')
if __name__=='__main__':
 source=OLD.read_text()
 changes={'from scripts.mood_comments_layout_v980 import compiled as mood_compiled':'from scripts.duel_editorial_layout_v1155 import compiled as static_compiled','editorial_handoff_verification_v2483':'editorial_handoff_verification_v2507','1896':'1955','1240':'1299',"('mood_comments',mood_compiled,range(1833,1872))":"('static_duel',static_compiled,range(1931,1951))",'range(1833,1872)':'range(1931,1951)','mood_comments_completion_v2482':'static_duel_completion_v2506',"h['fresh_reconciliations']==39":"h['fresh_reconciliations']==20",'247':'188',"'/COMMON/MESFILE.DK4':246":"'/COMMON/MESFILE.DK4':187",'V2483-audit-of-V2482':'V2507-audit-of-V2506','completed_this_turn=39,retained=39':'completed_this_turn=20,retained=20','all39':'all20'}
 for a,b in changes.items():
  assert a in source,a
  source=source.replace(a,b)
 needle='  batches.append(dict('
 assert source.count(needle)==1
 source=source.replace(needle,"  assert Counter(r['consumer']for r in notes['records'])=={'original-duel-side0-actor-text':8,'original-duel-side1-actor-text':12};assert final['current_native_static_duel_font_executions']==36 and final['current_native_copies']==40 and final['current_parent_draw_controls']==0 and final['historical_actual_holds']==6 and final['historical_original_duel_terminal_transitions_current_bound']==1;assert len(final['registered_stage_binding']['registered_layer_native_IDs'])==33 and final['registered_stage_binding']['selected_static_native_IDs']==list(ids);history=read('work/analysis/static_duel_history_v2505c/historical_static_duel_current_binding.json');assert history['actual_historical_challenge_name']=='Centurione'and'original_actor_IDs_1_32_and_conditional_Clifford_name_unchanged'not in history\n"+needle)
 exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
