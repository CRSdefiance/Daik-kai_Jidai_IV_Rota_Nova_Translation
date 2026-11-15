"""Require the candidate's own startup snapshot andall24 protected getters."""
from scripts.verify_maria390_startup_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text
source=checked_text(previous,{'scripts.build_registered_maria390_v1':'scripts.build_registered_maria305_v1',
    'all12 protected names from the Maria390 B152-B175 cumulative candidate own startup':
        'all12 protected names from the Maria305 B176-B195 cumulative candidate own startup'})
exec(compile(source,__file__+'::same-own-startup-andprotected-getter-guards','exec'),globals())
