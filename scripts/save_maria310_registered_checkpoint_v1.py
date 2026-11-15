"""Allow only verified noncredit metadata updates to the already-credited Maria310 batch."""
from pathlib import Path
from scripts import save_editorial_progress_checkpoint_v9 as previous
from scripts.source_locked_derivation_v5118 import checked_text

def qualify_completed_metadata(prior,key,value):
    root=Path('work/maria310_release_v1')
    done=previous.checkpoint.__globals__['load'](root/'completion_checkpoint.json')
    assert key=='Maria_SC3_B51_B57_clean_20261109' and done['new_credit']==prior[key]['new_credit']==310
    assert prior['records_editorially_completed']==done['counts']['completed']==20058
    assert prior[key]['completed_in_combined_family']==done['family']
    assert set(value)=={'all_fifth_formatting_gates_pending','stored_andrepresentative_checks_pending',
        'representative_gameplay_andregistered_integration_pending','registered_integration_pending',
        'current_batch_actual_gameplay_observations','current_batch_actual_gameplay_pages',
        'final_cumulative_integration_complete','registered_checkpoint_evidence'}
    assert all(value[k] is False for k in ['all_fifth_formatting_gates_pending','stored_andrepresentative_checks_pending',
        'representative_gameplay_andregistered_integration_pending','registered_integration_pending'])
    assert value['current_batch_actual_gameplay_observations']==64 and value['current_batch_actual_gameplay_pages']==70
    assert value['final_cumulative_integration_complete'] is True and 'new_credit' not in value
    assert {k:v for k,v in {**prior[key],**value}.items() if k not in value}=={k:v for k,v in prior[key].items() if k not in value}

source=checked_text(previous.source,{
    "        assert key in prior and isinstance(prior[key],dict) and prior[key].get('new_credit',0)==0\n        assert value['new_credit']==0 and key not in [batch_key,'latest_checkpoint']":
        """        assert key in prior and isinstance(prior[key],dict)
        if key=='Maria_SC3_B51_B57_clean_20261109':
            qualify_completed_metadata(prior,key,value)
        else:
            assert prior[key].get('new_credit',0)==0 and value['new_credit']==0
        assert key not in [batch_key,'latest_checkpoint']""",
})
env={**previous.checkpoint.__globals__,'qualify_completed_metadata':qualify_completed_metadata,'__file__':__file__}
exec(compile(source,__file__+'::same-progress-inverses-with-exclusive-verified-completed310-metadata-no-credit-change','exec'),env)
checkpoint=env['checkpoint']
