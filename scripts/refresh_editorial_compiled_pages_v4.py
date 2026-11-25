"""Refresh changed layouts, preserving the exact native proofs of all unchanged objects."""
from scripts import refresh_editorial_compiled_pages_v3 as previous
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(previous.source, {
    'scripts/check_editorial_compiled_pages_v4.py': 'scripts/check_editorial_compiled_pages_v6.py',
    "'--role-bindings',doc['dynamic_roles'],":
    "'--role-bindings','work/analysis/Hodram_B131_B150_clean_20261102/current_role7_bound_to_eight_source_bodies.json',",
    "sum(r['source_macros'][key] for r in subset['records'])":
    "sum(r.get('source_macros',{}).get(key,0) for r in subset['records'])",
})
exec(compile(source, __file__ + '::exact-unchanged-proof-reuse-new-FE-row-check', 'exec'), globals())
