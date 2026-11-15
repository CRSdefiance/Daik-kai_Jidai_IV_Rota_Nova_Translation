"""Preserve failed authoring draft;correct one invalid Python metadata identifier."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
OLD=Path('scripts/review_battle_declaration_v2495.py')
if __name__=='__main__':
 source=OLD.read_text();a='1902_1909_telling_target_not_direct_attack_command=True';assert source.count(a)==1;source=source.replace(a,'messages1902_1909_telling_target_not_direct_attack_command=True')
 exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
 save('work/analysis/battle_declaration_editorial_v2495/producer_binding.json',dict(failed_authoring_draft=str(OLD),failed_draft_sha256=sha(OLD.read_bytes()),failure='SyntaxError before execution:metadata keyword began with digits',failure_created_no_outputs_or_coverage=True,corrected_metadata_identifier_only=True,effective_source_sha256=sha(source.encode()),full_goal_complete=False))
