"""Apply related unfinished-batch updates in one exact atomic checkpoint."""
from scripts.save_editorial_progress_checkpoint_v2 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text
from scripts import save_editorial_progress_checkpoint_v1 as base

source=checked_text(previous,{
    'new_entries=None):':'new_entries=None, additional_updates=None):',
    "    for key,value in (new_entries or {}).items():":
        "    for key,value in (additional_updates or {}).items():\n        assert key in prior and isinstance(prior[key],dict) and prior[key].get('new_credit',0)==0\n        assert value['new_credit']==0 and key not in [batch_key,'latest_checkpoint']\n        ledger[key]={**prior[key],**value}\n    for key,value in (new_entries or {}).items():",
    "if k not in [batch_key, 'latest_checkpoint']":
        "if k not in [batch_key, 'latest_checkpoint',*(additional_updates or {})]",
})
env={**base.checkpoint.__globals__,'__file__':__file__}
exec(compile(source,__file__+'::same-atomic-checkpoint-related-uncredited-intakes','exec'),env)
checkpoint=env['checkpoint']
