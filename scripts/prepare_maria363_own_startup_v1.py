"""Freeze the unchanged31000-frame own-candidate Maria startup plan."""
from scripts.prepare_maria305_own_startup_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(previous, {
    'scripts.build_registered_maria305_v1': 'scripts.build_registered_maria363_v1',
    'Own cumulative Maria305 B176-B195 candidate': 'Own cumulative Maria363 B216-B252 candidate',
})
exec(compile(source,__file__+'::same-own-candidate-startup-plan','exec'),globals())
