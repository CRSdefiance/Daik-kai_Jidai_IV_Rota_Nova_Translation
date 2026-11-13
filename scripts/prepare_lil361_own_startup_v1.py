"""Freeze the qualified startup schedule for this exact cumulative successor."""
from scripts.prepare_lil269_own_startup_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text
source = checked_text(previous, {
    'scripts.build_registered_lil269_v1': 'scripts.build_registered_lil361_v1',
    'Own cumulative Lil269 B243-B282 candidate': 'Own cumulative Lil361 B283-B298 candidate',
})
exec(compile(source, __file__ + '::same-own-candidate-startup-plan', 'exec'), globals())
