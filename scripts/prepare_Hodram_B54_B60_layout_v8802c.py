"""Keep observed idioms, short tag and name phrases together without changing prose."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

if __name__=='__main__':
    root=Path('work/analysis/Hodram_B54_B60_layout_preparation_v8802c');assert not root.exists()
    result=derive('scripts/plan_Hodram_B54_B60_v8802b.py','scripts/plan_Hodram_B54_B60_v8802c.py',{
        'work/analysis/Hodram_B54_B60_layout_v8802b':'work/analysis/Hodram_B54_B60_layout_v8802c',
        "('mention','it')}":"('mention','it'),('good','luck'),('military','man'),('man','right'),(\"he'd\",'been'),('long','time'),('there','are'),('they','cared')}"
    })
    root.mkdir(parents=True);save(root/'source_locked_phrase_successor.json',dict(derivation=result,
        reason='Review of all82 automatic plans found good/luck and the short man/right tag unnecessarily divided, with other visible auxiliary and fixed-phrase boundaries. Add only coherent phrase costs to the unchanged full-width planner. Preserve every word, original viewport, font, guards, weak-ending QA and the earlier plans. These are automatic compiler preferences, not authored line breaks.',
        new_credit=0,new_emulator_runs=0,full_goal_complete=False))
