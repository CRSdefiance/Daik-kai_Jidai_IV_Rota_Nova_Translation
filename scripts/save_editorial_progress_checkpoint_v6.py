"""Advance the date on the existing atomic editorial checkpoint contract."""
from scripts import save_editorial_progress_checkpoint_v5 as previous
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(previous.source, {
    '# Current editorial checkpoint - 2026-11-05': '# Current editorial checkpoint - 2026-11-06',
})
env = {**previous.checkpoint.__globals__, '__file__': __file__}
exec(compile(source, __file__ + '::same-atomic-checkpoint-current-date', 'exec'), env)
checkpoint = env['checkpoint']
