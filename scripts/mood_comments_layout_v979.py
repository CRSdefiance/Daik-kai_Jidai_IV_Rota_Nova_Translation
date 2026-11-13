"""Mood and panic paragraphs in the proven original36-cell,three-row consumer."""
from types import FunctionType
from scripts import illness_critical_layout_v974 as base

WIDTH=base.WIDTH
MAX_LINES=base.MAX_LINES
PHRASES=base.KEEP_TOGETHER|{('high','spirits'),('right','now'),('feel','refreshed'),('ready','for'),('any','order'),('top','form'),('feel','like'),('do','anything'),('great','mood'),("work's",'going','smoothly'),('ready','to'),('get','to','work'),('strength','welling','up'),('from','deep','within'),('feel','fantastic'),('get','motivated'),('change','of','pace'),('kind','of','down'),('just','talking','to','myself'),('oh','I'),('just','talking'),('to','myself'),('maybe','a','change'),('want','to','talk'),('going','on'),('no','clue'),('all','this'),('stay','calm'),('at','a','time','like','this'),('calm','down')}
KEEP_TOGETHER={tuple(word.strip('.,!?;:').lower() for word in pair) for phrase in PHRASES for pair in zip(phrase,phrase[1:])}
WEAK=base.WEAK
layout=FunctionType(base.layout.__code__,{**base.layout.__globals__,'KEEP_TOGETHER':KEEP_TOGETHER})
serialize=base.serialize


def compiled(row):return serialize(layout(row['english']))
