"""Freeze the qualified31000-frame startup for the new cumulative candidate."""
from scripts.prepare_maria363_own_startup_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text
source=checked_text(previous,{'scripts.build_registered_maria363_v1':'scripts.build_registered_maria359_v1',
    'Own cumulative Maria363 B216-B252 candidate':'Own cumulative Maria359 B253-B274 candidate'})
exec(compile(source,__file__+'::same-own-candidate-startup-plan','exec'),globals())
