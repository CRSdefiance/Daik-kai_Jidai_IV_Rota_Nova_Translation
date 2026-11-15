"""Keep complete style compiler,allslot/getter andnegative checks for an explicit SC0 batch."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(Path('scripts/check_editorial_style_objects.py').read_text(encoding='utf-8'),{
    'from scripts.registered_editorial_runtime import RegisteredRuntime':'from scripts.registered_editorial_runtime_v2 import RegisteredRuntime',
    'ctx=RegisteredRuntime(args.release,args.startup)':'ctx=RegisteredRuntime(args.release,args.startup,captain=0)',
    "'/data/SC1.DK4'":"doc['file_path']",
    "    assert len(objects)==8 and cases==64 and sum(len(o['physical_record_IDs']) for o in objects)==48":
        "    assert len(objects)==doc['style_command_objects'] and cases==8*len(objects) and sum(len(o['physical_record_IDs']) for o in objects)==doc['style_physical_speech_objects']",
    'physical_alternatives=48,':"physical_alternatives=doc['style_physical_speech_objects'],",
    'PASS8 compiled4100 objects/48 physical alternatives/64 original target slot cases/72 semantic rejection checks; virtual prefixes not stored.':
        'PASS allsource-owned4100 objects,allphysical alternatives/allslot getters andallsemantic rejection checks;virtual prefixes not stored.',
})
exec(compile(source,__file__+'::same-complete-style-compiler-andnative-getter-contract-own-Rafael', 'exec'),globals())
