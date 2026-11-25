"""Advance the exact clean intake through all five drafted blocks."""
from pathlib import Path

from scripts.source_locked_derivation_v5118 import checked_text


parent=Path(__file__).with_name('qualify_rafael_B221_B240_clean_v1.py')
source=checked_text(parent.read_text(encoding='utf-8'),{
    'clean_source_census_v1.json':'clean_source_census_v2.json',
    "'B221_B222_clean_drafts_v1')":"'B221_B222_clean_drafts_v1','B223_B225_clean_drafts_v1')",
    'packet,styles,choices,drafts=map(load,INPUTS)':'packet,styles,choices,*drafts=map(load,INPUTS)',
    "drafted=set(map(key,drafts['records']))":"drafted={key(r) for doc in drafts for r in doc['records']}",
    "len(drafted)==30 and drafted=={key(r) for r in rows if r['block'] in (221,222)}":
        "len(drafted)==74 and drafted=={key(r) for r in rows if r['block'] in range(221,226)}",
    "for p,h in drafts['evidence'].items()":"for doc in drafts for p,h in doc['evidence'].items()",
    'independently_drafted_records=30,complete_draft_blocks=[221,222],remaining_clean_drafts=240':
        'independently_drafted_records=74,complete_draft_blocks=list(range(221,226)),remaining_clean_drafts=196',
    '270 clean source objects, 30 independent drafts':'270 clean source objects, 74 independent drafts',
})
if __name__=='__main__':
    exec(compile(source,__file__+'::same-clean-census-through-B225','exec'),globals())

