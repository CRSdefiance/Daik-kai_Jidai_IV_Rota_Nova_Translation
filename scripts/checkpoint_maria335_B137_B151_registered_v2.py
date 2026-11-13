"""Keep exact credit335 while updating only its now-observed metadata atomically."""
import inspect
from scripts import save_editorial_progress_checkpoint_v9 as previous
from scripts import checkpoint_maria335_B137_B151_registered_v1 as original
from scripts.source_locked_derivation_v5118 import checked_text

# V9 permits additional updates only to unfinished zero-credit batches. This
# batch has already been credited. Bind its identity, unchanged credit and the
# three completion-metadata fields rather than resetting that credit to zero.
checkpoint_source=checked_text(previous.source,{
    "assert key in prior and isinstance(prior[key],dict) and prior[key].get('new_credit',0)==0":
        "assert key=='Maria_SC3_B137_B151_clean_20261109' and key in prior and prior[key]['new_credit']==335\n"
        "        assert set(value)=={'observed_current_batch_source_bodies','representative_gameplay_pending','registered_integration_pending','new_credit'}\n"
        "        assert value['observed_current_batch_source_bodies']==44 and value['representative_gameplay_pending'] is False and value['registered_integration_pending'] is False",
    "assert value['new_credit']==0 and key not in [batch_key,'latest_checkpoint']":
        "assert value['new_credit']==prior[key]['new_credit']==335 and key not in [batch_key,'latest_checkpoint']",
})
scope={**previous.checkpoint.__globals__,'__file__':__file__}
exec(compile(checkpoint_source,__file__+'::same-atomic-backup-inverse-andzero-credit-delta-one-exact-completed-batch','exec'),scope)
main_source=inspect.getsource(original.main)
env={**original.main.__globals__,'checkpoint':scope['checkpoint'],'__file__':__file__}
exec(compile(main_source,__file__+'::unchanged-registered-proof-anddocument-checkpoint','exec'),env)
if __name__=='__main__':env['main']()
