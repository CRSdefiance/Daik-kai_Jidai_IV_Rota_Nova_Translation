"""Phrase-aware gunnery/deck prose in the proven36x3 native word planner."""

from types import FunctionType
from scripts import sails_boarding_layout_v881 as base

WIDTH=base.WIDTH
MAX_LINES=base.MAX_LINES
PHRASES=base.KEEP_TOGETHER|{('test-firing','right','now'),('empty','stomach'),('our','ship'),('our','home'),
    ('nice','and','clean'),('as','soon','as'),('now','and','then'),('give','it','my','all'),('under','my','mentor')}
KEEP_TOGETHER={tuple(word.strip('.,!?;:').lower() for word in pair)
    for phrase in PHRASES for pair in zip(phrase,phrase[1:])}
layout=FunctionType(base.layout.__code__,{**base.layout.__globals__,'KEEP_TOGETHER':KEEP_TOGETHER})
serialize=base.serialize


def compiled(row):return serialize(layout(row['english']))
