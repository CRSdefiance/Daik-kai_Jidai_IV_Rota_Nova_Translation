"""Current source1610 first-person expansion for all25 native actor models."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
OLD=Path('scripts/probe_battle_medical_pronoun_v900.py')
if __name__=='__main__':
 source=OLD.read_text();changes={'battle_medical_v900':'battle_medical_pronoun_v2391','all_routes_combined_v893_candidate':'all_routes_combined_v2284_candidate'}
 for old,new in changes.items():assert old in source,old;source=source.replace(old,new)
 exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
 save('work/analysis/battle_medical_pronoun_v2391/producer_binding.json',dict(original=str(OLD),original_sha256=sha(OLD.read_bytes()),effective_source_sha256=sha(source.encode()),historical_captured_models_are_CPU_inputs_not_new_current_hero_visits=True,no_ROM_live_RAM_or_name_change=True,full_goal_complete=False))
