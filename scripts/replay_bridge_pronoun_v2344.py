"""Current native IC first-person expansion and established First Mate/Xien terms."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
OLD=Path('scripts/probe_bridge_pronoun_v867.py')
if __name__=='__main__':
 source=OLD.read_text();changes={'bridge_duties_v867':'bridge_pronoun_v2344','all_routes_combined_v863_candidate':'all_routes_combined_v2284_candidate'}
 for old,new in changes.items():assert old in source,old;source=source.replace(old,new)
 exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
 save('work/analysis/bridge_pronoun_v2344/producer_binding.json',dict(original=str(OLD),original_sha256=sha(OLD.read_bytes()),effective_source_sha256=sha(source.encode()),historical_snapshots_are_CPU_inputs_not_new_current_four_hero_visits=True,no_ROM_live_RAM_or_name_change=True,full_goal_complete=False))
