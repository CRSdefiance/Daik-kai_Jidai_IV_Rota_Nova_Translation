"""Use a focused14401-frame budget for the19-object exchange; preserve the unexecuted longer runner."""
from pathlib import Path
if __name__=='__main__':
    p=Path('scripts/run_lil_B158_display_fixture_v3812.py');t=p.read_text(encoding='utf-8');changes={"'28401'":"'14401'",'range(2600,27501,240)':'range(2600,13501,240)','range(2350,28001,60)':'range(2350,14001,60)'}
    for a,b in changes.items():assert t.count(a)==1,(a,t.count(a));t=t.replace(a,b)
    exec(compile(t,str(p)+'::19-object-focused-capture-budget','exec'),dict(__name__='__main__',__file__=__file__))
