"""Correct the literal source-version key; preserve the failed preflight producer."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text
if __name__=='__main__':
    p=Path('scripts/prepare_lil_B224_stored_reference_v7149.py')
    source=checked_text(p.read_text('utf8'),{"'V6686':'V7118'":"'V7029':'V7118'"})
    exec(compile(source,str(p)+'::exact-source-version-literal','exec'),dict(__name__='__main__',__file__=__file__))
