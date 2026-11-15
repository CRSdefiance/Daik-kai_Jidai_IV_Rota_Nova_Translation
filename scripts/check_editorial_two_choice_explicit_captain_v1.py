"""Run unchanged two-choice provider/glyph/return/rejection checks on an explicit captain."""
import inspect
from scripts import check_editorial_two_choice_display as previous
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(inspect.getsource(previous.main),{
    '    args=parser.parse_args();assert not args.out.exists()':
        "    parser.add_argument('--captain',type=int,choices=range(4),required=True)\n    args=parser.parse_args();assert not args.out.exists()",
    'ctx=RegisteredRuntime(args.release,args.startup)':
        'ctx=RegisteredRuntime(args.release,args.startup,captain=args.captain)',
})
env={**vars(previous),'RegisteredRuntime':RegisteredRuntime,'__file__':__file__}
exec(compile(source,__file__+'::same-native-two-choice-guards-explicit-captain','exec'),env)
main=env['main']

if __name__=='__main__':main()
