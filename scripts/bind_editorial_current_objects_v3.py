"""Keep all native style/menu guards and require the explicit protagonist context."""
from scripts import bind_editorial_current_objects_v2 as previous
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(previous.source, {
    'from scripts.registered_editorial_runtime import RegisteredRuntime':
        'from scripts.registered_editorial_runtime_v2 import RegisteredRuntime',
    "    args=parser.parse_args();assert not args.out.exists();current,styles,choices=map(load,[args.current,args.styles,args.choices])":
        "    parser.add_argument('--captain',type=int,choices=range(4),required=True)\n"
        "    args=parser.parse_args();assert not args.out.exists();current,styles,choices=map(load,[args.current,args.styles,args.choices])",
    "ctx=RegisteredRuntime(runtime['release_proof'],runtime['startup_proof'])":
        "ctx=RegisteredRuntime(runtime['release_proof'],runtime['startup_proof'],captain=args.captain)",
})
exec(compile(source, __file__ + '::same-source-alias-slot-menu-andcurrent-native-guards-explicit-captain', 'exec'), globals())
