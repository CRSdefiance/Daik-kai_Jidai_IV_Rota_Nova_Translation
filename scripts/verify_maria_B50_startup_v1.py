"""Keep all own-candidate state, complete RAM and 12 protected-name getter checks."""
from scripts.verify_maria270_startup_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text
source=checked_text(previous,{
    'scripts.build_registered_maria270_v1':'scripts.build_registered_maria_B50_v1',
    'all12 protected names from the Maria270 cumulative candidate own startup':
        'all12 protected names from the Maria B50 cumulative candidate own startup',
})
exec(compile(source,__file__+'::same-own-candidate-startup-andoriginal-getters-B50','exec'),globals())
