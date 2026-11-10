"""Retain all exact receipt guards and allow a complete selection without rerunning native cases."""
import inspect
from scripts import prepare_editorial_native_resume_v1 as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(inspect.getsource(previous.main),{
    ";args=ap.parse_args();assert not args.out.exists()":";ap.add_argument('--allow-complete',action='store_true');args=ap.parse_args();assert not args.out.exists()",
    "doc,plan=map(load,[args.manuscript,args.plan]);assert plan['manuscript_sha256']==digest(args.manuscript) and not plan['failures']":
        "doc,plan=map(load,[args.manuscript,args.plan]);assert plan['manuscript_sha256']==digest(args.manuscript) and not plan['failures']\n    assert digest(doc['current_ROM'])==doc['runtime']['candidate_sha256']",
    "assert len(chosen)+len(pending)==len(plan['records']) and pending":"assert len(chosen)+len(pending)==len(plan['records']) and (pending or args.allow_complete)",
    "    sys.argv=['prepare_editorial_native_subset_v2'":"    if pending:\n        sys.argv=['prepare_editorial_native_subset_v2'",
    "    runpy.run_module('scripts.prepare_editorial_native_subset_v2',run_name='__main__')":
        "        runpy.run_module('scripts.prepare_editorial_native_subset_v2',run_name='__main__')\n    else:\n        args.out.mkdir(parents=True)",
    'all_fifth_gates_andremaining_native_visual_checks_pending=True':'all_fifth_gates_andremaining_visual_checks_pending=True,native_selection_complete=not pending',
})
scope={**previous.main.__globals__,'__file__':__file__};exec(compile(source,__file__+'::same-native-receipt-dependency-guards-optional-complete-selection','exec'),scope)
main=scope['main']
if __name__=='__main__':main()
