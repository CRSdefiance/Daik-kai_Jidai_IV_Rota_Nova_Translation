"""Battle Bridge phrases in the preserved36x3 native planner."""
from types import FunctionType
from scripts import battle_finance_layout_v920 as base
WIDTH=base.WIDTH
MAX_LINES=base.MAX_LINES
PHRASES=base.KEEP_TOGETHER|{('pull','myself','together'),('lay','down'),('a','barrage'),('deck','crew'),('hand-to-hand','combat'),('on','Camille'),('keep','you','informed'),('call','on'),('to','surrender'),('first','mate'),('the','Guild'),('a','truce'),('do','your','best'),('your','chance'),('your','skill'),('from','me'),('which','ship'),('show','you'),('those','shots'),('a','ram'),('my','chance'),('at','the','helm'),('put','my','skills','to','use'),('sail','handlers'),('coordinate','with','me'),('enemy','ship'),('prepare','to','board'),('huge','hole'),('their','flagship'),('finish','them','off'),('one','go')}
KEEP_TOGETHER={tuple(word.strip('.,!?;:').lower() for word in pair) for phrase in PHRASES for pair in zip(phrase,phrase[1:])}
layout=FunctionType(base.layout.__code__,{**base.layout.__globals__,'KEEP_TOGETHER':KEEP_TOGETHER})
serialize=base.serialize
def compiled(row):return serialize(layout(row['english']))
