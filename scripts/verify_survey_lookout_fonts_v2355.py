"""All24 current Survey/Lookout native font cases and48 cold/warm copies."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
OLD=Path('scripts/verify_work_fonts_v2309.py')
if __name__=='__main__':
 source=OLD.read_text();changes={'work_fonts_v2309':'survey_lookout_fonts_v2355','translations/work_contextual_editorial_manuscript_v1.json':'translations/survey_lookout_contextual_editorial_manuscript_v1.json','work_current_v2310_V2284':'bridge_current_v2346_V2284','scripts.work_comments_layout_v843 import compiled,layout':'scripts.survey_lookout_layout_v875 import compiled,layout','range(1386,1410)':'range(1499,1523)','scripts/work_comments_layout_v843.py':'scripts/survey_lookout_layout_v875.py','full36_cell1405_trailing_period_consumed_and_inside_visible_crop':'all_survey_position_tool_sun_stars_and_conditional_lookout_words_inside_visible_crop'}
 for old,new in changes.items():assert old in source,old;source=source.replace(old,new)
 exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
 save('work/analysis/survey_lookout_fonts_v2355/producer_binding.json',dict(original=str(OLD),original_sha256=sha(OLD.read_bytes()),effective_source_sha256=sha(source.encode()),genuine_initialized_UI_from_current_bridge_run_reused=True,no_new_current_four_hero_visits_or_live_RAM_change=True,full_goal_complete=False))
