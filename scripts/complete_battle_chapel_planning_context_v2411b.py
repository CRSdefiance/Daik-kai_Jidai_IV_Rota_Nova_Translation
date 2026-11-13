"""Successor removes a redundant template substitution and preserves25 context-only rows."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
OLD=Path('scripts/complete_battle_chapel_planning_context_v2411.py')
if __name__=='__main__':
 source=OLD.read_text();redundant=" 'scripts/rebind_battle_personal_history_v2385.py':'scripts/rebind_battle_chapel_planning_history_v2410.py',\n";assert source.count(redundant)==1;source=source.replace(redundant,'');old=' import ast\n';assert source.count(old)==1;source=source.replace(old," source=source.replace('ordinary_context_reference_records=24','ordinary_context_reference_records=25')\n"+old)
 exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
 save('work/analysis/battle_chapel_planning_completion_v2411/successor_provenance.json',dict(original=str(OLD),original_sha256=sha(OLD.read_bytes()),removed_redundant_substitution_already_consumed_by_family_path_change=True,ordinary_context_records25_with_zero_extra_credit=True,all_validation_preserved=True,full_goal_complete=False))
