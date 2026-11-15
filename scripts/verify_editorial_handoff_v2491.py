"""Scoped audit:17 retentions,required consumer enums,and unchanged cumulative release."""
from pathlib import Path
OLD=Path('scripts/verify_editorial_handoff_v2483.py')
if __name__=='__main__':
 source=OLD.read_text();changes={'scripts.mood_comments_layout_v980':'scripts.activity_special_layout_v986b','mood_compiled':'activity_compiled','editorial_handoff_verification_v2483':'editorial_handoff_verification_v2491','1896':'1913','1240':'1257',"('mood_comments',activity_compiled,range(1833,1872))":"('activity_special',activity_compiled,range(1872,1889))",'range(1833,1872)':'range(1872,1889)','mood_comments_completion_v2482':'activity_special_completion_v2490',"h['fresh_reconciliations']==39":"h['fresh_reconciliations']==17",'247':'230',"'/COMMON/MESFILE.DK4':246":"'/COMMON/MESFILE.DK4':229",'V2483-audit-of-V2482':'V2491-audit-of-V2490','completed_this_turn=39,retained=39':'completed_this_turn=17,retained=17','all39':'all17'}
 for a,b in changes.items():assert a in source,a;source=source.replace(a,b)
 needle='  batches.append(dict('
 assert source.count(needle)==1
 source=source.replace(needle,"  assert Counter(r['consumer']for r in notes['records'])=={'Deck-CabinInfoView':14,'assignment-refusal-modal':3};assert final['current_native_mixed_consumer_font_executions']==23 and final['current_native_copies']==34 and final['historical_actual_holds']==18 and final['historical_returns_current_rechecked']==9\n"+needle)
 exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
