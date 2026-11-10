"""Use existing real-actor0 formatting support only for explicitly source-bound records."""
import inspect
from scripts import plan_scoped_clean_editorial_v1 as previous
from scripts.source_locked_derivation_v5118 import checked_text

_original=inspect.getsource(previous.main)
source=checked_text(_original,{
    "args,remaining=ap.parse_known_args();doc=load(args.root/'formatting_v1/formatting_input.json')":
        "ap.add_argument('--actor0-source-ids',nargs='+',required=True)\n    args,remaining=ap.parse_known_args();assert len(args.actor0_source_ids)==len(set(args.actor0_source_ids));doc=load(args.root/'formatting_v1/formatting_input.json')",
    "    sys.argv=[sys.argv[0],*remaining]":
        '''    actor0_ids=repr(set(args.actor0_source_ids))
    source=checked_text(source,{'    return set(),bindings':"""    zero_rows=[row for row in doc['records'] if row.get('source_selector')==0]
    assert {row['id'] for row in zero_rows}==ACTOR0_IDS
    assert len(zero_rows)==len(ACTOR0_IDS)
    for row in zero_rows:
        assert row['kind']=='progressive' and not row.get('native_object_kind')
        assert row['source_complete_preamble_hex']=='0040ffff0000'
        assert bytes.fromhex(row['source_hex'])[0]==bytes.fromhex(row['current_hex'])[0]==0
    zeros={bytes.fromhex(row['source_hex']) for row in zero_rows}
    assert len(zeros)==len(zero_rows)
    return zeros,bindings""".replace('ACTOR0_IDS',actor0_ids)})
    sys.argv=[sys.argv[0],*remaining]''',
})
env={**previous.main.__globals__,'__file__':__file__}
exec(compile(source,__file__+'::same-complete-source-current-andnative-guards-explicit-real-zero-selector','exec'),env)
if __name__=='__main__':env['main']()
