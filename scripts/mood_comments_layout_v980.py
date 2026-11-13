"""Keep the quoted self-talk correction together without changing its English."""
from types import FunctionType
from scripts import mood_comments_layout_v979 as base

WIDTH=base.WIDTH
MAX_LINES=base.MAX_LINES
KEEP_TOGETHER=base.KEEP_TOGETHER|{('i','was'),('was','just')}
WEAK=base.WEAK
layout=FunctionType(base.layout.__code__,{**base.layout.__globals__,'KEEP_TOGETHER':KEEP_TOGETHER})
serialize=base.serialize


def compiled(row):return serialize(layout(row['english']))
