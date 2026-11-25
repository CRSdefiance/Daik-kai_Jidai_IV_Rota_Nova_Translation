"""Keep the complete preparation and bind dependencies against the original source."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

_wrapper = checked_text(Path('scripts/prepare_maria321_registered_v1.py').read_text(encoding='utf-8'), {
    '''    "Path('scripts/finalize_maria321_research_v3.py'),Path(__file__)":''':
        '''    "Path('scripts/finalize_maria305_research_v1.py'),Path(__file__)":''',
})
exec(compile(_wrapper,__file__+'::same-preparation-original-source-dependency-anchor','exec'),globals())
