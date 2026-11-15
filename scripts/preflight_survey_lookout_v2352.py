"""Next24 source/compiler preflight;no fresh review credit."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
OLD=Path('scripts/preflight_livestock_prayer_v2325.py')
if __name__=='__main__':
 source=OLD.read_text();changes={'scripts.livestock_prayer_layout_v854':'scripts.survey_lookout_layout_v875','livestock_prayer_preflight_v2325':'survey_lookout_preflight_v2352','livestock_prayer_context_source_v2324':'survey_lookout_context_source_v2351','livestock_prayer_editorial':'survey_lookout_editorial','range(1423,1447)':'range(1499,1523)','==1447':'==1523','registered_livestock854_compiler_used':'registered_survey875_compiler_used'}
 for old,new in changes.items():assert old in source,old;source=source.replace(old,new)
 exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
 save('work/analysis/survey_lookout_preflight_v2352/producer_binding.json',dict(original=str(OLD),original_sha256=sha(OLD.read_bytes()),effective_source_sha256=sha(source.encode()),no_new_editorial_credit=True,full_goal_complete=False))
