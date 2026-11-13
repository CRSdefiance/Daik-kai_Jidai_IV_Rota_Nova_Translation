"""Illness and near-death paragraphs in the original36-cell,three-row consumer."""
from types import FunctionType
from scripts import physical_wounds_layout_v968b as base

WIDTH=base.WIDTH
MAX_LINES=base.MAX_LINES
PHRASES=base.KEEP_TOGETHER|{('come','down','with'),('a','cold'),('going','around'),('some','sleep'),('clear','it','up'),('feeling','well'),('lost','my','appetite'),('take','a','break'),('because','of'),('a','little','illness'),('all','right'),('done','for'),('of','all','places'),("can't",'die','yet'),('my','time'),('finally','come'),('going','to','die'),('wish',"I'd",'eaten','more'),('more','first'),('a','place','like','this'),('my','dream'),('make','it','come','true'),('strongest','fleet'),('want','to','die'),('where','it','ends'),('feel','a','little','unwell')}
KEEP_TOGETHER={tuple(word.strip('.,!?;:').lower() for word in pair) for phrase in PHRASES for pair in zip(phrase,phrase[1:])}
WEAK=base.WEAK|{'because','until','with'}
layout=FunctionType(base.layout.__code__,{**base.layout.__globals__,'KEEP_TOGETHER':KEEP_TOGETHER,'WEAK':WEAK})
serialize=base.serialize


def compiled(row):return serialize(layout(row['english']))
