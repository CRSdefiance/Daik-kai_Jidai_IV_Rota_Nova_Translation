"""Survey/Lookout battle phrases in the preserved36x3 native planner."""
from types import FunctionType
from scripts import battle_bridge_layout_v926 as base
WIDTH=base.WIDTH
MAX_LINES=base.MAX_LINES
PHRASES=base.KEEP_TOGETHER|{('on','deck'),('a','battle'),('takes','nerve'),('stay','calm'),('work','out'),('our','position'),('at','a','time','like','this'),('all','these','shots'),('take','a','reading'),('taking','measurements'),('my','job'),('are','you','serious'),('never','stops'),('hard','work'),('take','my','measurements'),('in','the','middle'),('so','calmly'),('enemy','ship'),('checking','its','type'),('try','to','snipe'),('their','admiral'),('boarding','action'),('successful','shot'),('whole','battle'),('coming','this','way'),('cannon','fire'),('counting','on','you'),('impressive','sight'),('keep','coming'),('an','eye','out'),('any','reinforcements'),('is','everyone','ready'),('my','orders'),('admire','the','view'),('a','gun'),('take','aim')}
KEEP_TOGETHER={tuple(word.strip('.,!?;:').lower() for word in pair) for phrase in PHRASES for pair in zip(phrase,phrase[1:])}
layout=FunctionType(base.layout.__code__,{**base.layout.__globals__,'KEEP_TOGETHER':KEEP_TOGETHER})
serialize=base.serialize
def compiled(row):return serialize(layout(row['english']))
