"""Correct a preflight replacement key; preserve the unexecuted failed plan."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text
if __name__=='__main__':
    p=Path('scripts/prepare_lil_B223_reference_v7102.py')
    source=checked_text(p.read_text('utf8'),{"'B2231304_bytes'":"'B2141304_bytes'"})
    exec(compile(source,str(p)+'::correct-source-key','exec'),dict(__name__='__main__',__file__=__file__))
