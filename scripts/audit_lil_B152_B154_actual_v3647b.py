"""Distinguish four retained B22 initialization effects from five excluded story effects."""
from pathlib import Path
if __name__=='__main__':
    p=Path('scripts/audit_lil_B152_B154_actual_v3647.py');t=p.read_text(encoding='utf-8');a="sum(r['word']==0xA000 for r in selected)==0";b="sum(r['word']==0xA000 for r in selected)==4 and not any(r['word']==0xA000 and r.get('original_source_block') in [152,153,154] for r in selected)";assert a in t;t=t.replace(a,b).replace('lil_B152_B154_actual_v3647','lil_B152_B154_actual_v3647b');exec(compile(t,str(p)+'::B22-init-ownership','exec'),dict(__name__='__main__',__file__=__file__))
