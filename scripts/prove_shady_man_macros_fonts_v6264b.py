"""Bind the corrected exact-directory name proof without weakening macro or font checks."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text
source=Path('scripts/prove_shady_man_macros_fonts_v6264.py')
if __name__=='__main__':
    text=checked_text(source.read_text('utf-8'),{'shady_man_names_v6263/':'shady_man_names_v6263b/'})
    exec(compile(text,str(source)+'::current-directory-proof','exec'),dict(__name__='__main__',__file__=__file__))
