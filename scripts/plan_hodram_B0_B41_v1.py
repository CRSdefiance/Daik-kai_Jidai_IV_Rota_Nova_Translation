"""Plan388 exact-bound bodies; narrowly restore one source-script opaque cry."""
import inspect
import linecache
from pathlib import Path

from scripts import plan_hodram_B211_B230_v1 as source_qualifier
from scripts import plan_hodram_B211_B230_v2 as planner
from scripts.prepare_hodram_B0_B41_formatting_v1 import PROSE,MACROS,TERMS,ROLES,NAMES,NAME_REVIEW
from scripts.review_hodram_B0_B41_contextual_v1 import CURRENT,OBJECTS
from scripts.source_locked_derivation_v5118 import checked_text

qualifier_source=checked_text(inspect.getsource(source_qualifier.qualify_source),{
    "doc['blocks']==list(range(211,231))":
        "doc['blocks']==list(range(13))+list(range(15,31))+list(range(32,42))",
    "doc['physical_speech_objects']==270":"doc['physical_speech_objects']==388",
    "digest(doc['current_ROM'])==doc['current_ROM_sha256']==current['runtime']['candidate_sha256']":
        "digest(doc['current_ROM'])==doc['current_ROM_sha256']==current['current_ROM_sha256']==current['exact_native_context_reuse']['target_candidate_sha256']",
    'assert len(bindings)==270':'assert len(bindings)==388',
})
env={**source_qualifier.qualify_source.__globals__,**globals(),'__file__':__file__}
exec(compile(qualifier_source,__file__+'::same-source-current-preambles-and-alias-qualifier-current-target','exec'),env)
qualify_source=env['qualify_source']

RESTORED_SOURCE_LITERALS={'DK4_MES_B40_R0092':dict(source_selector=78,
    complete_preamble='0040ffff004e',reason='The old N-nooo invents a lexical refusal; restore only the exact deliberately opaque source-script cry.')}


def restored_source_literal(row):
    spec=RESTORED_SOURCE_LITERALS.get(row['id'])
    return bool(spec and row['source_selector']==spec['source_selector']
        and row['source_complete_preamble_hex']==spec['complete_preamble']
        and row['english'].encode('cp932')==bytes.fromhex(row['source_hex'])[1:]
        and row['english']==row['source_Japanese']
        and row['review']==dict(source=True,context=True,localization=True,naturalness=True,formatting=False))


source=checked_text(inspect.getsource(planner.main),{
    "assert all(row['english']==row['prior'] for row in native_literals.values())":
        "assert all(row['english']==row['prior'] or restored_source_literal(by_id[ident]) for ident,row in native_literals.items())",
    'exact_literal_bindings=native_literals,':'exact_literal_bindings=native_literals,exact_clean_source_restored_literals=RESTORED_SOURCE_LITERALS,',
})
env={**planner.main.__globals__,**globals(),'__file__':__file__}
filename=__file__+'::unchanged-width-controls-phase-and-pagination-with-one-exact-source-literal-restoration'
linecache.cache[filename]=(len(source),None,source.splitlines(keepends=True),filename)
exec(compile(source,filename,'exec'),env)
main=env['main']

if __name__=='__main__':main()
