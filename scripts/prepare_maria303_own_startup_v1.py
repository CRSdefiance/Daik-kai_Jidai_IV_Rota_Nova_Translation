"""Prepare the exact cumulative candidate's qualified ordinary startup plan."""
from scripts.prepare_maria310_own_startup_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text
source = checked_text(previous, {
    'scripts.build_registered_maria310_v1': 'scripts.build_registered_maria303_v1',
    'Own cumulative Maria310 candidate': 'Own cumulative Maria303 candidate',
})
exec(compile(source, __file__+'::same-candidate-owned-startup-plan303', 'exec'), globals())
