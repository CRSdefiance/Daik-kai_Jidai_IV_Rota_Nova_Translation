"""Reuse the qualified source/current planner for all 373 current-batch bodies."""
from types import FunctionType
from scripts import plan_hodram_B251_B280_v1 as previous
from scripts.prepare_hodram_B281_B300_formatting_v1 import PROSE,MACROS,TERMS,ROLES,NAMES,NAME_REVIEW
from scripts.review_hodram_B281_B300_contextual_v1 import CURRENT,OBJECTS
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous.source,{
    "doc['blocks']==list(range(251,281))":"doc['blocks']==list(range(281,301))",
    "doc['physical_speech_objects']==209":"doc['physical_speech_objects']==373",
    'assert len(bindings)==209':'assert len(bindings)==373',
})
env={**previous.env,**globals(),'__file__':__file__}
exec(compile(source,__file__+'::same-source-and-complete-preamble-qualifier-new-scope','exec'),env)
qualify_source=env['qualify_source']
main=FunctionType(previous.main.__code__,{**previous.main.__globals__,'qualify_source':qualify_source,'__file__':__file__},argdefs=previous.main.__defaults__)
if __name__=='__main__':main()
