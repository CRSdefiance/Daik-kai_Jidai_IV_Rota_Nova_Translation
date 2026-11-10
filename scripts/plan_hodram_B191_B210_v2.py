"""Keep source qualification while adding the exact one-record grammatical retention."""
from types import FunctionType, SimpleNamespace
from scripts import plan_editorial_scene_prose_v19 as previous
from scripts.plan_hodram_B191_B210 import qualify_source, parameters

main = FunctionType(previous.main.__code__, {**previous.main.__globals__, 'qualify_source': qualify_source,
    'previous': SimpleNamespace(**parameters), '__file__': __file__}, argdefs=previous.main.__defaults__)

if __name__ == '__main__':
    main()
