"""Advance the atomic editorial checkpoint date without changing its guards."""
from scripts import save_editorial_progress_checkpoint_v6 as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous.source,{
    '# Current editorial checkpoint - 2026-11-06':'# Current editorial checkpoint - 2026-11-07',
})
env={**previous.checkpoint.__globals__,'__file__':__file__}
exec(compile(source,__file__+'::same-atomic-checkpoint-current-date','exec'),env)
checkpoint=env['checkpoint']
