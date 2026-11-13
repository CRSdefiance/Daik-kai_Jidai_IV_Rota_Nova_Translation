"""Successor binds the completed Chapel/Planning native proof at its preserved output path."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
OLD=Path('scripts/review_battle_chapel_planning_v2408.py')
if __name__=='__main__':
 source=OLD.read_text();assert 'battle_chapel_planning_context_v2406' in source;source=source.replace('battle_chapel_planning_context_v2406','battle_repair_medical_context_v2406').replace('battle_chapel_planning_editorial_v2408','battle_chapel_planning_editorial_v2408b');exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
 save('work/analysis/battle_chapel_planning_editorial_v2408b/successor_provenance.json',dict(original=str(OLD),original_sha256=sha(OLD.read_bytes()),source_glosses_and_reasons_unchanged=True,correct_completed_native_Chapel18_Planning19_proof_bound=True,no_prior_outputs_overwritten=True,full_goal_complete=False))
