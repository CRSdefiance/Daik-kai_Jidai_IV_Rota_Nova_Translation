"""Bind the branch proof to the successor approved-name source packet."""
from pathlib import Path
if __name__=='__main__':
    p=Path('scripts/prove_lil_B158_branches_v3789.py');t=p.read_text(encoding='utf-8');assert t.count('lil_B158_source_v3788/')==1;t=t.replace('lil_B158_source_v3788/','lil_B158_source_v3788b/');exec(compile(t,str(p)+'::approved-name-source-packet','exec'),dict(__name__='__main__',__file__=__file__))
