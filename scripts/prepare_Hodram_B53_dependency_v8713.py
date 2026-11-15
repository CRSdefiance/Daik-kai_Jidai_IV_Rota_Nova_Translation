"""Read original event31 dependency context before consulting B53's earlier English."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

if __name__=='__main__':
    root=Path('work/analysis/Hodram_B53_dependency_tools_v8713');assert not root.exists()
    receipt=derive('scripts/inventory_Hodram_B53_clean_v8711.py','scripts/inventory_Hodram_B53_dependency_v8713.py',{
        'Inventory complete clean Hodram B53':'Inventory clean Hodram event31 dependency context',
        'Hodram_B53_clean_v8711':'Hodram_B53_dependency_context_v8713',
        'for number in [53]':'for number in [31]',
        'complete_clean_SC1_B53_EV1_andcoverage_before_current_English.json':'complete_clean_SC1_B31_dependency_context_before_B53_English.json',
        "g['block']==53":"g['block']==31",
    })
    root.mkdir(parents=True);save(root/'derivation.json',dict(derivation=receipt,
         explicit_EV1_dependency53_requires31_requires52_context_not_inferred_numeric_adjacency=True,
         source_context_read_only_no_B31_orB53_review_credit=True))
