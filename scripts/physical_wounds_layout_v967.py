"""Wound paragraphs in the proven original36-cell,three-row native consumer."""
from types import FunctionType
from scripts import physical_fatigue_layout_v960 as base

WIDTH=base.WIDTH
MAX_LINES=base.MAX_LINES
PHRASES=base.KEEP_TOGETHER|{('small','wound'),('still','all','right'),('serious','wound'),('can','still'),('like','this'),('spit','on','it'),("it'll",'heal'),('bad','way'),("wound's",'sapping'),('my','strength'),('got','hurt'),('holding','me','back'),('bleeding',"won't",'stop'),('but','I'),('scratch',"won't",'stop','me'),('it','hurts'),("I'm",'the','admiral'),('take','it'),('worry','about'),('little','wound')}
KEEP_TOGETHER={tuple(word.strip('.,!?;:').lower() for word in pair) for phrase in PHRASES for pair in zip(phrase,phrase[1:])}
layout=FunctionType(base.layout.__code__,{**base.layout.__globals__,'KEEP_TOGETHER':KEEP_TOGETHER})
serialize=base.serialize


def compiled(row):return serialize(layout(row['english']))
