"""Create separate output before executing the frozen Inn context researcher."""
from pathlib import Path
source=Path('scripts/replay_inn_context_v2251.py').read_text()
source=source.replace('inn_context_v2251','inn_context_v2251b')
old='source=OLD.read_text()';assert source.count(old)==1
source=source.replace(old,'ROOT.mkdir(parents=True);source=OLD.read_text()')
exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
