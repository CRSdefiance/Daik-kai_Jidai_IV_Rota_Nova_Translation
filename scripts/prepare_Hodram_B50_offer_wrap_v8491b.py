"""Keep the source gift phrase coherent through automatic full-width wrapping;no authored break orword change."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/Hodram_B50_offer_wrap_tools_v8491b')
if __name__=='__main__':
    assert not ROOT.exists();source=Path('scripts/plan_Hodram_B50_v8491.py').read_text('utf8');line=next(v for v in source.splitlines() if v.startswith('PAIRS='))
    result=derive('scripts/plan_Hodram_B50_v8491.py','scripts/plan_Hodram_B50_v8491b.py',{
        'Hodram_B50_layout_v8491':'Hodram_B50_layout_v8491b',line:line+"|{('here','take'),('take','this')}",
    })
    pages=derive('scripts/prove_Hodram_B50_pages_v8492.py','scripts/prove_Hodram_B50_pages_v8492b.py',{
        'Hodram_B50_layout_v8491':'Hodram_B50_layout_v8491b','Hodram_B50_pages_v8492':'Hodram_B50_pages_v8492b',
    })
    ROOT.mkdir(parents=True);save(ROOT/'derivation.json',dict(derivations=[result,pages],only_scoped_source_gift_phrase_coherence_pairs_added=True,pairs=[['here','take'],['take','this']],full216px_available_width_unchanged=True,all_prose_source_commands_native_metrics_QA_andguard_rules_preserved=True,no_manual_break_padding_shortening_orviewport_change=True,previous_automatic_plan_andunused_page_producer_preserved=True,new_credit=0,full_goal_complete=False))
