"""Retain source/current name ABI guards with an explicitly selected protagonist."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(Path('scripts/bind_editorial_actor_names.py').read_text(encoding='utf-8'),{
    'from scripts.registered_editorial_runtime import RegisteredRuntime':'from scripts.registered_editorial_runtime_v2 import RegisteredRuntime',
    "    parser.add_argument('--actors',type=int,nargs='+',required=True)":
        "    parser.add_argument('--actors',type=int,nargs='+',required=True)\n    parser.add_argument('--captain',type=int,choices=range(4),required=True)",
    'ctx=RegisteredRuntime(args.release,args.startup)':'ctx=RegisteredRuntime(args.release,args.startup,captain=args.captain)',
})
if __name__=='__main__':exec(compile(source,__file__+'::same-clean-current-getters-andwhole-RAM-inverses-explicit-captain','exec'),globals())
