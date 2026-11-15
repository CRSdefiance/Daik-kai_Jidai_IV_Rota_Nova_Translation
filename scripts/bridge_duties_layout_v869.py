"""Bridge duty phrases in the established bounded36x3 parity-safe formatter."""

from types import FunctionType
from scripts import planning_finance_layout_v860 as base

WIDTH=base.WIDTH
MAX_LINES=base.MAX_LINES
KEEP_TOGETHER=base.KEEP_TOGETHER|{('first','mate'),('first',"mate's"),('behind','the','scenes'),
    ('cannon','fire'),('sail','handler'),('work','together'),('Hard','starboard!')}
layout=FunctionType(base.layout.__code__,{**base.layout.__globals__,'KEEP_TOGETHER':KEEP_TOGETHER})
serialize=base.serialize


def compiled(row):return serialize(layout(row['english']))
