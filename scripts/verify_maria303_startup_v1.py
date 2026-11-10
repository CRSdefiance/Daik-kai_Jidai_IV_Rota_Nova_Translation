"""Require candidate-owned Maria/Hangzhou startup and both24 protected getters."""
from scripts.verify_maria310_startup_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text
source = checked_text(previous, {
    'scripts.build_registered_maria310_v1': 'scripts.build_registered_maria303_v1',
    'all12 protected names from the Maria310 cumulative candidate own startup':
        'all12 protected names from the Maria303 cumulative candidate own startup',
})
exec(compile(source, __file__+'::same-own-candidate-state-andprotected-getters303', 'exec'), globals())
