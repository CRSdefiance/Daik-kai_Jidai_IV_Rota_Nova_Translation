"""Preserve failed import;use the checked case-sensitive helper successor."""
from pathlib import Path
OLD=Path('scripts/complete_battle_declaration_context_v2499.py')
if __name__=='__main__':
 source=OLD.read_text();a='scripts.reconcile_contextual_declaration_retentions_v2499 import';assert source.count(a)==1;source=source.replace(a,'scripts.reconcile_contextual_declaration_retentions_v2499b import');source=source.replace("'scripts/reconcile_contextual_mood_retentions_v2482.py']","'scripts/reconcile_contextual_mood_retentions_v2482.py','scripts/reconcile_contextual_declaration_retentions_v2499.py','scripts/complete_battle_declaration_context_v2499.py']")
 exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
