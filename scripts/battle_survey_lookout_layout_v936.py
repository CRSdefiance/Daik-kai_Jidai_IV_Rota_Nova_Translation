"""Keep full survey clauses intact in the original36x3 planner."""
from types import FunctionType
from scripts import battle_survey_lookout_layout_v935 as base
WIDTH=base.WIDTH
MAX_LINES=base.MAX_LINES
KEEP_TOGETHER=base.KEEP_TOGETHER|{('taking','these'),('these','measurements'),('during','a'),('an','emergency'),('emergency','like'),('like','this')}
layout=FunctionType(base.layout.__code__,{**base.layout.__globals__,'KEEP_TOGETHER':KEEP_TOGETHER})
serialize=base.serialize
def compiled(row):return serialize(layout(row['english']))
