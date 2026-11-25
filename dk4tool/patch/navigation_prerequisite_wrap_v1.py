"""Apply compiled portrait breaks to two original Auto Move warning tables."""

from types import FunctionType

from dk4tool.patch.mutiny_static_wrap_v1 import assembly as static_assembly
from dk4tool.patch.sea_event_static_wrap_v1 import HOOK, LITERAL_COPY
from dk4tool.patch.ship_emergency_wrap_v1 import transform as extend_selector


SOURCE = 'c6cc19277ccd3e692b155dfc22a2279ce852382b464c76d27fa5e4a14a7599cb'
PRIOR = 0x01FFD600
SCOPE = {(0x02053DB8, 0x27C): (0x02118500, 0x02117820)}


def assembly():
    compile_selector = FunctionType(static_assembly.__code__,
        {**static_assembly.__globals__, 'SCOPE': SCOPE, 'PRIOR': PRIOR})
    return compile_selector()


def transform(source):
    extend = FunctionType(extend_selector.__code__, {**extend_selector.__globals__,
        'SOURCE': SOURCE, 'PRIOR': PRIOR, 'assembly': assembly})
    target, proof = extend(source)
    del proof['dynamic_wrapper']
    proof['scope'] = [dict(parent=parent, stack_selector_offset=offset, keys=keys)
                      for (parent, offset), keys in SCOPE.items()]
    return target, proof
