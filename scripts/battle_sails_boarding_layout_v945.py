"""Sail-handling and boarding phrases in the preserved36x3 native planner."""
from types import FunctionType
from scripts import battle_survey_lookout_layout_v936 as base
WIDTH=base.WIDTH
MAX_LINES=base.MAX_LINES
PHRASES=base.KEEP_TOGETHER|{('the','wind'),('enemy','fire'),('the','helmsman'),('cannon','fire'),('just','because'),('in','battle'),('handle','the','sails'),('should','be','able','to'),('any','shot'),('heading','windward'),('all','right'),('with','you'),('the','windward','position'),('sea','battle'),('match','my','movements'),('mast','crew'),('just','as','we','practiced'),('right','in','front','of','me'),('other','helmsmen'),('follow','my','lead'),('all','that','training'),('paid','off'),('lead','the','way'),('hand-to-hand','combat'),('count','on','me'),('everyone','ready'),('itching','to','show'),('what','I','can','do'),('a','veteran'),('do','great'),('out','there'),('treat','me'),('a','feast'),('make','an','opening'),('for','us'),('fewer','casualties'),('have','to','be'),('a','duel'),('trust','me')}
KEEP_TOGETHER={tuple(word.strip('.,!?;:').lower() for word in pair) for phrase in PHRASES for pair in zip(phrase,phrase[1:])}
layout=FunctionType(base.layout.__code__,{**base.layout.__globals__,'KEEP_TOGETHER':KEEP_TOGETHER})
serialize=base.serialize
def compiled(row):return serialize(layout(row['english']))
