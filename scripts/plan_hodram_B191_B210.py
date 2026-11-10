"""Reuse the calibrated paragraph/page planner with complete clean-source preamble locks."""
from types import FunctionType, SimpleNamespace
from scripts import plan_editorial_scene_prose_v18 as previous
from scripts import plan_hodram_B171_B190 as source_qualification
from scripts.source_locked_derivation_v5118 import checked_text
import inspect

source = checked_text(inspect.getsource(source_qualification.qualify_source), {
    'assert len(bindings) == 433': 'assert len(bindings) == 352',
})
env = dict(source_qualification.qualify_source.__globals__)
exec(compile(source, __file__ + '::352-exact-source-preambles', 'exec'), env)
qualify_source = env['qualify_source']
inherited = previous.main.__globals__['previous']
parameters = {**vars(inherited), 'PAIRS': inherited.PAIRS | {
    ('caterpillar', 'fungus'), ('celestial', 'maiden'), ('rocco', 'alemkel'), ('mast', 'rope'),
    ('glassmaking', 'guide'), ('jam', 'jack'), ('jack', 'ludwyan'), ('good', 'side'),
    ('at', 'once'), ('no', 'lower'), ('take', 'care'), ('made', 'in'), ('in', 'japan')}}
main = FunctionType(previous.main.__code__, {**previous.main.__globals__, 'qualify_source': qualify_source,
    'previous': SimpleNamespace(**parameters), '__file__': __file__}, argdefs=previous.main.__defaults__)

if __name__ == '__main__':
    main()
