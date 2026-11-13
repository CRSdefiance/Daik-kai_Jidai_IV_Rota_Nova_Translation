"""Select script-ID rows only; legacy shared prose uses message_id and is outside this source binding."""
from scripts.source_locked_derivation_v5118 import derive
if __name__=='__main__':
    print(derive('scripts/refine_Rafael_B50_context_v8135b.py','scripts/refine_Rafael_B50_context_v8135c.py',{
        "for f in ledger['completed_editorial_families'] for r in f['records']}":"for f in ledger['completed_editorial_families'] for r in f['records'] if 'id' in r}",
    }))
