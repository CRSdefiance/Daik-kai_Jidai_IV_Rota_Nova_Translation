"""Group complete spoken phrases while retaining every word and all native limits."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B204_phrase_tools_v6128')
if __name__=='__main__':
    assert not ROOT.exists()
    phrase="\n# Exact B204 whole-exchange review:keep short complete clauses and the ship rule intact.\nPROTECTED_BOUNDARIES = PROTECTED_BOUNDARIES | frozenset({('sounds','good'),('they','gave'),('gave','me'),('me','this'),('this','to'),('to','thank'),('thank','me'),('something','terrible'),('find','that'),('that','thief'),('one','figurehead'),('figurehead','per'),('per','ship')})\n"
    tools=[derive('dk4tool/dialogue/lil_B204_layout_v2.py','dk4tool/dialogue/lil_B204_layout_v3.py',{'def _word(value):':phrase+'\ndef _word(value):'})]
    tools.append(derive('scripts/plan_lil_B204_layout_v6126.py','scripts/plan_lil_B204_layout_v6129.py',{
        'layout_v6126':'layout_v6129','lil_B204_layout_v2':'lil_B204_layout_v3',
        "INPUT=Path('translations/lil_B204_editorial_manuscript_v2.json')":"INPUT=Path('translations/lil_B204_editorial_manuscript_v3.json')", "OUTPUT=Path('translations/lil_B204_editorial_manuscript_v3.json')":"OUTPUT=Path('translations/lil_B204_editorial_manuscript_v4.json')",
    }))
    ROOT.mkdir(parents=True);save(ROOT/'phrase_refinement_prepared.json',dict(tools=tools,words_source_selectors_native_addresses_metrics_216px_budget_four_rows_guards_and_pair_phase_unchanged=True,whole_exchange_phrase_findings=['R16 Sounds good','R33 complete thank-you gift claim','R45 Something terrible','R55 Find that thief','R69 one figurehead per ship'],no_authored_breaks_or_whole_row_narrowing=True,full_goal_complete=False));print('Five whole-exchange phrase refinements prepared;words and native geometry unchanged.')
