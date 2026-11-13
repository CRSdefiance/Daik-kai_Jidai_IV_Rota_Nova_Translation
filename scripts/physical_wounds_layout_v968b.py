"""Treat about as a weak continuation ending and keep the following noun phrase whole."""
from types import FunctionType
from scripts import physical_wounds_layout_v968 as base

WIDTH=base.WIDTH
MAX_LINES=base.MAX_LINES
KEEP_TOGETHER=base.KEEP_TOGETHER-{('worry','about')}
WEAK=base.layout.__globals__['WEAK']|{'about'}
layout=FunctionType(base.layout.__code__,{**base.layout.__globals__,'KEEP_TOGETHER':KEEP_TOGETHER,'WEAK':WEAK})
serialize=base.serialize


def compiled(row):return serialize(layout(row['english']))
