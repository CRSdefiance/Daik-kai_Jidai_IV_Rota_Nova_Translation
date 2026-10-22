"""Condition1 fatigue paragraphs in the proven36-cell,three-row native consumer."""
from types import FunctionType
from scripts import battle_gunnery_deck_layout_v952 as base

WIDTH=base.WIDTH
MAX_LINES=base.MAX_LINES
PHRASES=base.KEEP_TOGETHER|{('body','feels'),('so','heavy'),("I'm",'tired'),("I'm",'exhausted'),('let','me'),('me','rest'),('worn','out'),('a','break'),('Recreation','Room'),('no','strength','left'),("what's",'wrong','with','me'),('for','a','bit'),('seems','to','be'),('catching','up','with','me'),("don't",'feel','right'),('maybe',"I'm",'tired'),('so','dizzy'),('whole','body'),('all','right'),("don't",'worry')}
KEEP_TOGETHER={tuple(word.strip('.,!?;:').lower() for word in pair) for phrase in PHRASES for pair in zip(phrase,phrase[1:])}
layout=FunctionType(base.layout.__code__,{**base.layout.__globals__,'KEEP_TOGETHER':KEEP_TOGETHER})
serialize=base.serialize


def compiled(row):return serialize(layout(row['english']))
