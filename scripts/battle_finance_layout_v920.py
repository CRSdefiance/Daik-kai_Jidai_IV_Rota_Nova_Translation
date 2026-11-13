"""Finance and battle phrases in the preserved36x3 native planner."""

from types import FunctionType
from scripts import battle_chapel_planning_layout_v914 as base

WIDTH=base.WIDTH
MAX_LINES=base.MAX_LINES
PHRASES=base.KEEP_TOGETHER|{('a','purser'),('sea','battle'),('might','as','well'),('work','on'),
    ('financial','report'),('while','I','have','the','chance'),('nothing','to','do'),('at','the','same','time'),
    ('this',"month's",'profits'),('that','racket'),('fight','too'),('do','much'),('helpless','in','battle'),
    ('no','time'),('calculate','profits'),('supposed','to','do'),("Purser's",'Office'),('the','crew'),('from','here')}
KEEP_TOGETHER={tuple(word.strip('.,!?;:').lower() for word in pair)
    for phrase in PHRASES for pair in zip(phrase,phrase[1:])}
layout=FunctionType(base.layout.__code__,{**base.layout.__globals__,'KEEP_TOGETHER':KEEP_TOGETHER})
serialize=base.serialize


def compiled(row):return serialize(layout(row['english']))
