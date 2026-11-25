"""Keep Well with its following answer clause without modifying prose or authored breaks."""
from types import FunctionType
from scripts import illness_critical_layout_v973 as base

WIDTH=base.WIDTH
MAX_LINES=base.MAX_LINES
KEEP_TOGETHER=base.KEEP_TOGETHER|{('well','some')}
WEAK=base.WEAK
layout=FunctionType(base.layout.__code__,{**base.layout.__globals__,'KEEP_TOGETHER':KEEP_TOGETHER})
serialize=base.serialize


def compiled(row):return serialize(layout(row['english']))
