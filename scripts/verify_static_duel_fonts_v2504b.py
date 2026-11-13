"""Correct pre-execution syntax preflight;preserve the draft without output credit."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
OLD=Path('scripts/verify_static_duel_fonts_v2504.py')
if __name__=='__main__':
 source=OLD.read_text();assert source.count('else255')==1;source=source.replace('else255','else 255').replace('static_duel_fonts_v2504','static_duel_fonts_v2504b');compile(source,__file__,'exec');exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
 save('work/analysis/static_duel_fonts_v2504b/producer_binding.json',dict(failed_syntax_preflight_draft=str(OLD),failed_draft_sha256=sha(OLD.read_bytes()),syntax_only_correction_before_any_execution_or_output=True,effective_source_sha256=sha(source.encode()),full_goal_complete=False))
