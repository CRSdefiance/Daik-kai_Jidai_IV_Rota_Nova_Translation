"""Reuse the qualified complete-source planner for all387 new bodies, including actor0."""
from types import FunctionType
from scripts import plan_hodram_B301_B310_v1 as previous
from scripts.prepare_hodram_B311_B324_formatting_v1 import PROSE, MACROS, TERMS, ROLES, NAMES, NAME_REVIEW
from scripts.review_hodram_B311_B324_contextual_v1 import CURRENT, OBJECTS
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(previous.source, {
    "doc['blocks']==list(range(301,311))": "doc['blocks']==list(range(311,325))",
    "doc['physical_speech_objects']==225": "doc['physical_speech_objects']==387",
    'assert len(bindings)==225': 'assert len(bindings)==387',
})
env = {**previous.env, **globals(), '__file__': __file__}
exec(compile(source, __file__ + '::same-complete-preambles-aliases-and-source-current-guards-new-scope', 'exec'), env)
qualify_source = env['qualify_source']
main = FunctionType(previous.main.__code__, {**previous.main.__globals__, 'qualify_source': qualify_source,
                    '__file__': __file__}, argdefs=previous.main.__defaults__)
if __name__ == '__main__':
    main()
