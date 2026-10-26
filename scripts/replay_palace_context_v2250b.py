"""Correct generated path escaping; preserve2250's failed research attempt."""
from pathlib import Path
source=Path('scripts/replay_palace_context_v2250.py').read_text()
source=source.replace('palace_context_v2250','palace_context_v2250b')
old=":snapshot['path']}";assert source.count(old)==1
source=source.replace(old,":Path(snapshot['path']).as_posix()}")
exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
