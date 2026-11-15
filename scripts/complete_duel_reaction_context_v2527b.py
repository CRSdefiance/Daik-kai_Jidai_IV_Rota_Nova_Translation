"""Preserve the pre-write schema failure and reconcile through its corrected adapter."""
from pathlib import Path
OLD=Path('scripts/complete_duel_reaction_context_v2527.py')
if __name__=='__main__':
 source=OLD.read_text()
 a='scripts.reconcile_contextual_duel_reaction_retentions_v2527 import'
 assert source.count(a)==1
 source=source.replace(a,'scripts.reconcile_contextual_duel_reaction_retentions_v2527b import')
 source=source.replace("'scripts/preflight_duel_reaction_context_v2521c.py']","'scripts/preflight_duel_reaction_context_v2521c.py','scripts/reconcile_contextual_duel_reaction_retentions_v2527.py','scripts/complete_duel_reaction_context_v2527.py']")
 exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
