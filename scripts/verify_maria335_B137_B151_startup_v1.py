"""Require candidate-owned startup identity and all24 protected name getters."""
from scripts.verify_maria337_startup_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text
source=checked_text(previous,{'scripts.build_registered_maria337_v1':'scripts.build_registered_maria335_B137_B151_v1','all12 protected names from the Maria337 cumulative candidate own startup':'all12 protected names from the Maria335 B137-B151 cumulative candidate own startup'})
exec(compile(source,__file__+'::same-own-startup-andprotected-getter-guards','exec'),globals())
