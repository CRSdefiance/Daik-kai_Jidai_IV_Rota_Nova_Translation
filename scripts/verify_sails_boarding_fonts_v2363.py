"""All24 current native Sails/Boarding font cases and48 bounded copies."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
OLD=Path('scripts/verify_work_fonts_v2309.py')
if __name__=='__main__':
 source=OLD.read_text();changes={'work_fonts_v2309':'sails_boarding_fonts_v2363','translations/work_contextual_editorial_manuscript_v1.json':'translations/sails_boarding_contextual_editorial_manuscript_v1.json','work_current_v2310_V2284':'boarding_current_v2364_V2284','scripts.work_comments_layout_v843 import compiled,layout':'scripts.sails_boarding_layout_v881 import compiled,layout','range(1386,1410)':'range(1523,1547)','scripts/work_comments_layout_v843.py':'scripts/sails_boarding_layout_v881.py','full36_cell1405_trailing_period_consumed_and_inside_visible_crop':'complete_three_row1524_two_sail_types_and_wind_qualification_inside_visible_crop','assert len(cases)==24 and len(copies)==48;save(':'assert len(next(c for c in cases if c["message_ID"]==1524)["generated_lines"])==3;assert len(cases)==24 and len(copies)==48;save('}
 for old,new in changes.items():assert old in source,old;source=source.replace(old,new)
 exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
 save('work/analysis/sails_boarding_fonts_v2363/producer_binding.json',dict(original=str(OLD),original_sha256=sha(OLD.read_bytes()),effective_source_sha256=sha(source.encode()),registered_formatter='scripts/sails_boarding_layout_v881.py',all24_independent_complete_words_and_bodies_checked=True,full_goal_complete=False))
