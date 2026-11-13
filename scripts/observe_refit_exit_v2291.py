"""Same read-only revised font observer in a separate successor run folder."""
from pathlib import Path
source=Path('scripts/observe_refit_spritsail_v2286.py').read_text().replace('refit_spritsail_actual_v2287','refit_spritsail_actual_v2292')
exec(compile(source,__file__,'exec'),globals())
