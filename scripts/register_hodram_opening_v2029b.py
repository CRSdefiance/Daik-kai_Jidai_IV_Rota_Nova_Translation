"""Use the compiler successor's severity-aware QA; no prose or gate relaxation."""
from pathlib import Path
SOURCE=Path('scripts/register_hodram_opening_v2029.py')
if __name__=='__main__':
    text=SOURCE.read_text(encoding='utf-8')
    changes={
        'from dk4tool.patch import hodram_opening_editorial as owned':'from dk4tool.patch import hodram_opening_editorial_v2 as owned',
        'dk4tool/patch/hodram_opening_editorial.py':'dk4tool/patch/hodram_opening_editorial_v2.py',
        'from dk4tool.patch.hodram_opening_editorial import':'from dk4tool.patch.hodram_opening_editorial_v2 import',
        'translations/hodram_opening_editorial_release_v1.json':'translations/hodram_opening_editorial_release_v2.json',
        'hodram_opening_release_v2029':'hodram_opening_release_v2029b',
        'release_stack_v2029_pending.json':'release_stack_v2029b_pending.json',
    }
    for old,new in changes.items():
        assert old in text,old
        text=text.replace(old,new)
    exec(compile(text,str(SOURCE),'exec'),{'__name__':'__main__','__file__':__file__})
