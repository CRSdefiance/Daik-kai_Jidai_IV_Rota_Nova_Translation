"""Retain the apostrophe syntax diagnostic and run the corrected clean-only gloss producer."""
from pathlib import Path
if __name__=='__main__':
    source=Path('scripts/read_lil_B184_clean_context_v5038.py');text=source.read_text(encoding='utf-8')
    old="'It is strange that something this delicious had not been popular before now,isn't it?'"
    assert text.count(old)==1
    text=text.replace(old,'"It is strange that something this delicious had not been popular before now,isn\'t it?"').replace('lil_B184_clean_context_v5038','lil_B184_clean_context_v5038b')
    exec(compile(text,str(source)+'::apostrophe-corrected','exec'),{'__name__':'__main__','__file__':__file__})
