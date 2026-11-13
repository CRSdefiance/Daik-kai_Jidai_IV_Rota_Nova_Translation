"""Prepare the next clean-source inventory without reading predecessor English or inheriting B209 content."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B210_clean_tools_v6495')
if __name__=='__main__':
    assert not ROOT.exists();row=derive('scripts/inventory_lil_B209_clean_v6446.py','scripts/inventory_lil_B210_clean_v6495.py',{'B209':'B210','inventory_v6446':'inventory_v6495','blocks[209]':'blocks[210]','block=209':'block=210'});ROOT.mkdir(parents=True);save(ROOT/'source_locked_preparation.json',dict(derived=row,clean_source_only_no_current_English_read=True,full_goal_complete=False));print('B210 clean-only inventory prepared;no B209 prose or actor assumptions copied.')
