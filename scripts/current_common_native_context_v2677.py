"""Use the registered2674 parser with the proven bounded current-code context."""
from pathlib import Path
source=Path('scripts/current_common_native_context_v2620b.py').read_text()
needle="exec(compile(source,__file__,'exec'),globals())"
replacement="source=source.replace('from dk4tool.patch.refit_contextual_spritsail_v1 import current_entries','from dk4tool.patch.surrender_advice_contextual_v1 import current_entries')\n"+needle
assert source.count(needle)==1
exec(compile(source.replace(needle,replacement),__file__,'exec'),globals())
