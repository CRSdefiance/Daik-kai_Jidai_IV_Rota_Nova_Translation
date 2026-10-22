"""Keep possessive/noun and fixed verb/adjective pairs together in survey prose."""

from types import FunctionType
from scripts import survey_lookout_layout_v874 as base

WIDTH=base.WIDTH
MAX_LINES=base.MAX_LINES
KEEP_TOGETHER=base.KEEP_TOGETHER|{('our','position'),('supposed','to'),('basic','skill')}
layout=FunctionType(base.layout.__code__,{**base.layout.__globals__,'KEEP_TOGETHER':KEEP_TOGETHER})
serialize=base.serialize


def compiled(row):return serialize(layout(row['english']))
