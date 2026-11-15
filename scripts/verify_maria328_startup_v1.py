"""Require the own-candidate Maria startup and both24 protected name getters."""
from scripts.verify_maria303_startup_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous,{'scripts.build_registered_maria303_v1':'scripts.build_registered_maria328_v2',
    'all12 protected names from the Maria303 cumulative candidate own startup':
        'all12 protected names from the Maria328 cumulative candidate own startup'})
exec(compile(source,__file__+'::same-complete-own-RAM-startup-andprotected-getter-guards','exec'),globals())
