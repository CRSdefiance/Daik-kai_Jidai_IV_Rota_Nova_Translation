"""Successor preflight binds Planning19/Finance20 to its own registered compiler."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
OLD=Path('scripts/preflight_livestock_prayer_v2325.py')
if __name__=='__main__':
 source=OLD.read_text();changes={'scripts.livestock_prayer_layout_v854':'scripts.planning_finance_layout_v860','livestock_prayer_preflight_v2325':'planning_finance_preflight_v2332','livestock_prayer_context_source_v2324':'planning_finance_context_source_v2331','livestock_prayer_editorial':'planning_finance_editorial','range(1423,1447)':'range(1447,1471)','==1447':'==1471','registered_livestock854_compiler_used':'registered_planning860_compiler_used'}
 for old,new in changes.items():assert old in source,old;source=source.replace(old,new)
 exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
 save('work/analysis/planning_finance_preflight_v2332/producer_binding.json',dict(original=str(OLD),original_sha256=sha(OLD.read_bytes()),effective_source_sha256=sha(source.encode()),fresh_credit=0,full_goal_complete=False))
