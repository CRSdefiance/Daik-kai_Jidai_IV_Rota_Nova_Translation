"""Require the candidate-owned snapshot and all24 protected original getters."""
from scripts.verify_maria305_startup_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(previous, {
    'scripts.build_registered_maria305_v1': 'scripts.build_registered_maria363_v1',
    'all12 protected names from the Maria305 B176-B195 cumulative candidate own startup':
        'all12 protected names from the Maria363 B216-B252 cumulative candidate own startup',
})
exec(compile(source,__file__+'::same-own-startup-andprotected-getter-guards','exec'),globals())
