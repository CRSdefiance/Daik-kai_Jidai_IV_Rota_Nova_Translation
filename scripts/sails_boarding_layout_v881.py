"""Normalize phrase hints to the original planners lowercase adjacent-pair API."""

from types import FunctionType
from scripts import sails_boarding_layout_v880 as base

WIDTH=base.WIDTH
MAX_LINES=base.MAX_LINES
KEEP_TOGETHER={tuple(word.strip('.,!?;:').lower() for word in pair)
    for phrase in base.KEEP_TOGETHER for pair in zip(phrase,phrase[1:])}
layout=FunctionType(base.layout.__code__,{**base.layout.__globals__,'KEEP_TOGETHER':KEEP_TOGETHER})
serialize=base.serialize


def compiled(row):return serialize(layout(row['english']))
