"""Advance the integrated handoff to the exact B210 clean-draft census."""
from pathlib import Path

from scripts.source_locked_derivation_v5118 import checked_text

parent=Path(__file__).with_name('save_rafael_B181_B200_release_checkpoint_v1.py')
source=checked_text(parent.read_text(encoding='utf-8'),{
    'scripts.qualify_rafael_B201_B220_clean_census_v1':'scripts.qualify_rafael_B201_B220_clean_census_v2',
    '(403,138,265)':'(403,179,224)',
    '138 clean drafts':'179 clean drafts',
    'other 265 clean drafts':'other 224 clean drafts',
    'The 138 clean drafts include all 12 captions for the six independent merchant offers in B208.':
        'The 179 clean drafts include all 12 captions for the six independent merchant offers in B208 and three captions for the book offer in B209.',
    'next_action=\'Continue clean drafts, then bind all complete exchanges to the verified cumulative ROM.\',\n            current_batch_not_yet_integrated=True,guide_photos=False)},':
        'next_action=\'Continue clean drafts from B211, then bind all complete exchanges to the verified cumulative ROM.\',\n'
        '            current_batch_not_yet_integrated=True,guide_photos=False),NEXT:dict(new_credit=0,independently_drafted_records=179,\n'
        '            independent_draft_blocks=list(range(201,211)),remaining_clean_meanings_anddrafts=224,\n'
        '            evidence={str(NEXT_CENSUS):digest(NEXT_CENSUS)})},',
    "    integrated=sys.argv[1:]==['--integrated']":
        "    integrated=sys.argv[1:]==['--integrated']\n    assert integrated",
})
if __name__ == '__main__':
    exec(compile(source,__file__+'::same-integrated-checkpoint-and-advanced-clean-intake', 'exec'),globals())
