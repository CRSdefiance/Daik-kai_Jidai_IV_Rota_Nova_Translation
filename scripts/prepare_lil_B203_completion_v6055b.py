"""Correct the prepared producer docstring without rewriting historical derivations."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    proof=derive('scripts/complete_lil_B203_v6055.py','scripts/complete_lil_B203_v6055b.py',{'verify19 disjoint reviews':'verify22 disjoint reviews'})
    root=Path('work/analysis/lil_B203_completion_preparation_v6055b');root.mkdir(parents=True);save(root/'derivation.json',proof)
