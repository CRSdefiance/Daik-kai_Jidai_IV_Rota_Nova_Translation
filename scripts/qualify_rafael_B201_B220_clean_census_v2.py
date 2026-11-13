"""Advance the clean census through Ian's book offer and the Namahage scene."""
from pathlib import Path

from scripts.source_locked_derivation_v5118 import checked_text

parent=Path(__file__).with_name('qualify_rafael_B201_B220_clean_census_v1.py')
source=checked_text(parent.read_text(encoding='utf-8'),{
    "('B201_B203','B204_B206','B207_B208')": "('B201_B203','B204_B206','B207_B208','B209_B210')",
    'clean_source_census_v1.json': 'clean_source_census_v2.json',
    '[47,35,56]':'[47,35,56,41]',
    'list(range(201,209))':'list(range(201,211))',
    "for d in drafts)==12":"for d in drafts)==15",
    "len(drafted)==138 and drafted=={key(r) for r in rows if r['block']<=208}":
        "len(drafted)==179 and drafted=={key(r) for r in rows if r['block']<=210}",
    'independent_drafts=138,clean_draft_speeches=126,clean_draft_captions=12':
        'independent_drafts=179,clean_draft_speeches=164,clean_draft_captions=15',
    'remaining_clean_drafts=265':'remaining_clean_drafts=224',
    '138 drafts':'179 drafts',
})
if __name__ == '__main__':
    exec(compile(source,__file__+'::exact-clean-only-coverage-through-B210', 'exec'),globals())
