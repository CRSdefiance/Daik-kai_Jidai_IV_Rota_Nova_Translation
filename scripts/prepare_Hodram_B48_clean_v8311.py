"""Read the source-qualified alternate outcome alongside B47; no chronology inferred from numbers."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/Hodram_B48_clean_tools_v8311')
if __name__=='__main__':
    assert not ROOT.exists()
    result=derive('scripts/inventory_Hodram_B47_clean_v8310.py','scripts/inventory_Hodram_B48_clean_v8311.py',{
        'Hodram_B47_clean_v8310':'Hodram_B48_clean_v8311','for number in [47]:':'for number in [48]:','B47':'B48',"if g['block']==47:":"if g['block']==48:",
    })
    ROOT.mkdir(parents=True);save(ROOT/'clean_alternate_outcome_inventory_successor.json',dict(derivation=result,
        source_only_current_English_unconsulted_no_credit=True,all_atomic_test_inputs_unchanged=True,full_goal_complete=False))
