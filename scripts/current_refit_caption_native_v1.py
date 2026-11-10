"""Use unchanged native raster instructions with the accepted108-row Refitting surface."""
import inspect
from scripts.execute_scene_caption_raster import execute as original
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(inspect.getsource(original),{
    '(168, 84)':'(168, 108)',
    '168-by-84':'168-by-108',
    "if deck and any(not row.startswith('  ') for row in text.split('\\n')[1:]):":
        "if deck and any(len(row)%2 for row in text.split('\\n')[:-1]):",
    'Deck continuations require generated two-space guards':'Current Refit lines require the validated even-byte pending-flush boundaries',
})
env={**original.__globals__,'__file__':__file__}
exec(compile(source,__file__+'::same-native-addresses-current-accepted-refit-geometry-and-pair-safe-host-guard','exec'),env)
execute=env['execute']
