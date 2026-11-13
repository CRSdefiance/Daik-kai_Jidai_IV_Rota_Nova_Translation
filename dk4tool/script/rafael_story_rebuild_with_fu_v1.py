"""Keep the complete block inverse planner and additionally protect the FU macro."""
import inspect
from dk4tool.script.reviewed_scene_rebuild import rebuild_block as original
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(inspect.getsource(original),{
    "(b'FI', b'FA', b'FO')":"(b'FI', b'FA', b'FO', b'FU')",
})
env={**original.__globals__,'__file__':__file__}
exec(compile(source,__file__+'::same-complete-block-inverses-plus-source-FU','exec'),env)
rebuild_block=env['rebuild_block']
