"""Retain the first plan and allow an ordinary fairy/tale wrap instead of an early first row."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text,derive
if __name__=='__main__':
    jobs=[('scripts/plan_lil_B217_layout_v6836.py','scripts/plan_lil_B217_layout_v6836b.py',{'layout_v6836':'layout_v6836b',"('fairy','tale'),":''}),('scripts/verify_lil_B217_native_pages_v6837.py','scripts/verify_lil_B217_native_pages_v6837b.py',{'layout_v6836/':'layout_v6836b/'}),('scripts/probe_lil_B217_paragraph_QA_v6841.py','scripts/probe_lil_B217_paragraph_QA_v6841b.py',{'layout_v6836/':'layout_v6836b/'})]
    for a,b,c in jobs:assert not Path(b).exists();checked_text(Path(a).read_text('utf8'),c)
    for a,b,c in jobs:print(derive(a,b,c))
