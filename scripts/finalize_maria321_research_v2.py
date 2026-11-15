"""Bind the original combined page/alignment assertion; preserve all other gates."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

_wrapper = checked_text(Path('scripts/finalize_maria321_research_v1.py').read_text(encoding='utf-8'), {
    '''    "stored['complete_stored_pages'] == native['pages'] == 302": "stored['complete_stored_pages'] == native['pages'] == 325",''':
        '''    "(native['pages'], stored['complete_stored_pages'], native['selected_alignment_cases']) == (302, 302, 1176)": "(native['pages'], stored['complete_stored_pages'], native['selected_alignment_cases']) == (325, 325, 1268)",''',
})
exec(compile(_wrapper, __file__+'::same-complete-finalizer-contract-correct-combined-assertion-anchor', 'exec'), globals())
