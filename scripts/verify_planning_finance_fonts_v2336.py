"""Twenty-four complete current native Planning/Finance fonts and bounded copies."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
OLD=Path('scripts/verify_work_fonts_v2309.py')
if __name__=='__main__':
 source=OLD.read_text();changes={'work_fonts_v2309':'planning_finance_fonts_v2336','translations/work_contextual_editorial_manuscript_v1.json':'translations/planning_finance_contextual_editorial_manuscript_v1.json','work_current_v2310_V2284':'finance_current_v2335_V2284','scripts.work_comments_layout_v843 import compiled,layout':'scripts.planning_finance_layout_v860 import compiled,layout','range(1386,1410)':'range(1447,1471)','scripts/work_comments_layout_v843.py':'scripts/planning_finance_layout_v860.py','full36_cell1405_trailing_period_consumed_and_inside_visible_crop':'full35_cell1466_continuation_and_trailing_period_inside_visible_crop','assert len(cases)==24 and len(copies)==48;save(':'assert len(next(c for c in cases if c["message_ID"]==1466)["generated_lines"][1])==35;assert len(cases)==24 and len(copies)==48;save('}
 for old,new in changes.items():assert old in source,old;source=source.replace(old,new)
 exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
 save('work/analysis/planning_finance_fonts_v2336/producer_binding.json',dict(original=str(OLD),original_sha256=sha(OLD.read_bytes()),effective_source_sha256=sha(source.encode()),family_compiler='scripts/planning_finance_layout_v860.py',full_goal_complete=False))
