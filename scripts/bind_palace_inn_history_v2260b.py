"""Use V799's exact registered parser for the label-layer family capture."""
from pathlib import Path
from dk4tool.patch import palace_label_boundaries
source=Path('scripts/bind_palace_inn_history_v2260.py').read_text().replace('palace_inn_history_v2260','palace_inn_history_v2260b')
old='owned=palace_editorial if group<3 else inn_editorial';assert source.count(old)==1
source=source.replace(old,'owned=palace_label_boundaries if group==2 else palace_editorial if group<3 else inn_editorial')
exec(compile(source,__file__,'exec'),globals())
