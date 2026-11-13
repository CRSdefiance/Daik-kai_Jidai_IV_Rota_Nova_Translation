"""Use the qualified complete-source planner for the 225 body scope."""
from types import FunctionType
from scripts import plan_hodram_B281_B300_v1 as previous
from scripts.prepare_hodram_B301_B310_formatting_v1 import PROSE,MACROS,TERMS,ROLES,NAMES,NAME_REVIEW
from scripts.review_hodram_B301_B310_contextual_v1 import CURRENT,OBJECTS
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous.source,{
    "doc['blocks']==list(range(281,301))":"doc['blocks']==list(range(301,311))",
    "doc['physical_speech_objects']==373":"doc['physical_speech_objects']==225",
    'assert len(bindings)==373':'assert len(bindings)==225',
})
env={**previous.env,**globals(),'__file__':__file__}
exec(compile(source,__file__+'::same-preambles-aliases-and-source-current-qualifier','exec'),env)
qualify_source=env['qualify_source']
main=FunctionType(previous.main.__code__,{**previous.main.__globals__,'qualify_source':qualify_source,'__file__':__file__},argdefs=previous.main.__defaults__)
if __name__=='__main__':main()
