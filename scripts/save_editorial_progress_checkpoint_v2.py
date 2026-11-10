"""Keep v1's exact atomic backups and additionally register new unfinished batches."""
import inspect
from scripts import save_editorial_progress_checkpoint_v1 as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(inspect.getsource(previous.checkpoint),{
    'completed, protected):':'completed, protected, new_entries=None):',
    "    ledger['latest_checkpoint'] = summary":
        "    for key,value in (new_entries or {}).items():\n        assert key not in prior\n        ledger[key]=value\n    ledger['latest_checkpoint'] = summary",
})
env={**previous.checkpoint.__globals__,'__file__':__file__}
exec(compile(source,__file__+'::same-atomic-checkpoint-with-new-uncredited-intakes','exec'),env)
checkpoint=env['checkpoint']
