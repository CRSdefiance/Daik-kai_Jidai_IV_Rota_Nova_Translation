"""Use the existing planner with the exact new source/current scope and dependencies."""
import inspect
from types import FunctionType
from scripts import plan_hodram_B211_B230_v1 as old_qualifier
from scripts import plan_hodram_B211_B230_v2 as planner
from scripts.prepare_hodram_B251_B280_formatting_v1 import PROSE,MACROS,TERMS,ROLES,NAMES,NAME_REVIEW
from scripts.review_hodram_B251_B280_contextual_v1 import CURRENT,OBJECTS
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(inspect.getsource(old_qualifier.qualify_source),{
    "doc['blocks']==list(range(211,231))":"doc['blocks']==list(range(251,281))",
    "doc['physical_speech_objects']==270":"doc['physical_speech_objects']==209",
    'assert len(bindings)==270':'assert len(bindings)==209',
})
env={**old_qualifier.qualify_source.__globals__,**globals(),'__file__':__file__}
exec(compile(source,__file__+'::same-source-current-preambles-aliases-andruntime-qualifier','exec'),env)
qualify_source=env['qualify_source']
main=FunctionType(planner.main.__code__,{**planner.main.__globals__,'qualify_source':qualify_source,'__file__':__file__},argdefs=planner.main.__defaults__)
if __name__=='__main__':main()
