"""Survey/lookout phrase groups in the proven36x3 native parity formatter."""

from types import FunctionType
from scripts import bridge_duties_layout_v869 as base

WIDTH=base.WIDTH
MAX_LINES=base.MAX_LINES
KEEP_TOGETHER=base.KEEP_TOGETHER|{('current','position'),("sun's",'position'),('work','out'),
    ('right','away'),('rest','easy'),('all','your','senses'),('Hang','on','a','second!')}
layout=FunctionType(base.layout.__code__,{**base.layout.__globals__,'KEEP_TOGETHER':KEEP_TOGETHER})
serialize=base.serialize


def compiled(row):return serialize(layout(row['english']))
