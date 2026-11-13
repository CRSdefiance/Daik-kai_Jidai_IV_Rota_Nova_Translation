"""Require own-candidate Maria/Hangzhou startup,RAM identity andboth getters forall12 protected names."""
from scripts.verify_maria_B50_startup_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text
source=checked_text(previous,{
    'scripts.build_registered_maria_B50_v1':'scripts.build_registered_maria310_v1',
    'all12 protected names from the Maria B50 cumulative candidate own startup':
        'all12 protected names from the Maria310 cumulative candidate own startup',
})
exec(compile(source,__file__+'::same-own-candidate-state-and24-protected-getters310','exec'),globals())
