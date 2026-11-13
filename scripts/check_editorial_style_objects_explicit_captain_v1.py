"""Keep complete native style-pointer andcompiler guards for an explicit route/captain scope."""
import inspect
from scripts import check_editorial_style_objects as previous
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(inspect.getsource(previous.main),{
    '    args=parser.parse_args();assert not args.out.exists()':
        "    parser.add_argument('--captain',type=int,choices=range(4),required=True)\n    args=parser.parse_args();assert not args.out.exists()",
    'ctx=RegisteredRuntime(args.release,args.startup)':
        'ctx=RegisteredRuntime(args.release,args.startup,captain=args.captain)',
    "read_file('/data/SC1.DK4')":"read_file(doc['file_path'])",
    "assert len(objects)==8 and cases==64 and sum(len(o['physical_record_IDs']) for o in objects)==48":
        "assert len(objects)==doc['style_command_objects']==len(current['style_objects'])\n    assert cases==8*len(objects)\n    assert sum(len(o['physical_record_IDs']) for o in objects)==doc['style_physical_speech_objects']==len(current['style_records'])",
    'physical_alternatives=48,':"physical_alternatives=doc['style_physical_speech_objects'],",
    "print('PASS8 compiled4100 objects/48 physical alternatives/64 original target slot cases/72 semantic rejection checks; virtual prefixes not stored.')":
        "print(dict(objects=len(objects),physical_alternatives=doc['style_physical_speech_objects'],original_target_slot_cases=cases,compiler_rejections=sum(len(n['rejected']) for n in negatives),virtual_prefixes_not_stored=True))",
})
env={**vars(previous),'RegisteredRuntime':RegisteredRuntime,'__file__':__file__}
exec(compile(source,__file__+'::same-complete-native-style-object-slot-andrejection-guards-explicit-route-captain','exec'),env)
main=env['main']

if __name__=='__main__':main()
