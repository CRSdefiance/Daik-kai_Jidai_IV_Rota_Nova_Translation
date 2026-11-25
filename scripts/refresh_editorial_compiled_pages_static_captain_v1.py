"""Retain exact dependency reuse and refresh static-selector layouts with all native guards."""
from scripts import refresh_editorial_compiled_pages_explicit_captain_v1 as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous.source,{
    'scripts/check_editorial_compiled_pages_explicit_captain_v1.py':
        'scripts/check_editorial_compiled_pages_static_captain_v1.py',
})
exec(compile(source,__file__+'::same-exact-byte-reuse-andall-native-guards-static-captain','exec'),globals())
