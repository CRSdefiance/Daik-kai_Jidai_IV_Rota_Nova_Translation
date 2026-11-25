"""Prefer coherent phrases within the same row count;preserve every original QA diagnostic."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
if __name__=='__main__':
    s=Path('scripts/plan_Rafael_B49_layout_v8090.py').read_text(encoding='utf8')
    old="ENV={**previous.ENV,'BOUND_ZERO_SOURCE_BODIES':BOUND_ZERO_SOURCE_BODIES,'get_profile':get_profile,'PAIRS':PAIRS}"
    replacement='''COHERENT_PAIRS={
    ('who','gave'),('navy','guy'),('fight','out'),('beyond','this'),('west','to'),
    ('north','sea'),('new','world'),('far','east'),('argot','company'),
    ('martin','speyer'),('hanseatic','league'),('trade','house'),("don't",'you'),("aren't",'you'),
}
ADAPTER=checked_text(ADAPTER,{
    'return (0,0,0,0,0,0),()':'return (0,0,0,0,0,0,0),()',
    'cost[3]+1,cost[4]+weak,cost[5]+':'cost[3]+1,cost[4]+int(not final and pair in COHERENT_PAIRS),cost[5]+weak,cost[6]+',
})
ENV={**previous.ENV,'BOUND_ZERO_SOURCE_BODIES':BOUND_ZERO_SOURCE_BODIES,'get_profile':get_profile,'PAIRS':PAIRS,'COHERENT_PAIRS':COHERENT_PAIRS}'''
    print(derive('scripts/plan_Rafael_B49_layout_v8090.py','scripts/plan_Rafael_B49_layout_v8090b.py',{
        'Rafael_B49_layout_v8090':'Rafael_B49_layout_v8090b',old:replacement,
        'source_word_boundary_pairs=sorted(PAIRS)':'source_word_boundary_pairs=sorted(PAIRS),source_coherent_phrase_pairs=sorted(COHERENT_PAIRS)',
        'orphan_then_short_internal_rows_then_sentence_page_boundaries_rows_soft_weak_preferences_final_balance':'orphan_then_short_internal_rows_then_sentence_page_boundaries_rows_coherent_phrases_soft_weak_preferences_final_balance',
    }))
