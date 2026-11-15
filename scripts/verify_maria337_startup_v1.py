"""Require own-candidate startup identity and all24 protected name getters."""
from scripts.verify_maria330_startup_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text
source=checked_text(previous,{'scripts.build_registered_maria330_v1':'scripts.build_registered_maria337_v1','all12 protected names from the Maria330 cumulative candidate own startup':'all12 protected names from the Maria337 cumulative candidate own startup'})
exec(compile(source,__file__+'::same-own-startup-andprotected-getter-contract','exec'),globals())
