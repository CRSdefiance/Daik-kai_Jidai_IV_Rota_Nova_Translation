"""Preserve the complete current-text binder with an explicitly required protagonist context."""
from scripts import extract_editorial_current_v6 as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous.source,{
    'from scripts.registered_editorial_runtime import RegisteredRuntime':
        'from scripts.registered_editorial_runtime_v2 import RegisteredRuntime',
    "    ap.add_argument('--startup', type=Path, required=True)":
        "    ap.add_argument('--startup', type=Path, required=True)\n    ap.add_argument('--captain',type=int,choices=range(4),required=True)",
    'ctx = RegisteredRuntime(args.release,args.startup)':
        'ctx = RegisteredRuntime(args.release,args.startup,captain=args.captain)',
})
exec(compile(source,__file__+'::same-source-preamble-command-catalogue-andown-RAM-guards-explicit-captain','exec'),globals())
