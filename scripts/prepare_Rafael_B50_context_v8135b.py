"""Preserve failed context producer; older ledger rows may inherit file identity from their family."""
from scripts.source_locked_derivation_v5118 import derive
if __name__=='__main__':
    print(derive('scripts/refine_Rafael_B50_context_v8135.py','scripts/refine_Rafael_B50_context_v8135b.py',{
        "completed={(r['file_path'],r['id']):r":"completed={(r.get('file_path',f.get('file_path')),r['id']):r",
        "if f['file_path']=='/data/SC0.DK4'":"if f.get('file_path')=='/data/SC0.DK4'",
    }))
