"""Record Rafael2952 with the source-only progress through B225."""
from pathlib import Path

from scripts.source_locked_derivation_v5118 import checked_text


parent=Path(__file__).with_name('save_rafael2952_registered_checkpoint_v1.py')
source=checked_text(parent.read_text(encoding='utf-8'),{
    'from scripts.qualify_rafael_B221_B240_clean_v1 import OUT as NEXT':
        "NEXT=Path('work/analysis/Rafael_B221_B240_clean_20261106/clean_source_census_v2.json')",
    "next_batch['independently_drafted_records']==30":"next_batch['independently_drafted_records']==74",
    'with 30 independent drafts':'with 74 independent drafts',
    'The letter and red-sword rumor have 30 clean-first drafts, including 15 voice variants. Complete the remaining 240 drafts before opening current English.':
        'The five drafted exchanges cover the Muramasa letter, the red sword rumor, the swans, the Three Kingdoms fan and Kublai Khan’s prophecy. Complete the remaining 196 drafts before opening current English.',
    'Draft the remaining 240 clean objects':'Draft the remaining 196 clean objects',
    'independently_drafted_records=30,independent_draft_blocks=[221,222]':
        'independently_drafted_records=74,independent_draft_blocks=list(range(221,226))',
    'remaining_clean_meanings_anddrafts=240':'remaining_clean_meanings_anddrafts=196',
})
if __name__=='__main__':
    exec(compile(source,__file__+'::same-registered-checkpoint-advanced-clean-intake','exec'),globals())

