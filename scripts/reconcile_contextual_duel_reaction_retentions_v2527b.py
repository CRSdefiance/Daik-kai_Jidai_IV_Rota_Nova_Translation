"""Read the legacy context's current_ROM_sha256 field without altering its proof."""
from pathlib import Path
OLD=Path('scripts/reconcile_contextual_duel_reaction_retentions_v2527.py')
source=OLD.read_text()
needle="exec(compile(source,__file__,'exec'),globals())"
assert source.count(needle)==1
source=source.replace(needle,"source=source.replace(\"context['candidate_sha256']\",\"context['current_ROM_sha256']\")\n"+needle)
exec(compile(source,__file__,'exec'),globals())
