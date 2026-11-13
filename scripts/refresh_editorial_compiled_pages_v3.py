"""Refresh changed pages with the source-bound style/dynamic-role checker."""
from scripts import refresh_editorial_compiled_pages_v2 as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous.source,{
    "sys.executable,'scripts/check_editorial_compiled_pages.py',":
        "sys.executable,'scripts/check_editorial_compiled_pages_v4.py',",
    "        '--release',runtime['release_proof'],'--startup',runtime['startup_proof'],":
        "        '--release',runtime['release_proof'],'--startup',runtime['startup_proof'],\n        '--role-bindings',doc['dynamic_roles'],",
})
exec(compile(source,__file__+'::same-exact-proof-reuse-qualified-style-dynamic-inputs','exec'),globals())
