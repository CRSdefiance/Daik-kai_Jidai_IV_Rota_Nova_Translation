"""Correct copied checkpoint headings before the completion producer is executed."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B226_completion_labels_v7283c')
if __name__=='__main__':
    assert not ROOT.exists()
    r=derive('scripts/complete_lil_B226_v7283.py','scripts/complete_lil_B226_v7283c.py',{'V7236':'V7283'})
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_checkpoint_labels.json',r)
