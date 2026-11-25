"""Keep the source's verb/object and missing-ornament statement together."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B204_predicate_tools_v6130')
if __name__=='__main__':
    assert not ROOT.exists()
    tools=[derive('dk4tool/dialogue/lil_B204_layout_v3.py','dk4tool/dialogue/lil_B204_layout_v4.py',{'def _word(value):':"PROTECTED_BOUNDARIES = PROTECTED_BOUNDARIES | frozenset({('use','figureheads'),('shachihoko','is'),('is','gone')})\n\ndef _word(value):"})]
    tools.append(derive('scripts/plan_lil_B204_layout_v6129.py','scripts/plan_lil_B204_layout_v6130.py',{'layout_v6129':'layout_v6130','lil_B204_layout_v3':'lil_B204_layout_v4',"INPUT=Path('translations/lil_B204_editorial_manuscript_v3.json')":"INPUT=Path('translations/lil_B204_editorial_manuscript_v4.json')","OUTPUT=Path('translations/lil_B204_editorial_manuscript_v4.json')":"OUTPUT=Path('translations/lil_B204_editorial_manuscript_v5.json')"}))
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_predicate_refinement.json',dict(tools=tools,source_phrase_findings=['R33 use figureheads','R55 shachihoko is gone'],no_words_native_metrics_guard_pair_phase_row_limit_or_manual_break_changes=True,full_goal_complete=False));print('Two source-bound predicate groupings prepared;all words and native limits unchanged.')
