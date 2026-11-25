"""Preserve the rejected first plan;keep literal uppercase I away from a protected-break macro hazard."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text,derive
if __name__=='__main__':
    jobs=[('scripts/plan_lil_B218_layout_v6881.py','scripts/plan_lil_B218_layout_v6881b.py',{'layout_v6881':'layout_v6881b','tail=solve(stop,line+1)':"if not final and words[stop-1]=='I':continue\n            tail=solve(stop,line+1)"}),('scripts/verify_lil_B218_native_pages_v6882.py','scripts/verify_lil_B218_native_pages_v6882b.py',{'layout_v6881/':'layout_v6881b/'}),('scripts/probe_lil_B218_paragraph_QA_v6886.py','scripts/probe_lil_B218_paragraph_QA_v6886b.py',{'layout_v6881/':'layout_v6881b/'})]
    for a,b,c in jobs:assert not Path(b).exists();checked_text(Path(a).read_text('utf8'),c)
    for a,b,c in jobs:print(derive(a,b,c))
