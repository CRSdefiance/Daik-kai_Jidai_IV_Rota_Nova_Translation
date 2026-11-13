"""Read complete clean Hodram B46 to contextualize the B45 invitation before current English."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/Hodram_B46_context_tools_v8179')
if __name__=='__main__':
    assert not ROOT.exists()
    receipt=derive('scripts/inventory_Hodram_next_clean_v8178.py','scripts/inventory_Hodram_B46_clean_v8179.py',{
        'Inventory complete clean Hodram B45 andoriginal EV1 context;numeric adjacency proves no chronology.':'Inventory complete clean Hodram B46 andoriginal EV1 context for the B45 invitation;numeric adjacency proves no chronology.',
        'Hodram_next_clean_v8178':'Hodram_B46_clean_context_v8179','for number in [45]':'for number in [46]',
        'complete_clean_SC1_B45_EV1_andcoverage_before_current_English.json':'complete_clean_SC1_B46_EV1_andcoverage_before_current_English.json',
        "g['block']==45":"g['block']==46",
    })
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_derivation.json',receipt)
    print('Prepared complete clean Hodram B46 context inventory;no currentEnglish orcredit.')
