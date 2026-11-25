"""Keep the observed contracted auxiliary together across the Proof explanation."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

if __name__=='__main__':
    root=Path('work/analysis/Hodram_B54_B60_layout_preparation_v8802d');assert not root.exists()
    result=derive('scripts/plan_Hodram_B54_B60_v8802c.py','scripts/plan_Hodram_B54_B60_v8802d.py',{
        'work/analysis/Hodram_B54_B60_layout_v8802c':'work/analysis/Hodram_B54_B60_layout_v8802d',
        "('they','cared')}":"('they','cared'),(\"we'd\",'been'),('been','praying')}"
    })
    root.mkdir(parents=True);save(root/'source_locked_auxiliary_successor.json',dict(derivation=result,
        reason='Direct review of the complete native B59R23 pages found page1 ending with We\'d and page2 starting been praying. Add coherent contracted-auxiliary phrase costs to preserve natural continuation without changing prose or any viewport/font/native guard/QA rule. Preserve all earlier plans and native pages.',
        new_credit=0,new_emulator_runs=0,full_goal_complete=False))
