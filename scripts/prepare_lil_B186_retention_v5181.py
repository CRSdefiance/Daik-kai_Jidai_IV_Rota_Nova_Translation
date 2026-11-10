"""Prepare exact cumulative/reconstruction retention without pruning any artifact."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B186_retention_tools_v5181')
if __name__=='__main__':
    assert not ROOT.exists()
    row=derive('scripts/pin_lil_B185_v5126.py','scripts/pin_lil_B186_v5181.py',{
        'B185':'B186','retention_v5126':'retention_v5181','release_v5123':'release_v5178',
        'reference_v5108':'reference_v5161','display_v5113':'display_v5166','V5122':'V5177',
    })
    ROOT.mkdir(parents=True);save(ROOT/'prepared_preserve_all_pins.json',dict(derivation=row,no_pruning=True,full_goal_complete=False))
    print('Prepared B186 cumulative and exact-reconstruction pins;all previous research ROMs remain pinned.')
