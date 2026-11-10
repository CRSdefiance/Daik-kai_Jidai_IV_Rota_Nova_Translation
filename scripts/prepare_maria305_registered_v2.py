"""Retain the failed preparation and qualify the exact pure-rehearsal successor."""
from scripts.prepare_maria305_registered_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(previous, {
    'dk4tool.patch.maria305_release_v1':'dk4tool.patch.maria305_release_v2',
    'dk4tool/patch/maria305_release_v1.py':'dk4tool/patch/maria305_release_v2.py',
    "OUT=ROOT/'registered_preparation_v1'":"OUT=ROOT/'registered_preparation_v2'",
})
exec(compile(source,__file__+'::same-preparation-original-producer-identity','exec'),globals())
