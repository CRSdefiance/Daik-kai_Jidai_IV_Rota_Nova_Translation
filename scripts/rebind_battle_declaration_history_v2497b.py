"""Preserve incomplete rebinder;provide the missing explicit historical ROM binding."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
OLD=Path('scripts/rebind_battle_declaration_history_v2497.py')
if __name__=='__main__':
 source=OLD.read_text();a="'oldarm':oldarm,'finish':finish";assert source.count(a)==1;source=source.replace(a,"'oldarm':oldarm,'oldrom':oldrom,'finish':finish");source=source.replace('activity_special_unused','activity_special_unused').replace('battle_declaration_history_v2497','battle_declaration_history_v2497b')
 exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
 save('work/analysis/battle_declaration_history_v2497b/successor_binding.json',dict(failed_producer=str(OLD),failed_producer_sha256=sha(OLD.read_bytes()),failure='NameError:missing oldrom in scoped finish namespace before any output or credit',explicit_historical_ROM_binding_added=True,effective_source_sha256=sha(source.encode()),full_goal_complete=False))
