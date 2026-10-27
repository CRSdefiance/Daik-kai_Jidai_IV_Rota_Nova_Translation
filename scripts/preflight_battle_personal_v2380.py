"""Next25 source/compiler preflight against the registered battle-personal stage."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
OLD=Path('scripts/preflight_livestock_prayer_v2325.py')
if __name__=='__main__':
 source=OLD.read_text();changes={'scripts.livestock_prayer_layout_v854':'scripts.battle_personal_layout_v892','livestock_prayer_preflight_v2325':'battle_personal_preflight_v2380','livestock_prayer_context_source_v2324/all24':'battle_personal_context_source_v2379/all25','livestock_prayer_editorial':'battle_personal_editorial','range(1423,1447)':'range(1571,1596)','==1447':'==1595','registered_livestock854_compiler_used':'registered_battle_personal892_compiler_used','next24_preflight':'next25_preflight','all24_complete_clean_current_compiled_payloads_match':'all25_complete_clean_current_compiled_payloads_match','next_records=24':'next_records=25'}
 for old,new in changes.items():assert old in source,old;source=source.replace(old,new)
 exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
 save('work/analysis/battle_personal_preflight_v2380/producer_binding.json',dict(original=str(OLD),original_sha256=sha(OLD.read_bytes()),effective_source_sha256=sha(source.encode()),no_new_editorial_credit=True,full_goal_complete=False))
