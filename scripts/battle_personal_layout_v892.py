"""Battle hobby prose through the existing36-column,three-row native planner."""

from types import FunctionType
from scripts import gunnery_deck_layout_v887 as base

WIDTH=base.WIDTH
MAX_LINES=base.MAX_LINES
PHRASES=base.KEEP_TOGETHER|{('time','for','a','break'),('naval','warfare','encyclopedia'),
    ('putting','down'),('even','in','battle'),('sea','battle'),('this','page'),('fishing','rod'),
    ('comes','first'),('a','moment'),('taking','care','of'),('my','sword'),('precious','model'),
    ('something','first'),('my','best'),('my','turn'),('tough','opponents'),('nods','off'),
    ('read','the','cards'),('special','move'),('too','full'),('my','model')}
KEEP_TOGETHER={tuple(word.strip('.,!?;:').lower() for word in pair)
    for phrase in PHRASES for pair in zip(phrase,phrase[1:])}
layout=FunctionType(base.layout.__code__,{**base.layout.__globals__,'KEEP_TOGETHER':KEEP_TOGETHER})
serialize=base.serialize


def compiled(row):return serialize(layout(row['english']))
