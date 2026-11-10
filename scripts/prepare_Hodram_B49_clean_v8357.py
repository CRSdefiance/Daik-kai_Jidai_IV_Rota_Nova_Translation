"""Open the next source-qualified Hodram exchange from clean Japanese before any current English."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/Hodram_B49_clean_tools_v8357');assert not root.exists()
    d=derive('scripts/inventory_Hodram_B48_clean_v8311.py','scripts/inventory_Hodram_B49_clean_v8357.py',{
        'Hodram_B48_clean_v8311':'Hodram_B49_clean_v8357','editorial_handoff_verification_v8292':'editorial_handoff_verification_v8342',
        '7171':'7199','for number in [48]:':'for number in [49]:','B48':'B49',"if g['block']==48:":"if g['block']==49:",
    })
    root.mkdir(parents=True);save(root/'clean_next_exchange_source_locked_derivation.json',dict(derivation=d,source_only_no_current_English_ornew_completion_credit=True,numeric_adjacency_not_assumed_chronology=True,full_goal_complete=False))
