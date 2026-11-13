"""Gunnery/deck-cleaning battle phrases in the original36x3 planner."""
from types import FunctionType
from scripts import battle_sails_boarding_layout_v945 as base
WIDTH=base.WIDTH
MAX_LINES=base.MAX_LINES
PHRASES=base.KEEP_TOGETHER|{('target','acquired'),("don't",'miss'),('better','Aim'),('fire','more','shots'),('land','a','hit'),('keep','firing'),('one','of','them'),('hit','allies'),('show','you'),('sink','their','flagship'),('gun','batteries'),('too','close'),('be','able','to','fire'),('waste','ammunition'),('careful','aim'),('next','shot'),('right','away'),('having','deckhands'),('an','edge'),('boarding','battles'),('it','comes','to'),('give','me','the','word'),('nothing','else','to','do'),('time','like','this'),('taking','it','easy'),('might','as','well'),('boarding','starts'),('built','up'),('scrubbing','the','deck'),('first','aboard'),('boarding','fight'),('this','battle'),('the','others'),('deck','cleaning'),('sea','battle'),('everyone','else'),('of','all','things'),("I've",'built'),('until','the'),('the','boarding')}
KEEP_TOGETHER={tuple(word.strip('.,!?;:').lower() for word in pair) for phrase in PHRASES for pair in zip(phrase,phrase[1:])}
layout=FunctionType(base.layout.__code__,{**base.layout.__globals__,'KEEP_TOGETHER':KEEP_TOGETHER})
serialize=base.serialize
def compiled(row):return serialize(layout(row['english']))
