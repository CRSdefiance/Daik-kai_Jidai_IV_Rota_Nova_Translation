"""Select sixteen whole clean exchanges while retaining B294's earlier credited context."""
from pathlib import Path
from scripts import prepare_lil269_source_intake_v1 as previous
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(previous.source, {
    '1423': '1154', '5297': '5566', '269': '361',
    'len(selected) == 40': 'len(selected) == 16',
    'complete_exchanges=40': 'complete_exchanges=16',
    "        assert len(group['records']) == sum(r['block'] == group['block'] for r in census['records'])":
        """        whole=group.get('complete_clean_context_records',group['records'])
        context=group.get('preserved_credited_context_records',[])
        assert len(whole)==sum(r['block']==group['block'] for r in census['records'])
        assert len(whole)==len(group['records'])+len(context)
        assert {r['id'] for r in whole}=={r['id'] for r in group['records']+context}
        for row in context:
            raw=bytes.fromhex(row['source_hex']);at=row['source_reference']['offset']
            assert block[at:at+len(raw)]==raw and row['covered'] and row['exact_credited_source_bindings']
            assert all((row['file_path'],b['id']) in credits for b in row['exact_credited_source_bindings'])
        assert not context or (group['block']==294 and len(context)==1 and len(whole)==16)""",
})
env = {**previous.env, 'ROOT': Path('work/Lil361_B283_B298_clean_20261110'),
    'CENSUS': Path('work/story_source_coverage_20261110_SC2_v4/coverage.json'),
    'PACKET': Path('work/story_source_coverage_20261110_SC2_v4/residual_clean_source_packet.json'),
    'RELEASE': Path('work/lil269_B243_B282_release_v1/registered_release_verification.json'),
    'BLOCKS': list(range(283,299)), '__file__': __file__}
exec(compile(source, __file__ + '::same-clean-source-credit-andcomplete-context-guards', 'exec'), env)
if __name__ == '__main__':
    env['main']()
