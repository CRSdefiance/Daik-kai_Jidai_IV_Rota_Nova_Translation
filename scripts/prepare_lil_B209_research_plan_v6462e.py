"""Keep the source's grudge against Tokugawa together under the unchanged native width."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B209_layout_tools_v6462e')
if __name__=='__main__':
    assert not ROOT.exists();r=derive('scripts/plan_lil_B209_research_v6462d.py','scripts/plan_lil_B209_research_v6462e.py',{
        'layout_research_v6462d\')':'layout_research_v6462e\')',
        "('wipe','them')}":"('wipe','them'),('grudge','against'),('against','tokugawa')}",
        "said them us me him her'.split())":"said them us me him her against'.split())",
    });ROOT.mkdir(parents=True);save(ROOT/'prepared_tool.json',dict(tool=r,first_letter_and_other_words_unchanged=True,grudge_against_Tokugawa_phrase_preserved=True,all_native_and_actual_page_checks_pending=True,full_goal_complete=False))
