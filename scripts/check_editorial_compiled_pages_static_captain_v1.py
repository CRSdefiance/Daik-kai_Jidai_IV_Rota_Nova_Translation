"""Reuse all page guards for source scopes containing only intrinsic static selectors."""
from scripts import check_editorial_compiled_pages_explicit_captain_v1 as previous
from scripts.check_editorial_compiled_pages_v6 import check_FE_rows
from scripts.check_editorial_compiled_pages_v7 import validate_documented_layouts
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous.source,{
    "assert f'assert captain=={args.captain} and identity==(prefix if prefix<207 else DYNAMIC_BINDINGS[prefix])' in macro_adapter":
        "assert f'assert identity==prefix and captain=={args.captain}' in macro_adapter\n    assert all(r['source_selector']<207 for r in doc['records'] if r['kind']=='progressive')",
})
exec(compile(source,__file__+'::same-native-guards-stricter-intrinsic-only-selector-contract','exec'),globals())
