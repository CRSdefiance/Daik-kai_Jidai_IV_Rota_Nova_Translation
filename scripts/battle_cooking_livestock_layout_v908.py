"""Cooking/pig-care phrases using the preserved36x3 native planner."""

from types import FunctionType
from scripts import battle_repair_medical_layout_v902 as base

WIDTH=base.WIDTH
MAX_LINES=base.MAX_LINES
PHRASES=base.KEEP_TOGETHER|{('before','battle'),('even','in','battle'),('cook','plenty'),
    ('something','special'),('victory','feast'),('get','us','ready'),('at','a','time','like','this'),
    ('in','the','middle'),('good','food'),('boost','morale'),('eat','this'),('cannon','fire'),
    ('loving','care'),('worked','up'),('hold','still'),('making','that','racket'),
    ('telling','you'),('not','a','pig'),('pig','still','needs','care'),('feel','tense'),
    ('pig','around'),('in','a','panic'),("I've",'had','enough'),("don't",'be','scared'),
    ("it's",'all','right'),('be','over','soon')}
KEEP_TOGETHER={tuple(word.strip('.,!?;:').lower() for word in pair)
    for phrase in PHRASES for pair in zip(phrase,phrase[1:])}
layout=FunctionType(base.layout.__code__,{**base.layout.__globals__,'KEEP_TOGETHER':KEEP_TOGETHER})
serialize=base.serialize


def compiled(row):return serialize(layout(row['english']))
