"""Preserve the rejected derivation; remove an absent, unused uppercase template key."""
from pathlib import Path
if __name__=='__main__':
    p=Path('scripts/prepare_lil_B157_handoff_verifier_v3783.py');t=p.read_text(encoding='utf-8');assert t.count("'V3719':'V3759',")==1;t=t.replace("'V3719':'V3759',",'');exec(compile(t,str(p)+'::absent-template-key-correction','exec'),dict(__name__='__main__',__file__=__file__))
