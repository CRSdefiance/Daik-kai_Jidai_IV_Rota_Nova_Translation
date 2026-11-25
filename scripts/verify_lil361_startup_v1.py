"""Require own cumulative startup and both getters for twelve protected names."""
from scripts.verify_lil269_startup_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text
source = checked_text(previous, {
    'scripts.build_registered_lil269_v1': 'scripts.build_registered_lil361_v1',
    'all12 protected names from the Lil269 cumulative candidate own startup':
        'all12 protected names from the Lil361 cumulative candidate own startup',
})
exec(compile(source, __file__ + '::same-own-startup-and24-protected-getter-guards', 'exec'), globals())
