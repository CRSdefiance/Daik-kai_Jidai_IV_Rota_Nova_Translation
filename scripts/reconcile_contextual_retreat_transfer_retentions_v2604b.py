"""Preserve2604;match only the executable final adapter call,not its quoted text."""
from pathlib import Path
source=Path('scripts/reconcile_contextual_retreat_transfer_retentions_v2604.py').read_text();old='needle="exec(compile(source,__file__,\'exec\'),globals())"';assert source.count(old)==1
source=source.replace(old,'needle="\\nexec(compile(source,__file__,\'exec\'),globals())"')
exec(compile(source,__file__,'exec'),globals())
