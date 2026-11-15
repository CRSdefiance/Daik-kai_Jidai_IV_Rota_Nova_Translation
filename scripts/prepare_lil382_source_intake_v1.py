"""Preserve nine credited context rows while selecting382 exact uncredited SC2 records."""
import inspect
from pathlib import Path
from scripts import prepare_lil391_source_intake_v1 as previous
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(inspect.getsource(previous.main), {
    '    keys = []': '    keys = [];context_keys=[]',
    "        for row in group['records']:\n            assert not row['covered'] and not row['exact_credited_source_bindings']":
        """        group['complete_clean_context_records']=deepcopy(group['records'])
        pending=[]
        for row in group['records']:
            if row['covered']:
                assert len(row['exact_credited_source_bindings'])==1
                binding=row['exact_credited_source_bindings'][0]
                assert (row['file_path'],binding['id']) in credits
                context_keys.append((row['file_path'],row['id']))
                continue
            assert not row['covered'] and not row['exact_credited_source_bindings']
            pending.append(row)""",
    "            keys.append((row['file_path'], row['id']))":
        "            keys.append((row['file_path'], row['id']))\n        group['records']=pending;group['missing_source_objects']=len(pending)",
    'assert len(keys) == len(set(keys)) == 391 and not set(keys) & credits':
        "assert len(keys) == len(set(keys)) == 382 and not set(keys) & credits\n    assert len(context_keys)==9 and len(keys)+len(context_keys)==391",
    'groups=selected, records=391, selected_blocks=BLOCKS, complete_exchanges=30,':
        'groups=selected, records=382, selected_blocks=BLOCKS, complete_exchanges=30,full_clean_context_objects=391,credited_context_objects=9,',
    'source_objects=391, complete_exchanges=30, consumer_counts=dict(counts),':
        'source_objects=382, complete_exchanges=30, consumer_counts=dict(counts),full_clean_context_objects=391,credited_context_objects=9,',
    'source_objects=391, complete_exchanges=30, consumers=dict(counts),':
        'source_objects=382, complete_exchanges=30, consumers=dict(counts),credited_context_only=9,',
})
env = {**previous.main.__globals__, 'ROOT': Path('work/Lil382_residual_A_clean_20261110'), '__file__': __file__}
exec(compile(source, __file__+'::same-exact-source-andcredit-guards-explicit-credited-context-only', 'exec'), env)
if __name__ == '__main__':
    env['main']()
