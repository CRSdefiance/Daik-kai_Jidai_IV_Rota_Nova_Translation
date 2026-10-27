"""Re-execute eight original relative sites for the next59-object complete-exchange batch."""
from pathlib import Path
if __name__=='__main__':
    a=Path('scripts/prove_lil_B142_B145_branches_v3578.py');t=a.read_text(encoding='utf-8');changes=[('lil_B142_B145_branches_v3578','lil_B152_B154_branches_v3622'),('work/analysis/lil_B142_B145_source_v3571/all38_clean_current_complete_context.json','work/analysis/lil_B152_B154_source_v3619/all59_clean_current_complete_context.json')]
    for x,y in changes:assert x in t,x;t=t.replace(x,y)
    exec(compile(t,str(Path(__file__))+'::eight_source_relative_sites','exec'),dict(__name__='__main__',__file__=__file__))
