"""Preserve the rejected derivation and its exact profile; remove redundant quoted phrase protection."""
from pathlib import Path
if __name__=='__main__':
    p=Path('scripts/prepare_lil_B158_layout_v3793.py');t=p.read_text(encoding='utf-8');a=",('couldn\\'t','help')";assert t.count(a)==1;t=t.replace(a,'');assert t.count('assert not p.exists()')==1;t=t.replace('assert not p.exists()','assert p.exists()');a="p.write_text(text,encoding='utf-8',newline='\\n')";assert t.count(a)==1;t=t.replace(a,"assert p.read_text(encoding='utf-8')==text");exec(compile(t,str(p)+'::preserved-profile-redundant-phrase-correction','exec'),dict(__name__='__main__',__file__=__file__))
