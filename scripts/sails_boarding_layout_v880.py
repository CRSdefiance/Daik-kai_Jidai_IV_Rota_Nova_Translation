"""Complete sail/boarding phrases in the established36x3 parity-safe planner."""

from types import FunctionType
from scripts import survey_lookout_layout_v875 as base

WIDTH=base.WIDTH
MAX_LINES=base.MAX_LINES
KEEP_TOGETHER=base.KEEP_TOGETHER|{('fore-and-aft','and','square','sails'),('fore-and-aft','sails'),
    ('square','sails'),('Half','Open.'),('sail','handler'),('dead','calm'),('read','the','wind'),
    ('boarding','combat.'),('from','the','front'),('a','little','better')}
layout=FunctionType(base.layout.__code__,{**base.layout.__globals__,'KEEP_TOGETHER':KEEP_TOGETHER})
serialize=base.serialize


def compiled(row):return serialize(layout(row['english']))
