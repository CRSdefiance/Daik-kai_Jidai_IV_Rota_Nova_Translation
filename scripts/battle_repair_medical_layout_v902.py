"""Phrase-aware repair/medical dialogue in the existing36x3 native planner."""

from types import FunctionType
from scripts import battle_personal_layout_v892 as base

WIDTH=base.WIDTH
MAX_LINES=base.MAX_LINES
PHRASES=base.KEEP_TOGETHER|{('right','away'),('take','a','hit'),('a','shipwright'),('turn','to','shine'),
    ('hull','damage'),('be','right','there'),('fix','it','right','up'),('plenty','to','do'),
    ('leave','the','repairs'),('focus','on','the','fight'),('emergency','repairs'),('in','no','time'),
    ('take','care','of'),('the','wounded'),('gets','hurt'),('angel','in','white'),('spit','on','it'),
    ('expert','doctor'),('looking','after','you'),('patch','you','up'),("don't",'push','yourself'),
    ('come','see','me'),('throw','your','life','away')}
KEEP_TOGETHER={tuple(word.strip('.,!?;:').lower() for word in pair)
    for phrase in PHRASES for pair in zip(phrase,phrase[1:])}
layout=FunctionType(base.layout.__code__,{**base.layout.__globals__,'KEEP_TOGETHER':KEEP_TOGETHER})
serialize=base.serialize


def compiled(row):return serialize(layout(row['english']))
