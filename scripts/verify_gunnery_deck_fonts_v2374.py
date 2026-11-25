"""All24 current native Gunnery/Deck fonts and48 cold/warm COMMON copies."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
OLD=Path('scripts/verify_work_fonts_v2309.py')
if __name__=='__main__':
 source=OLD.read_text();changes={'work_fonts_v2309':'gunnery_deck_fonts_v2374','translations/work_contextual_editorial_manuscript_v1.json':'translations/gunnery_deck_contextual_editorial_manuscript_v1.json','work_current_v2310_V2284':'gunnery_current_v2375_V2284','scripts.work_comments_layout_v843 import compiled,layout':'scripts.gunnery_deck_layout_v887 import compiled,layout','range(1386,1410)':'range(1547,1571)','scripts/work_comments_layout_v843.py':'scripts/gunnery_deck_layout_v887.py','full36_cell1405_trailing_period_consumed_and_inside_visible_crop':'complete_test_firing_empty_stomach_mentor_IC_literal_and_Emilio_words_inside_crop'}
 for old,new in changes.items():assert old in source,old;source=source.replace(old,new)
 exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
 save('work/analysis/gunnery_deck_fonts_v2374/producer_binding.json',dict(original=str(OLD),original_sha256=sha(OLD.read_bytes()),effective_source_sha256=sha(source.encode()),registered_formatter='scripts/gunnery_deck_layout_v887.py',full_goal_complete=False))
