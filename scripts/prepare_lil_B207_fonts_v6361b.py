"""Retain the caught unused derivation key;prepare the unchanged intended verifier."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text
if __name__=='__main__':
    source=Path('scripts/prepare_lil_B207_fonts_v6361.py')
    text=checked_text(source.read_text('utf-8'),{"'.blocks[206]':'.blocks[207]',":''})
    exec(compile(text,str(source)+'::unused-key-removed','exec'),dict(__name__='__main__',__file__=__file__))
