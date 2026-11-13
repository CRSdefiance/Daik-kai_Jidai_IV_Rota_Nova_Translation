"""Keep the about-a-little-wound phrase intact without editing prose or manual breaks."""
from types import FunctionType
from scripts import physical_wounds_layout_v967 as base

WIDTH=base.WIDTH
MAX_LINES=base.MAX_LINES
KEEP_TOGETHER=base.KEEP_TOGETHER|{('about','a'),('a','little'),('wound','like')}
layout=FunctionType(base.layout.__code__,{**base.layout.__globals__,'KEEP_TOGETHER':KEEP_TOGETHER})
serialize=base.serialize


def compiled(row):return serialize(layout(row['english']))
