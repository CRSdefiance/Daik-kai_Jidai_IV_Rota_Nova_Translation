"""Preserve the I-hazard correction and allow one ordinary complete-clause boundary."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text,derive
if __name__=='__main__':
    jobs=[('scripts/plan_lil_B218_layout_v6881b.py','scripts/plan_lil_B218_layout_v6881c.py',{'layout_v6881b':'layout_v6881c','candidate=((cost[0]+tiny':"if row['id']=='DK4_MES_B218_R0023' and pair==('it','whatever'):weak=0\n            candidate=((cost[0]+tiny"}),('scripts/verify_lil_B218_native_pages_v6882b.py','scripts/verify_lil_B218_native_pages_v6882c.py',{'layout_v6881b/':'layout_v6881c/'}),('scripts/probe_lil_B218_paragraph_QA_v6886b.py','scripts/probe_lil_B218_paragraph_QA_v6886c.py',{'layout_v6881b/':'layout_v6881c/'})]
    for a,b,c in jobs:assert not Path(b).exists();checked_text(Path(a).read_text('utf8'),c)
    for a,b,c in jobs:print(derive(a,b,c))
