"""Require candidate-owned startup and both original getters for twelve protected names."""
from scripts.verify_maria359_startup_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text
source=checked_text(previous,{'scripts.build_registered_maria359_v1':'scripts.build_registered_maria349_v1',
    'all12 protected names from the Maria359 B253-B274 cumulative candidate own startup':'all12 protected names from the Maria349 B275-B285 cumulative candidate own startup'})
exec(compile(source,__file__+'::same-own-startup-and24-protected-getter-guards','exec'),globals())
