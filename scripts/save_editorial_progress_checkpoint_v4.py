"""Atomically mark a previously unstarted coverage container in progress without credit."""
from scripts import save_editorial_progress_checkpoint_v3 as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous.source,{
    'new_entries=None, additional_updates=None):':'new_entries=None, additional_updates=None, coverage_unit_updates=None):',
    "    ledger['latest_checkpoint'] = summary":
        """    if coverage_unit_updates:
        assert all(set(value)<={'status','active_batch','progress_evidence','progress_evidence_sha256'}
            and value['status']=='in-progress' for value in coverage_unit_updates.values())
        units=[];seen=set()
        for unit in prior['coverage_units']:
            key=unit['id']
            if key in coverage_unit_updates:
                assert unit['status'] in ['not-started','in-progress'] and key not in seen
                units.append({**unit,**coverage_unit_updates[key]});seen.add(key)
            else:units.append(unit)
        assert seen==set(coverage_unit_updates)
        ledger['coverage_units']=units
    ledger['latest_checkpoint'] = summary""",
    "[batch_key, 'latest_checkpoint',*(additional_updates or {})]":
        "[batch_key, 'latest_checkpoint',*(additional_updates or {}),*(['coverage_units'] if coverage_unit_updates else [])]",
})
env={**previous.checkpoint.__globals__,'__file__':__file__}
exec(compile(source,__file__+'::same-atomic-uncredited-checkpoint-coverage-start-status','exec'),env)
checkpoint=env['checkpoint']
