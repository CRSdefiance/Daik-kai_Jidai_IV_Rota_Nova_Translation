"""Freeze the qualified31000-frame startup for the new cumulative candidate."""
from scripts.prepare_maria349_own_startup_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text
source = checked_text(previous, {
    'scripts.build_registered_maria349_v1': 'scripts.build_registered_maria315_v1',
    'Own cumulative Maria349 B275-B285 candidate': 'Own cumulative Maria315 B286-B302 candidate',
})
exec(compile(source, __file__+'::same-own-candidate-startup-plan', 'exec'), globals())
