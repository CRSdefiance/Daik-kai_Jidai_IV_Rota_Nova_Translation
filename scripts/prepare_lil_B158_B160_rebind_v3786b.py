"""Preserve the rejected derivation and correct its quoted selector assertion key."""
from pathlib import Path
if __name__=='__main__':
    p=Path('scripts/prepare_lil_B158_B160_rebind_v3786.py');t=p.read_text(encoding='utf-8');a="'source_selector']==254 for r in rows)==6':'source_selector']==254 for r in rows)==4'";b='"source_selector\']==254 for r in rows)==6":"source_selector\']==254 for r in rows)==4"';assert t.count(a)==1;t=t.replace(a,b);exec(compile(t,str(p)+'::quoted-selector-assertion-correction','exec'),dict(__name__='__main__',__file__=__file__))
