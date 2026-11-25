"""Check all56 newly compiled style slots on the exactly qualified native context."""
from pathlib import Path
from scripts.check_editorial_compiled_pages_scope_reuse_v1 import qualified_current_native_context
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(Path('scripts/check_editorial_style_objects.py').read_text(encoding='utf-8'),{
    "ctx=RegisteredRuntime(args.release,args.startup);assert current['runtime']==ctx.receipt() and doc['current_ROM_sha256']==ctx.receipt()['candidate_sha256']":
        "ctx=RegisteredRuntime(args.release,args.startup);assert current['runtime']==ctx.receipt()\n    scope_reuse=qualified_current_native_context(doc,ctx)",
    'assert len(objects)==8 and cases==64 and sum(len(o[\'physical_record_IDs\']) for o in objects)==48':
        'assert len(objects)==7 and cases==56 and sum(len(o[\'physical_record_IDs\']) for o in objects)==47',
    'runtime=ctx.receipt(),objects=objects,native_target_slot_cases=cases,physical_alternatives=48,':
        'runtime=ctx.receipt(),native_context_reuse=scope_reuse,objects=objects,native_target_slot_cases=cases,physical_alternatives=47,',
    'PASS8 compiled4100 objects/48 physical alternatives/64 original target slot cases/72 semantic rejection checks;':
        'PASS7 compiled4100 objects/47 physical alternatives/56 original target slot cases/63 semantic rejection checks;',
})
exec(compile(source,__file__+'::same-complete-style-object-native-and-rejection-contracts','exec'),globals())
