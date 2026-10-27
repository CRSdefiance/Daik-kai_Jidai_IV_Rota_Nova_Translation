"""Fifty current original native selectors for Planning19 and Finance20."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
OLD=Path('scripts/replay_livestock_prayer_context_v2326.py')
if __name__=='__main__':
 source=OLD.read_text();changes={'scripts.prepare_livestock_prayer_context_v852':'scripts.prepare_planning_finance_context_v857','livestock_prayer_context_v2326':'planning_finance_context_v2333',"(17,1423,'Livestock'),(18,1435,'Chapel')":"(19,1447,'Planning'),(20,1459,'Finance')",'(17,1423),(18,1435)':'(19,1447),(20,1459)','range(1423,1447)':'range(1447,1471)','Sera_uses_ordinary_voice_no_special_override_for_roles17_or18':'Sera_uses_ordinary_voice_no_special_override_for_roles19_or20'}
 for old,new in changes.items():assert old in source,old;source=source.replace(old,new)
 exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
 save('work/analysis/planning_finance_context_v2333/producer_binding.json',dict(original=str(OLD),original_sha256=sha(OLD.read_bytes()),effective_source_sha256=sha(source.encode()),full_goal_complete=False))
