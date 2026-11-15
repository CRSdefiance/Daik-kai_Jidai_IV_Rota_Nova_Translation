"""Scoped planning/finance phrases for the proven36x3 native word planner."""

from types import FunctionType

from scripts import livestock_prayer_layout_v854 as base

WIDTH=base.WIDTH
MAX_LINES=base.MAX_LINES
KEEP_TOGETHER=base.KEEP_TOGETHER|{('market','prices'),('clear','picture'),('dream','up'),('best','shot')}
WEAK=base.WEAK|{'on'}
layout=FunctionType(base.layout.__code__,{**base.layout.__globals__,
    'KEEP_TOGETHER':KEEP_TOGETHER,'WEAK':WEAK})
serialize=base.serialize


def compiled(row):return serialize(layout(row['english']))
