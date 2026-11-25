"""Check all 175 stored tutorial speech bodies against the original catalogue lookup."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

TEMPLATE=Path('scripts/check_rafael_B36_B41_stored_catalogue.py')
source=checked_text(TEMPLATE.read_text(encoding='utf-8'),{
    'Rafael_B36_B41_stored_catalogue_20261104':'Rafael_B177_B180_stored_catalogue_v1_20261105',
    'Rafael_B36_B41_stored_native_20261104':'Rafael_B177_B180_stored_v1_20261105',
    'Rafael_B36_B41_current_20261104':'Rafael_B177_B180_current1424_20261105',
    'assert len(previous_aliases)==3':"assert set(previous_aliases)<={row['id'] for row in rows}",
    '175 newly stored bodies survive original catalogue lookup byte forbyte;three former alias overrides cannot restore old glyphs orwrapping.':
        '175 stored tutorial bodies pass the original full-buffer catalogue lookup.',
    '[STORED,CURRENT,Path(original.__file__),Path(__file__)]':'[STORED,CURRENT,TEMPLATE,Path(original.__file__),Path(__file__)]',
})
if __name__=='__main__':
    exec(compile(source,__file__+'::same-full-buffer-lookup-for-new-tutorial-bodies','exec'),globals())
