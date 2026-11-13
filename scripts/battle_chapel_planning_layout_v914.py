"""Prayer and strategy phrases with the preserved36x3 native planner."""

from types import FunctionType
from scripts import battle_cooking_livestock_layout_v908 as base

WIDTH=base.WIDTH
MAX_LINES=base.MAX_LINES
PHRASES=base.KEEP_TOGETHER|{('our','fleet'),('grant','peace'),('those','who','fell'),('my','friends'),
    ('everyone','stays','safe'),('rather','fight','than','pray'),('God','is','with','us'),('so','many','more','lives'),
    ('lend','your','strength'),('my','other','friends'),('my','fleet'),('prayed','to','God'),('sure','to','win'),
    ('stay','safe'),('sea','battle'),('sea','battles'),('out','of','the','question'),('a','strategist'),
    ('nothing','to','do'),('direct','tactics'),('no','schemes'),('let','me','fight'),('sneak','a','bite'),
    ('no','part','to','play'),('only','way'),('assign','me'),('Marine','Barracks'),('much','point'),('Strategy','Room')}
KEEP_TOGETHER={tuple(word.strip('.,!?;:').lower() for word in pair)
    for phrase in PHRASES for pair in zip(phrase,phrase[1:])}
layout=FunctionType(base.layout.__code__,{**base.layout.__globals__,'KEEP_TOGETHER':KEEP_TOGETHER})
serialize=base.serialize


def compiled(row):return serialize(layout(row['english']))
