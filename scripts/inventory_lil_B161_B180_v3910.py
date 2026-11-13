"""Inventory20 next clean blocks against all5411 file-qualified completed keys; no credit."""
from pathlib import Path
if __name__=='__main__':
    DRAFT=Path('scripts/inventory_lil_B149_B160_v3613.py');t=DRAFT.read_text(encoding='utf-8');changes={'lil_B149_B160_clean_scope_v3613':'lil_B161_B180_clean_scope_v3910','editorial_handoff_verification_v3612':'editorial_handoff_verification_v3909','len(known)==5069':'len(known)==5411','range(149,161)':'range(161,181)','complete_clean_B149_B160_next_exchange_inventory':'complete_clean_B161_B180_next_exchange_inventory','next12 clean blocks':'next20 clean blocks'}
    for a,b in changes.items():assert a in t,a;t=t.replace(a,b)
    t=t.replace('producer_sha256=sha(Path(__file__).read_bytes())','producer_sha256=sha(Path(__file__).read_bytes()),draft_producer=str(DRAFT),draft_producer_sha256=sha(DRAFT.read_bytes())');exec(compile(t,__file__,'exec'),dict(__name__='__main__',__file__=__file__,DRAFT=DRAFT))
