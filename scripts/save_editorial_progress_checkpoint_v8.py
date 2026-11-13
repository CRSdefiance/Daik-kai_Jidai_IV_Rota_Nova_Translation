"""Keep the atomic zero-credit checkpoint contract and advance the handoff date."""
from scripts import save_editorial_progress_checkpoint_v7 as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous.source,{'# Current editorial checkpoint - 2026-11-07':'# Current editorial checkpoint - 2026-11-09'})
env={**previous.checkpoint.__globals__,'__file__':__file__}
exec(compile(source,__file__+'::same-atomic-checkpoint-current-calendar-date','exec'),env)
checkpoint=env['checkpoint']
