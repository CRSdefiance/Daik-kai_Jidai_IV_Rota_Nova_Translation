"""Save complete-exchange subsets while retaining full sealed/current inventory guards."""
import inspect
from scripts import save_clean_editorial_comparisons_v1 as previous
from scripts.seal_clean_editorial_prose_stage_v2 import row_key
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(inspect.getsource(previous.main), {
    '    args=ap.parse_args();assert args.out.parent==args.root':
        "    ap.add_argument('--expected-selected-records',type=int,required=True)\n"
        '    args=ap.parse_args();assert args.out.parent==args.root',
    '    assert sum(len(v) for v in decisions.values())==args.expected_records':
        '    assert 0 < args.expected_selected_records <= args.expected_records\n'
        '    assert sum(len(v) for v in decisions.values())==args.expected_selected_records',
})
env = {**vars(previous), 'row_key': row_key, '__file__': __file__}
exec(compile(source, __file__+'::same-individual-guards-explicit-complete-exchange-subset-count', 'exec'), env)
if __name__ == '__main__':
    env['main']()
