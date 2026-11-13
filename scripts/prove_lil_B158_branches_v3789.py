"""Run all24 source-relative sites with both images and complete RAM/guard preservation."""
from pathlib import Path
if __name__=='__main__':
    p=Path('scripts/prove_lil_B157_branches_v3747.py');t=p.read_text(encoding='utf-8');changes={'lil_B157_branches_v3747':'lil_B158_branches_v3789','work/analysis/lil_B157_source_v3746/all75_clean_current_complete_context.json':'work/analysis/lil_B158_source_v3788/all19_clean_current_complete_context.json','B157-all8-relative-sites-main-RAM-guards':'B158-all24-relative-sites-main-RAM-guards'}
    for a,b in changes.items():assert a in t,a;t=t.replace(a,b)
    exec(compile(t,str(p)+'::B158-source24-spans','exec'),dict(__name__='__main__',__file__=__file__))
