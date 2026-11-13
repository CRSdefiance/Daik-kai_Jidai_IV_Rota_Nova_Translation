"""Preserve complete compound-object/inverse guards and additionally protect FU."""
from dk4tool.script import reviewed_scene_rebuild_v3 as previous
from scripts.source_locked_derivation_v5118 import checked_text

SOURCE=checked_text(previous.SOURCE,{"(b'FI', b'FA', b'FO')":"(b'FI', b'FA', b'FO', b'FU')"})
env={**previous.__dict__,'__file__':__file__}
exec(compile(SOURCE,__file__+'::same-full-compound-andinverse-guards-plus-FU','exec'),env)
rebuild_block=env['rebuild_block']
